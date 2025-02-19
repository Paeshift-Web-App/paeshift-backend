import os
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^6*1)&derg*vwfqgex#eocbb0=i2bh7lc8o14zze@3t#8hk2sm"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# CORS settings (make sure you have 'corsheaders' in INSTALLED_APPS if you want to use it)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:8000",
    
]

# Application definition
INSTALLED_APPS = [
    # "corsheaders",  # Uncomment if you decide to use CORS
    # "jazzmin",      # If you want to use jazzmin theme for admin
    
    "jobs",
    "channels",  # Django Channels
    # Django default apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',           # Needed by allauth
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # The allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers you want to enable:
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',

]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1

SITE_ID = 1  # Make sure this matches a Site entry in your admin

# allauth settings:
LOGIN_REDIRECT_URL = '/'  # or your front-end route
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True  # optional

# If you want email verification:
ACCOUNT_EMAIL_VERIFICATION = 'none'  # or 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True




# Channels configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # For production, uncomment and configure Redis:
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

# Google Maps API key (if you're doing reverse geocoding)
GOOGLE_MAPS_API_KEY = "YOUR_REAL_API_KEY"

MIDDLEWARE = [
    # If you’re using CORS, ensure you have 'corsheaders' in INSTALLED_APPS
    # and uncomment the line below:
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "payshift.urls"  # Adjust if your main project is spelled differently

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # if you have templates
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

STATIC_URL = '/static/'

# If you have a React build, you can serve its static files here:
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'build' / 'static',  # e.g. React static files
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collectstatic

# WSGI and ASGI
WSGI_APPLICATION = "payshift.wsgi.application"

# IMPORTANT: Match your project name for ASGI:
# if your project folder is "payshift", do "payshift.asgi.application"
# if it's "PayShift", do "PayShift.asgi.application"
ASGI_APPLICATION = "payshift.asgi.application"

# Database (SQLite example)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
