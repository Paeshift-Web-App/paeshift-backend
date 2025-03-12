import uuid
import requests
from django.conf import settings
from django.db import transaction
from ninja import Router, Schema
from django.http import JsonResponse
from django.shortcuts import render

from jobs.models import User, Profile
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
    callback_url = "http://127.0.0.1:8000/payments/payment-completed/"

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

    if response.status_code == 200 and response_data.get("data") and response_data["data"].get("authorization_url"):
        return JsonResponse({"authorization_url": response_data["data"]["authorization_url"]})
    return JsonResponse({"error": "Error initializing Paystack payment", "details": response_data.get("message", "Unknown error")})


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

    if response.status_code == 200 and response_data.get("data") and response_data["data"].get("link"):
        return JsonResponse({"authorization_url": response_data["data"]["link"]})
    return JsonResponse({"error": "Error initializing Flutterwave payment", "details": response_data.get("message", "Unknown error")})


# ✅ Verify Payment and Update User Balance
@router.get("/verify-payment")
def verify_payment(request, reference: str, user_id: int, payment_method: str):
    """
    Verifies the payment with Paystack or Flutterwave and updates the user's wallet balance.
    """
    if payment_method == "paystack":
        verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    elif payment_method == "flutterwave":
        verify_url = f"https://api.flutterwave.com/v3/transactions/{reference}/verify"
        headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}
    else:
        return JsonResponse({"error": "Invalid payment method"}, status=400)

    response = requests.get(verify_url, headers=headers)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("data") and response_data["data"].get("status") == "success":
        # Extract payment amount
        amount = response_data["data"]["amount"]
        if payment_method == "paystack":
            amount = amount / 100  # Convert from Kobo to Naira for Paystack

        try:
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                profile = Profile.objects.get(user=user)

                # Update balance
                profile.balance += amount
                profile.save()

                # Save payment record
                Payment.objects.create(
                    user=user,
                    amount=amount,
                    reference=reference,
                    status="successful",
                    payment_method=payment_method,
                )

            return JsonResponse({"message": "Payment verified. Wallet updated.", "new_balance": profile.balance})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Profile not found for user"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Failed to update wallet", "details": str(e)}, status=500)

    return JsonResponse({"error": "Payment verification failed", "details": response_data.get("message", "Unknown error")}, status=400)


# ✅ Renders Payment Page (HTML)
@router.get("/payment-page")
def payment_page(request):
    """
    Renders the payment initiation HTML page.
    """
    return render(request, "payments.html")
