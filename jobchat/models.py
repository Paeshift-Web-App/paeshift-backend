from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import *

User = get_user_model()

class Message(models.Model):
    """Stores chat messages between users for a specific job."""
    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Related Job"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Sender"
    )
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")

    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["-timestamp"]), models.Index(fields=["job"])]
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


class LocationHistory(models.Model):
    """Stores the location updates of users related to a job."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="location_histories", verbose_name="User"
    )
    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="locations", verbose_name="Job"
    )
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    address = models.CharField(max_length=255, blank=True, verbose_name="Address")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["job"]),
            models.Index(fields=["user", "latitude", "longitude"]),
        ]
        verbose_name = "Location History"
        verbose_name_plural = "Location Histories"

    def __str__(self):
        return f"Location for {self.user.username} on {self.job} at {self.timestamp}"
