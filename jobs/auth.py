from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from ninja import *
from ninja.responses import Response

from .models import *
from .router import *
from .schemas import *

from .auth import *
from .jobs import *
from .ratings import *




@router.post("/login")
def login_view(request, payload: LoginSchema):
    """POST /auth/login - Authenticates a user by email/password and logs them in."""
    user = authenticate(request, username=payload.email, password=payload.password)
    if user:
        login(request, user)
        return Response({"message": "Login successful"}, status=200)
    return Response({"error": "Invalid credentials"}, status=400)

@router.post("/signup")
def signup(request, payload: SignupSchema):
    """POST /auth/signup - Creates a new user account if email is unique and passwords match."""
    if User.objects.filter(username=payload.email).exists():
        return Response({"error": "Email already exists"}, status=400)
    if payload.password != payload.confirmPassword:
        return Response({"error": "Passwords do not match"}, status=400)
    try:
        User.objects.create_user(
            first_name=payload.firstName,
            last_name=payload.lastName,
            username=payload.email,
            email=payload.email,
            password=payload.password,
        )
        return Response({"message": "Registration successful"}, status=201)
    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"}, status=500)


