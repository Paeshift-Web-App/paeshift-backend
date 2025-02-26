from django.contrib import admin
from .models import *
from jobchat.models import *

from django.contrib import admin
from django.contrib.sites.models import Site

class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "domain", "name")  # Display PK (id), domain, and name
    ordering = ("id",)  # Optional: Order by ID

admin.site.unregister(Site)  # Unregister default admin
admin.site.register(Site, SiteAdmin)  # Register with custom admin

@admin.register(JobIndustry)
class JobIndustryAdmin(admin.ModelAdmin):
    """
    Admin for the JobIndustry model.
    """
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(JobSubCategory)
class JobSubCategoryAdmin(admin.ModelAdmin):
    """
    Admin for the JobSubCategory model.
    """
    list_display = ("industry", "name")
    search_fields = ("industry__name", "name")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin for the main Job model, including newly added fields
    like industry, sub_category, rate_per_hour, etc.
    """
    list_display = (
        "title",
        "client",
        "status",
        "industry",
        "subcategory",
        "rate",
        "applicants_needed",
        "job_type",
        "shift_type",
        "created_at",
    )
    list_filter = (
        "status",
        "payment_status",
        "created_at",
        "industry",
        "subcategory",
        "job_type",
        "shift_type",
    )
    search_fields = (
        "title",
        "client__username",
        "applicant__username",
        "industry__name",
        "subcategory__name",
    )
    readonly_fields = ("created_at", "last_location_update")

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "saved_at")
    search_fields = ("user__username", "job__title")
    readonly_fields = ("saved_at",)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "job", "is_accepted", "applied_at")
    list_filter = ("is_accepted",)
    search_fields = ("applicant__username", "job__title")
    readonly_fields = ("applied_at",)

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("title", "job", "created_by", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "created_by__username")
    readonly_fields = ("created_at", "updated_at")

@admin.register(LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "latitude", "longitude", "timestamp")
    search_fields = ("user__username", "job__title")
    readonly_fields = ("timestamp",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payer",
        "recipient",
        "job",
        "original_amount",
        "payment_status",
        "created_at",
    )
    list_filter = ("payment_status", "created_at")
    search_fields = ("payer__username", "recipient__username", "job__title", "pay_code")
    readonly_fields = ("created_at", "confirmed_at")

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "reviewed", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "reviewed__username")
    readonly_fields = ("created_at",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "profile_pic")
    list_filter = ("role",)
    search_fields = ("user__username", "role")
