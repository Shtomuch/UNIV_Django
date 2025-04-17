#!/usr/bin/env sh
set -e

# на випадок, якщо /data не примонтовано томом
mkdir -p /data

# міграції
python manage.py migrate --noinput

exec "$@"   # запускає gunicorn (CMD)
