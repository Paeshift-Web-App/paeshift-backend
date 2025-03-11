from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os
from jobchat.models import *  
# jobs/models.py (or wherever your models live)
from django.db import models

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
        ('multiple_days', 'Weekly'),
    ]
    SHIFT_TYPE_CHOICES = [
        ('day_shift', 'Day Shift'),
        ('night_shift', 'Night Shift'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
    ]
    
    # Job details
    title = models.CharField(max_length=255)
    industry = models.ForeignKey("JobIndustry", on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey("JobSubCategory", on_delete=models.CASCADE, blank=True, null=True)
    applicants_needed = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='single_day')
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES, default='day_shift')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", blank=True, null=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="applied_jobs", blank=True, null=True)
    
    # Scheduling
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    pay_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Additional fields
    # image = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Location tracking
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_address = models.CharField(max_length=255, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

    # Payment status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.title} - {self.status}"

    @property
    def no_of_applications(self):
        """Returns the total number of applications for this job."""
        return self.applications.count()


# class JobApplication(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
#     applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied_jobs")
#     status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")])
#     applied_at = models.DateTimeField(auto_now_add=True)


# class JobAssignment(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="assigned_workers")
#     worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_jobs")
#     assigned_at = models.DateTimeField(auto_now_add=True)






# from django.db import models
# from django.contrib.auth.models import User

# class Job(models.Model):
#     STATUS_CHOICES = [
#         ('upcoming', 'Upcoming'),
#         ('ongoing', 'Ongoing'),
#         ('completed', 'Completed'),
#         ('canceled', 'Canceled'),
#     ]
#     JOB_TYPE_CHOICES = [
#         ('single_day', 'Single Day'),
#         ('multiple_days', 'Multiple Days'),
#     ]
#     SHIFT_TYPE_CHOICES = [
#         ('day_shift', 'Day Shift'),
#         ('night_shift', 'Night Shift'),
#     ]
#     PAYMENT_STATUS_CHOICES = [
#         ("Pending", "Pending"),
#         ("Completed", "Completed"),
#         ("Failed", "Failed")
#     ]
    
#     # Job details
#     title = models.CharField(max_length=255)
#     industry = models.ForeignKey("JobIndustry", on_delete=models.CASCADE, blank=True, null=True)
#     subcategory = models.ForeignKey("JobSubCategory", on_delete=models.CASCADE, blank=True, null=True)
#     applicants_needed = models.PositiveIntegerField(default=1)
#     job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='single_day')
#     shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES, default='day_shift')
#     client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", blank=True, null=True)
#     applicants = models.ManyToManyField(User, related_name="applied_jobs", blank=True)
    
#     # Scheduling
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
#     date = models.DateField(blank=True, null=True)
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)
#     duration = models.DurationField(blank=True, null=True)  # Changed to DurationField
#     rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

#     # Additional fields
#     location = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_deleted = models.BooleanField(default=False)  # Soft delete functionality

#     # Location tracking
#     last_latitude = models.FloatField(null=True, blank=True)
#     last_longitude = models.FloatField(null=True, blank=True)
#     last_address = models.CharField(max_length=255, blank=True)
#     last_location_update = models.DateTimeField(null=True, blank=True)

#     # Payment status
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending")

#     def __str__(self):
#         return f"{self.title} - {self.status}"

#     @property
#     def no_of_applications(self):
#         """Returns the total number of applicants for this job."""
#         return self.applicants.count()

# # ------------------------------------------------------
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
# 8) RATING
# ------------------------------------------------------


class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    rating = models.PositiveIntegerField()  # e.g. 1–5
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewed} ({self.rating})"


    # @staticmethod
    # def get_average_rating(user: User) -> float:
    #     qs = Rating.objects.filter(reviewed=user)
    #     if qs.exists():
    #         total = sum(r.rating for r in qs)
    #         return round(total / qs.count(), 2)
    #     return 0.0

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

