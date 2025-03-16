# from django.contrib import admin
# from import_export.admin import ExportMixin
# from import_export import resources
# from .models import AdminRole, Task, Dispute

# # Resource for exporting AdminRole to Excel
# class AdminRoleResource(resources.ModelResource):
#     class Meta:
#         model = AdminRole

# # Resource for exporting Task to Excel
# class TaskResource(resources.ModelResource):
#     class Meta:
#         model = Task

# # Resource for exporting Dispute to Excel
# class DisputeResource(resources.ModelResource):
#     class Meta:
#         model = Dispute


# @admin.register(AdminRole)
# class AdminRoleAdmin(ExportMixin, admin.ModelAdmin):  # Add ExportMixin for Excel download
#     list_display = ('user', 'role')
#     search_fields = ('user__username', 'role')
#     list_filter = ('role',)  # Allow filtering by role
#     resource_class = AdminRoleResource  # Enable Excel export


# @admin.register(Task)
# class TaskAdmin(ExportMixin, admin.ModelAdmin):
#     list_display = ('title', 'task_type', 'assigned_to', 'completed', 'created_at')
#     search_fields = ('title', 'assigned_to__username')
#     list_filter = ('task_type', 'completed')
#     ordering = ('-created_at',)
#     resource_class = TaskResource  # Enable Excel export


# @admin.register(Dispute)
# class DisputeAdmin(ExportMixin, admin.ModelAdmin):
#     list_display = ('job', 'created_by', 'assigned_admin', 'status', 'created_at')
#     search_fields = ('job__title', 'created_by__username', 'assigned_admin__username')
#     list_filter = ('status',)
#     ordering = ('-created_at',)
#     resource_class = DisputeResource  # Enable Excel export
