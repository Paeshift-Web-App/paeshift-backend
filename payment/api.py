# payments/api.py

import uuid
import logging
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import requests
from ninja import Router, Schema

# Import models – ensure your User, Profile, and Job models are imported correctly.
from jobs.models import User, Profile, Job
from .models import Payment, EscrowPayment  # Use EscrowPayment if needed

router = Router(tags=["Payments"])
logger = logging.getLogger(__name__)

# ================================================================
# Schemas
# ================================================================

class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str
    first_name: str
    last_name: str
    phone: str
    payment_method: str  # "paystack" or "flutterwave"

# ================================================================
# Helper Function: Payment Request
# ================================================================

def _make_payment_request(url, headers, data):
    """
    Helper function to make a POST request to a payment gateway.
    Raises an exception on error.
    """
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Payment request error: {str(e)}")
        raise

# ================================================================
# Payment Initiation Endpoint
# ================================================================

@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """
    Initializes a payment via Paystack or Flutterwave.
    The callback URL is set to your React app on port 5173.
    """
    pay_code = str(uuid.uuid4())
    # Callback URL points to your React dashboard (adjust port/path as needed)
    callback_url = "http://localhost:5173/dashboard"

    try:
        if payload.payment_method.lower() == "paystack":
            return _process_paystack_payment(payload, pay_code, callback_url)
        elif payload.payment_method.lower() == "flutterwave":
            return _process_flutterwave_payment(payload, pay_code, callback_url)
        else:
            return JsonResponse({"error": "Invalid payment method"}, status=400)
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed", "details": str(e)}, status=500)

def _process_paystack_payment(payload, pay_code, callback_url):
    """Handle Paystack payment initialization."""
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "reference": pay_code,
        "email": f"{payload.first_name.lower()}@test.com",
        "amount": int(payload.total * 100),  # Convert NGN to kobo
        "callback_url": callback_url,
        "currency": "NGN"
    }
    response_data = _make_payment_request("https://api.paystack.co/transaction/initialize", headers, data)
    if response_data.get("status") and response_data["data"].get("authorization_url"):
        return JsonResponse({"authorization_url": response_data["data"]["authorization_url"]})
    return JsonResponse({
        "error": "Error initializing Paystack payment",
        "details": response_data.get("message", "Unknown error")
    }, status=400)

def _process_flutterwave_payment(payload, pay_code, callback_url):
    """Handle Flutterwave payment initialization."""
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "tx_ref": pay_code,
        "amount": payload.total,
        "currency": "NGN",
        "redirect_url": callback_url,
        "payment_options": "card,banktransfer,ussd",  # Specify allowed options
        "customer": {
            "email": f"{payload.first_name.lower()}@test.com",
            "name": f"{payload.first_name} {payload.last_name}",
            "phone_number": payload.phone,
        },
        "customizations": {
            "title": "Job Payment",
            "description": "Payment for job reservation",
            "logo": "https://yourwebsite.com/logo.png"  # Replace with your actual logo URL
        }
    }
    response_data = _make_payment_request("https://api.flutterwave.com/v3/payments", headers, data)
    if response_data.get("status") == "success" and response_data["data"].get("link"):
        return JsonResponse({"authorization_url": response_data["data"]["link"]})
    return JsonResponse({
        "error": "Error initializing Flutterwave payment",
        "details": response_data.get("message", "Unknown error")
    }, status=400)

# ================================================================
# Payment Verification Endpoint
# ================================================================

@router.get("/verify-payment")
def verify_payment(request, reference: str, user_id: int, payment_method: str):
    """
    Verifies the payment with Paystack or Flutterwave and updates the user's wallet balance.
    It creates a Payment record (deposit) and updates the user's Profile.balance.
    """
    try:
        if payment_method.lower() == "paystack":
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            amount_divisor = 100  # Convert from kobo
        elif payment_method.lower() == "flutterwave":
            verify_url = f"https://api.flutterwave.com/v3/transactions/{reference}/verify"
            headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}
            amount_divisor = 1
        else:
            return JsonResponse({"error": "Invalid payment method"}, status=400)

        response = requests.get(verify_url, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("status") == "success" and response_data["data"].get("status") == "successful":
            amount = Decimal(response_data["data"]["amount"]) / amount_divisor
            with transaction.atomic():
                user = get_object_or_404(User, id=user_id)
                profile = get_object_or_404(Profile, user=user)
                profile.balance += amount
                profile.save()
                Payment.objects.create(
                    payer=user,
                    job=get_object_or_404(Job, id=response_data["data"].get("metadata", {}).get("job_id", 0)),
                    original_amount=amount,
                    service_fee=amount * Decimal("0.05"),
                    final_amount=amount - (amount * Decimal("0.05")),
                    pay_code=reference,
                    payment_status="Completed",
                    status="Completed",
                    payment_method=payment_method,
                    reference=reference
                )
            return JsonResponse({"message": "Payment verified. Wallet updated.", "new_balance": str(profile.balance)})
        return JsonResponse({
            "error": "Payment verification failed",
            "details": response_data.get("message", "Unknown error")
        }, status=400)
    except requests.RequestException as e:
        logger.error(f"Payment verification request error: {str(e)}")
        return JsonResponse({"error": "Failed to connect to payment gateway"}, status=500)
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed", "details": str(e)}, status=500)

# ================================================================
# UI Endpoints
# ================================================================

@router.get("/payment-page")
def payment_page(request):
    """Render the payment initiation HTML page."""
    return render(request, "payments.html")

@router.get("/payment-completed/")
def payment_completed(request):
    """Handle payment completion callback."""
    reference = request.GET.get("reference")  # For Paystack
    tx_ref = request.GET.get("tx_ref")         # For Flutterwave
    status = request.GET.get("status")
    return JsonResponse({
        "message": "Payment completed",
        "reference": reference or tx_ref,
        "status": status
    })
