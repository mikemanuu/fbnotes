# Base image
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . /app/

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
