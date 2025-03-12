import uuid
import requests
import logging
from django.conf import settings
from django.db import transaction
from ninja import Router, Schema
from django.http import JsonResponse
from django.shortcuts import render
from jobs.models import User, Profile
from .models import Payment

router = Router(tags=["Payments"])
logger = logging.getLogger(__name__)

# ✅ Schema for initiating payments
class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str
    first_name: str
    last_name: str
    phone: str
    payment_method: str  # "paystack" or "flutterwave"


# ✅ Initiate Payment (Paystack or Flutterwave)
@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """
    Initializes a payment via Paystack or Flutterwave.
    """
    pay_code = str(uuid.uuid4())
    
    # Dynamically construct the callback URL using request.build_absolute_uri()
    callback_url = request.build_absolute_uri("/payments/payment-completed/")

    try:
        if payload.payment_method == "paystack":
            return process_paystack_payment(payload, pay_code, callback_url)
        elif payload.payment_method == "flutterwave":
            return process_flutterwave_payment(payload, pay_code, callback_url)
        else:
            return JsonResponse({"error": "Invalid payment method"}, status=400)
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed"}, status=500)



# ✅ Paystack Payment Processing
def process_paystack_payment(payload, pay_code, callback_url):
    """
    Handles Paystack payment initialization.
    """
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

    try:
        response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        if response_data.get("status") and response_data["data"].get("authorization_url"):
            return JsonResponse({"authorization_url": response_data["data"]["authorization_url"]})
        else:
            return JsonResponse({"error": "Error initializing Paystack payment", "details": response_data.get("message", "Unknown error")}, status=400)
    except requests.RequestException as e:
        logger.error(f"Paystack request error: {str(e)}")
        return JsonResponse({"error": "Failed to connect to Paystack", "details": str(e)}, status=500)
    except ValueError as e:
        logger.error(f"Paystack JSON decode error: {str(e)}")
        return JsonResponse({"error": "Invalid response from Paystack"}, status=500)


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
            "email": f"{payload.first_name.lower()}@test.com",
            "name": f"{payload.first_name} {payload.last_name}",
            "phone_number": payload.phone,
        },
    }

    try:
        response = requests.post("https://api.flutterwave.com/v3/payments", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        if response_data.get("status") == "success" and response_data["data"].get("link"):
            return JsonResponse({"authorization_url": response_data["data"]["link"]})
        else:
            return JsonResponse({"error": "Error initializing Flutterwave payment", "details": response_data.get("message", "Unknown error")}, status=400)
    except requests.RequestException as e:
        logger.error(f"Flutterwave request error: {str(e)}")
        return JsonResponse({"error": "Failed to connect to Flutterwave", "details": str(e)}, status=500)
    except ValueError as e:
        logger.error(f"Flutterwave JSON decode error: {str(e)}")
        return JsonResponse({"error": "Invalid response from Flutterwave"}, status=500)


# ✅ Verify Payment and Update User Balance
@router.get("/verify-payment")
def verify_payment(request, reference: str, user_id: int, payment_method: str):
    """
    Verifies the payment with Paystack or Flutterwave and updates the user's wallet balance.
    """
    try:
        if payment_method == "paystack":
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        elif payment_method == "flutterwave":
            verify_url = f"https://api.flutterwave.com/v3/transactions/{reference}/verify"
            headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}
        else:
            return JsonResponse({"error": "Invalid payment method"}, status=400)

        response = requests.get(verify_url, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("status") == "success" and response_data["data"].get("status") == "successful":
            amount = response_data["data"]["amount"]
            if payment_method == "paystack":
                amount = amount / 100  # Convert from kobo to naira

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

            return JsonResponse({"message": "Payment verified. Wallet updated.", "new_balance": profile.balance})

        return JsonResponse({"error": "Payment verification failed", "details": response_data.get("message", "Unknown error")}, status=400)

    except requests.RequestException as e:
        logger.error(f"Payment verification request error: {str(e)}")
        return JsonResponse({"error": "Failed to connect to payment gateway"}, status=500)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found for user"}, status=404)
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        return JsonResponse({"error": "Payment processing failed"}, status=500)


# ✅ Renders Payment Page (HTML)
@router.get("/payment-page")
def payment_page(request):
    """
    Renders the payment initiation HTML page.
    """
    return render(request, "payments.html")

@router.get("/payment-completed/")
def payment_completed(request):
    """
    Handles the callback from Paystack or Flutterwave after payment is completed.
    """
    reference = request.GET.get("reference")  # For Paystack
    tx_ref = request.GET.get("tx_ref")  # For Flutterwave
    status = request.GET.get("status")

    # Process the payment status here
    return JsonResponse({"message": "Payment completed", "reference": reference or tx_ref, "status": status})