from django.contrib import admin
from .models import Job, Application, LiveLocation

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(LiveLocation)
