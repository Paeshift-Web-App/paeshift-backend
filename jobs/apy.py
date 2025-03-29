# ==============================
# 📌 Standard Library Imports
# ==============================
import os
import uuid
import requests
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2

# ==============================
# 📌 Django Imports
# ==============================
from django.db import IntegrityError
from django.db.models import Avg, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash,
    get_user_model, get_backends
)
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# ==============================
# 📌 Third-Party Imports
# ==============================
from ninja import Router, File, Query
from ninja.files import UploadedFile
from ninja.responses import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# ==============================
# 📌 Local Imports (Models & Schemas)
# ==============================
from .models import (
    Job, JobIndustry, JobSubCategory, Profile, Review, SavedJob, 
    Application, Dispute, Feedback
)
from .schemas import (
    LoginSchema, SignupSchema, CreateJobSchema, IndustrySchema,
    SubCategorySchema, JobDetailSchema, LocationSchema,
    ReviewCreateSchema, DisputeCreateSchema, DisputeUpdateSchema,
    PasswordResetSchema, PasswordResetRequestSchema, FeedbackSchema
)

# ==============================
# 📌 Initialize Router & User Model
# ==============================
router = Router(tags=["Jobs"])
User = get_user_model()


# ==============================
# 📌 Paystack Configuration
# ==============================
PAYSTACK_SECRET_KEY = getattr(settings, "PAYSTACK_SECRET_KEY", None)
PAYSTACK_PUBLIC_KEY = getattr(settings, "PAYSTACK_PUBLIC_KEY", None)
PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

if not PAYSTACK_SECRET_KEY:
    raise ValueError("PAYSTACK_SECRET_KEY is missing in settings.py")

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------

@router.post("/password-reset", tags=["Auth"])
def reset_password(request, payload: PasswordResetSchema):
    try:
        uid = force_str(urlsafe_base64_decode(payload.token.split("/")[0]))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, payload.token.split("/")[1]):
            return {"error": "Invalid or expired token"}, 400

        user.password = make_password(payload.new_password)
        user.save()

        return {"message": "Password reset successful"}
    
    except (User.DoesNotExist, ValueError, TypeError):
        return {"error": "Invalid reset link"}, 400

# ✅ Request Password Reset (Send Email)
@router.post("/password-reset/request", tags=["Auth"])
def request_password_reset(request, payload: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email=payload.email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [payload.email],
        )

        return {"message": "Password reset link sent to your email"}
    
    except User.DoesNotExist:
        return {"error": "No account found with this email"}, 404

# =========================================================

def authenticated_user_or_error(request, message="You must be logged in"):
    """Check if user is authenticated, return user or error response"""
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        return None, JsonResponse({"error": message}, status=401)
    try:
        user = get_object_or_404(User, id=user_id)
        return user, None
    except Exception as e:
        return None, JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
def user_profile_pic_path(instance, filename):
    """Generate unique path for profile pictures"""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")

def fetch_all_users():
    """Fetch all users from the database"""
    return list(User.objects.all().values("id", "username", "email", "date_joined"))

def get_related_object(model, field, value):
    """
    Helper function to retrieve an object by a specific field.
    Returns a tuple: (object, None) if found, or (None, JsonResponse error) if not.
    """
    try:
        obj = model.objects.get(**{field: value})
        return obj, None
    except model.DoesNotExist:
        return None, JsonResponse({"error": f"{model.__name__} with {field} '{value}' does not exist."}, status=400)

@router.get("/whoami", tags=["Auth"])
def whoami(request):
    """
    GET /jobs/whoami - Returns user's ID, username, role, wallet balance, and reviews.
    """
    # Retrieve the user ID from the session; if missing, use a test user.
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # Use a test user if session is missing
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)

    # Ensure the Profile exists; this also creates it if missing.
    profile, _ = Profile.objects.get_or_create(user=user)

    # Get user's role and wallet balance
    role = profile.role
    wallet_balance = profile.balance  # Assuming balance is stored in this field
    badges = profile.badges  # if you want to include any badges

    # Compute average rating for the user
    average_rating = Review.objects.filter(reviewed=user).aggregate(avg_rating=Avg("rating"))["avg_rating"] or 5.0

    # Fetch all reviews for the user and serialize them
    user_reviews = list(
        Review.objects.filter(reviewed=user).values("reviewer__username", "rating", "feedback", "created_at")
    )

    return JsonResponse({
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": role,
        "wallet_balance": str(wallet_balance),  # converting Decimal to string if needed
        "badges": badges,
        "rating": round(average_rating, 2),
        "user_reviews": user_reviews,
    })

@router.post("/login", tags=["Auth"])
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

@router.post("/signup", tags=["Auth"])
def signup_view(request, payload: SignupSchema):
    """POST /jobs/signup - Creates a new user and profile"""
    try:
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        user.backend = get_backends()[0].__class__.__name__
        login(request, user)
        
        Profile.objects.create(user=user, role= payload.role)  # Default role, modify if needed

        return Response({"message": "success"}, status=200)
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

