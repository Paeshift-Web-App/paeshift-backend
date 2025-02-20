from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    # any other auth views you want
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    # ... other endpoints ...
]
