#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clear static files and collect again
rm -rf staticfiles
python manage.py collectstatic --no-input --clear

# Run all migrations (including Django core)
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
python manage.py shell -c "
from django.contrib.auth.models import User;
User.objects.create_superuser('admin', 'admin@maratona.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')
"

# Set RENDER environment variable
export RENDER=true
