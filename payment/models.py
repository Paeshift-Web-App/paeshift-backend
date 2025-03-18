# payments/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
from jobs.models import Job

User = get_user_model()

# ================================================================
# Payment Models
# ================================================================

class Payment(models.Model):
    """
    Records all payment transactions between users
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
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    original_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    service_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    final_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    pay_code = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    refund_requested = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment {self.pay_code} - {self.payer.email} -> {self.recipient.email if self.recipient else 'N/A'} ({self.payment_status})"

    def calculate_fees(self):
        """Calculate service fees and final amount"""
        self.service_fee = self.original_amount * Decimal('0.05')
        self.final_amount = self.original_amount - self.service_fee
        self.save()





# ================================================================
# Wallet Models
# ================================================================

class Wallet(models.Model):
    """
    Tracks user balances and transactions
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="wallet"
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

    def add_funds(self, amount):
        """Add funds to wallet"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += Decimal(amount)
        self.save()

    def deduct_funds(self, amount):
        """Deduct funds from wallet"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False  # Insufficient funds

# ================================================================
# Escrow Models
# ================================================================

class EscrowPayment(models.Model):
    """
    Manages funds held in escrow for job transactions
    """
    STATUS_CHOICES = [
        ('held', 'Funds Held'),
        ('released', 'Funds Released'),
        ('refunded', 'Funds Refunded'),
    ]

    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="escrow_payment"
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_payments'
    )
    applicant = models.ForeignKey(
        User,
        related_name='applicant_payments',
        null=True,
        on_delete=models.SET_NULL
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    service_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    escrow_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='held'
    )
    paystack_reference = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Escrow Payment"
        verbose_name_plural = "Escrow Payments"

    def __str__(self):
        return f"Escrow {self.id} - {self.job.title} ({self.status})"

    def calculate_fees(self):
        """Calculate escrow fees and amounts"""
        self.service_fee = self.total_amount * Decimal('0.05')
        self.escrow_amount = self.total_amount - self.service_fee
        self.save()

    def release_funds(self):
        """Release funds to applicant"""
        if self.status != 'held':
            raise ValueError("Funds can only be released from held status")
        
        self.status = 'released'
        self.save()
        # Add logic to transfer funds to applicant's wallet

    def refund_funds(self):
        """Refund funds to client"""
        if self.status != 'held':
            raise ValueError("Funds can only be refunded from held status")
        
        self.status = 'refunded'
        self.save()
        # Add logic to refund funds to client's wallet