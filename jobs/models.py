from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os
from jobchat.models import *  

User = get_user_model()

def user_profile_pic_path(instance, filename):
    """
    Generates a unique path for user profile images.
    E.g.: 'profile_pics/user_<id>/<timestamp>_<filename>'
    """
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")


# ------------------------------------------------------
# 1) INDUSTRY & SUBCATEGORY MODELS
# ------------------------------------------------------
class JobIndustry(models.Model):
    """
    A top-level industry category (e.g. 'Construction', 'IT', 'Hospitality', etc.).
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class JobSubCategory(models.Model):
    """
    A more specific category within a JobIndustry (e.g. 'Plumbing', 'Web Development', etc.).
    """
    industry = models.ForeignKey(
        JobIndustry,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} (under {self.industry.name})"


# ------------------------------------------------------
# 2) JOB MODEL
# ------------------------------------------------------
class Job(models.Model):
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

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Relationship fields
    industry = models.ForeignKey(
        JobIndustry,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    subcategory = models.ForeignKey(
        JobSubCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # Additional job details
    rate_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Hourly rate for the job."
    )
    applicants_needed = models.PositiveIntegerField(
        default=1,
        help_text="Number of workers needed."
    )
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='single_day',
        help_text="Single day or multiple-day job."
    )
    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_TYPE_CHOICES,
        default='day_shift',
        help_text="Day shift or night shift."
    )

    # Who posted the job, and who is assigned (if any)
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs",
        blank=True,
        null=True
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="applied_jobs",
        blank=True,
        null=True
    )

    # Status / scheduling
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional total pay or budget."
    )
    image = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional URL or path to an image."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Location details (optional live tracking fields)
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_address = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

    # Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed")
        ],
        default="Pending"
    )

    def __str__(self):
        return f"{self.title} - {self.status}"

    @property
    def no_of_application(self):
        """
        Returns the total number of applications for this job.
        """
        return self.applications.count()


# ------------------------------------------------------
# 3) SAVED JOBS
# ------------------------------------------------------
class SavedJob(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_jobs"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="saved_by_users"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.job}"


# ------------------------------------------------------
# 4) APPLICATION
# ------------------------------------------------------
class Application(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.applicant} for {self.job}"


# ------------------------------------------------------
# 5) DISPUTE
# ------------------------------------------------------
class Dispute(models.Model):
    """
    A dispute raised by either a client or applicant regarding a Job.
    """
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="disputes"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="disputes_raised"
    )
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
# 7) PAYMENT
# ------------------------------------------------------
class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Refunded", "Refunded"),
        ("Failed", "Failed"),
    ]

    payer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments_made"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments_received",
        null=True,
        blank=True
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pay_code = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    refund_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.pay_code} - {self.payer.email} - {self.payment_status}"


# ------------------------------------------------------
# 8) RATING
# ------------------------------------------------------
class Rating(models.Model):
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings"
    )
    reviewed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_ratings"
    )
    rating = models.PositiveIntegerField()  # e.g., 1-5 or 1-10 scale
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} rated {self.reviewed} - {self.rating}"

    @staticmethod
    def get_average_rating(user):
        qs = Rating.objects.filter(reviewed=user)
        if qs.exists():
            total = sum(r.rating for r in qs)
            return round(total / qs.count(), 2)
        return 0


# ------------------------------------------------------
# 9) PROFILE
# ------------------------------------------------------
class Profile(models.Model):
    """
    Profile model storing user’s profile pic & role.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    profile_pic = models.ImageField(
        upload_to=user_profile_pic_path,
        null=True,
        blank=True
    )
    ROLE_CHOICES = [
        ("applicant", "Applicant"),
        ("client", "Client"),
        ("admin", "Admin"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="client",
        blank=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

