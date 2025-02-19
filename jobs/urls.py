# jobs/urls.py
from ninja import NinjaAPI
from .api import router as jobs_router
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),  # allauth routes
    # ... your other routes
]

api = NinjaAPI()
api.add_router("", jobs_router)

urlpatterns = [
    path("", api.urls),  
    path('accounts/', include('allauth.urls')),  # allauth routes
]
