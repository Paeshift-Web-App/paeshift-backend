from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from ninja import NinjaAPI
from payment.api import router as payments_router  
from notifications.api import router as notifications_router  

# ==============================
# 📌 API Instances
# ==============================
api = NinjaAPI(title="Main API", version="2.0.0", urls_namespace="mainapi")

# Secondary API instance (e.g., for job-specific functionality)
app_api = NinjaAPI(title="Other API", version="1.0.0", urls_namespace="otherapi")

# ==============================
# 📌 Register API Routers
# ==============================
api.add_router("/payments/", payments_router) 
api.add_router("/notifications/", notifications_router)  # ✅ Fixed

# ==============================
# 📌 URL Patterns
# ==============================
urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Authentication routes (make sure these apps are installed and configured)
    path("", include("socialauth.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/signup/", lambda request: redirect("/accounts/google/login/"), name="account_signup"),

    # App-specific URLs
    path("jobs/", include("jobs.urls")),
    path("jobchat/", include("jobchat.urls")),
    path("tracker/", include("tracker.urls")),
    path("payment/", include("payment.urls")),

    # Ninja API endpoints
    # path("api/", api.urls),  # Main API endpoints
]












