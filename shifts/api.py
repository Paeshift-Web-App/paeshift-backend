# shifts/api.py
from ninja import Router
from django.utils import timezone

router = Router(tags=["Shifts"])

@router.post("/jobs/{job_id}/start-shift")
def start_shift(request, job_id: int):
    job = Job.objects.get(id=job_id)
    if request.user != job.applicant:
        return {"error": "Unauthorized"}
    
    job.shift_start = timezone.now()
    job.save()
    return {"status": "shift_started", "start_time": job.shift_start}

@router.post("/jobs/{job_id}/end-shift")
def end_shift(request, job_id: int):
    job = Job.objects.get(id=job_id)
    if request.user != job.applicant:
        return {"error": "Unauthorized"}
    
    job.shift_end = timezone.now()
    job.save()
    return {"status": "shift_ended", "duration": job.duration}