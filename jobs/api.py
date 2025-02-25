# jobs/api.py

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.responses import Response
from typing import List, Optional
import os
from django.utils import timezone
from .models import *
from .schemas import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.contrib.auth import login, get_backends
from django.contrib.auth.decorators import login_required
from ninja.errors import ValidationError
router = Router()
User = get_user_model()
from ninja.security import django_auth

# router = Router(auth=django_auth)

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
# @router.get("/google-login")
# def google_login(request):
#     return redirect("/accounts/google/login/")


# @router.get("/facebook-login")
# def facebook_login(request):
#     return redirect("/accounts/facebook/login/")




@router.get("/whoami")
def whoami(request):
    """
    GET /jobs/whoami
    Returns the user’s ID, username, and session-based role.
    """
    if not request.user.is_authenticated:
        return {"error": "Not logged in"}
    
    return {
        "user_id": request.user.id,
        "username": request.user.username,
        "role": request.session.get("user_role", "unknown")
    }

def fetch_all_users():
    """
    Fetch all users from the database.
    Returns a list of user dictionaries.
    """
    # Customize fields as needed
    users = User.objects.all().values("id", "username", "email", "date_joined")
    return list(users)

def user_profile_pic_path(instance, filename):
    """
    Example function to generate a unique path for user profile images.
    E.g.: 'profile_pics/user_<id>/<timestamp>_<filename>'
    """
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")

# ----------------------------------------------------------------------
# 0) All Users Endpoint
# ----------------------------------------------------------------------
@router.get("/all-users")
def get_all_users_view(request):
    """
    GET /jobs/all-users
    Returns a list of all user dictionaries.
    """
    user_list = fetch_all_users()
    return {"users": user_list}

# ----------------------------------------------------------------------
# 1) Logout
# ----------------------------------------------------------------------
@router.post("/logout")
def logout_view(request):
    """
    POST /jobs/logout
    Logs out the current session-based user.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)

# ----------------------------------------------------------------------
# 2) Change Password
# ----------------------------------------------------------------------
@router.post("/change-password")
def change_password(request, oldPassword: str, newPassword: str, confirmPassword: str):
    """
    POST /jobs/change-password
    Allows the logged-in user to change their password if oldPassword is correct
    and newPassword matches confirmPassword.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    user = request.user

    if not check_password(oldPassword, user.password):
        return Response({"error": "Incorrect old password"}, status=400)

    if newPassword != confirmPassword:
        return Response({"error": "Passwords do not match"}, status=400)

    user.set_password(newPassword)
    user.save()
    update_session_auth_hash(request, user)
    return Response({"message": "Password changed successfully"}, status=200)

# ----------------------------------------------------------------------
# 3) Profile Endpoints (Get & Update)
# ----------------------------------------------------------------------
@router.get("/profile")
def get_profile(request):
    """
    GET /jobs/profile
    Fetches the current user's profile info.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    user = request.user
    # If you have a separate Profile model:
    # profile = getattr(user, "profile", None)
    # pic_url = profile.profile_pic.url if (profile and profile.profile_pic) else ""

    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "profilePicUrl": "",  # or pic_url if storing images
    }
    return data





@router.put("/profile")
def update_profile(
    request,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    file: UploadedFile = File(None),
):
    """
    PUT /jobs/profile
    Updates the logged-in user's profile fields + optional file (profile pic).
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    user = request.user

    # Update text fields
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        # Ensure no duplicates
        if User.objects.filter(username=email).exclude(pk=user.pk).exists():
            return Response({"error": "Email already in use"}, status=400)
        user.email = email
        user.username = email  # if you treat email as username

    user.save()

    # If handling file uploads for a profile pic:
    if file is not None:
        profile, created = Profile.objects.get_or_create(user=user)
        profile.profile_pic = file
        profile.save()

    return Response({"message": "Profile updated successfully"}, status=200)

