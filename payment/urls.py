from django.urls import path
from ninja import NinjaAPI
from .views import payment_page
from .api import router as payment_api_router

api = NinjaAPI()
api.add_router("/payments", payment_api_router)

urlpatterns = [
    path("payments/", payment_page, name="payment_page"),
    path("api/", api.urls),  # ✅ Ensure API routes are included
]
