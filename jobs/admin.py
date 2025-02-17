from django.contrib import admin
from .models import Job, Application, LocationHistory

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(LocationHistory)
