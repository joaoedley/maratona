#!/bin/bash

# Install system dependencies for PostgreSQL
apt-get update
apt-get install -y libpq-dev python3-dev gcc

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
