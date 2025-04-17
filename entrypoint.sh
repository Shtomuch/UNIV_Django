#!/usr/bin/env sh
set -e

# якщо /data не існує
mkdir -p /data

# міграції
python manage.py migrate --noinput

# створюємо суперюзера, якщо задані змінні
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && \
   [ -n "$DJANGO_SUPERUSER_EMAIL" ] && \
   [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then

  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email    "$DJANGO_SUPERUSER_EMAIL" \
  || true   # ігноруємо помилку, якщо вже є
fi

# запускаємо gunicorn
exec "$@"
