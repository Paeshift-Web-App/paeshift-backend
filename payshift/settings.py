import os

from pathlib import Path


if os.getenv("DJANGO_USE_LOCALHOST"):
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
else:
    ALLOWED_HOSTS = ["127.0.0.1"]
# -----------------------------
# BASE DIRECTORY & SECRET KEY
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-^6*1)&derg*vwfqgex#eocbb0=i2bh7lc8o14zze@3t#8hk2sm"
DEBUG = True
ALLOWED_HOSTS = []
FRONTEND_URL = "http://localhost:5173"  # Change for production
DEFAULT_FROM_EMAIL = "noreply@yourapp.com"

# -----------------------------
# MEDIA (UPLOADS) CONFIG
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# -----------------------------
# CORS (IF YOU NEED IT)
# -----------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:8000",
]

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = False  # True in production
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Allow JS to read CSRF token
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "X-CSRFToken",
]  # Allow custom h



# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    "daphne",
    "channels",                # For Django Channels
    "corsheaders",            # Uncomment if using corsheaders
    # "jazzmin",                # Optional admin theme

    'django.contrib.sites',  # ✅ Keep only one instance of this
    "jobs",
    "jobchat", 
    "notifications",
    "socialauth",          # Your main Django app
    'payment',
    "rest_framework",
    "rest_framework_simplejwt",
    
    
    "django.contrib.admin",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers for social login
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.twitter",
    'allauth.socialaccount.providers.apple',
]




# SITE_ID = 1  # Placeholder

# ✅ Enable session authentication
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # ✅ Important for session-based auth
        "rest_framework.authentication.TokenAuthentication",  # ✅ If using token-based auth
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # ✅ Requires authentication
    ],
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
# -----------------------------
# AUTH BACKENDS & SITE_ID
# -----------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 3  # Ensure this matches the Site entry in your admin


PAYSTACK_SECRET_KEY = "sk_test_ef9e10ac4bf5dcd69617a61636d21c88528afb1d"
PAYSTACK_PUBLIC_KEY = "pk_test_01db91d9678ee0d25483a7d0bc9783951938b45d"

FLUTTERWAVE_SECRET_KEY = "FLWSECK_TEST-5cfee76ec023b25f6e002bad2bfc1d95-X"
FLUTTERWAVE_PUBLIC_KEY = "FLWPUBK_TEST-c9b0667be3b2500fb3ee42a46a8ae054-X"


# settings.py
BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual domain in production


# -----------------------------
# ALLAUTH CONFIG
# -----------------------------
LOGIN_REDIRECT_URL = "/dashboard"  # ✅ Redirect after login
LOGOUT_REDIRECT_URL = "/login"  # ✅ Redirect after logout
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # ✅ New way to handle logout redirection

ACCOUNT_EMAIL_VERIFICATION = "none"  # Set to "mandatory" if email confirmation is needed
ACCOUNT_EMAIL_REQUIRED = True  # ✅ Force email requirement
ACCOUNT_USERNAME_REQUIRED = False  # ✅ Disable username field

# ✅ Use new authentication method
ACCOUNT_LOGIN_METHODS = {"email"}  # ✅ Correct replacement for ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_UNIQUE_EMAIL = True  # ✅ Prevent duplicate emails

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["email", "profile"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,  # ✅ Enables secure PKCE authentication
    },
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "FIELDS": ["id", "email", "name", "first_name", "last_name"],
        "VERSION": "v17.0",
    },
}
# app = SocialApp(
#     provider="facebook",
#     name="Facebook Login",
#     client_id="3640745886229353",
#     secret="3640745886229353"
# )




import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'allauth_debug.log',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


AUTH_USER_MODEL = "auth.User"  # Default Django user model
# OR your custom user model (e.g., "socialauth.User")
# -----------------------------
# CHANNELS CONFIG
# -----------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # For production with Redis, comment out the above and uncomment below:
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

# -----------------------------
# OPTIONAL: GOOGLE MAPS API KEY
# -----------------------------
GOOGLE_MAPS_API_KEY = "YOUR_REAL_API_KEY"

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    # If using corsheaders, uncomment the line below and ensure "corsheaders" in INSTALLED_APPS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    "allauth.account.middleware.AccountMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# ROOT URLS & TEMPLATES
# -----------------------------
ROOT_URLCONF = "payshift.urls"  # Adjust to your main project's urls
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # If you keep templates here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -----------------------------
# STATIC FILES (CSS, JS, IMAGES)
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'build' / 'static',  # Example if you have a React build
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collectstatic

# -----------------------------
# WSGI & ASGI
# -----------------------------
WSGI_APPLICATION = "payshift.wsgi.application"
ASGI_APPLICATION = "payshift.asgi.application"  # If your main project is "payshift"

# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # Increased from default 5 seconds
            'check_same_thread': False,  # Allow multiple threads
        }
    }
}

# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
