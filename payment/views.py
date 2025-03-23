

from .models import Payment
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
import uuid
import json
import requests

def payment_page(request):
    """
    Renders a page displaying Payment records.
    """
    payments = Payment.objects.all()
    return render(request, "payments.html", {"payments": payments})



