from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from .views import admin_signup, admin_dashboard
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    
    path("adminaccess/signup/", admin_signup, name="admin_signup"),
    path("adminaccess/login/", LoginView.as_view(template_name="admin_login.html"), name="admin_login"),
    path("adminaccess/logout/", LogoutView.as_view(next_page="admin_login"), name="admin_logout"),
    path("adminaccess/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("adminaccess/", admin.site.urls),  # Django default admin
    
    # User Management
    path('adminaccess/users/', views.get_all_users),
    path('adminaccess/users/<int:user_id>/', views.get_user_by_id),
    path('adminaccess/users/<int:user_id>/activate/', views.activate_user),
    path('adminaccess/users/<int:user_id>/delete/', views.delete_user),

    # Job Management
    path('adminaccess/jobs/', views.get_all_jobs),
    path('adminaccess/jobs/<int:job_id>/', views.get_job_by_id),
    path('adminaccess/jobs/<int:job_id>/status/', views.update_job_status),
    path('adminaccess/jobs/<int:job_id>/delete/', views.delete_job),

    # Dispute Management
    path('adminaccess/disputes/', views.get_all_disputes),
    path('adminaccess/disputes/<int:dispute_id>/', views.get_dispute_by_id),
    path('adminaccess/disputes/<int:dispute_id>/resolve/', views.resolve_dispute),
    path('adminaccess/disputes/<int:dispute_id>/delete/', views.delete_dispute),

    # Payment Management
    path('adminaccess/payments/', views.get_all_payments),
    path('adminaccess/payments/<int:payment_id>/', views.get_payment_by_id),
    path('adminaccess/payments/<int:payment_id>/status/', views.update_payment_status),
    path('adminaccess/payments/<int:payment_id>/delete/', views.delete_payment),

    # Analytics & Reports
    path('adminaccess/analytics/', views.generate_analytics_report),
]