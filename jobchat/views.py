# chat/views.py
from django.shortcuts import render
from jobs.models import Job
from django.http import JsonResponse
from .models import *
from jobs.models import *


def chat_room(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'chat_room.html', {'job_id': job.id})


def client_list(request):
    clients = LocationHistory.objects.values('user__username', 'latitude', 'longitude').distinct()
    data = [{"name": c['user__username'], "latitude": c['latitude'], "longitude": c['longitude']} for c in clients]
    return JsonResponse(data, safe=False)


def get_messages(request, job_id):
    messages = Message.objects.filter(job_id=job_id).order_by('timestamp')
    if not messages.exists():
        return JsonResponse({"error": "No messages found."}, status=404)
    
    data = [{"sender": m.sender.username, "content": m.content, "timestamp": str(m.timestamp)} for m in messages]
    return JsonResponse(data, safe=False)


def get_job_locations(request, job_id):
    locations = LocationHistory.objects.filter(job_id=job_id).order_by('-timestamp')
    data = [{"latitude": loc.latitude, "longitude": loc.longitude, "address": loc.address} for loc in locations]
    return JsonResponse(data, safe=False)