@router.post("/logout", tags=["Auth"])
def logout_view(request):
    """POST /jobs/logout - Logs out the current user"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)

@router.post("/change-password", tags=["Auth"])
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


   
@router.get("/check-session")
def check_session(request):
    user_id = request.session.get("_auth_user_id")
    return JsonResponse({"user_id": user_id})
    
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

@router.put("/profile", tags=["Profile"])
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
# ----------------------------------------------------------------------
# Job Endpoints
# ----------------------------------------------------------------------


@router.get("/job-industries/", response=list[IndustrySchema], tags=["Jobs"])
def get_job_industries(request):
    return JobIndustry.objects.all()

@router.get("/job-subcategories/", response=list[SubCategorySchema], tags=["Jobs"])
def get_job_subcategories(request):
    return JobSubCategory.objects.all()

@router.post("/create-job", auth=None, tags=["Jobs"])
def create_job(request, payload: CreateJobSchema):
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # Temporary test user
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

    # 🔹 Calculate job duration in hours
    start_datetime = datetime.combine(job_date, start_time)
    end_datetime = datetime.combine(job_date, end_time)

    if end_datetime <= start_datetime:
        return JsonResponse({"error": "End time must be later than start time"}, status=400)

    duration_seconds = (end_datetime - start_datetime).total_seconds()
    duration_hours = round(duration_seconds / 3600, 2)  # Convert seconds to hours

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

    # 🔹 Create the job WITHOUT the `duration` field
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
            rate=Decimal(str(payload.rate)),  # ✅ Convert to Decimal
            location=payload.location,
            payment_status="Pending",
            status="pending",
        )


    # 🔹 Generate unique transaction reference
    transaction_ref = str(uuid.uuid4())

    return JsonResponse({
        "success": True,
        "message": "Job created successfully. Proceed to payment.",
        "job_id": new_job.id,
        "transaction_ref": transaction_ref,
        "duration": duration_hours  # ✅ Include duration in response
    }, status=201)

@router.get("/clientjobs")
def get_client_jobs(request, page: int = Query(1, gt=0), page_size: int = Query(50, gt=0)):
    """Retrieve jobs posted by a client with pagination"""
    
    # Authenticate user
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        # Fallback: Use first available user for testing
        user = User.objects.first()
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)
    
    # Query jobs for the authenticated client
    qs = Job.objects.filter(client_id=user.id).order_by("-date")

    # Paginate results
    paginator = Paginator(qs, page_size)
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = []  # Empty page, return empty list

    # Serialize jobs manually (since duration is a computed property)
    jobs_data = []
    for job in jobs_page:
        duration_hours = (
            ((job.actual_shift_end - job.actual_shift_start).total_seconds() / 3600)
            if job.actual_shift_start and job.actual_shift_end
            else None
        )

        jobs_data.append({
            "id": job.id,
            "title": job.title,
            "client_username": job.client.username,
            "duration": round(duration_hours, 2) if duration_hours else "Not started",
            "date": job.date.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "location": job.location,
            "rate": str(job.rate),  # Convert Decimal to string for JSON compatibility
            "applicants_needed": job.applicants_needed,
            "status": job.status,
            "payment_status": job.payment_status,
        })
    
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

# ====================================================

def serialize_job(job, include_extra=False):
    """Serialize job object into a dictionary with optional extra fields"""
    base_data = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "status": job.status,
        "date": job.date if job.date else None,
        "start_time": job.start_time if job.start_time else None,
        "end_time": job.end_time if job.end_time else None,
        "duration": str(job.duration),  # Ensuring it remains a string
        "rate": str(job.rate),
        "location": job.location,
        "latitude": job.latitude if job.latitude else None,
        "longitude": job.longitude if job.longitude else None,
        "is_shift_ongoing": job.is_shift_ongoing,
        "employer_name": job.client.first_name if job.client else "Anonymous",
        "date_posted": job.created_at if job.created_at else None,
        "updated_at": job.updated_at if job.updated_at else None,
        "applicants_needed": job.applicants_needed,
        "job_type": job.job_type,
        "shift_type": job.shift_type,
        "payment_status": job.payment_status,
        "total_amount": str(job.total_amount),
        "service_fee": str(job.service_fee),
        "start_date": job.date if job.date else None,
        "start_time_str": str(job.start_time) if job.start_time else None,
        "end_time_str": str(job.end_time) if job.end_time else None
    }

    return base_data


# ----------------------------------------------------------------------
# Saved Jobs Endpoints
# ----------------------------------------------------------------------
@router.post("/save-job/{job_id}", tags=["Jobs"])
def save_job(request, job_id: str):
    """POST /jobs/save-job/<job_id> - Saves a job for the current user"""
    user, error = authenticated_user_or_error(request)

    job, error = get_related_object(Job, "pk", job_id)  # ✅ Fix: Removed extra argument

    if error:
        return error
    
    saved_job, created = SavedJob.objects.get_or_create(user=user, job=job)
    message = "Job saved successfully" if created else "Job is already saved"
    return Response({"message": message}, status=201 if created else 200)

@router.delete("/save-job/{job_id}", tags=["Jobs"])
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
    except Exception as e:
        return Response({"error": "An unexpected error occurred"}, status=500)

@router.get("/saved-jobs", tags=["Jobs"])
def user_saved_jobs(request):
    """
    GET /jobs/saved-jobs - Lists all saved jobs for the authenticated user.
    """
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # Use a test user if session is missing
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)
    # Use the authenticated user (from session) in the query
    saved_records = SavedJob.objects.filter(user=user).select_related("job")

    saved_jobs_list = [
        {
            "saved_job_id": record.id,
            "saved_at": record.saved_at.strftime("%Y-%m-%d %H:%M:%S"),
            "job": {
                "title": record.job.title,
                "industry": record.job.industry.name if record.job.industry else None,
                "subcategory": record.job.subcategory.name if record.job.subcategory else None,
                "status": record.job.status,
                "pay_status": record.job.status,
                "location": record.job.location,
                "created_at": record.job.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        }
        for record in saved_records
    ]

    return JsonResponse({"saved_jobs": saved_jobs_list}, status=200)


@router.get("/accepted-list", tags=["Jobs"])
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
















@router.get("/{job_id}", response=JobDetailSchema)  # Dynamic route after
def job_detail(request, job_id: int):
    """GET /jobs/<job_id> - Returns details for a single job"""
    job = get_object_or_404(Job, id=job_id)
    return serialize_job(job, include_extra=True)

# ----------------------------------------------------------------------
# Review Endpoints
# ----------------------------------------------------------------------


# router = Router(tags=["Jobs"])  # attach the router to "Jobs" or "Ratings"
@router.post("/ratings", tags=["Review"], )
def create_rating(request, payload: ReviewCreateSchema):
    """
    POST /jobs/ratings
    Submits a rating for another user.
    """
    # 1) Make sure user is authenticated (session-based, or however you handle it)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to rate."}, status=401)
    
    # 2) Ensure the "reviewed_id" user exists
    reviewed_user = get_object_or_404(User, pk=payload.reviewed_id)

    # 3) Create the rating
    new_rating = Review.objects.create(
        reviewer=request.user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback or ""
    )
    return {
        "message": "Review submitted",
        "rating_id": new_rating.id
    }






@router.get("/ratings/{user_id}", tags=["Review"])
def get_user_ratings(request, user_id: int):
    """GET /jobs/ratings/{user_id} - Retrieves all ratings for a user"""
    reviewed_user = get_object_or_404(User, pk=user_id)
    all_ratings = Review.objects.filter(reviewed=reviewed_user)
    return {
        "user_id": reviewed_user.id,
        "username": reviewed_user.username,
        "average_rating": Review.get_average_rating(reviewed_user),
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
    """
    Creates a dispute for a job.

    Returns:
      - 201 with dispute id and status on success.
      - 400 if the user already raised a dispute for the job.
      - 401 if the user is not authenticated.
      - 422 if dispute data is invalid.
    """
    # Check authentication using our helper function
    user, error = authenticated_user_or_error(request)
    if error:
        return JsonResponse({"error": error.content.decode()}, status=401)

    # Get the job or 404 if not found
    job = get_object_or_404(Job, pk=job_id)

    # Check if the user already raised a dispute for this job
    existing_dispute = Dispute.objects.filter(job=job, created_by=user).first()
    if existing_dispute:
        return JsonResponse({"error": "You have already raised a dispute for this job."}, status=400)

    # Create the dispute using cleaned-up payload values
    dispute = Dispute.objects.create(
        job=job,
        created_by=user,
        title=payload.title.strip(),
        description=payload.description.strip(),
    )

    return JsonResponse({
        "message": "Dispute created successfully.",
        "dispute_id": dispute.id,
        "status": dispute.status,
    }, status=201)


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




# -------------------------------------------------------------------
# 📌 SHIFT SCHEDULING
# -------------------------------------------------------------------

@router.post("/jobs/{job_id}/shifts", tags=["Shifts"])
def create_or_update_shift(request, job_id: int, payload: dict):
    """
    Creates or updates shift info for a given job (morning/night).
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    job = get_object_or_404(Job, pk=job_id)

    # If you have a Shift model, replace this placeholder
    shift_data = {
        "job_id": job.id,
        "shiftType": payload.get("shiftType", "morning"),
        "startTime": payload.get("startTime", "08:00"),
        "endTime": payload.get("endTime", "17:00"),
    }
    
    return {"message": "Shift created/updated", "shift": shift_data}


