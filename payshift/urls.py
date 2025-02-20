# payshift/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Ninja
from ninja import NinjaAPI
from accounts.api import accounts_router
from payment.api import payment_router

# Create a NinjaAPI instance
api = NinjaAPI()

# Register your routers
api.add_router("/accounts", accounts_router)
api.add_router("/payment", payment_router)
# api.add_router("/jobs", jobs_router)
# api.add_router("/jobchat", jobchat_router)

urlpatterns = [
    path("admin/", admin.site.urls),

    # django-allauth routes for social logins:
    path("accounts/", include("allauth.urls")),

    # If your "jobs" app has its own urls.py:
    path("jobs/", include("jobs.urls")),

    # Expose NinjaAPI at /api/:
    path("api/", api.urls),

    # (Optional) If you still use python-social-auth for some reason:
    # path("oauth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
