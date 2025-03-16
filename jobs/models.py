# jobs/models.py

import os
from pathlib import Path
from decimal import Decimal
from django.db import models
from django.utils import timezone
import django
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model

User = get_user_model()

def user_profile_pic_path(instance, filename):
    """
    Generates a unique upload path for user profile pictures.
    Example: "profile_pics/user_5/20250314_142355_myphoto.jpg"
    """
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")

# ------------------------------------------------------
# 1️⃣ Job Industry & Subcategory Models
# ------------------------------------------------------
class JobIndustry(models.Model):
    """Represents a top-level job industry (e.g., IT, Healthcare, Construction)."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class JobSubCategory(models.Model):
    """
    Represents a specific subcategory under a JobIndustry (e.g., Plumbing under Construction).
    """
    industry = models.ForeignKey(
        JobIndustry, on_delete=models.CASCADE, related_name="subcategories"
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} (under {self.industry.name})"

# ------------------------------------------------------
# 2️⃣ Job Model
# ------------------------------------------------------
class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
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
        ('morning', 'Morning (6AM - 2PM)'),
        ('afternoon', 'Afternoon (2PM - 8PM)'),
        ('night', 'Night (8PM - 6AM)'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('held', 'Held in Escrow'),
        ('partial', 'Partially Paid'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="No description provided")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    industry = models.ForeignKey(JobIndustry, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(JobSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    applicants_needed = models.PositiveIntegerField(default=1)
    # ManyToMany through Application for accepted applicants
    applicants_accepted = models.ManyToManyField(
        User, through='Application', related_name='accepted_jobs', blank=True
    )
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='single_day')
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurring_days = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="Comma-separated days (e.g., Monday,Wednesday,Friday)"
    )
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    actual_shift_start = models.DateTimeField(null=True, blank=True)
    actual_shift_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
 
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'payment_status']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    @property
    def duration(self):
        """Calculate actual worked duration in hours."""
        if self.actual_shift_start and self.actual_shift_end:
            delta = self.actual_shift_end - self.actual_shift_start
            return round(delta.total_seconds() / 3600, 2)
        return 0

    @property
    def is_shift_ongoing(self):
        """Return True if the shift has started but not ended."""
        return self.actual_shift_start and not self.actual_shift_end

    def save(self, *args, **kwargs):
        # Auto-calculate total_amount and service_fee if not set
        if not self.total_amount:
            self.service_fee = self.rate * Decimal('0.05')
            self.total_amount = self.rate + self.service_fee
        # Optionally update status based on date
        if self.date < timezone.now().date() and self.status in ['pending', 'upcoming']:
            self.status = 'ongoing'
        super().save(*args, **kwargs)

# ------------------------------------------------------
# 3️⃣ Application Model
# ------------------------------------------------------
class Application(models.Model):
    APPLICANT_STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    is_shown_up = models.BooleanField(default=False)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant} - {self.job} ({self.get_status_display()})"

# ------------------------------------------------------
# 4️⃣ Saved Job Model
# ------------------------------------------------------
class SavedJob(models.Model):
    """Tracks jobs that a user has saved."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user} saved {self.job}"

# ------------------------------------------------------
# 5️⃣ Dispute Model
# ------------------------------------------------------
class Dispute(models.Model):
    """Represents a dispute raised regarding a Job."""
    DISPUTE_STATUS_CHOICES = [
        ("open", "Open"),
        ("in_review", "In Review"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="disputes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disputes_raised")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=DISPUTE_STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute #{self.id} - {self.title} ({self.status})"

# ------------------------------------------------------
# 6️⃣ Rating Model
# ------------------------------------------------------
class Rating(models.Model):
    """User ratings and reviews."""
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
            models.CheckConstraint(check=models.Q(rating__gte=1.0) & models.Q(rating__lte=5.0), name="rating_range"),
            models.UniqueConstraint(fields=["reviewer", "reviewed"], name="unique_rating")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewed} ({self.rating})"

    @classmethod
    def get_average_rating(cls, user):
        result = cls.objects.filter(reviewed=user).aggregate(avg_rating=models.Avg('rating'))
        return result['avg_rating'] or 0.0

# ------------------------------------------------------
# 7️⃣ Profile Model
# ------------------------------------------------------
class Profile(models.Model):
    """Stores additional profile details for a user."""
    ROLE_CHOICES = [
        ("applicant", "Applicant"),
        ("client", "Client"),
        ("admin", "Admin"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="applicant")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    badges = models.JSONField(default=list, blank=True)


    def __str__(self):
        return f"Profile of {self.user.username}"

    def add_to_balance(self, amount):
        if amount > 0:
            self.balance += Decimal(amount)
            self.save()

    def deduct_from_balance(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False
