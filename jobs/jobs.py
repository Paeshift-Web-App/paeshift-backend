from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination

from .models import Job, Application
from .schemas import JobListSchema, ApplicationListSchema
from ninja import Router
from .models import Job
from .schemas import *

router = Router()

@router.get("/client-posted", response=list[JobListSchema])
def client_posted_jobs(request):
    return Job.objects.all()


@router.get("/{job_id}", response=JobListSchema)
def job_detail(request, job_id: int):
    """Get details for a single job."""
    job = get_object_or_404(Job.objects.select_related("client"), id=job_id)
    return job

@router.get("/list", response=list[ApplicationListSchema])
def list_accepted_applications(request):
    """Get all accepted applications with job details."""
    return Application.objects.filter(is_accepted=True).select_related("job", "applicant")