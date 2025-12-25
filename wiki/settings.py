"""
Django settings for wiki project.
Optimized for Koyeb + Supabase/PostgreSQL
"""
import sys
import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as messages

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ====== SECURITY SETTINGS ======
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-123456')
# Ensure DEBUG is set to False in production environment variables
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ====== HOST CONFIGURATION FOR KOYEB ======
ALLOWED_HOSTS = []

# For development
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])

# Allow all hosts in production on Koyeb (Simplest approach)
# Koyeb manages ingress internally.
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

# CSRF_TRUSTED_ORIGINS can remain empty unless you are using specific custom domains
CSRF_TRUSTED_ORIGINS = []

# ====== APPLICATION DEFINITION ======
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Moved up for static file serving
    'encyclopedia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [],
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
# Use DATABASE_URL from environment, fallback to SQLite for local dev
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

# ====== PASSWORD VALIDATION ======
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====== INTERNATIONALIZATION ======
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ====== STATIC FILES ======
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / 'encyclopedia' / 'static']

# ====== DEFAULT PRIMARY KEY ======
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====== AUTHENTICATION ======
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ====== MESSAGES ======
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ====== CACHE ======
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# ====== APP SPECIFIC SETTINGS ======
# GitHub Sync - Environment variables are expected to be set on the platform
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.environ.get('GITHUB_REPO_OWNER', '')
GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', '')

# AI Images - Environment variable IMGBB_API_KEY can be left empty if not used
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', '')

# ====== PRODUCTION SECURITY (Ensures secure settings when DEBUG is False) ======
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    # Note: Koyeb handles SSL/HTTPS termination automatically, no proxy config needed
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'

if 'runserver' in sys.argv or 'migrate' in sys.argv:
    print("=" * 60)
    print("DEBUG: Checking imports...")
    
    try:
        from encyclopedia import views
        print("✅ Successfully imported views")
        
        # Check for required attributes
        required = ['generate_ai_image', 'generate_ai_image_process', 'ai_image_result']
        for attr in required:
            if hasattr(views, attr):
                print(f"✅ Found: {attr}")
            else:
                print(f"❌ Missing: {attr}")
                
    except Exception as e:
        print(f"❌ Import error: {e}")
    
    print("=" * 60)
