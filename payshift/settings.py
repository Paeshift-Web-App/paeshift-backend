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

# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    # "corsheaders",            # Uncomment if using corsheaders
    # "jazzmin",                # Optional admin theme

    "jobs", 
    "socialauth",          # Your main Django app
    "channels",                # For Django Channels

    # Django default apps
    "django.contrib.admin",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',  # ✅ Keep only one instance of this
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

# -----------------------------
# AUTH BACKENDS & SITE_ID
# -----------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1  # Ensure this matches the Site entry in your admin


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
    }
}

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
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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
