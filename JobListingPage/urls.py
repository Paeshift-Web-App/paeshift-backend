from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, JobViewSet, JobApplicationViewSet, SavedJobViewSet




router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'job-applications', JobApplicationViewSet)
router.register(r'saved-jobs', SavedJobViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]