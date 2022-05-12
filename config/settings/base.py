"""Base settings to build other settings files upon."""
from environs import Env
from pathlib import Path

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# Base
DEBUG = env.bool("DJANGO_DEBUG", False)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Language and timezone
TIME_ZONE = "America/Guayaquil"
LANGUAGE_CODE = "es-EC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("PG_DB"),
        "USER": env("PG_USER"),
        "PASSWORD": env("PG_PASSWORD"),
        "HOST": env("PG_HOST"),
        "PORT": env("PG_PORT"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLs
ROOT_URLCONF = "config.urls"

# WSGI
WSGI_APPLICATION = "config.wsgi.application"

# Apps
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]

LOCAL_APPS = [
    "apps.company",
    "apps.transaction",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
]

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = (
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://storage.googleapis.com",
    "https://googleapis.com",
)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://storage.googleapis.com",
    "https://googleapis.com",
]
