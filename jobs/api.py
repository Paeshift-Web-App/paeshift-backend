# jobs/api.py

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash,
    get_user_model, get_backends
)
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.responses import Response
from typing import List, Optional
import os
from datetime import datetime
from .models import *
from .schemas import *
import os
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ninja import Router
from .models import Job, JobIndustry, JobSubCategory
from .schemas import *
from django.shortcuts import render

router = Router()
User = get_user_model()
router = Router()
User = get_user_model()

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def authenticated_user_or_error(request, error_message="Not logged in", status_code=401):
    """Check if user is authenticated, return user or error response"""
    if not request.user.is_authenticated:
        return None, Response({"error": error_message}, status=status_code)
    return request.user, None

def user_profile_pic_path(instance, filename):
    """Generate unique path for profile pictures"""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")

def fetch_all_users():
    """Fetch all users from the database"""
    return list(User.objects.all().values("id", "username", "email", "date_joined"))

def get_related_object(model, field_name, value, error_message="Not found"):
    """Generic function to fetch related objects with error handling"""
    try:
        return model.objects.get(**{field_name: value}), None
    except model.DoesNotExist:
        return None, Response({"error": error_message}, status=404)




# ----------------------------------------------------------------------
# Authentication Endpoints
# ----------------------------------------------------------------------
@router.get("/whoami")
def whoami(request):
    """GET /jobs/whoami - Returns user's ID, username, and role"""
    if not request.user.is_authenticated:
        return {"error": "Not logged in"}
    return {
        "user_id": request.user.id,
        "username": request.user.username,
        # "role": request.session.get("role", "unknown")
    }

@router.post("/login")
def login_view(request, payload: LoginSchema):
    """POST /jobs/login - Authenticates and logs in a user"""
    user = authenticate(request, username=payload.email, password=payload.password)
    if user:
        login(request, user)
        request.session["user_id"] = user.id
        request.session.modified = True
        print("Logged-in User ID:", user.id)  # Debugging
        return Response({"message": "Login successful", "user_id": user.id}, status=200)
    
    if user is not None:
        login(request, user)  # Sets the session cookie
        return JsonResponse({"success": True})
    return Response({"error": "Invalid credentials"}, status=401)

@router.post("/signup")
def signup_view(request, payload: SignupSchema):
    """POST /jobs/signup - Creates a new user and profile"""
    try:
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name
        )
        user.backend = get_backends()[0].__class__.__name__
        login(request, user)
        Profile.objects.create(user=user, role=payload.role)
        return Response({"message": "success"}, status=200)
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

@router.post("/logout")
def logout_view(request):
    """POST /jobs/logout - Logs out the current user"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)

@router.post("/change-password")
def change_password(request, oldPassword: str, newPassword: str, confirmPassword: str):
    """POST /jobs/change-password - Changes user's password"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    if not check_password(oldPassword, user.password):
        return Response({"error": "Incorrect old password"}, status=400)
    if newPassword != confirmPassword:
        return Response({"error": "Passwords do not match"}, status=400)
    user.set_password(newPassword)
    user.save()
    update_session_auth_hash(request, user)
    return Response({"message": "Password changed successfully"}, status=200)

@router.get("/csrf-token")
def get_csrf_token(request):
    """GET /jobs/csrf-token - Returns CSRF token"""
    from django.middleware.csrf import get_token
    return {"csrf_token": get_token(request)}

# ----------------------------------------------------------------------
# User/Profile Endpoints
# ----------------------------------------------------------------------
@router.get("/all-users")
def get_all_users_view(request):
    """GET /jobs/all-users - Returns list of all users"""
    return {"users": fetch_all_users()}

