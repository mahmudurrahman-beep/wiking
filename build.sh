#!/usr/bin/env bash
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Setting up database..."
python manage.py migrate

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "📝 Importing wiki entries..."
# First ensure entries directory exists
mkdir -p entries
python import_entries.py

echo "✅ Build completed!"
