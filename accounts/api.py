from ninja import Router

accounts_router = Router()


from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.responses import Response

import requests  # for verifying tokens if needed (google, facebook, etc.)
from .models import *
from .schemas import *
User = get_user_model()

auth_router = Router()

# ------------------------------------------------------
# 1) EMAIL/PASSWORD SIGNUP
# ------------------------------------------------------
@auth_router.post("/signup")
def signup_view(request, payload: EmailSignupSchema):
    """
    POST /auth/signup
    Creates a new user account with email/password.
    """
    # 1) Basic validations
    if payload.password != payload.confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)
    if User.objects.filter(username=payload.email).exists():
        return Response({"error": "Email already exists"}, status=400)

    try:
        # 2) Create the user
        user = User.objects.create_user(
            username=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
        )
        # 3) Optionally log them in immediately
        login(request, user)
        return Response({"message": "Registration successful"}, status=201)

    except IntegrityError:
        return Response({"error": "Email already exists"}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)


# ------------------------------------------------------
# 2) EMAIL/PASSWORD LOGIN
# ------------------------------------------------------
@auth_router.post("/login")
def login_view(request, payload: EmailLoginSchema):
    """
    POST /auth/login
    Authenticates a user by email/password and logs them in (session-based).
    """
    user = authenticate(request, username=payload.email, password=payload.password)
    if user:
        login(request, user)
        return Response({"message": "Login successful"}, status=200)
    return Response({"error": "Invalid credentials"}, status=401)


# ------------------------------------------------------
# 3) LOGOUT
# ------------------------------------------------------
@auth_router.post("/logout")
def logout_view(request):
    """
    POST /auth/logout
    Logs out the current session-based user.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Not logged in"}, status=401)
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)


# ------------------------------------------------------
# 4) SOCIAL LOGIN
# ------------------------------------------------------
@auth_router.post("/social-login")
def social_login_view(request, payload: SocialLoginSchema):
    """
    POST /auth/social-login
    The front-end obtains an access token from Google/Facebook/Apple.
    Then sends JSON like:
      {
        "provider": "google",
        "access_token": "<token>"
      }
    We verify the token, get user info, create or retrieve a User, and log them in.
    """
    provider = payload.provider.lower()
    access_token = payload.access_token

    if provider == "google":
        # Example Google endpoint to get user info
        google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        try:
            resp = requests.get(
                google_userinfo_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if resp.status_code == 200:
                data = resp.json()
                # data might contain {sub, email, name, picture, ...}
                email = data.get("email")
                if not email:
                    return Response({"error": "No email returned by Google"}, status=400)

                # create/retrieve user
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        "email": email,
                        "first_name": data.get("given_name", ""),
                        "last_name": data.get("family_name", ""),
                        # "password": <some random> if needed
                    }
                )
                # If user is newly created, you might set a random password or empty
                # user.set_unusable_password() or user.set_password(something)
                user.save()

                # log them in
                login(request, user)
                return {"message": "Google login successful"}
            else:
                return Response({"error": "Failed to verify Google token"}, status=400)
        except Exception as e:
            return Response({"error": f"Google verification error: {str(e)}"}, status=400)

    elif provider == "facebook":
        # Example: verify Facebook token and get user info
        facebook_debug_url = (
            f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        )
        try:
            resp = requests.get(facebook_debug_url)
            if resp.status_code == 200:
                data = resp.json()
                # data might contain {id, name, email, ...}
                email = data.get("email")
                if not email:
                    return Response({"error": "No email returned by Facebook"}, status=400)

                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        "email": email,
                        "first_name": data.get("name", ""),  # might parse name
                    }
                )
                user.save()
                login(request, user)
                return {"message": "Facebook login successful"}
            else:
                return Response({"error": "Failed to verify Facebook token"}, status=400)
        except Exception as e:
            return Response({"error": f"Facebook verification error: {str(e)}"}, status=400)

    elif provider == "apple":
        # Apple requires verifying a JWT. Typically you'd decode the JWT using
        # a library like pyjwt + Apple public keys, or rely on your front-end
        # to do some of that. This is just an example placeholder.
        try:
            # decode/verify the Apple token, parse the email or sub
            # For brevity, let's assume we have an "email"
            email = "apple_user@example.com"  # you'd decode from the token
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": "",
                    "last_name": ""
                }
            )
            user.save()
            login(request, user)
            return {"message": "Apple login successful"}
        except Exception as e:
            return Response({"error": f"Apple verification error: {str(e)}"}, status=400)

    else:
        return Response({"error": "Unknown social provider"}, status=400)


# def login_facebook_connect(request):
#     status = 'unknown failure'
#     try:
#         expires = request.POST['expires']
#         ss = request.POST['ss']
#         session_key = request.POST['session_key']
#         user = request.POST['user']
#         sig = request.POST['sig']

#         pre_hash_string = "expires=%ssession_key=%sss=%suser=%s%s" % (
#             expires,
#             session_key,
#             ss,
#             user,
#             settings.FACEBOOK_APPLICATION_SECRET,
#         )
#         post_hash_string = hashlib.new('md5')
#         post_hash_string.update(pre_hash_string)
#         if post_hash_string.hexdigest() == sig:
#             try:
#                 fb = FacebookUser.objects.get(facebook_id=user)
#                 status = "logged in existing user"
#             except FacebookUser.DoesNotExist:
#                 contrib_user = User()
#                 contrib_user.save()
#                 contrib_user.username = u"fbuser_%s" % contrib_user.id

#                 fb = FacebookUser()
#                 fb.facebook_id = user
#                 fb.contrib_user = contrib_user

#                 temp = hashlib.new('sha1')
#                 temp.update(str(datetime.datetime.now()))
#                 password = temp.hexdigest()

#                 contrib_user.set_password(password)
#                 fb.contrib_password = password
#                 fb.save()
#                 contrib_user.save()
#                 status = "created new user"

#             authenticated_user = auth.authenticate(
#                                          username=fb.contrib_user.username,
#                                          password=fb.contrib_password)
#             auth.login(request, authenticated_user)
#         else:
#             status = 'wrong hash sig'

#             logging.debug("FBConnect: user %s with exit status %s" % (user, status))

#     except e:
#         logging.debug("Exception thrown in the FBConnect ajax call: %s" % e)

#     return HttpResponse("%s" % status)


# accounts/api.py
from ninja import Router
from django.shortcuts import redirect
from django.conf import settings

accounts_router = Router()

@accounts_router.get("/facebook")
def facebook_login(request):
    """
    Example: Kick off the Facebook OAuth process manually.
    Typically you'd just link to 'social:begin' route,
    but here's a custom approach.
    """
    # You might do some custom logic or validations,
    # then redirect to the actual social auth URL:
    return redirect("/oauth/login/facebook")
