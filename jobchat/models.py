from django.db import models
from django.conf import settings
from jobs.models import Job
from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

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
        return f"{self.sender.timestamp}: {self.content[:50]}"


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
        return f"Location for {self.user} on {self.job} at {self.timestamp}"



# class Message(models.Model):
#     """Stores chat messages between users for a specific job."""
#     job = models.ForeignKey(
#         Job,
#         on_delete=models.CASCADE,
#         related_name="messages",
#         verbose_name="Job"
#     )
#     sender = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="sent_messages",
#         verbose_name="Sender"
#     )
#     content = models.TextField(verbose_name="Message Content")
#     timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")

#     class Meta:
#         ordering = ["-timestamp"]
#         indexes = [
#             models.Index(fields=["-timestamp"]),
#             models.Index(fields=["job"]),
#             models.Index(fields=["sender"]),
#         ]
#         verbose_name = "Chat Message"
#         verbose_name_plural = "Chat Messages"