@router.get("/jobs/{job_id}/shifts", tags=["Shifts"])
def get_job_shifts(request, job_id: int):
    """
    Returns the shift schedule details for a given job.
    """
    job = get_object_or_404(Job, pk=job_id)

    # Placeholder return since there's no Shift model in the provided code
    return {"message": f"Shifts for job {job.id} (placeholder)"}


@router.post("/jobs/{job_id}/start-shift", tags=["Shifts"])
@permission_classes([IsAuthenticated])
def start_shift(request, job_id: int):
    """
    Mark a job shift as started.
    """
    job = get_object_or_404(Job, id=job_id)

    # Check if user is an accepted applicant for the job
    if request.user not in job.applicants_accepted.all():
        return Response({"error": "Unauthorized"}, status=403)

    job.actual_shift_start = timezone.now()
    job.save()
    
    return {"status": "shift_started", "start_time": job.actual_shift_start}


@router.post("/jobs/{job_id}/end-shift", tags=["Shifts"])
@permission_classes([IsAuthenticated])
def end_shift(request, job_id: int):
    """
    Mark a job shift as ended.
    """
    job = get_object_or_404(Job, id=job_id)

    # Check if user is an accepted applicant for the job
    if request.user not in job.applicants_accepted.all():
        return Response({"error": "Unauthorized"}, status=403)

    job.actual_shift_end = timezone.now()
    job.save()
    
    return {"status": "shift_ended", "duration": job.duration}



@router.post("/feedback", tags=["Feedback"])
def submit_feedback(request, payload: FeedbackSchema):
    """POST /api/feedback - Submit feedback to PayShift"""
    user = request.user if request.user.is_authenticated else None

    feedback = Feedback.objects.create(
        user=user,
        message=payload.message,
        rating=payload.rating
    )

    return JsonResponse({
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id
    }, status=201)


