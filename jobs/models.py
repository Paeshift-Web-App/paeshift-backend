import os
import uuid
import requests
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# 🔹 Profile Image Upload Path
def user_profile_pic_path(instance, filename):
    """Generates a unique path for user profile images."""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")


# ------------------------------------------------------
# 1️⃣ INDUSTRY & SUBCATEGORY MODELS
# ------------------------------------------------------
class JobIndustry(models.Model):
    """Represents a top-level job industry (e.g., IT, Healthcare, Construction)."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class JobSubCategory(models.Model):
    """Specific categories under an industry (e.g., Plumbing under Construction)."""
    industry = models.ForeignKey(JobIndustry, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} (under {self.industry.name})"


# ------------------------------------------------------
# 2️⃣ JOB MODEL
# ------------------------------------------------------
class Job(models.Model):
    """Represents a job posting."""

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    JOB_TYPE_CHOICES = [
        ('single_day', 'Single Day'),
        ('multiple_days', 'Multiple Days'),
    ]
    SHIFT_TYPE_CHOICES = [
        ('day_shift', 'Day Shift'),
        ('night_shift', 'Night Shift'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    # Job details
    title = models.CharField(max_length=255)
    industry = models.ForeignKey(JobIndustry, on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey(JobSubCategory, on_delete=models.CASCADE, blank=True, null=True)
    applicants_needed = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='single_day')
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES, default='day_shift')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", blank=True, null=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="applied_jobs", blank=True, null=True)

    # Scheduling
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Location
    location = models.CharField(max_length=255, blank=True, null=True)
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_address = models.CharField(max_length=255, blank=True, null=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    shift_start = models.DateTimeField(null=True)
    shift_end = models.DateTimeField(null=True)
    is_online = models.BooleanField(default=False)
    shift_type = models.CharField(max_length=20, choices=[('morning', 'Morning'), ('night', 'Night')])
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        return f"{self.title} - {self.status}"

    @property
    def duration(self):
        if self.shift_start and self.shift_end:
            return (self.shift_end - self.shift_start).total_seconds() / 3600
        return 0


# ------------------------------------------------------
# 3️⃣ SAVED JOBS
# ------------------------------------------------------
class SavedJob(models.Model):
    """Tracks jobs that users have saved/bookmarked."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.job}"


# ------------------------------------------------------
# 4️⃣ APPLICATION
# ------------------------------------------------------
class Application(models.Model):
    """Tracks user applications to jobs."""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.applicant} for {self.job}"


# ------------------------------------------------------
# 5️⃣ DISPUTE
# ------------------------------------------------------
class Dispute(models.Model):
    """A dispute raised by either a client or applicant regarding a Job."""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="disputes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disputes_raised")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("in_review", "In Review"),
            ("resolved", "Resolved"),
            ("closed", "Closed"),
        ],
        default="open",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute #{self.id} - {self.title} ({self.status})"


# ------------------------------------------------------
# 6️⃣ RATING
# ------------------------------------------------------
class Rating(models.Model):
    """User ratings and reviews system."""
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1, rating__lte=5),
                name="rating_between_1_and_5",
            ),
            models.UniqueConstraint(
                fields=["reviewer", "reviewed"], name="unique_reviewer_reviewed"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewed} ({self.rating})"

    @staticmethod
    def get_average_rating(user: User) -> float:
        """Calculates the average rating of a given user."""
        ratings = user.received_ratings.all()
        return sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0.0


# ------------------------------------------------------
# 7️⃣ PROFILE
# ------------------------------------------------------
class Profile(models.Model):
    """Stores user’s profile details."""
    ROLE_CHOICES = [
        ("applicant", "Applicant"),
        ("client", "Client"),
        ("admin", "Admin"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added balance field

    def __str__(self):
        return f"Profile of {self.user.username}"
