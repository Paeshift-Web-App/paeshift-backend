from django.contrib import admin
from .models import (
    Job, SavedJob, Application, Dispute, LocationHistory,
    Payment, Rating, Profile
)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "amount", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("title", "client__username", "applicant__username")
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
    list_display = ("payer", "recipient", "job", "original_amount", "payment_status", "created_at")
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
