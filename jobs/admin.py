from django.contrib import admin
from .models import *
from jobchat.models import *

# 🚀 REMOVE Site-related registration
# from django.contrib.sites.models import Site
# try:
#     admin.site.unregister(Site)
# except admin.sites.NotRegistered:
#     pass  # ✅ Skip if not registered

# try:
#     admin.site.register(Site)
# except admin.sites.AlreadyRegistered:
#     pass  # ✅ Skip if already registered

# ------------------------------------------------------
# 🔹 JOB-RELATED ADMIN CONFIGURATIONS
# ------------------------------------------------------

@admin.register(JobIndustry)
class JobIndustryAdmin(admin.ModelAdmin):
    """Admin for Job Industries."""
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(JobSubCategory)
class JobSubCategoryAdmin(admin.ModelAdmin):
    """Admin for Job Subcategories."""
    list_display = ("industry", "name")
    search_fields = ("industry__name", "name")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title", "client", "status", "industry", "subcategory",
        "rate", "applicants_needed", "job_type", "shift_type", "created_at",
    )
    list_filter = ("status", "created_at", "industry", "subcategory", "job_type", "shift_type")
    search_fields = ("title", "client__username", "applicant__username", "industry__name", "subcategory__name")
    readonly_fields = ("created_at", "last_location_update")

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    """Admin for Saved Jobs."""
    list_display = ("user", "job", "saved_at")
    search_fields = ("user__username", "job__title")
    readonly_fields = ("saved_at",)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin for Job Applications."""
    list_display = ("applicant", "job", "is_accepted", "applied_at")
    list_filter = ("is_accepted",)
    search_fields = ("applicant__username", "job__title")
    readonly_fields = ("applied_at",)

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    """Admin for Job Disputes."""
    list_display = ("title", "job", "created_by", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "created_by__username")
    readonly_fields = ("created_at", "updated_at")

@admin.register(LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    """Admin for Tracking User Location History."""
    list_display = ("user", "job", "latitude", "longitude", "timestamp")
    search_fields = ("user__username", "job__title")
    readonly_fields = ("timestamp",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin for Ratings & Reviews."""
    list_display = ("reviewer", "reviewed", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "reviewed__username")
    readonly_fields = ("created_at",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for User Profiles."""
    list_display = ("user", "role", "profile_pic")
    list_filter = ("role",)
    search_fields = ("user__username", "role")