# ----------------------------------------------------------------------
# 4) Auth Endpoints (Login & Signup)
# ----------------------------------------------------------------------
@router.post("/login")
def login_view(request, payload: LoginSchema):
    """
    POST /jobs/login
    Authenticates a user and logs them in. Stores role in session.
    """
    user = authenticate(
        request, 
        username=payload.email, 
        password=payload.password
    )
    if user is not None:
        login(request, user)
        request.session["user_id"] = user.id  # Explicitly store ID
        request.session.modified = True  # Ensure session is saved
        
        print("Logged-in User ID:", user.id)  # Debugging

        return Response({
            "message": "Login successful",
            "user_id": user.id,
        }, status=200)
    
    return Response({"error": "Invalid credentials"}, status=401)
@router.post("/signup")
def signup_view(request, payload: SignupSchema):
    """
    POST /jobs/signup
    Creates a new user account and a corresponding profile.
    """
    try:
        # Create the user
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password  # create_user() handles hashing
        )

        # Manually assign an authentication backend
        user.backend = get_backends()[0].__class__.__name__

        # Log the user in
        login(request, user)

        # Create the profile
        Profile.objects.create(user=user, role=payload.role)

        return Response({"message": "success"}, status=200)
    
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    
    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"}, status=500)









@router.get("/csrf-token")
def get_csrf_token(request):
    from django.middleware.csrf import get_token
    return {"csrf_token": get_token(request)}

# ----------------------------------------------------------------------
# 5) Jobs Endpoints
# ----------------------------------------------------------------------



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from jobs.models import Job, JobIndustry, JobSubCategory
from ninja.router import Router

router = Router()



router = Router()

@router.post("/create-job")
def create_job(request, payload: CreateJobSchema):
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        return JsonResponse({"error": "User session not found."}, status=401)

    user = get_object_or_404(User, id=user_id)

    # Convert date and time
    try:
        job_date = datetime.strptime(payload.date, "%Y-%m-%d").date()
        job_time = datetime.strptime(payload.time, "%H:%M").time()
    except ValueError as e:
        return JsonResponse({"error": f"Invalid date/time format: {str(e)}"}, status=400)

    # Get Industry and Subcategory
    job_industry = None
    if payload.industry:
        job_industry = get_object_or_404(JobIndustry, name=payload.industry)

    job_subcategory = None
    if payload.subcategory:
        job_subcategory = get_object_or_404(JobSubCategory, name=payload.subcategory)

    # Create job
    new_job = Job.objects.create(
        client=user,
        title=payload.title,
        description=payload.description,
        industry=job_industry,
        subcategory=job_subcategory,
        applicants_needed=payload.applicants_needed,
        job_type=payload.job_type,
        shift_type=payload.shift_type,
        date=job_date,
        time=job_time,
        duration=payload.duration,
        rate=payload.rate,
        location=payload.location,
        image=payload.image,
        payment_status=payload.payment_status,
    )

    return JsonResponse({"success": True, "message": "Job created successfully", "job_id": new_job.id}, status=201)

    
@router.get("/accepted-list")
def list_accepted_applications(request):
    """
    GET /jobs/list
    Returns only the applications where is_accepted=True,
    along with the related job details.
    """
    apps_qs = Application.objects.filter(is_accepted=True).select_related("job", "applicant")
    data = []
    for app in apps_qs:
        job = app.job
        data.append({
            "application_id": app.id,
            "applicant_name": app.applicant.first_name,
            "is_accepted": app.is_accepted,
            "applied_at": str(app.applied_at),

            "job_id": job.id,
            "client_name": job.client.first_name if job.client else "Unknown Client",
            "status": job.status,
            "title": job.title,
            "date": str(job.date) if job.date else "",
            "time": str(job.time) if job.time else "",
            "duration": job.duration,
            "amount": str(job.amount),
            "location": job.location,
            "date_posted": "2 days ago",
            "no_of_application": job.no_of_application,
        })
    return data

@router.get("/{job_id}")
def job_detail(request, job_id: int):
    """
    GET /jobs/<job_id>
    Returns detail for a single job.
    """
    job = get_object_or_404(Job, id=job_id)
    data = {
        "id": job.id,
        "employerName": job.client.first_name if job.client else "Anonymous",
        "title": job.title,
        "date": str(job.date) if job.date else "",
        "time": str(job.time) if job.time else "",
        "duration": job.duration,
        "amount": str(job.amount),
        "location": job.location,
        "applicantNeeded": 1,  # or your real field if you track how many needed
        "startDate": str(job.date) if job.date else "",
        "startTime": str(job.time) if job.time else "",
    }
    return data

