from django.urls import path
from .views import payment_page

urlpatterns = [
    path("payments/", payment_page, name="payment_page"),
    # path("initiate-payment/", initiate_payment, name="initiate_payment"),
]
