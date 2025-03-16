from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Admin Roles Model
class AdminRole(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('finance', 'Finance Admin'),
        ('support', 'Support Admin'),
        ('moderator', 'Moderator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Task Model for Admins
class Task(models.Model):
    TASK_TYPES = [
        ("dispute_settlement", "Dispute Settlement"),
        ("job_review", "Job Review"),
        ("transaction_verification", "Transaction Verification"),
    ]

    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_task_type_display()})"

