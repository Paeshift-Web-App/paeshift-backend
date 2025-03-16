from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from .models import LocationHistory, Message

# Resource for exporting LocationHistory
class LocationHistoryResource(resources.ModelResource):
    class Meta:
        model = LocationHistory

# Resource for exporting Messages
class MessageResource(resources.ModelResource):
    class Meta:
        model = Message


@admin.register(LocationHistory)
class LocationHistoryAdmin(ExportMixin, admin.ModelAdmin):  
    list_display = ('user', 'latitude', 'longitude', 'timestamp')  # Fields to display
    search_fields = ('user__username', 'latitude', 'longitude')  # Enable searching
    list_filter = ('user', 'timestamp')  # Enable filtering by user & timestamp
    ordering = ('-timestamp',)  # Show newest records first
    resource_class = LocationHistoryResource  # Enable Excel export


@admin.register(Message)
class MessageAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('sender',  'content', 'timestamp')  # Display fields
    list_filter = ('sender', 'timestamp')  # Filter by sender & receiver
    ordering = ('-timestamp',)  # Show latest messages first
    resource_class = MessageResource  # Enable Excel export
