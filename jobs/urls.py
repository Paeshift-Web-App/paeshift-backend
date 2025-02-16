# jobs/urls.py
from django.urls import path
from ninja import NinjaAPI
from .api import router as jobs_router

api = NinjaAPI()
api.add_router("", jobs_router)

urlpatterns = [
    path("", api.urls),  
]
