import uuid
import logging
import json
import requests
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from .schemas import *
# Import models – adjust these imports to match your project structure.
from jobs.models import User, Profile, Job
from .models import Payment, EscrowPayment  # Use EscrowPayment if needed

router = Router(tags=["Payments"])
logger = logging.getLogger(__name__)


# ================================================================
# Helper Function: Make Payment Request
# ================================================================

def _make_payment_request(url, headers, data):
    """Helper function to send a request to a payment gateway."""
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Payment request error: {str(e)}")
        raise

# ================================================================
# Payment Initiation (Saves Payment Before Redirecting)
# ================================================================

@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """
    Saves a payment record with "Pending" status before redirecting the user.
    The callback URL is set to your React dashboard (port 5173).
    """
    pay_code = str(uuid.uuid4())  # Generate unique reference
    callback_url = "http://localhost:5173/dashboard"  # Redirect back after payment

    # Ensure user is authenticated
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        user = User.objects.first()  # For testing, use first user if session missing
        if not user:
            return JsonResponse({"error": "No users available for testing"}, status=500)
    else:
        user = get_object_or_404(User, id=user_id)

    # Convert the total to a Decimal using a string conversion
    try:
        total_amount = Decimal(str(payload.total))
    except Exception as e:
        return JsonResponse({"error": "Invalid total amount format", "details": str(e)}, status=400)

    # **Calculate service fee (10%) and final amount**
    service_fee = total_amount * Decimal("0.10")
    final_amount = total_amount - service_fee


    # Save payment record before redirecting
    with transaction.atomic():
        payment = Payment.objects.create(
            payer=user,
            job=None,  # Change this if the payment is related to a specific job
            original_amount=total_amount,
            service_fee=service_fee,
            final_amount=final_amount,
            pay_code=pay_code,
            payment_status="Pending",
            # payment_method=payload.payment_method.lower(),
            # reference=pay_code
        )

    logger.info(f"Payment created: {payment.pay_code}")

    try:
        if payload.payment_method.lower() == "paystack":
            return _process_paystack_payment(payload, payment, callback_url)
        elif payload.payment_method.lower() == "flutterwave":
            return _process_flutterwave_payment(payload, payment, callback_url)
        else:
            return JsonResponse({"error": "Invalid payment method"}, status=400)
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed", "details": str(e)}, status=500)




# ================================================================
# Paystack Payment Processing
# ================================================================

def _process_paystack_payment(payload, payment, callback_url):
    """Handle Paystack payment initialization."""
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "reference": payment.pay_code,
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

# ================================================================
# Flutterwave Payment Processing
# ================================================================

def _process_flutterwave_payment(payload, payment, callback_url):
    """Handle Flutterwave payment initialization."""
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "tx_ref": payment.pay_code,
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
    Verifies the payment with the payment gateway and updates the user's wallet balance.
    If the payment does not exist, it will create a new record.
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
            service_fee = amount * Decimal("0.05")
            final_amount = amount - service_fee

            with transaction.atomic():
                user = get_object_or_404(User, id=user_id)
                profile = get_object_or_404(Profile, user=user)

                # **Ensure payment record exists, create if missing**
                payment, created = Payment.objects.get_or_create(
                    reference=reference,
                    defaults={
                        "payer": user,
                        "original_amount": amount,
                        "service_fee": service_fee,
                        "final_amount": final_amount,
                        "payment_status": "Completed",
                        "pay_code": reference,  # Use reference as pay_code if missing
                    },
                )

                if not created:  # If payment exists, update its status
                    payment.payment_status = "Completed"
                    payment.original_amount = amount
                    payment.service_fee = service_fee
                    payment.final_amount = final_amount
                    payment.save()

                # Update the user's wallet balance
                profile.balance += final_amount
                profile.save()

            return JsonResponse({
                "message": "Payment verified and recorded.",
                "new_balance": str(profile.balance),
                "payment_status": "Completed"
            })
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

# @router.get("/payment-page")
# def payment_page(request):
#     """Render the payment initiation HTML page."""
#     return render(request, "payments.html")

# @router.get("/payment-completed/")
# def payment_completed(request):
#     """Handle payment completion callback."""
#     reference = request.GET.get("reference")  # For Paystack
#     tx_ref = request.GET.get("tx_ref")         # For Flutterwave
#     return JsonResponse({
#         "message": "Payment completed",
#         "reference": reference or tx_ref,
#         "status": "Success"
#     })
