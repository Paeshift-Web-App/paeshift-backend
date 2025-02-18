# jobs/admin.py

from django.contrib import admin
from .models import Job, Application, LocationHistory

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Displays Job model entries with the ID and relevant fields.
    """
    list_display = (
        'id',
        'title',
        'last_latitude',
        'last_longitude',
        'last_address',
        'last_location_update',
    )
    search_fields = ('title', 'last_address')
    ordering = ('-id',)  # sorts so newest ID is first

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Displays Application model entries with the ID, job, and applicant fields.
    """
    list_display = (
        'id',
        'job',
        'applicant',
        'is_accepted',
        'applied_at',
    )
    list_filter = ('is_accepted', 'applied_at')
    search_fields = ('job__title', 'applicant__username')
    ordering = ('-applied_at',)

@admin.register(LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    """
    Displays LocationHistory entries with the ID, job, user, lat/long, etc.
    """
    list_display = (
        'id',
        'job',
        'user',
        'latitude',
        'longitude',
        'address',
        'timestamp',
    )
    list_filter = ('job', 'user', 'timestamp')
    search_fields = ('address', 'job__title', 'user__username')
    ordering = ('-timestamp',)