@router.get("/industries", response=List[IndustrySchema])
def list_industries(request):
    """
    GET /jobs/industries
    Returns all JobIndustry records.
    """
    qs = JobIndustry.objects.all()
    return qs

@router.get("/subcategories", response=List[SubCategorySchema])
def list_subcategories(request, industry_id: Optional[int] = None):
    """
    GET /jobs/subcategories?industry_id=<ID>
    Returns all JobSubCategory records.
    If `industry_id` is provided, filters subcategories for that industry.
    """
    if industry_id:
        qs = JobSubCategory.objects.filter(industry_id=industry_id)
    else:
        qs = JobSubCategory.objects.all()
    return qs
# ----------------------------------------------------------------------
# 6) Saved Jobs Endpoints
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Save a job (POST)
# ----------------------------------------------------------------------
@router.post("/save-job/{job_id}")
def save_job(request, job_id: int):
    """
    POST /jobs/save-job/<job_id>
    Saves the job for the current user (session-based).
    """
    if not request.user.is_authenticated:
        return Response({"error": "You must be logged in to save jobs."}, status=401)

    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found."}, status=404)

    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if created:
        return Response({"message": "Job saved successfully."}, status=201)
    else:
        return Response({"message": "Job is already saved."}, status=200)


# ----------------------------------------------------------------------
# Unsave a job (DELETE)
# ----------------------------------------------------------------------
@router.delete("/save-job/{job_id}")
def unsave_job(request, job_id: int):
    """
    DELETE /jobs/save-job/<job_id>
    Removes the job from the user's saved list.
    """
    if not request.user.is_authenticated:
        return Response({"error": "You must be logged in to unsave jobs."}, status=401)

    try:
        saved_record = SavedJob.objects.get(user=request.user, job_id=job_id)
    except SavedJob.DoesNotExist:
        return Response({"error": "You haven't saved this job yet."}, status=404)

    saved_record.delete()
    return Response({"message": "Job unsaved successfully."}, status=200)

@router.get("/saved-jobs")
def list_saved_jobs(request):
    """
    GET /jobs/saved-jobs
    Lists all jobs the current user has saved.
    """
    if not request.user.is_authenticated:
        return Response({"error": "You must be logged in."}, status=401)

    saved_records = SavedJob.objects.filter(user=request.user).select_related("job")
    data = []
    for record in saved_records:
        job = record.job
        data.append({
            "saved_job_id": record.id,
            "saved_at": str(record.saved_at),
            "job_id": job.id,
            "title": job.title,
            "status": job.status,
            "date": str(job.date) if job.date else "",
            "time": str(job.time) if job.time else "",
            "duration": job.duration,
            "amount": str(job.amount),
            "location": job.location,
        })
    return data

