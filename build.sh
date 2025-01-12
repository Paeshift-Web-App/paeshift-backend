#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create a superuser (optional)
# python manage.py createsuperuser --noinput

# Output Django settings to verify environment variables
echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY"
echo "DEBUG=$DEBUG"
echo "DATABASE_URL=$DATABASE_URL"
