# jobs/urls.py
from django.urls import path
from ninja import NinjaAPI
from .api import router as jobs_router

# Create a local NinjaAPI instance specifically for this app
jobs_api = NinjaAPI(title="Jobs API")

# Mount the router from jobs/api.py at the root
jobs_api.add_router("", jobs_router)

urlpatterns = [
    # All endpoints from jobs_router are now available under this path
    path("", jobs_api.urls),  # e.g. /jobs/... in your main urls.py
]
