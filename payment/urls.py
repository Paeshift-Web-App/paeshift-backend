from django.urls import path, include
from .views import payment_page
from django.urls import path
from .views import initiate_payment
# from .api import router

urlpatterns = [
    path("payments/", payment_page, name="payment_page"),
    path("initiate-payment/", initiate_payment, name="initiate_payment"),
    # path("api/", router.urls),
]

