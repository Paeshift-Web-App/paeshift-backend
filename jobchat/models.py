from django.db import models
from django.conf import settings
from jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

# ====================================================
# ✅ MESSAGE MODEL (Job Chat System)
# ====================================================
class Message(models.Model):
    """Stores messages exchanged in job chats."""
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # ✅ Indexed for faster queries

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


# ====================================================
# ✅ LOCATION HISTORY MODEL (Real-time Tracking)
# ====================================================
class LocationHistory(models.Model):
    """Stores users' location history for jobs."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="location_histories"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # ✅ Indexed for performance

    class Meta:
        ordering = ["-timestamp"]  # ✅ Always fetch latest first

    def __str__(self):
        return f"{self.user.username} - {self.job.title} @ ({self.latitude}, {self.longitude})"


# ====================================================
# ✅ USER LOCATION MODEL (Live User Location)
# ====================================================
class UserLocation(models.Model):
    """Stores users' current location and last update time."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_locations"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="user_locations"
    )
    address = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True, db_index=True)
    timestamp = models.DateTimeField(auto_now=True, db_index=True)  # ✅ Ensures updated location queries are fast

    class Meta:
        ordering = ["-timestamp"]  # ✅ Fetch latest location first

    def __str__(self):
        return f"{self.user.username} - {self.job.title} @ {self.address or 'Unknown'}"
