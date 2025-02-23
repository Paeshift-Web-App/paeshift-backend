from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from ninja import NinjaAPI
from socialauth.views import home
from payment.api import payment_router

# ✅ Initialize API
api = NinjaAPI()
# api.add_router("/payment", payment_router)

# ✅ Redirect users to Google signup instead of showing "Sign Up Closed"
def signup_redirect(request):
    return redirect("/accounts/google/login/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("socialauth.urls")),  # ✅ SocialAuth as root URL
    path("accounts/", include("allauth.urls")),  # ✅ Django-Allauth for authentication
    path("accounts/signup/", signup_redirect, name="account_signup"),  # ✅ Force Google signup
    path("jobs/", include("jobs.urls")),  # ✅ Job-related routes
    path("jobchat/", include("jobchat.urls")),  # ✅ Job-related routes
   
    # path("api/", api.urls),                      # The single API

]
