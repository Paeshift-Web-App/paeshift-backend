from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from .views import admin_signup, admin_dashboard
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    
    path("admin/signup/", admin_signup, name="admin_signup"),
    path("admin/login/", LoginView.as_view(template_name="admin_login.html"), name="admin_login"),
    path("admin/logout/", LogoutView.as_view(next_page="admin_login"), name="admin_logout"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/", admin.site.urls),  # Django default admin
    
    # User Management
    path('admin/users/', views.get_all_users),
    path('admin/users/<int:user_id>/', views.get_user_by_id),
    path('admin/users/<int:user_id>/activate/', views.activate_user),
    path('admin/users/<int:user_id>/delete/', views.delete_user),

    # Job Management
    path('admin/jobs/', views.get_all_jobs),
    path('admin/jobs/<int:job_id>/', views.get_job_by_id),
    path('admin/jobs/<int:job_id>/status/', views.update_job_status),
    path('admin/jobs/<int:job_id>/delete/', views.delete_job),

    # Dispute Management
    path('admin/disputes/', views.get_all_disputes),
    path('admin/disputes/<int:dispute_id>/', views.get_dispute_by_id),
    path('admin/disputes/<int:dispute_id>/resolve/', views.resolve_dispute),
    path('admin/disputes/<int:dispute_id>/delete/', views.delete_dispute),

    # Payment Management
    path('admin/payments/', views.get_all_payments),
    path('admin/payments/<int:payment_id>/', views.get_payment_by_id),
    path('admin/payments/<int:payment_id>/status/', views.update_payment_status),
    path('admin/payments/<int:payment_id>/delete/', views.delete_payment),

    # Analytics & Reports
    path('admin/analytics/', views.generate_analytics_report),
]