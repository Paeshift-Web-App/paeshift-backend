from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

User = get_user_model()

def user_profile_pic_path(instance, filename):
    """
    Example function to generate a unique path for user profile images.
    E.g.: 'profile_pics/user_<id>/<timestamp>_<filename>'
    """
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("profile_pics", f"user_{instance.user.id}", f"{timestamp}_{filename}")

class Job(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Last shared location fields (to store the most recent location)
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_address = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # Optional: Track when the last location was updated
    last_location_update = models.DateTimeField(null=True, blank=True)
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
        return self.applications.count()


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


class Dispute(models.Model):
    """
    Represents a dispute raised by either a client or applicant regarding a Job.
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

    # Optionally store who last updated the dispute
    # last_updated_by = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="disputes_updated",
    # )

    # resolution = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Dispute #{self.id} - {self.title} ({self.status})"


class LocationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location for {self.user} on {self.job}"


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
        ratings = Rating.objects.filter(reviewed=user)
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 0


class Profile(models.Model):
    """
    Example Profile model storing a user’s profile pic & other fields.
    Typically you'd put this in jobs/models.py or a separate app.
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
    # Add any other fields you like

    def __str__(self):
        return f"Profile of {self.user.username}"
