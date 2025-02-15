# jobs/urls.py
from django.urls import path
from ninja import NinjaAPI
from .api import router as jobs_router

api = NinjaAPI()
# If you do this, final route => /jobs/signup
api.add_router("", jobs_router)

urlpatterns = [
    path("", api.urls),  # => /jobs
]
