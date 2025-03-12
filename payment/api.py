import uuid
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from ninja import Router, Schema

from .models import Payment

router = Router(tags=["Payments"])

class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""

# import uuid
# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from ninja import Router, Schema

# from .models import Payment  # Your Payment model

# router = Router(tags=["Payments"])

class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""

@router.post("/initiate-payment")
def initiate_payment(request, payload: InitiatePaymentSchema):
    """
    Initializes a Paystack payment.
    
    Expects a POST request with a JSON body containing:
      - total (float, in Naira)
      - reservation_code (optional)
      - first_name, last_name, phone (optional)
      
    The endpoint uses the logged-in user's email and returns the authorization URL.
    """
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must be logged in."}, status=401)

    # Convert Naira to kobo
    total_in_kobo = int(payload.total * 100)
    reservation_code = payload.reservation_code
    pay_code = str(uuid.uuid4())
    user = request.user

    # Set callback URL (adjust as needed)
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

    try:
        response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
        response_data = response.json()
    except Exception as e:
        return JsonResponse({"error": "Network busy, please try again.", "details": str(e)}, status=500)

    # If successful, return the authorization URL
    if response.status_code == 200 and "data" in response_data and "authorization_url" in response_data["data"]:
        auth_url = response_data["data"]["authorization_url"]

        # Optionally, you can save a Payment record here.
        # Payment.objects.create(user=user, amount=payload.total, pay_code=pay_code, order_no=reservation_code, ...)

        return JsonResponse({"authorization_url": auth_url}, status=200)
    else:
        return JsonResponse({
            "error": "Error initializing payment",
            "details": response_data.get("message", "Unknown error")
        }, status=response.status_code)


@router.get("/payments")
def payment_page(request):
    """
    Renders an HTML page displaying Payment records.
    (For testing purposes, we are using Django's render function.)
    """
    payments = Payment.objects.all()
    return render(request, "payments.html", {"payments": payments})
