# payments/api.py

import uuid
import logging
import hashlib
import hmac
import json
from decimal import Decimal
from django.db import transaction
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from ninja import Router, Schema
from jobs.models import User, Profile, Job
from .models import Payment, EscrowPayment
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods
from ninja import Router
from ninja.responses import Response
from payment.models import EscrowPayment
from jobs.models import Job
import hashlib
import hmac
import json

router = Router(tags=["Payments"])
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
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
# Payment Processing
# ================================================================

def _make_payment_request(url, headers, data):
    """Helper function to make payment gateway requests."""
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Payment request error: {str(e)}")
        raise

@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """Initialize payment via Paystack or Flutterwave."""
    pay_code = str(uuid.uuid4())
    callback_url = request.build_absolute_uri("/payments/payment-completed/")

    try:
        if payload.payment_method == "paystack":
            return _process_paystack_payment(payload, pay_code, callback_url)
        elif payload.payment_method == "flutterwave":
            return _process_flutterwave_payment(payload, pay_code, callback_url)
        return JsonResponse({"error": "Invalid payment method"}, status=400)
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed"}, status=500)

def _process_paystack_payment(payload, pay_code, callback_url):
    """Handle Paystack payment initialization."""
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "reference": pay_code,
        "email": f"{payload.first_name.lower()}@test.com",
        "amount": int(payload.total * 100),  # Convert to kobo
        "callback_url": callback_url,
        "currency": "NGN"
    }

    response_data = _make_payment_request(
        "https://api.paystack.co/transaction/initialize", headers, data
    )

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
        "customer": {
            "email": f"{payload.first_name.lower()}@test.com",
            "name": f"{payload.first_name} {payload.last_name}",
            "phone_number": payload.phone,
        },
    }

    response_data = _make_payment_request(
        "https://api.flutterwave.com/v3/payments", headers, data
    )

    if response_data.get("status") == "success" and response_data["data"].get("link"):
        return JsonResponse({"authorization_url": response_data["data"]["link"]})
    return JsonResponse({
        "error": "Error initializing Flutterwave payment",
        "details": response_data.get("message", "Unknown error")
    }, status=400)

# ================================================================
# Payment Verification
# ================================================================

@router.get("/verify-payment")
def verify_payment(request, reference: str, user_id: int, payment_method: str):
    """Verify payment and update user balance."""
    try:
        if payment_method == "paystack":
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            amount_divisor = 100  # Convert from kobo
        elif payment_method == "flutterwave":
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
                user = User.objects.get(id=user_id)
                profile = Profile.objects.get(user=user)
                profile.balance += amount
                profile.save()

                Payment.objects.create(
                    user=user,
                    amount=amount,
                    reference=reference,
                    status="successful",
                    payment_method=payment_method,
                )

            return JsonResponse({
                "message": "Payment verified. Wallet updated.",
                "new_balance": profile.balance
            })

        return JsonResponse({
            "error": "Payment verification failed",
            "details": response_data.get("message", "Unknown error")
        }, status=400)

    except requests.RequestException as e:
        logger.error(f"Payment verification request error: {str(e)}")
        return JsonResponse({"error": "Failed to connect to payment gateway"}, status=500)
    except (User.DoesNotExist, Profile.DoesNotExist) as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed"}, status=500)

# ================================================================
# Webhook & Escrow Management
# ================================================================

@router.post("/payment/webhook")
@require_http_methods(["POST"])
def paystack_webhook(request):
    """Handle Paystack webhook events."""
    signature = request.headers.get('x-paystack-signature')
    body = request.body.decode('utf-8')
    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'), 
        body.encode('utf-8'), 
        digestmod=hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return JsonResponse({"error": "Invalid signature"}, status=403)

    event = json.loads(body)
    
    if event['event'] == 'charge.success':
        return _handle_successful_payment(event['data'])
    
    return JsonResponse({"status": "unhandled event"}, status=200)

def _handle_successful_payment(data):
    """Process successful payment from webhook."""
    job = get_object_or_404(Job, id=data['metadata']['job_id'])
    
    with transaction.atomic():
        escrow_payment = EscrowPayment.objects.create(
            job=job,
            client=job.client,
            total_amount=Decimal(data['amount']) / 100,  # Convert from kobo
            paystack_reference=data['reference'],
            status='held'
        )
        escrow_payment.calculate_fees()
        
        job.payment_status = 'completed'
        job.save()
    
    return JsonResponse({"status": "success"}, status=200)

# ================================================================
# UI Endpoints
# ================================================================

@router.get("/payment-page")
def payment_page(request):
    """Render payment page."""
    return render(request, "payments.html")

@router.get("/payment-completed/")
def payment_completed(request):
    """Handle payment completion callback."""
    reference = request.GET.get("reference")  # Paystack
    tx_ref = request.GET.get("tx_ref")  # Flutterwave
    status = request.GET.get("status")

    return JsonResponse({
        "message": "Payment completed",
        "reference": reference or tx_ref,
        "status": status
    })