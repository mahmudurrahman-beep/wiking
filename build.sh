#!/bin/bash
echo "=== Building Django Wiki ==="

# Install dependencies
echo "1. Installing Python packages..."
pip install -r requirements.txt

# Run database migrations
echo "2. Running database migrations..."
python manage.py migrate --noinput

# Create default directories if they don't exist
echo "3. Setting up file structure..."
mkdir -p entries
mkdir -p history
mkdir -p encyclopedia/static/encyclopedia

# Create a default admin user if not exists
echo "4. Setting up default users..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@wiki.com', 'admin123')
    print('✓ Superuser created: admin/admin123')
else:
    print('✓ Superuser already exists')
"

# Collect static files
echo "5. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build Complete ==="
echo "Note: Git sync happens at runtime, not during build."
