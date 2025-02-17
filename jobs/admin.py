from django.contrib import admin
from .models import Job, SavedJob, Application, Profile

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'job_type', 'created_at', 'updated_at')
    list_filter = ('job_type', 'location', 'created_at')
    search_fields = ('title', 'company', 'location', 'description')
    ordering = ('-created_at',)

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__email', 'job__title')
    ordering = ('-saved_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__email', 'job__title')
    ordering = ('-applied_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('user__email', 'phone_number')
    ordering = ('-created_at',)
