from django.shortcuts import render
from django.http import JsonResponse
from jobs.models import Job
from .models import Message, LocationHistory

def chat_room(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'chat_room.html', {'job_id': job.id})

def get_messages(request, job_id):
    """Fetches all messages for a job chat."""
    messages = Message.objects.filter(job_id=job_id).order_by("timestamp")
    return JsonResponse([{"sender": m.sender.username, "content": m.content, "timestamp": m.timestamp} for m in messages], safe=False)

def get_job_locations(request, job_id):
    """Fetches the latest location updates for a job."""
    locations = LocationHistory.objects.filter(job_id=job_id).order_by("-timestamp")
    return JsonResponse([{"latitude": loc.latitude, "longitude": loc.longitude, "address": loc.address} for loc in locations], safe=False)
