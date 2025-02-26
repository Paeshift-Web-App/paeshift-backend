
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title="PaeShift API",
        default_version='v1',
        description="API for user authentication",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mod.timson@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    
    public=True,
    permission_classes=(permissions.AllowAny,),
    # authentication_classes=[],
    # authorization_classes=[],
    
)
    
urlpatterns = [
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #path("", include("userAuth.urls")),
    #path("token/", include("rest_framework_simplejwt.urls")),
    
    path("admin/", admin.site.urls),
    path("userApi/v1/", include("authUser.urls")),
    path("jobListing/v1/", include("JobListingPage.urls")),
   
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)