@router.get("/profile")
def get_profile(request):
    """GET /jobs/profile - Fetches current user's profile info"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    profile = getattr(user, "profile", None)
    pic_url = profile.profile_pic.url if (profile and profile.profile_pic) else ""
    return {
        "name": f"{user.first_name} {user.last_name}",  # Include full name
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "profilePicUrl": pic_url
    }

@router.put("/profile")
def update_profile(request, first_name: str = None, last_name: str = None, 
                  email: str = None, file: UploadedFile = File(None)):
    """PUT /jobs/profile - Updates user's profile"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None and email != user.email:
        if User.objects.filter(username=email).exclude(pk=user.pk).exists():
            return Response({"error": "Email already in use"}, status=400)
        user.email = user.username = email
    
    if file is not None:
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.profile_pic = file
        profile.save()
    
    user.save()
    return Response({"message": "Profile updated successfully"}, status=200)

# ----------------------------------------------------------------------
# Job Endpoints
# ----------------------------------------------------------------------


def get_related_object(model, field, value):
    """
    Helper function to retrieve an object by a specific field.
    Returns a tuple: (object, None) if found, or (None, JsonResponse error) if not.
    """
    try:
        obj = model.objects.get(**{field: value})
        return obj, None
    except model.DoesNotExist:
        error = JsonResponse(
            {"error": f"{model.__name__} with {field} '{value}' does not exist."}, status=400
        )
        return None, error
   
   
   
@router.get("/check-session")
def check_session(request):
    user_id = request.session.get("_auth_user_id")
    return JsonResponse({"user_id": user_id})
    
@router.get("/job-industries/", response=list[IndustrySchema])
def get_job_industries(request):
    return JobIndustry.objects.all()

@router.get("/job-subcategories/", response=list[SubCategorySchema])
def get_job_subcategories(request):
    return JobSubCategory.objects.all()

@router.post("/create-job", auth=None)
def create_job(request, payload: CreateJobSchema):
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        # Temporary: Use a default user for testing
        user = User.objects.first()  # Or create a test user
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)

    try:
        job_date = datetime.strptime(payload.date, "%Y-%m-%d").date()
        start_time = datetime.strptime(payload.start_time, "%H:%M").time()
        end_time = datetime.strptime(payload.end_time, "%H:%M").time()
    except ValueError as e:
        return JsonResponse({"error": f"Invalid date/time format: {str(e)}"}, status=400)

    industry_obj = None
    if payload.industry and payload.industry.strip():
        try:
            industry_id = int(payload.industry)
            industry_obj = get_object_or_404(JobIndustry, id=industry_id)
        except ValueError:
            industry_obj = get_object_or_404(JobIndustry, name=payload.industry.strip())

    subcategory_obj = None
    if payload.subcategory and payload.subcategory.strip():
        try:
            subcategory_id = int(payload.subcategory)
            subcategory_obj = get_object_or_404(JobSubCategory, id=subcategory_id)
        except ValueError:
            subcategory_obj = get_object_or_404(JobSubCategory, name=payload.subcategory.strip())

    new_job = Job.objects.create(
        client=user,
        title=payload.title,
        industry=industry_obj,
        subcategory=subcategory_obj,
        applicants_needed=payload.applicants_needed,
        job_type=payload.job_type,
        shift_type=payload.shift_type,
        date=job_date,
        start_time=start_time,
        end_time=end_time,
        duration=payload.duration,
        rate=payload.rate,
        location=payload.location,
        payment_status=payload.payment_status,
    )

    return JsonResponse({
        "success": True,
        "message": "Job created successfully",
        "job_id": new_job.id
    }, status=201)



from ninja import Router, Query
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from jobs.models import Job
from django.contrib.auth import get_user_model