# ==============================
# 📌 Standard Library Imports
# ==============================
import os
import uuid
import requests
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2

# ==============================
# 📌 Django Imports
# ==============================
from django.db import IntegrityError
from django.db.models import Avg, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash,
    get_user_model, get_backends
)
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# ==============================
# 📌 Third-Party Imports
# ==============================
from ninja import Router, File, Query
from ninja.files import UploadedFile
from ninja.responses import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ninja import Schema
from ninja.responses import Response
# ==============================
# 📌 Local Imports (Models & Schemas)
# ==============================
from .models import (
    Job, JobIndustry, JobSubCategory, Profile, Review, SavedJob, 
    Application, Dispute, Feedback
)
from .schemas import (
    LoginSchema, SignupSchema, CreateJobSchema, IndustrySchema,
    SubCategorySchema, JobDetailSchema, LocationSchema,
    ReviewCreateSchema, DisputeCreateSchema, DisputeUpdateSchema,
    PasswordResetSchema, PasswordResetRequestSchema, FeedbackSchema
)

# ==============================
# 📌 Initialize Router & User Model
# ==============================
router = Router()
User = get_user_model()


# ==============================
# 📌 Paystack Configuration
# ==============================
PAYSTACK_SECRET_KEY = getattr(settings, "PAYSTACK_SECRET_KEY", None)
PAYSTACK_PUBLIC_KEY = getattr(settings, "PAYSTACK_PUBLIC_KEY", None)
PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

if not PAYSTACK_SECRET_KEY:
    raise ValueError("PAYSTACK_SECRET_KEY is missing in settings.py")

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------


def authenticated_user_or_error(request, message="You must be logged in"):
    """Check if user is authenticated, return user or error response"""
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        return None, JsonResponse({"error": message}, status=401)
    try:
        user = get_object_or_404(User, id=user_id)
        return user, None
    except Exception as e:
        return None, JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
def get_csrf_token(request):
    """GET /jobs/csrf-token - Returns CSRF token"""
    from django.middleware.csrf import get_token
    return {"csrf_token": get_token(request)}

def check_session(request):
    user_id = request.session.get("_auth_user_id")
    return JsonResponse({"user_id": user_id})

def fetch_all_users():
    """Fetch all users from the database"""
    return list(User.objects.all().values("id", "username", "email", "date_joined"))

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


# =========================================================
# Auth Endpoints
# =========================================================
   
@router.post("/password-reset", tags=["Auth"])
def reset_password(request, payload: PasswordResetSchema):
    try:
        uid = force_str(urlsafe_base64_decode(payload.token.split("/")[0]))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, payload.token.split("/")[1]):
            return {"error": "Invalid or expired token"}, 400

        user.password = make_password(payload.new_password)
        user.save()

        return {"message": "Password reset successful"}
    
    except (User.DoesNotExist, ValueError, TypeError):
        return {"error": "Invalid reset link"}, 400

@router.post("/password-reset/request", tags=["Auth"])
def request_password_reset(request, payload: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email=payload.email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [payload.email],
        )

        return {"message": "Password reset link sent to your email"}
    
    except User.DoesNotExist:
        return {"error": "No account found with this email"}, 404
    
@router.post("/login", tags=["Auth"])
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

@router.post("/signup", tags=["Auth"])
def signup_view(request, payload: SignupSchema):
    """POST /jobs/signup - Creates a new user and profile"""
    try:
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            
        )
        user.backend = get_backends()[0].__class__.__name__
        login(request, user)
        
        Profile.objects.create(user=user, role= payload.role)  # Default role, modify if needed

        return Response({"message": "success"}, status=200)
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

@router.post("/logout", tags=["Auth"])
def logout_view(request):
    """POST /jobs/logout - Logs out the current user"""
    user, error = authenticated_user_or_error(request)
    if error:
        return error
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)

@router.post("/change-password", tags=["Auth"])
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


    
# ----------------------------------------------------------------------
# User/Profile Endpoints
# ----------------------------------------------------------------------

@router.get("/all-users", tags=["User"])
def get_all_users_view(request):
    """GET /jobs/all-users - Returns list of all users"""
    return {"users": fetch_all_users()}

@router.get("/whoami", tags=["User"])
def whoami(request):
    """
    GET /jobs/whoami - Returns user's ID, username, role, wallet balance, and reviews.
    """
    # Retrieve the user ID from the session; if missing, use a test user.
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # Use a test user if session is missing
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)

    """GET /jobs/profile - Fetches current user's profile info"""
    # user, error = authenticated_user_or_error(request)
    # if error:
    #     return error
    # Ensure the Profile exists; this also creates it if missing.
    profile, _ = Profile.objects.get_or_create(user=user)
    profile = getattr(user, "profile", None)

    # Get user's role and wallet balance
    role = profile.role
    wallet_balance = profile.balance  # Assuming balance is stored in this field
    badges = profile.badges  # if you want to include any badges

    # Compute average rating for the user
    average_rating = Review.objects.filter(reviewed=user).aggregate(avg_rating=Avg("rating"))["avg_rating"] or 5.0

    # Fetch all reviews for the user and serialize them
    user_reviews = list(
        Review.objects.filter(reviewed=user).values("reviewer__username", "rating", "feedback", "created_at")
    )

    pic_url = profile.profile_pic.url if (profile and profile.profile_pic) else ""
   
    return JsonResponse({
        "name": f"{user.first_name} {user.last_name}",  # Include full name
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": role,
        "wallet_balance": str(wallet_balance),  # converting Decimal to string if needed
        "badges": badges,
        "rating": round(average_rating, 2),
        "user_reviews": user_reviews,
        "profilePicUrl": pic_url,
        
    })

