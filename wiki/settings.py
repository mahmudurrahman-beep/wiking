import sys
import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# ====== SECURITY SETTINGS ======
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-only-for-dev')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ====== HOST & CSRF CONFIGURATION ======
# Fix: Ensure these are parsed as lists from the environment strings
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'wiking.koyeb.app,localhost').split(',')

csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://wiking.koyeb.app')
CSRF_TRUSTED_ORIGINS = csrf_origins.split(',')

if DEBUG:
    ALLOWED_HOSTS.extend(['127.0.0.1', '[::1]'])

# ====== APPLICATION DEFINITION ======
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Added for better static handling
    'django.contrib.staticfiles',
    'encyclopedia', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wiki.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wiki.wsgi.application'

# ====== DATABASE ======
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ====== STATIC FILES ======
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Make sure this directory actually exists in your repo!
STATICFILES_DIRS = [BASE_DIR / 'encyclopedia' / 'static']

# ====== PRODUCTION SECURITY (Koyeb Specific) ======
if not DEBUG:
    # Essential for Koyeb to know the request is secure
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# (Keep your AUTH_PASSWORD_VALIDATORS, Internationalization, and Debug Helpers as they were)
