from django.db import models 
from django.conf import settings
from jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"  # ✅ Fixed sender reference

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

    def __str__(self):
        return f"Location for {self.user.username} on {self.job.title} at {self.timestamp}"

