from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from ninja import Router, Schema
from ninja.responses import Response

from .models import Job, Application, SavedJob

router = Router()

# -------------------------------------------------------
# 1) Auth Schemas
# -------------------------------------------------------
class LoginSchema(Schema):
    email: str
    password: str

class SignupSchema(Schema):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str


# -------------------------------------------------------
# 2) Auth Endpoints
# -------------------------------------------------------
@router.post("/login")
def login_view(request, payload: LoginSchema):
    """
    POST /jobs/login
    Authenticates a user by email/password and logs them in.
    """
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=200)
    return Response({"error": "Invalid credentials"}, status=400)


@router.post("/signup")
def signup(request, payload: SignupSchema):
    """
    POST /jobs/signup
    Creates a new user account if email is unique and passwords match.
    """
    firstName = payload.firstName
    lastName = payload.lastName
    email = payload.email
    password = payload.password
    confirmPassword = payload.confirmPassword

    if not all([firstName, lastName, email, password, confirmPassword]):
        return Response({"error": "All fields are required"}, status=400)

    if password != confirmPassword:
        return Response({"error": "Passwords do not match"}, status=400)

    if User.objects.filter(username=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    try:
        User.objects.create(
            first_name=firstName,
            last_name=lastName,
            username=email,  # Django uses 'username' internally
            email=email,
            password=make_password(password),
        )
        return Response({"message": "Registration successful"}, status=201)
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"}, status=500)


# -------------------------------------------------------
# 3) Jobs Endpoints
# -------------------------------------------------------
@router.get("/client-posted")
def client_posted_jobs(request):
    """
    GET /jobs/client-posted
    Returns a list of all jobs posted by clients (adjust logic as needed).
    """
    # Example: if you want only "client" role, you'd filter Job by job.client's group or role
    # For now, we just return all
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
            "date_posted": "2 days ago",  # Or compute from job.created_at
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
            # Application fields
            "application_id": app.id,
            "applicant_name": app.applicant.first_name,
            "is_accepted": app.is_accepted,
            "applied_at": str(app.applied_at),

            # Job fields
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
        "applicantNeeded": 1,  # or some field if your model tracks how many needed
        "startDate": str(job.date) if job.date else "",
        "startTime": str(job.time) if job.time else "",
    }
    return data


# -------------------------------------------------------
# 4) Saved Jobs Endpoints
# -------------------------------------------------------
@router.post("/save-job/{job_id}")
def save_job(request, job_id: int):
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