@router.get("/wallet/balance/", tags=["User"])
def get_wallet_balance(request):
    """Retrieve the wallet balance for the current authenticated user"""
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    # Ensure the user has a profile with a balance field
    profile, _ = Profile.objects.get_or_create(user=user)

    return JsonResponse({
        "user_id": user.id,
        "wallet_balance": str(profile.balance)  # Convert Decimal to string for JSON response
    }, status=200)
   
   
@router.put("/profile/update", tags=["Profile"])
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

def serialize_job(job, include_extra=False):
    """Serialize job object into a dictionary with optional extra fields"""
    base_data = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "status": job.status,
        "date": job.date if job.date else None,
        "start_time": job.start_time if job.start_time else None,
        "end_time": job.end_time if job.end_time else None,
        "duration": str(job.duration),  # Ensuring it remains a string
        "rate": str(job.rate),
        "location": job.location,
        "latitude": job.latitude if job.latitude else None,
        "longitude": job.longitude if job.longitude else None,
        "is_shift_ongoing": job.is_shift_ongoing,
        "employer_name": job.client.first_name if job.client else "Anonymous",
        "date_posted": job.created_at if job.created_at else None,
        "updated_at": job.updated_at if job.updated_at else None,
        "applicants_needed": job.applicants_needed,
        "job_type": job.job_type,
        "shift_type": job.shift_type,
        "payment_status": job.payment_status,
        "total_amount": str(job.total_amount),
        "service_fee": str(job.service_fee),
        "start_date": job.date if job.date else None,
        "start_time_str": str(job.start_time) if job.start_time else None,
        "end_time_str": str(job.end_time) if job.end_time else None
    }

    return base_data


@router.get("/job-industries/", response=list[IndustrySchema], tags=["Jobs"])
def get_job_industries(request):
    return JobIndustry.objects.all()

@router.get("/job-subcategories/", response=list[SubCategorySchema], tags=["Jobs"])
def get_job_subcategories(request):
    return JobSubCategory.objects.all()

@router.get("/alljobs",tags=["Jobs"])
def get_jobs(request):
    jobs = Job.objects.all()
    return {"jobs": list(jobs.values("id", "title", "client__username", "duration", "date", "start_time", "end_time", "location", "rate", "applicants_needed"))}


@router.get("/{job_id}", response=JobDetailSchema,tags=["Jobs"])  # Dynamic route after
def job_detail(request, job_id: int):
    """GET /jobs/<job_id> - Returns details for a single job"""
    job = get_object_or_404(Job, id=job_id)
    return serialize_job(job, include_extra=True)


# ----------------------------------------------------------------------
#  Client Job Endpoints
# ----------------------------------------------------------------------


@router.get("/clientjobs/details/", tags=["Client's Jobs"])
def get_client_jobs_details(request, page: int = Query(1, gt=0), page_size: int = Query(50, gt=0)):
    """
    ✅ GET /clientjobs/details/
    Retrieves **detailed** job postings by the logged-in client.
    """
    # Authenticate user
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    user = get_object_or_404(User, id=user_id)

    # Fetch jobs created by the authenticated client
    qs = Job.objects.filter(client=user).order_by("-date")

    # Paginate results
    paginator = Paginator(qs, page_size)
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = []  # Return empty list if page is out of range

    # Serialize job data
    jobs_data = []
    for job in jobs_page:
        duration_hours = (
            ((job.actual_shift_end - job.actual_shift_start).total_seconds() / 3600)
            if job.actual_shift_start and job.actual_shift_end
            else None
        )

        jobs_data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "industry": job.industry.name if job.industry else None,
            "subcategory": job.subcategory.name if job.subcategory else None,
            "client_username": job.client.username,
            "date_posted": job.created_at.strftime("%Y-%m-%d"),
            "date": job.date.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "location": job.location,
            "rate": str(job.rate),  # Convert Decimal to string
            "applicants_needed": job.applicants_needed,
            "status": job.status,
            "payment_status": job.payment_status,
            "total_duration_hours": round(duration_hours, 2) if duration_hours else "Not started",
        })

    return JsonResponse({
        "jobs": jobs_data,
        "page": page,
        "total_pages": paginator.num_pages,
        "total_jobs": paginator.count,
    }, status=200)



@router.get("/clientjobs/details/{client_id}/", tags=["Client's Jobs"])
def get_client_jobs_by_id(request, client_id: int, page: int = Query(1, gt=0), page_size: int = Query(50, gt=0)):
    """
    ✅ GET /clientjobs/details/{client_id}/
    Retrieves **detailed** job postings by a specific client.
    """
    # Fetch client user object
    client = get_object_or_404(User, id=client_id)

    # Fetch jobs created by the given client
    qs = Job.objects.filter(client=client).order_by("-date")

    # Paginate results
    paginator = Paginator(qs, page_size)
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = []  # Return empty list if page is out of range

    # Serialize job data
    jobs_data = []
    for job in jobs_page:
        duration_hours = (
            ((job.actual_shift_end - job.actual_shift_start).total_seconds() / 3600)
            if job.actual_shift_start and job.actual_shift_end
            else None
        )

        jobs_data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "industry": job.industry.name if job.industry else None,
            "subcategory": job.subcategory.name if job.subcategory else None,
            "client_username": job.client.username,
            "date_posted": job.created_at.strftime("%Y-%m-%d"),
            "date": job.date.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "location": job.location,
            "rate": str(job.rate),  # Convert Decimal to string
            "applicants_needed": job.applicants_needed,
            "status": job.status,
            "payment_status": job.payment_status,
            "total_duration_hours": round(duration_hours, 2) if duration_hours else "Not started",
        })

    return JsonResponse({
        "client_id": client.id,
        "client_username": client.username,
        "jobs": jobs_data,
        "page": page,
        "total_pages": paginator.num_pages,
        "total_jobs": paginator.count,
    }, status=200)


