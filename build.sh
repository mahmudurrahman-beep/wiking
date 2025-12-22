#!/bin/bash
echo "=== Building Django Wiki ==="
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
echo "=== Build Complete ==="
