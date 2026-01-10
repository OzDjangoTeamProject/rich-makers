#!/usr/bin/env bash
set -euo pipefail

echo "✨ Starting application..."

PY="/app/.venv/bin/python"

echo "🔎 Python executable: $($PY -c 'import sys; print(sys.executable)')"
echo "🔎 Django version: $($PY -c 'import django; print(django.get_version())')"

if [[ "${WAIT_FOR_DB:-1}" == "1" ]]; then
  DB_HOST="${DJANGO_DB_HOST:-db}"
  DB_PORT="${DJANGO_DB_PORT:-5432}"
  echo "⏳ Waiting for DB at ${DB_HOST}:${DB_PORT}..."
  for i in {1..60}; do
    if (echo >"/dev/tcp/${DB_HOST}/${DB_PORT}") >/dev/null 2>&1; then
      echo "✅ DB is reachable."
      break
    fi
    echo "… still waiting (${i}/60)"
    sleep 1
  done
fi

echo "🧩 Running migrations..."
$PY manage.py migrate --noinput

if [[ "${COLLECTSTATIC:-1}" == "1" ]]; then
  echo "📦 Collecting static files..."
  $PY manage.py collectstatic --noinput
fi

echo "🚀 Launching Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"
