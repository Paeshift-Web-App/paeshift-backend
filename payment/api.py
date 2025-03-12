# import uuid
# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render
# from ninja import NinjaAPI, Schema

# from .models import Payment  # Ensure you have the Payment model

# # Create a NinjaAPI instance
# api = NinjaAPI(title="Payment API")

# class InitiatePaymentSchema(Schema):
#     total: float
#     reservation_code: str = ""
#     first_name: str = ""
#     last_name: str = ""
#     phone: str = ""

# @api.post("/initiate-payment")
# def initiate_payment(request, payload: InitiatePaymentSchema):
#     """
#     Initializes a Paystack payment.
#     """
#     if not request.user.is_authenticated:
#         return JsonResponse({"error": "User must be logged in."}, status=401)

#     total_in_kobo = int(payload.total * 100)
#     reservation_code = payload.reservation_code
#     pay_code = str(uuid.uuid4())
#     user = request.user

#     callback_url = "http://127.0.0.1:8000/completed/"

#     headers = {
#         "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "reference": pay_code,
#         "email": user.email,
#         "amount": total_in_kobo,
#         "callback_url": callback_url,
#         "order_number": reservation_code,
#     }

#     try:
#         response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
#         response_data = response.json()
#     except Exception as e:
#         return JsonResponse({"error": "Network busy, please try again.", "details": str(e)}, status=500)

#     if response.status_code == 200 and "data" in response_data and "authorization_url" in response_data["data"]:
#         return JsonResponse({"authorization_url": response_data["data"]["authorization_url"]}, status=200)
#     else:
#         return JsonResponse({
#             "error": "Error initializing payment",
#             "details": response_data.get("message", "Unknown error")
#         }, status=response.status_code)

# @api.get("/payments")
# def payment_page_api(request):
#     """
#     Renders an HTML page displaying Payment records.
#     """
#     payments = Payment.objects.all()
#     return render(request, "payments.html", {"payments": payments})