@router.get("/client/workers/list/{client_id}/", tags=["Client's Jobs"])
def get_applicants_worked_with(request, client_id: int):
    """
    ✅ GET /client/workers/list/{client_id}/
    Retrieves a list of **applicants (workers)** who have worked with a given client.
    """

    # Fetch the client user object
    client = get_object_or_404(User, id=client_id)

    # Query jobs that the client has completed (status = "completed")
    completed_jobs = Job.objects.filter(client=client, status="completed")

    # Get unique applicants who worked on these jobs
    applicants = User.objects.filter(application__job__in=completed_jobs, application__status="accepted").distinct()

    # Serialize the applicant data
    applicants_list = [
        {
            "applicant_id": applicant.id,
            "username": applicant.username,
            "full_name": f"{applicant.first_name} {applicant.last_name}",
            "email": applicant.email,
            "date_joined": applicant.date_joined.strftime("%Y-%m-%d"),
            "total_jobs_worked": Application.objects.filter(applicant=applicant, status="accepted").count(),
        }
        for applicant in applicants
    ]

    return JsonResponse({
        "client_id": client.id,
        "client_username": client.username,
        "total_applicants": len(applicants_list),
        "applicants": applicants_list
    }, status=200)





@router.post("/create-job", auth=None, tags=["Job Management"])
def create_job(request, payload: CreateJobSchema):
    
    # user, error = authenticated_user_or_error(request)
    # if error:
    #     return error    
    
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # Temporary test user
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

    # 🔹 Calculate job duration in hours
    start_datetime = datetime.combine(job_date, start_time)
    end_datetime = datetime.combine(job_date, end_time)

    if end_datetime <= start_datetime:
        return JsonResponse({"error": "End time must be later than start time"}, status=400)

    duration_seconds = (end_datetime - start_datetime).total_seconds()
    duration_hours = round(duration_seconds / 3600, 2)  # Convert seconds to hours

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

    # 🔹 Create the job WITHOUT the `duration` field
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
            rate=Decimal(str(payload.rate)),  # ✅ Convert to Decimal
            location=payload.location,
            payment_status="Pending",
            status="pending",
        )


    # 🔹 Generate unique transaction reference
    transaction_ref = str(uuid.uuid4())

    return JsonResponse({
        "success": True,
        "message": "Job created successfully. Proceed to payment.",
        "job_id": new_job.id,
        "transaction_ref": transaction_ref,
        "duration": duration_hours  # ✅ Include duration in response
    }, status=201)




@router.put("/job/cancel/{job_id}/", tags=["Job Management"])
def cancel_job(request, job_id: int):
    """
    ✅ PUT /job/cancel/{job_id}/
    Updates the status of a job to 'canceled'.
    """

    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    # Get the job and check if the user is the owner (client)
    job = get_object_or_404(Job, id=job_id)

    if job.client != user:
        return JsonResponse({"error": "You do not have permission to cancel this job"}, status=403)

    # Ensure the job can be canceled (it shouldn't be completed or already canceled)
    if job.status in ["completed", "canceled"]:
        return JsonResponse({"error": f"Job is already {job.status}"}, status=400)

    # Update job status to 'canceled'
    job.status = "canceled"
    job.save()

    return JsonResponse({
        "message": "Job has been successfully canceled",
        "job_id": job.id,
        "new_status": job.status
    }, status=200)
































# ----------------------------------------------------------------------
# Saved Jobs Endpoints
# ----------------------------------------------------------------------



@router.get("/saved-jobs/", tags=["Saved Jobs"])
def user_saved_jobs(request):
    """GET /api/saved-jobs/ - Lists all saved jobs for the authenticated user."""
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    saved_records = SavedJob.objects.filter(user=user).select_related("job")

    if not saved_records.exists():
        return JsonResponse({"error": "No saved jobs found"}, status=404)

    saved_jobs_list = []
    for record in saved_records:
        try:
            saved_jobs_list.append({
                "saved_job_id": record.id,
                "saved_at": record.saved_at.strftime("%Y-%m-%d %H:%M:%S"),
                "job": {
                    "id": record.job.id,
                    "title": record.job.title,
                    "industry": record.job.industry.name if record.job.industry else None,
                    "subcategory": record.job.subcategory.name if record.job.subcategory else None,
                    "status": record.job.status,
                    "pay_status": record.job.pay_status,  # Fixed pay_status field
                    "location": record.job.location,
                    "created_at": record.job.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            })
        except Exception as e:
            return JsonResponse({"error": f"Error processing job: {str(e)}"}, status=500)

    return JsonResponse({"saved_jobs": saved_jobs_list}, status=200)



# ✅ Save a job
@router.post("/saved-jobs/add/{job_id}/", tags=["Saved Jobs"])
def save_job(request, job_id: int):
    """
    ✅ POST /jobs/saved-jobs/add/{job_id}/
    Saves a job for the authenticated user.
    """
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "User not authenticated"}, status=403)  

    job = get_object_or_404(Job, id=job_id)

    if SavedJob.objects.filter(user=user, job=job).exists():
        return Response({"error": "Job already saved"}, status=400)  

    SavedJob.objects.create(user=user, job=job)
    return Response({"message": "Job saved successfully"}, status=201)


