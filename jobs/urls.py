# jobs/urls.py
from django.urls import path
from .views import jobs  # Import the jobs view from your views.py
from ninja import NinjaAPI
from .api import router as jobs_router

# Create a local NinjaAPI instance specifically for this app
jobs_api = NinjaAPI(title="Jobs API")

# Mount the router from jobs/api.py at the root
jobs_api.add_router("", jobs_router)

urlpatterns = [
    path("", jobs_api.urls), 
    path('jobs/', jobs, name='jobs'),  # Maps /jobs/ to the jobs view
    
]
# from django.urls import path

# app_name = 'myapp'  # Optional: Namespace for URL names

# urlpatterns = [
# ]