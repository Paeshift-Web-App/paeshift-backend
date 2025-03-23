# jobs/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.contrib.sites.models import Site
from .models import (
    JobIndustry, JobSubCategory, Job, SavedJob,
    Application, Dispute, Review, Profile
)

# Ensure that the Site model is registered only once.
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
try:
    admin.site.register(Site)
except admin.sites.AlreadyRegistered:
    pass

@admin.register(JobIndustry)
class JobIndustryAdmin(admin.ModelAdmin):
    """Admin for Job Industries."""
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 20

@admin.register(JobSubCategory)
class JobSubCategoryAdmin(admin.ModelAdmin):
    """Admin for Job Subcategories."""
    list_display = ("name", "industry")
    list_filter = ("industry",)
    search_fields = ("name", "industry__name")
    list_per_page = 20

from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin for Job Postings."""
    list_display = (
        "title", "client", "status", "payment_status",
        "industry", "subcategory", "rate", "applicants_needed",
        "job_type", "shift_type", "created_at"
    )
    list_filter = (
        "status", "payment_status", "created_at",
        "industry", "subcategory", "job_type", "shift_type"
    )
    search_fields = (
        "title", "client__username", "industry__name",
        "subcategory__name", "location"
    )

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "client", "industry", "subcategory")
        }),
        ("Job Details", {
            "fields": ("job_type", "shift_type", "applicants_needed", "date", "start_time", "end_time", "recurring_days")
        }),
        ("Financials", {
            "fields": ("rate", "service_fee", "total_amount", "payment_status")
        }),
        ("Location", {
            "fields": ("location", "latitude", "longitude", "last_location_update")
        }),
        ("Status & Tracking", {
            "fields": ("status", "actual_shift_start", "actual_shift_end", "updated_at")
        }),
    )

    readonly_fields = ("created_at", "updated_at")  # 🛠️ Fix: Make created_at read-only

    list_per_page = 20








@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    """Admin for Saved Jobs."""
    list_display = ("user", "job", "saved_at")
    search_fields = ("user__username", "job__title")
    readonly_fields = ("saved_at",)
    list_per_page = 20

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin for Job Applications."""
    list_display = ("applicant", "job", "status", "is_shown_up", "rating", "applied_at")
    list_filter = ("status", "is_shown_up", "rating")
    search_fields = ("applicant__username", "job__title")
    readonly_fields = ("applied_at",)
    list_per_page = 20

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    """Admin for Job Disputes."""
    list_display = ("title", "job", "created_by", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "created_by__username", "job__title")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for Ratings & Reviews."""
    list_display = ("reviewer", "reviewed", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "reviewed__username")
    readonly_fields = ("created_at",)
    list_per_page = 20

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for User Profiles."""
    list_display = ("user", "role", "balance", "profile_pic_preview")
    list_filter = ("role",)
    search_fields = ("user__username", "role")
    # readonly_fields = ("profile_pic_preview")
    list_per_page = 20

    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.profile_pic.url
            )
        return "-"
    profile_pic_preview.short_description = "Profile Picture"