from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@router.get("/clientjobs", auth=None)
def get_client_jobs(request, page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)):
    # Ensure the user is authenticated
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        # Temporary: Use a default user for testing
        user = User.objects.first()  # Or create a test user
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)
    
    # Filter jobs using the authenticated user's id
    qs = Job.objects.filter(client_id=user.id).order_by("-date")
    
    # Paginate the queryset
    paginator = Paginator(qs, page_size)
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        # Return an empty list if page is out-of-range
        jobs_page = []

    # Convert the page of jobs into a list of dictionaries
    jobs_data = list(jobs_page.object_list.values(
        "id",
        "title",
        "client__username",
        "duration",
        "date",
        "start_time",
        "end_time",
        "location",
        "rate",
        "applicants_needed"
    ))
    
    return JsonResponse({
        "jobs": jobs_data,
        "page": page,
        "total_pages": paginator.num_pages,
        "total_jobs": paginator.count,
    })


@router.get("/alljobs")
def get_jobs(request):
    jobs = Job.objects.all()
    return {"jobs": list(jobs.values("id", "title", "client__username", "duration", "date", "start_time", "end_time", "location", "rate", "applicants_needed"))}




# Adding new helper function for job serialization
def serialize_job(job, include_extra=False):
    """Serialize job object into dictionary with optional extra fields"""
    base_data = {
        "id": job.id,
        "title": job.title,
        "status": job.status,
        "date": str(job.date) if job.date else "",
        "time": str(job.time) if job.time else "",
        "duration": job.duration,
        "amount": str(job.amount),
        "location": job.location
    }
    if include_extra:
        base_data.update({
            "employerName": job.client.first_name if job.client else "Anonymous",
            "applicantNeeded": job.applicants_needed,  # Assuming this field exists
            "startDate": str(job.date) if job.date else "",
            "startTime": str(job.time) if job.time else ""
        })
    return base_data

# ----------------------------------------------------------------------
# Job Endpoints (continued)
# ----------------------------------------------------------------------
@router.get("/accepted-list")
def list_accepted_applications(request):
    """GET /jobs/accepted-list - Returns accepted applications with job details"""
    apps_qs = Application.objects.filter(is_accepted=True).select_related("job", "applicant")
    return [{
        "application_id": app.id,
        "applicant_name": app.applicant.first_name,
        "is_accepted": app.is_accepted,
        "applied_at": str(app.applied_at),
        "job": serialize_job(app.job),
        "client_name": app.job.client.first_name if app.job.client else "Unknown Client",
        "date_posted": "2 days ago",
        "no_of_application": app.job.no_of_application
    } for app in apps_qs]

@router.get("/{job_id}")
def job_detail(request, job_id: int):
    """GET /jobs/<job_id> - Returns details for a single job"""
    job = get_object_or_404(Job, id=job_id)
    return serialize_job(job, include_extra=True)

@router.get("/industries", response=List[IndustrySchema])
def list_industries(request):
    """GET /jobs/industries - Returns all JobIndustry records"""
    return JobIndustry.objects.all()

@router.get("/subcategories", response=List[SubCategorySchema])
def list_subcategories(request, industry_id: Optional[int] = None):
    """GET /jobs/subcategories?industry_id=<ID> - Returns JobSubCategory records"""
    qs = JobSubCategory.objects.filter(industry_id=industry_id) if industry_id else JobSubCategory.objects.all()
    return qs

# ----------------------------------------------------------------------
# Saved Jobs Endpoints
# ----------------------------------------------------------------------
@router.post("/save-job/{job_id}")
def save_job(request, job_id: int):
    """POST /jobs/save-job/<job_id> - Saves a job for the current user"""
    user, error = authenticated_user_or_error(request, "You must be logged in to save jobs")
    if error:
        return error
    job, error = get_related_object(Job, "pk", job_id, "Job not found")
    if error:
        return error
    saved_job, created = SavedJob.objects.get_or_create(user=user, job=job)
    message = "Job saved successfully" if created else "Job is already saved"
    return Response({"message": message}, status=201 if created else 200)