# ----------------------------------------------------------------------
# 7) LOCATION UPDATE (Optional)
# ----------------------------------------------------------------------
@router.post("/jobs/{job_id}/update-location")
def update_location(request, job_id: int, payload: LocationSchema):
    """
    The client user posts their lat/long for a specific job.
    Optionally store in DB or broadcast to a Channels group for real-time.
    """
    if not request.user.is_authenticated:
        return {"error": "Not logged in"}, 401

    # Example if you want to store each location in DB:
    # LocationHistory.objects.create(
    #     user=request.user,
    #     job_id=job_id,
    #     latitude=payload.latitude,
    #     longitude=payload.longitude
    # )

    # If using Channels for real-time:
    # channel_layer = get_channel_layer()
    # group_name = f"job_{job_id}"
    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {
    #         "type": "location_update",
    #         "latitude": payload.latitude,
    #         "longitude": payload.longitude,
    #     }
    # )

    return {"message": "Location updated (optionally broadcasted)"}





# ------------------------------------------------------------------------------
# A) RATING SYSTEM
# ------------------------------------------------------------------------------
@router.post("/ratings", tags=["Ratings"])
def create_rating(request, payload: RatingCreateSchema):
    """
    POST /jobs/ratings
    Allows a user (client or applicant) to submit a rating for another user.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    # Validate that the reviewed user exists
    reviewed_user = get_object_or_404(User, pk=payload.reviewedUserId)

    # Create a new rating
    new_rating = Rating.objects.create(
        reviewer=request.user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback
    )
    return {"message": "Rating submitted", "rating_id": new_rating.id}


@router.get("/ratings/{user_id}", tags=["Ratings"])
def get_user_ratings(request, user_id: int):
    """
    GET /jobs/ratings/{user_id}
    Retrieves all ratings for a specific user, plus average rating.
    """
    reviewed_user = get_object_or_404(User, pk=user_id)

    # Query all ratings where "reviewed = user_id"
    all_ratings = Rating.objects.filter(reviewed=reviewed_user)
    data_list = []
    for r in all_ratings:
        data_list.append({
            "id": r.id,
            "reviewer": r.reviewer.username,
            "rating": r.rating,
            "feedback": r.feedback,
            "created_at": r.created_at.isoformat()
        })

    # Example: compute average rating
    avg_rating = Rating.get_average_rating(reviewed_user)

    return {
        "user_id": reviewed_user.id,
        "username": reviewed_user.username,
        "average_rating": avg_rating,
        "ratings": data_list
    }

# ------------------------------------------------------------------------------
# B) DISPUTE RESOLUTION
# ------------------------------------------------------------------------------
@router.post("/jobs/{job_id}/disputes", tags=["Disputes"])
def create_dispute(request, job_id: int, payload: DisputeCreateSchema):
    """
    POST /jobs/{job_id}/disputes
    Creates a new dispute regarding a specific job.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    job = get_object_or_404(Job, pk=job_id)
    # The user raising the dispute could be either the client or the applicant

    dispute = Dispute.objects.create(
        job=job,
        created_by=request.user,
        title=payload.title,
        description=payload.description
    )
    return {"message": "Dispute created", "dispute_id": dispute.id}


@router.get("/jobs/{job_id}/disputes", tags=["Disputes"])
def list_job_disputes(request, job_id: int):
    """
    GET /jobs/{job_id}/disputes
    Returns all disputes for a specific job.
    """
    job = get_object_or_404(Job, pk=job_id)
    disputes = job.disputes.select_related("created_by").all()

    data = []
    for d in disputes:
        data.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "status": d.status,
            "created_by": d.created_by.username,
            "created_at": d.created_at.isoformat(),
            "updated_at": d.updated_at.isoformat()
        })
    return data


@router.get("/disputes/{dispute_id}", tags=["Disputes"])
def dispute_detail(request, dispute_id: int):
    """
    GET /jobs/disputes/{dispute_id}
    Fetches detail for a single dispute.
    """
    dispute = get_object_or_404(Dispute, pk=dispute_id)
    return {
        "id": dispute.id,
        "title": dispute.title,
        "description": dispute.description,
        "status": dispute.status,
        "created_by": dispute.created_by.username,
        "created_at": dispute.created_at.isoformat(),
        "updated_at": dispute.updated_at.isoformat()
    }


@router.put("/disputes/{dispute_id}", tags=["Disputes"])
def update_dispute(request, dispute_id: int, payload: DisputeUpdateSchema):
    """
    PUT /jobs/disputes/{dispute_id}
    Updates an existing dispute (change status, add resolution, etc.).
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    dispute = get_object_or_404(Dispute, pk=dispute_id)

    # Possibly check if request.user is the dispute creator or the job's client
    if payload.status:
        dispute.status = payload.status
    if payload.resolution:
        # If you have a 'resolution' field in Dispute, set it here
        # dispute.resolution = payload.resolution
        pass

    dispute.save()
    return {"message": "Dispute updated", "dispute_id": dispute.id}

# # ------------------------------------------------------------------------------
# # C) PAYMENT SYSTEM
# # ------------------------------------------------------------------------------
# @router.post("/jobs/{job_id}/payments", tags=["Payments"])
# def create_payment(request, job_id: int, payload: PaymentCreateSchema):
#     """
#     POST /jobs/{job_id}/payments
#     Creates a payment record for a given job.
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     job = get_object_or_404(Job, pk=job_id)

