from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Default Django User model
from .models import *
from jobs.models import *


@receiver(post_save, sender=User)
def create_wallet_and_profile(sender, instance, created, **kwargs):
    """
    Creates a wallet, profile, and initial rating when a user is created.
    """
    if created:
        # ✅ Create wallet with default balance
        Wallet.objects.create(user=instance, balance=0.00)



        # ✅ Assign initial rating
        # Rating.objects.create(reviewed=instance, reviewer=instance, rating=5.0)

        print(f"✅ Wallet & Profile created for {instance.email}")
