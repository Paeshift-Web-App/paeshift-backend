from django.contrib import admin
from .models import Job, JobApplication, SavedJob


# Admin for Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'job_date', 'payment', 'applicants_needed')
    search_fields = ('title', 'location', 'posted_by__user__username')
    list_filter = ('job_date', 'date_posted')

# Admin for JobApplication
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status')
    search_fields = ('job__title', 'applicant__user__username')
    list_filter = ('status',)

# Admin for SavedJob
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_on')
    search_fields = ('user__user__username', 'job__title')
