from django.contrib import admin

from . models import CustomUser, Profile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "lastName", "email"]
    list_filter = ["username", "lastName", "email"]
   # search_fields = ["username", "fullName", "email"]
    list_per_page = 20
    readonly_fields = ["email"]
   # ordering=["fullName", -"date"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "lastName", "location", "rating"]
    list_filter = ["user", "lastName", "location", "rating"]
   # search_fields = ["user", "fullName", "country"]
    list_per_page = 20
    readonly_fields = ["bio"]
    ordering=["lastName"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)