# ✅ Delete a saved job
@router.delete("/saved-jobs/delete/{job_id}/", tags=["Saved Jobs"])
def unsave_job(request, job_id: int):
    """DELETE /api/saved-jobs/delete/{job_id}/ - Removes a job from user's saved list"""
    user = request.user

    if not user.is_authenticated:
        return Response({"error": "User not authenticated"}, status=403)

    try:
        saved_record = SavedJob.objects.get(user=user, job_id=job_id)
        saved_record.delete()
        return Response({"message": "Job unsaved successfully"}, status=200)
    except SavedJob.DoesNotExist:
        return Response({"error": "You haven't saved this job yet"}, status=404)
    except Exception as e:
        return Response({"error": "An unexpected error occurred"}, status=500)









# ----------------------------------------------------------------------
# Review Endpoints
# ----------------------------------------------------------------------

@router.post("/ratings", tags=["Review"], )
def create_rating(request, payload: ReviewCreateSchema):
    """
    POST /jobs/ratings
    Submits a rating for another user.
    """
    # 1) Make sure user is authenticated (session-based, or however you handle it)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to rate."}, status=401)
    
    # 2) Ensure the "reviewed_id" user exists
    reviewed_user = get_object_or_404(User, pk=payload.reviewed_id)

    # 3) Create the rating
    new_rating = Review.objects.create(
        reviewer=request.user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback or ""
    )
    return {
        "message": "Review submitted",
        "rating_id": new_rating.id
    }


