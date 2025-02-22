from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import home, dashboard

urlpatterns = [
    path("", home, name="home"),  # ✅ Root page
    path("accounts/", include("allauth.urls")),  # ✅ Allauth handles authentication
    path("dashboard/", dashboard, name="dashboard"),  
    path("logout/", LogoutView.as_view(), name="account_logout"),  # ✅ Uses the correct name
]

# http://127.0.0.1:8000/accounts/login/
# http://127.0.0.1:8000/accounts/logout/
# http://127.0.0.1:8000/accounts/3rdparty/signup/
# http://127.0.0.1:8000/accounts/google/login/?process=login