from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs",blank=True, null=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="applied_jobs", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"), 
        ("Completed", "Completed"), 
        ("Failed", "Failed")
    ], default="Pending")

    @property
    def no_of_application(self):
        return self.applications.count()

    def __str__(self):
        return f"{self.title} - {self.status}"


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.job}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.applicant} for {self.job}"


class LiveLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
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

    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_made")  
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received", null=True, blank=True)  
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="payments")
        
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    pay_code = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)  
    refund_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.pay_code} - {self.payer.email} - {self.payment_status}"


class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    rating = models.PositiveIntegerField()  
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} rated {self.reviewed} - {self.rating}%"

    @staticmethod
    def get_average_rating(user):
        ratings = Rating.objects.filter(reviewed=user)
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 0
