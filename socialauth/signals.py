from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def populate_profile(request, user, **kwargs):
    """Automatically update user profile after signing up via social login"""
    if user.socialaccount_set.exists():
        social_account = user.socialaccount_set.first()
        extra_data = social_account.extra_data

        user.first_name = extra_data.get("given_name", "")
        user.last_name = extra_data.get("family_name", "")
        user.save()
