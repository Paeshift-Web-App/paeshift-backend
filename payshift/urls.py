from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from ninja import NinjaAPI
# from payment.api import router as payment_api_router

api = NinjaAPI()
# api.add_router("/payments", payment_api_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("socialauth.urls")),  
    path("accounts/", include("allauth.urls")),  
    path("accounts/signup/", lambda request: redirect("/accounts/google/login/"), name="account_signup"),  
    # path("accounts/signup/", signup_redirect, name="account_signup"),  # ✅ Force Google signup
    path("jobs/", include("jobs.urls")),  
    path("jobchat/", include("jobchat.urls")),  
    path("payment/", include("payment.urls")),  

    # path("api/", api.urls),  # ✅ Register API
]