@router.delete("/save-job/{job_id}")
def unsave_job(request, job_id: int):
    """DELETE /jobs/save-job/<job_id> - Removes a job from user's saved list"""
    user, error = authenticated_user_or_error(request, "You must be logged in to unsave jobs")
    if error:
        return error
    try:
        saved_record = SavedJob.objects.get(user=user, job_id=job_id)
        saved_record.delete()
        return Response({"message": "Job unsaved successfully"}, status=200)
    except SavedJob.DoesNotExist:
        return Response({"error": "You haven't saved this job yet"}, status=404)

@router.get("/saved-jobs")
def list_saved_jobs(request):
    """GET /jobs/saved-jobs - Lists all saved jobs for the current user"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    saved_records = SavedJob.objects.filter(user=user).select_related("job")
    return [{
        "saved_job_id": record.id,
        "saved_at": str(record.saved_at),
        "job": serialize_job(record.job)
    } for record in saved_records]

# ----------------------------------------------------------------------
# Location Update Endpoint
# ----------------------------------------------------------------------
@router.post("/jobs/{job_id}/update-location")
def update_location(request, job_id: int, payload: LocationSchema):
    """POST /jobs/{job_id}/update-location - Updates user's location for a job"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    return {"message": "Location updated (optionally broadcasted)"}

# ----------------------------------------------------------------------
# Rating Endpoints
# ----------------------------------------------------------------------
@router.post("/ratings", tags=["Ratings"])
def create_rating(request, payload: RatingCreateSchema):
    """POST /jobs/ratings - Submits a rating for another user"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    reviewed_user = get_object_or_404(User, pk=payload.reviewedUserId)
    new_rating = Rating.objects.create(
        reviewer=user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback
    )
    return {"message": "Rating submitted", "rating_id": new_rating.id}

@router.get("/ratings/{user_id}", tags=["Ratings"])
def get_user_ratings(request, user_id: int):
    """GET /jobs/ratings/{user_id} - Retrieves all ratings for a user"""
    reviewed_user = get_object_or_404(User, pk=user_id)
    all_ratings = Rating.objects.filter(reviewed=reviewed_user)
    return {
        "user_id": reviewed_user.id,
        "username": reviewed_user.username,
        "average_rating": Rating.get_average_rating(reviewed_user),
        "ratings": [{
            "id": r.id,
            "reviewer": r.reviewer.username,
            "rating": r.rating,
            "feedback": r.feedback,
            "created_at": r.created_at.isoformat()
        } for r in all_ratings]
    }

# ----------------------------------------------------------------------
# Dispute Endpoints
# ----------------------------------------------------------------------
@router.post("/jobs/{job_id}/disputes", tags=["Disputes"])
def create_dispute(request, job_id: int, payload: DisputeCreateSchema):
    """POST /jobs/{job_id}/disputes - Creates a dispute for a job"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    job = get_object_or_404(Job, pk=job_id)
    dispute = Dispute.objects.create(
        job=job,
        created_by=user,
        title=payload.title,
        description=payload.description
    )
    return {"message": "Dispute created", "dispute_id": dispute.id}

@router.get("/jobs/{job_id}/disputes", tags=["Disputes"])
def list_job_disputes(request, job_id: int):
    """GET /jobs/{job_id}/disputes - Lists all disputes for a job"""
    job = get_object_or_404(Job, pk=job_id)
    disputes = job.disputes.select_related("created_by").all()
    return [{
        "id": d.id,
        "title": d.title,
        "description": d.description,
        "status": d.status,
        "created_by": d.created_by.username,
        "created_at": d.created_at.isoformat(),
        "updated_at": d.updated_at.isoformat()
    } for d in disputes]

@router.get("/disputes/{dispute_id}", tags=["Disputes"])
def dispute_detail(request, dispute_id: int):
    """GET /jobs/disputes/{dispute_id} - Fetches details for a dispute"""
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
    """PUT /jobs/disputes/{dispute_id} - Updates an existing dispute"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    dispute = get_object_or_404(Dispute, pk=dispute_id)
    if payload.status:
        dispute.status = payload.status
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
