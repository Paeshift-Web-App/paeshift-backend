# from ninja import Router
# from django.contrib.auth import authenticate, login
# from ninja.responses import JsonResponse  # ✅ Correct

# from .schemas import LoginSchema, SignupSchema

# router = Router()

# @router.post("/login")
# def login_view(request, payload: LoginSchema):
#     user = authenticate(request, username=payload.email, password=payload.password)
#     if user:
#         login(request, user)
#         return JsonResponse({"message": "Login successful"})
#     return JsonResponse({"error": "Invalid credentials"}, status=401)