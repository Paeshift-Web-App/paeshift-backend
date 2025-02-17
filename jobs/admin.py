from django.contrib import admin
from .models import *

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    search_fields = ('title', 'company', 'location', 'description')
    ordering = ('-created_at',)

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'job__title')
    ordering = ('-saved_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'job__title')
    ordering = ('-applied_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'phone_number')
