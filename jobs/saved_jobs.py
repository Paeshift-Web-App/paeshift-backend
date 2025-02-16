from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import HttpBearer

from ..models import Job, SavedJob
from ..schemas.jobs import SavedJobSchema

router = Router()

@router.post("/save-job/{job_id}", auth=HttpBearer())
def save_job(request, job_id: int):
    """Save a job for the authenticated user."""
    job = get_object_or_404(Job, id=job_id)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    return {"message": "Job saved successfully" if created else "Job already saved"}

@router.get("/saved-jobs", response=list[SavedJobSchema], auth=HttpBearer())
def list_saved_jobs(request):
    """Get all jobs saved by the authenticated user."""
    return SavedJob.objects.filter(user=request.user).select_related("job")