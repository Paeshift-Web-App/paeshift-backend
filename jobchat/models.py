from django.db import models
from django.conf import settings
from jobs.models import Job

class Message(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class LocationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="location_histories"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