#     # For instance, the user paying is the client, or it might be a different logic
#     # Possibly ensure job.client == request.user, or something similar
#     payment = Payment.objects.create(
#         payer=request.user,  # or job.client
#         recipient=None,      # set a recipient if you have logic for who gets paid
#         job=job,
#         original_amount=payload.original_amount,
#         service_fee=payload.service_fee,
#         final_amount=payload.final_amount,
#         pay_code=payload.pay_code  # or auto-generate if needed
#     )
#     return {"message": "Payment created", "payment_id": payment.id}


# @router.get("/jobs/{job_id}/payments", tags=["Payments"])
# def list_payments_for_job(request, job_id: int):
#     """
#     GET /jobs/{job_id}/payments
#     Returns a list of payment records for the specified job.
#     """
#     job = get_object_or_404(Job, pk=job_id)
#     payments = job.payments.all()

#     data = []
#     for p in payments:
#         data.append({
#             "id": p.id,
#             "payer": p.payer.username,
#             "recipient": p.recipient.username if p.recipient else None,
#             "original_amount": str(p.original_amount),
#             "service_fee": str(p.service_fee),
#             "final_amount": str(p.final_amount),
#             "pay_code": p.pay_code,
#             "payment_status": p.payment_status,
#             "created_at": p.created_at.isoformat(),
#             "confirmed_at": p.confirmed_at.isoformat() if p.confirmed_at else None
#         })
#     return data


# @router.put("/payments/{payment_id}", tags=["Payments"])
# def update_payment(request, payment_id: int, payload: PaymentUpdateSchema):
#     """
#     PUT /jobs/payments/{payment_id}
#     Allows updating a payment’s status or details.
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     payment = get_object_or_404(Payment, pk=payment_id)

#     # Possibly check if request.user is the payer or an admin. Exclude admin logic if not needed
#     if payload.payment_status:
#         payment.payment_status = payload.payment_status
#     if payload.refund_requested is not None:
#         payment.refund_requested = payload.refund_requested

#     payment.save()
#     return {"message": "Payment updated", "payment_id": payment.id}

# # ------------------------------------------------------------------------------
# # D) SHIFT SCHEDULING
# # ------------------------------------------------------------------------------
# @router.post("/jobs/{job_id}/shifts", tags=["Shifts"])
# def create_or_update_shift(request, job_id: int, payload: ShiftSchema):
#     """
#     POST /jobs/{job_id}/shifts
#     Creates or updates shift info for a given job (morning/night).
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     job = get_object_or_404(Job, pk=job_id)

#     # If you have a Shift model, you might do something like:
#     # shift, created = Shift.objects.update_or_create(
#     #     job=job,
#     #     shiftType=payload.shiftType,
#     #     defaults={
#     #         "startTime": payload.startTime,
#     #         "endTime": payload.endTime
#     #     }
#     # )
#     # For now, we'll just return a placeholder
#     return {"message": "Shift created/updated for job", "job_id": job.id}

# @router.get("/jobs/{job_id}/shifts", tags=["Shifts"])
# def get_job_shifts(request, job_id: int):
#     """
#     GET /jobs/{job_id}/shifts
#     Returns the shift schedule details for a given job.
#     """
#     job = get_object_or_404(Job, pk=job_id)

#     # If you have a Shift model:
#     # shifts = Shift.objects.filter(job=job)
#     # data = []
#     # for s in shifts:
#     #     data.append({
#     #         "id": s.id,
#     #         "shiftType": s.shiftType,
#     #         "startTime": s.startTime,
#     #         "endTime": s.endTime
#     #     })
#     # return data

#     return {"message": f"Shifts for job {job.id} (placeholder)"}

# # ------------------------------------------------------------------------------
# # E) REAL-TIME JOB MATCHING (Optional)
# # ------------------------------------------------------------------------------
# @router.post("/jobs/match", tags=["Matching"])
# def match_jobs(request, payload: MatchSchema):
#     """
#     POST /jobs/match
#     (Optional) If the system triggers a job matching algorithm.
#     Accepts job details, user preference, or location data.
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     # Some job matching logic or placeholders
#     # e.g., find applicants near a location, check shift/time, rating, etc.
#     return {"message": "Job matching triggered (placeholder)"}
