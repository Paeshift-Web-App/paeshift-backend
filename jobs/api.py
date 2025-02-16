# jobs/api.py

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ninja import Router
from ninja.responses import Response

from .models import *
from .schemas import *  

router = Router()

# -------------------------------------------------------
# 1) Auth Endpoint (Login and Signup)
# -------------------------------------------------------
@router.post("/login")
def login_view(request, payload: LoginSchema):
    """
    POST /jobs/login
    Authenticates a user by email/password and logs them in (session-based).
    Expects JSON:
      {
        "email": "...",
        "password": "..."
      }
    Returns:
      200 - {"message": "Login successful"} if valid
      401 - {"error": "Invalid credentials"} if invalid
    """
    user = authenticate(request, username=payload.email, password=payload.password)
    if user:
        login(request, user)
        return Response({"message": "Login successful"}, status=200)
    return Response({"error": "Invalid credentials"}, status=401)


@router.post("/signup")
def signup_view(request, payload: SignupSchema):
    """
    POST /jobs/signup
    Creates a new user account if email is unique and passwords match.
    Expects JSON:
      {
        "firstName": "...",
        "lastName": "...",
        "email": "...",
        "password": "...",
        "confirmPassword": "..."
      }
    Returns:
      201 - {"message": "Registration successful"} on success
      400 - {"error": "..."} if validation fails
    """
    # Check required fields
    if not all([
        payload.firstName,
        payload.lastName,
        payload.email,
        payload.password,
        payload.confirmPassword
    ]):
        return Response({"error": "All fields are required"}, status=400)

    # Check password match
    if payload.password != payload.confirmPassword:
        return Response({"error": "Passwords do not match"}, status=400)

    # Check if user already exists
    if User.objects.filter(username=payload.email).exists():
        return Response({"error": "Email already exists"}, status=400)

    # Attempt to create user
    try:
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            password=payload.password,
        )
        # Optionally log them in immediately
        login(request, user)

        return Response({"message": "Registration successful"}, status=201)

    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"}, status=500)
# -------------------------------------------------------
# 2) Jobs Endpoints
# -------------------------------------------------------
@router.get("/client-posted")
def client_posted_jobs(request):
    """
    GET /jobs/client-posted
    Returns a list of all jobs posted by clients (adjust logic if needed).
    """
    jobs_qs = Job.objects.all()
    data = []
    for job in jobs_qs:
        data.append({
            "id": job.id,
            "name": job.client.first_name if job.client else "Unknown Client",
            "status": job.status,
            "title": job.title,
            "date": str(job.date) if job.date else "",
            "time": str(job.time) if job.time else "",
            "duration": job.duration,
            "amount": str(job.amount),
            "location": job.location,
            "date_posted": "2 days ago",  # or compute from job.created_at
            "no_of_application": job.no_of_application,
        })
    return data


@router.get("/list")
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


# -------------------------------------------------------
# 3) Saved Jobs Endpoints
# -------------------------------------------------------
@router.post("/save-job/{job_id}")
def save_job(request, job_id: int):
    """
    POST /jobs/save-job/<job_id>
    Saves the job for the current user (session-based).
    """
    if not request.user.is_authenticated:
        return Response({"error": "You must be logged in to save jobs."}, status=401)

    job = get_object_or_404(Job, id=job_id)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        return Response({"message": "Job is already saved."}, status=200)
    return Response({"message": "Job saved successfully."}, status=201)


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
