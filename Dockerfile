# ---------- базовий образ ----------
FROM python:3.12-slim

# ---------- системні пакети ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc \
        libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- каталоги та змінні середовища ----------
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=CI_CD_Project.settings \
    PYTHONPATH=/app

# База лежить у /data  →  створимо каталог і дамо права
RUN mkdir /data

WORKDIR /app

# ---------- Python‑залежності ----------
COPY requirements*.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- код і статика ----------
COPY . .
RUN python manage.py collectstatic --noinput

# ---------- entrypoint + gunicorn ----------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "CI_CD_Project.wsgi:application", "--bind", "0.0.0.0:8000"]
