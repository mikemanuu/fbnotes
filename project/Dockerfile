# Base image
FROM python:3.11-slim

# Set working directory to where manage.py will be
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies for MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project folder (the one containing manage.py)
COPY . /app/

# Expose Django port
EXPOSE 8000

# Default command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
