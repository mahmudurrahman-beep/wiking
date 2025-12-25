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
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ====== HOST CONFIGURATION FOR KOYEB ======
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# For development
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])

CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.koyeb.app')]

# ====== APPLICATION DEFINITION ======
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'encyclopedia',  # Your local app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Best practice: Right under SecurityMiddleware
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

# WhiteNoise Configuration for Koyeb/Heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure this directory exists or remove if not using a project-level static folder
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
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.environ.get('GITHUB_REPO_OWNER', '')
GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', '')
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', '')

# ====== PRODUCTION SECURITY ======
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'

# ====== DEBUG HELPER ======
if 'runserver' in sys.argv or 'migrate' in sys.argv:
    print("=" * 60)
    print("DEBUG: Checking imports...")
    try:
        from encyclopedia import views
        print("✅ Successfully imported views")
        required = ['generate_ai_image', 'generate_ai_image_process', 'ai_image_result']
        for attr in required:
            status = "✅ Found" if hasattr(views, attr) else "❌ Missing"
            print(f"{status}: {attr}")
    except Exception as e:
        print(f"❌ Import error: {e}")
    print("=" * 60)
