#!/bin/sh
set -e

echo "Waiting for database..."
sleep 3  # DB 부팅 대기용

python manage.py makemigrations --check --noinput || python manage.py makemigrations
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2