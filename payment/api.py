import uuid
import requests
from django.conf import settings
from ninja import Router, Schema
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Payment

router = Router(tags=["Payments"])

# ✅ Schema for initiating payments
class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    payment_method: str  # "paystack" or "flutterwave"


# ✅ Initiate Payment (Paystack or Flutterwave)
@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """
    Initializes a payment via Paystack or Flutterwave.
    """
    total_in_kobo = int(payload.total * 100)
    pay_code = str(uuid.uuid4())
    callback_url = "http://127.0.0.1:8000/completed/"

    if payload.payment_method == "paystack":
        return process_paystack_payment(payload, total_in_kobo, pay_code, callback_url)
    elif payload.payment_method == "flutterwave":
        return process_flutterwave_payment(payload, pay_code, callback_url)
    else:
        return JsonResponse({"error": "Invalid payment method"}, status=400)


# ✅ Paystack Payment Processing
def process_paystack_payment(payload, total_in_kobo, pay_code, callback_url):
    """
    Handles Paystack payment initialization.
    """
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "reference": pay_code,
        "email": payload.first_name + "@test.com",
        "amount": total_in_kobo,
        "callback_url": callback_url,
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and "data" in response_data and "authorization_url" in response_data["data"]:
        return {"authorization_url": response_data["data"]["authorization_url"]}
    return {"error": "Error initializing Paystack payment", "details": response_data.get("message", "Unknown error")}


# ✅ Flutterwave Payment Processing
def process_flutterwave_payment(payload, pay_code, callback_url):
    """
    Handles Flutterwave payment initialization.
    """
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "tx_ref": pay_code,
        "amount": payload.total,
        "currency": "NGN",
        "redirect_url": callback_url,
        "customer": {
            "email": payload.first_name + "@test.com",
            "name": f"{payload.first_name} {payload.last_name}",
            "phone_number": payload.phone,
        },
    }

    response = requests.post("https://api.flutterwave.com/v3/payments", headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and "data" in response_data and "link" in response_data["data"]:
        return {"authorization_url": response_data["data"]["link"]}
    return {"error": "Error initializing Flutterwave payment", "details": response_data.get("message", "Unknown error")}
