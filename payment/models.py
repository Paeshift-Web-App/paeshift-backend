from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job  # Import the Job model from your "jobs" app

User = get_user_model()

class Payment(models.Model):
    """
    Payment model referencing the Job model from the 'jobs' app.
    Handles transactions between payer and recipient.
    """
    
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
        return f"Payment {self.pay_code} - {self.payer.email} -> {self.recipient.email if self.recipient else 'N/A'} ({self.payment_status})"
