from django.urls import path
from .views import payment_page

urlpatterns = [
    path("payments/", payment_page, name="payment_page"),
]
