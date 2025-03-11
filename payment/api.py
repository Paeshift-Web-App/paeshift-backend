# api.py
import random
import requests
from ninja import NinjaAPI, Schema
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
api = NinjaAPI()

# ---------------------
# Paystack Endpoints
# ---------------------
@api.get("/payment-page")
def payment_page(request):
    return render(request, "payment.html", {})

class PaystackPaymentRequest(Schema):
    amount: int  # Amount in Naira
    email: str

@api.post("/paystack/initialize")
def paystack_initialize(request, payload: PaystackPaymentRequest):
    """
    Initialize a Paystack payment.
    """
    amount_in_kobo = payload.amount * 100  # Convert Naira to kobo
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload_data = {
        "email": payload.email,
        "amount": amount_in_kobo,
    }
    url = "https://api.paystack.co/transaction/initialize"
    response = requests.post(url, headers=headers, json=payload_data)
    return response.json()

@api.get("/paystack/verify")
def paystack_verify(request, reference: str):
    """
    Verify a Paystack transaction using its reference.
    """
    if not reference:
        return {"error": "Missing reference"}
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    return response.json()

# ---------------------
# Flutterwave Endpoints
# ---------------------

class FlutterwavePaymentRequest(Schema):
    amount: float  # Allows for decimals if needed
    email: str
    currency: str = "NGN"

@api.post("/flutterwave/initialize")
def flutterwave_initialize(request, payload: FlutterwavePaymentRequest):
    """
    Initialize a Flutterwave payment.
    """
    # Generate a random transaction reference
    tx_ref = "MC-" + str(random.randint(1000000, 9999999))
    payload_data = {
        "tx_ref": tx_ref,
        "amount": payload.amount,
        "currency": payload.currency,
        "redirect_url": "http://yourdomain.com/flutterwave/callback",  # Change to your callback URL
        "customer": {
            "email": payload.email,
        },
        "customizations": {
            "title": "Payment for Items",
            "description": "Payment for purchasing items",
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
    }
    url = "https://api.flutterwave.com/v3/payments"
    response = requests.post(url, headers=headers, json=payload_data)
    return response.json()

@api.get("/flutterwave/callback")
def flutterwave_callback(request, tx_ref: str, status: str, transaction_id: str):
    """
    Handle Flutterwave's redirect after payment.
    Optionally, verify the payment with Flutterwave's verify endpoint here.
    """
    return {"tx_ref": tx_ref, "status": status, "transaction_id": transaction_id}




# # ------------------------------------------------------------------------------
# # C) PAYMENT SYSTEM
# # ------------------------------------------------------------------------------
# @router.post("/jobs/{job_id}/payments", tags=["Payments"])
# def create_payment(request, job_id: int, payload: PaymentCreateSchema):
#     """
#     POST /jobs/{job_id}/payments
#     Creates a payment record for a given job.
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     job = get_object_or_404(Job, pk=job_id)

#     # For instance, the user paying is the client, or it might be a different logic
#     # Possibly ensure job.client == request.user, or something similar
#     payment = Payment.objects.create(
#         payer=request.user,  # or job.client
#         recipient=None,      # set a recipient if you have logic for who gets paid
#         job=job,
#         original_amount=payload.original_amount,
#         service_fee=payload.service_fee,
#         final_amount=payload.final_amount,
#         pay_code=payload.pay_code  # or auto-generate if needed
#     )
#     return {"message": "Payment created", "payment_id": payment.id}


# @router.get("/jobs/{job_id}/payments", tags=["Payments"])
# def list_payments_for_job(request, job_id: int):
#     """
#     GET /jobs/{job_id}/payments
#     Returns a list of payment records for the specified job.
#     """
#     job = get_object_or_404(Job, pk=job_id)
#     payments = job.payments.all()

#     data = []
#     for p in payments:
#         data.append({
#             "id": p.id,
#             "payer": p.payer.username,
#             "recipient": p.recipient.username if p.recipient else None,
#             "original_amount": str(p.original_amount),
#             "service_fee": str(p.service_fee),
#             "final_amount": str(p.final_amount),
#             "pay_code": p.pay_code,
#             "payment_status": p.payment_status,
#             "created_at": p.created_at.isoformat(),
#             "confirmed_at": p.confirmed_at.isoformat() if p.confirmed_at else None
#         })
#     return data


# @router.put("/payments/{payment_id}", tags=["Payments"])
# def update_payment(request, payment_id: int, payload: PaymentUpdateSchema):
#     """
#     PUT /jobs/payments/{payment_id}
#     Allows updating a payment’s status or details.
#     """
#     if not request.user.is_authenticated:
#         return Response({"error": "Not logged in"}, status=401)

#     payment = get_object_or_404(Payment, pk=payment_id)

#     # Possibly check if request.user is the payer or an admin. Exclude admin logic if not needed
#     if payload.payment_status:
#         payment.payment_status = payload.payment_status
#     if payload.refund_requested is not None:
#         payment.refund_requested = payload.refund_requested

#     payment.save()
#     return {"message": "Payment updated", "payment_id": payment.id}