@router.get("/applicant/reviews/{applicant_id}/", tags=["Review"])
def get_applicant_reviews(request, applicant_id: int):
    """
    ✅ GET /applicant/reviews/{applicant_id}/
    Retrieves all **ratings & reviews** for a specific applicant.
    """

    # Fetch the applicant user object
    applicant = get_object_or_404(User, id=applicant_id)

    # Get all reviews where this applicant was reviewed
    reviews = Review.objects.filter(reviewed=applicant).select_related("reviewer")

    # Calculate the applicant's **average rating**
    average_rating = reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0.0

    # Serialize review data
    review_list = [
        {
            "reviewer": review.reviewer.username,
            "rating": review.rating,
            "feedback": review.feedback,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for review in reviews
    ]

    return JsonResponse({
        "applicant_id": applicant.id,
        "applicant_username": applicant.username,
        "average_rating": round(average_rating, 2),
        "total_reviews": reviews.count(),
        "reviews": review_list
    }, status=200)


@router.get("/ratings/{user_id}", tags=["Review"])
def get_user_ratings(request, user_id: int):
    """GET /jobs/ratings/{user_id} - Retrieves all ratings for a user"""
    reviewed_user = get_object_or_404(User, pk=user_id)
    all_ratings = Review.objects.filter(reviewed=reviewed_user)
    return {
        "user_id": reviewed_user.id,
        "username": reviewed_user.username,
        "average_rating": Review.get_average_rating(reviewed_user),
        "ratings": [{
            "id": r.id,
            "reviewer": r.reviewer.username,
            "rating": r.rating,
            "feedback": r.feedback,
            "created_at": r.created_at.isoformat()
        } for r in all_ratings]
    }





# ----------------------------------------------------------------------
# Applicant Clients Endpoints
# ----------------------------------------------------------------------



@router.get("/applicant/jobs/details/{applicant_id}/", tags=["Applicant's Jobs"])
def get_jobs_applied_by_applicant(request, applicant_id: int):
    """
    ✅ GET /applicant/jobs/details/{applicant_id}/
    Retrieves **all jobs an applicant has applied for**, including job details.
    """

    # Fetch the applicant user object
    applicant = get_object_or_404(User, id=applicant_id)

    # Get jobs where the applicant has submitted an application
    applied_jobs = (
        Job.objects.filter(applications__applicant=applicant)
        .select_related("client", "industry", "subcategory")
        .order_by("-date")
    )

    # Convert queryset to list of job details
    jobs_list = [
        {
            "job_id": job.id,
            "title": job.title,
            "industry": job.industry.name if job.industry else None,
            "subcategory": job.subcategory.name if job.subcategory else None,
            "client_id": job.client.id,
            "client_username": job.client.username,
            "client_name": f"{job.client.first_name} {job.client.last_name}".strip(),
            "date": job.date.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "location": job.location,
            "rate": str(job.rate),  # Convert Decimal to string for JSON
            "status": job.status,
            "payment_status": job.payment_status,
        }
        for job in applied_jobs
    ]

    return JsonResponse({
        "applicant_id": applicant.id,
        "applicant_username": applicant.username,
        "total_jobs_applied": len(jobs_list),
        "jobs": jobs_list
    }, status=200)



@router.get("/applicant/jobs/count/{applicant_id}/", tags=["Applicant's Jobs"])
def get_total_jobs_taken(request, applicant_id: int):
    """
    ✅ GET /applicant/jobs/count/{applicant_id}/
    Retrieves the **total number of jobs** an applicant has taken.
    """

    # Fetch the applicant user object
    applicant = get_object_or_404(User, id=applicant_id)

    # Count the number of jobs where the applicant's application was accepted
    total_jobs_taken = Application.objects.filter(applicant=applicant, status="accepted").count()

    return JsonResponse({
        "applicant_id": applicant.id,
        "applicant_username": applicant.username,
        "total_jobs_taken": total_jobs_taken
    }, status=200)


@router.get("/accepted-list", tags=["Applicant's Jobs"])
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


@router.get("/applicant/clients/list/{applicant_id}/", tags=["Applicant's Clients"])
def get_clients_worked_with(request, applicant_id: int):
    """
    ✅ GET /applicant/clients/list/{applicant_id}/
    Retrieves a list of **clients** an applicant has worked with.
    """

    # Fetch the applicant user object
    applicant = get_object_or_404(User, id=applicant_id)

    # Get distinct clients the applicant has worked with based on completed jobs
    clients = (
        Job.objects.filter(status="completed", applications__applicant=applicant)
        .values("client__id", "client__username", "client__first_name", "client__last_name")
        .distinct()
    )

    # Convert the queryset to a list of dictionaries
    clients_list = [
        {
            "client_id": client["client__id"],
            "client_username": client["client__username"],
            "client_name": f"{client['client__first_name']} {client['client__last_name']}".strip(),
        }
        for client in clients
    ]

    return JsonResponse({
        "applicant_id": applicant.id,
        "applicant_username": applicant.username,
        "total_clients_worked_with": len(clients_list),
        "clients": clients_list
    }, status=200)


# ----------------------------------------------------------------------
# Dispute Endpoints
# ----------------------------------------------------------------------

@router.post("/jobs/{job_id}/disputes", tags=["Disputes"])
def create_dispute(request, job_id: int, payload: DisputeCreateSchema):
    """
    Creates a dispute for a job.

    Returns:
      - 201 with dispute id and status on success.
      - 400 if the user already raised a dispute for the job.
      - 401 if the user is not authenticated.
      - 422 if dispute data is invalid.
    """
    # Check authentication using our helper function
    user, error = authenticated_user_or_error(request)
    if error:
        return JsonResponse({"error": error.content.decode()}, status=401)

    # Get the job or 404 if not found
    job = get_object_or_404(Job, pk=job_id)

    # Check if the user already raised a dispute for this job
    existing_dispute = Dispute.objects.filter(job=job, created_by=user).first()
    if existing_dispute:
        return JsonResponse({"error": "You have already raised a dispute for this job."}, status=400)

    # Create the dispute using cleaned-up payload values
    dispute = Dispute.objects.create(
        job=job,
        created_by=user,
        title=payload.title.strip(),
        description=payload.description.strip(),
    )

    return JsonResponse({
        "message": "Dispute created successfully.",
        "dispute_id": dispute.id,
        "status": dispute.status,
    }, status=201)


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

# -------------------------------------------------------------------
# 📌 SHIFT SCHEDULING
# -------------------------------------------------------------------

@router.post("/jobs/{job_id}/shifts", tags=["Shifts"])
def create_or_update_shift(request, job_id: int, payload: dict):
    """
    Creates or updates shift info for a given job (morning/night).
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)

    job = get_object_or_404(Job, pk=job_id)

    # If you have a Shift model, replace this placeholder
    shift_data = {
        "job_id": job.id,
        "shiftType": payload.get("shiftType", "morning"),
        "startTime": payload.get("startTime", "08:00"),
        "endTime": payload.get("endTime", "17:00"),
    }
    
    return {"message": "Shift created/updated", "shift": shift_data}


@router.get("/jobs/{job_id}/shifts", tags=["Shifts"])
def get_job_shifts(request, job_id: int):
    """
    Returns the shift schedule details for a given job.
    """
    job = get_object_or_404(Job, pk=job_id)

    # Placeholder return since there's no Shift model in the provided code
    return {"message": f"Shifts for job {job.id} (placeholder)"}


@router.post("/jobs/{job_id}/start-shift", tags=["Shifts"])
@permission_classes([IsAuthenticated])
def start_shift(request, job_id: int):
    """
    Mark a job shift as started.
    """
    job = get_object_or_404(Job, id=job_id)

    # Check if user is an accepted applicant for the job
    if request.user not in job.applicants_accepted.all():
        return Response({"error": "Unauthorized"}, status=403)

    job.actual_shift_start = timezone.now()
    job.save()
    
    return {"status": "shift_started", "start_time": job.actual_shift_start}


@router.post("/jobs/{job_id}/end-shift", tags=["Shifts"])
@permission_classes([IsAuthenticated])
def end_shift(request, job_id: int):
    """
    Mark a job shift as ended.
    """
    job = get_object_or_404(Job, id=job_id)

    # Check if user is an accepted applicant for the job
    if request.user not in job.applicants_accepted.all():
        return Response({"error": "Unauthorized"}, status=403)

    job.actual_shift_end = timezone.now()
    job.save()
    
    return {"status": "shift_ended", "duration": job.duration}



@router.post("/feedback", tags=["Feedback"])
def submit_feedback(request, payload: FeedbackSchema):
    """POST /api/feedback - Submit feedback to PayShift"""
    user = request.user if request.user.is_authenticated else None

    feedback = Feedback.objects.create(
        user=user,
        message=payload.message,
        rating=payload.rating
    )

    return JsonResponse({
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id
    }, status=201)


