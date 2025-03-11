from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.sites.models import Site
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payer",
        "recipient",
        "job",
        "original_amount",
        "payment_status",
        "created_at",
    )
    list_filter = ("payment_status", "created_at")
    search_fields = ("payer__username", "recipient__username", "job__title", "pay_code")
    readonly_fields = ("created_at", "confirmed_at")