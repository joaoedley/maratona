#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clear static files and collect again
rm -rf staticfiles
python manage.py collectstatic --no-input --clear
python manage.py migrate
