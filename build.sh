#!/bin/bash
echo "=== Building Django Wiki with AI ==="

# Install dependencies
echo "1. Installing Python packages..."
pip install -r requirements.txt

# Run database migrations
echo "2. Running database migrations..."
python manage.py migrate --noinput

# Create a default admin user if not exists
echo "3. Setting up default users..."
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

# Create entries directory if it doesn't exist
echo "4. Setting up file structure..."
mkdir -p entries
mkdir -p history
mkdir -p encyclopedia/static/encyclopedia

# Create placeholder logo if it doesn't exist
if [ ! -f "encyclopedia/static/encyclopedia/logo.jpg" ]; then
    echo "Creating placeholder logo..."
    echo "Placeholder" > encyclopedia/static/encyclopedia/logo.jpg
fi

# Collect static files
echo "5. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build Complete ==="
