import sys
import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ====== SECURITY SETTINGS ======
# Uses your 50-char string from environment; provides a fallback for build phase
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-build-fallback-1234567890-random-string')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ====== HOST & CSRF CONFIGURATION ======
# Converts "wiking.koyeb.app,localhost" into ['wiking.koyeb.app', 'localhost']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'wiking.koyeb.app,localhost,127.0.0.1').split(',')

# Converts "https://wiking.koyeb.app" into ['https://wiking.koyeb.app']
csrf_env = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://wiking.koyeb.app')
CSRF_TRUSTED_ORIGINS = csrf_env.split(',')

# ====== APPLICATION DEFINITION ======
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Better static handling
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

# ====== DATABASE CONFIGURATION ======
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

# ====== STATIC FILES (WhiteNoise) ======
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use this storage for maximum stability on Koyeb
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Ensure 'encyclopedia/static' exists in your repo
STATICFILES_DIRS = [BASE_DIR / 'encyclopedia' / 'static']

# ====== PRODUCTION SECURITY (Crucial for Koyeb) ======
if not DEBUG:
    # This tells Django that Koyeb is handling the HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'

# ====== GITHUB & API SETTINGS ======
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.environ.get('GITHUB_REPO_OWNER', '')
GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', '')

# (Keep your remaining Password Validators / Internationalization settings here)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
