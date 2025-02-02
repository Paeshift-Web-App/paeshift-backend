# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import UserProfileViewSet, JobViewSet, JobApplicationViewSet, SavedJobViewSet




# urlpatterns = [
#     path("api/userProfile/", UserProfileViewSet.as_view()),
#     path("api/job/", JobViewSet.as_view()),
#     path("api/jobApplication/", JobApplicationViewSet.as_view()),
#     path("api/savedJob/", SavedJobViewSet.as_view()),
# ]


# from django.urls import path
# from .views import UserProfileViewSet, JobViewSet, JobApplicationViewSet, SavedJobViewSet

# urlpatterns = [
#     path("api/userProfile/", UserProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path("api/job/", JobViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path("api/jobApplication/", JobApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path("api/savedJob/", SavedJobViewSet.as_view({'get': 'list', 'post': 'create'})),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, JobViewSet, JobApplicationViewSet, SavedJobViewSet

# Router setup
router = DefaultRouter()
router.register(r'userProfile', UserProfileViewSet, basename='user-profile')
router.register(r'job', JobViewSet, basename='job')
router.register(r'jobApplication', JobApplicationViewSet, basename='job-application')
router.register(r'savedJob', SavedJobViewSet, basename='saved-job')

urlpatterns = [
    path("", include(router.urls)),  # This automatically includes all routes
]
