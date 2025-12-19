#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# --- CRITICAL: Add this line after migrate ---
python import_entries.py

echo "✅ Build, migrations, and data import complete."
