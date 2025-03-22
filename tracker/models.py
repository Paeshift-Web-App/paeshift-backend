from django.db import models
from django.conf import settings
from jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

# ====================================================
# ✅ JOB TRACKER MODEL (Tracks job progress)
# ====================================================
class JobTracker(models.Model):
    """Tracks the status and progress of jobs."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    job = models.OneToOneField(
        Job, on_delete=models.CASCADE, related_name="tracker"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job {self.job.title}: {self.get_status_display()}"

    def start_job(self):
        """Marks the job as started."""
        self.status = "ongoing"
        self.started_at = models.DateTimeField(auto_now_add=True)
        self.save()

    def complete_job(self):
        """Marks the job as completed."""
        self.status = "completed"
        self.ended_at = models.DateTimeField(auto_now_add=True)
        self.save()

    def cancel_job(self):
        """Marks the job as cancelled."""
        self.status = "cancelled"
        self.save()
