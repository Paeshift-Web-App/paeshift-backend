# ==============================
# 📌 Standard Library Imports
# ==============================
import os
import uuid
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timedelta

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
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ninja import Router
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from jobs.models import Job, Application
from jobchat.models import LocationHistory
from math import radians, sin, cos, sqrt, atan
# ==============================
# 📌 Third-Party Imports
# ==============================
from ninja import Router, File, Query
from ninja.files import UploadedFile
from ninja.responses import Response
import requests

# ==============================
# 📌 Local Imports (Models & Schemas)
# ==============================
from .models import (
    Job, JobIndustry, JobSubCategory, Profile, Rating, SavedJob, 
    Application, Dispute
)
from .schemas import (
    LoginSchema, SignupSchema, CreateJobSchema, IndustrySchema,
    SubCategorySchema, JobDetailSchema, LocationSchema,
    RatingCreateSchema, DisputeCreateSchema, DisputeUpdateSchema
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


# Adding new helper function for job serialization
# ----------------------------------------------------------------------
# Authentication Endpoints
# ----------------------------------------------------------------------
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.db.models import Avg
# from jobs.models import User, Rating
# from yourapp.models import Profile  # Update "yourapp" to your actual app name if different
# from ninja import Router

router = Router()

@router.get("/whoami")
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
    average_rating = Rating.objects.filter(reviewed=user).aggregate(avg_rating=Avg("rating"))["avg_rating"] or 5.0

    # Fetch all reviews for the user and serialize them
    user_reviews = list(
        Rating.objects.filter(reviewed=user).values("reviewer__username", "rating", "feedback", "created_at")
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


@router.post("/payment")
def payment(request):
    return render(request, 'payment.html')




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


@router.get("/{job_id}", response=JobDetailSchema)
def job_detail(request, job_id: int):
    """
    GET /jobs/<job_id> - Retrieve details for a single job.
    """
    job = get_object_or_404(Job, id=job_id)
    return serialize_job(job)



@router.post("/create-job", auth=None)
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
def save_job(request, job_id: str):
    """POST /jobs/save-job/<job_id> - Saves a job for the current user"""
    user, error = authenticated_user_or_error(request)

    job, error = get_related_object(Job, "pk", job_id)  # ✅ Fix: Removed extra argument

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





# ----------------------------------------------------------------------
# Rating Endpoints
# ----------------------------------------------------------------------


# router = Router(tags=["Jobs"])  # attach the router to "Jobs" or "Ratings"
@router.post("/ratings", tags=["Ratings"], )
def create_rating(request, payload: RatingCreateSchema):
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
    new_rating = Rating.objects.create(
        reviewer=request.user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback or ""
    )
    return {
        "message": "Rating submitted",
        "rating_id": new_rating.id
    }






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


@router.post("/jobs/{job_id}/start-shift")
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


@router.post("/jobs/{job_id}/end-shift")
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

