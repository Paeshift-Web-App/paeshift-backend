from django.apps import AppConfig

class SocialAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "socialauth"

    def ready(self):
        import socialauth.signals  # ✅ Import the signals
