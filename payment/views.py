from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
import uuid
import json
import requests

from .models import Payment

def initiate_payment(request):
    """
    Initializes a Paystack payment.
    Expects a POST request with 'total', 'reservation_code',
    and optionally 'first_name', 'last_name', and 'phone'.
    """
    if request.method == "POST":
        # Validate amount
        try:
            total = float(request.POST.get("total"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount.")
            return redirect("checkout")
        
        # Convert Naira to kobo
        total_in_kobo = int(total * 100)
        reservation_code = request.POST.get("reservation_code", "")
        pay_code = str(uuid.uuid4())
        
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "User must be logged in.")
            return redirect("checkout")
        user = request.user
        
        # Optional additional fields (if needed)
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        phone = request.POST.get("phone", "")
        
        # Set callback URL (adjust for your environment)
        callback_url = "http://127.0.0.1:8000/completed/"
        
        # Prepare Paystack request data
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "reference": pay_code,
            "email": user.email,
            "amount": total_in_kobo,
            "callback_url": callback_url,
            "order_number": reservation_code,
        }
        
        # Call Paystack initialization endpoint
        try:
            response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
            response_data = response.json()
        except Exception as e:
            messages.error(request, "Network busy, please try again.")
            return redirect("checkout")
        
        # Check if the initialization was successful
        if response.status_code == 200 and "data" in response_data and "authorization_url" in response_data["data"]:
            auth_url = response_data["data"]["authorization_url"]
            
            # Optionally save a Payment record here if needed.
            # For example:
            # Payment.objects.create(user=user, amount=total, pay_code=pay_code, order_no=reservation_code, ...)
            
            return redirect(auth_url)
        else:
            messages.error(request, "Error initializing payment: " + str(response_data.get("message", "Unknown error")))
            return redirect("checkout")
    else:
        return HttpResponse("Invalid request method", status=405)


def payment_page(request):
    """
    Renders a page displaying Payment records.
    """
    payments = Payment.objects.all()
    return render(request, "payments.html", {"payments": payments})
