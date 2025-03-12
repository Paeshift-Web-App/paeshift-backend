from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
import uuid
import json
import requests

from .models import Payment
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
import uuid
import json
import requests

from .models import Payment


# import uuid
import requests
from django.conf import settings
from ninja import Router, Schema
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Payment

def payment_page(request):
    """
    Renders a page displaying Payment records.
    """
    payments = Payment.objects.all()
    return render(request, "payments.html", {"payments": payments})
