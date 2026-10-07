# 1. Base Python image
FROM python:3.13-slim

# 2. Environment variables: Output logs directly to terminal
ENV PYTHONUNBUFFERED=1

# 3. Update OS & install build dependencies
RUN apt-get update && apt-get -y install gcc libpq-dev gettext && rm -rf /var/lib/apt/lists/*

# 4. Create working directory inside container
WORKDIR /app

# 5. Copy requirements first for Docker layer caching
COPY requirements.txt /app/requirements.txt

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 7. Copy remaining project code into container
COPY . /app/

# 8. Collect static files during image build (uses dummy SECRET_KEY if env var isn't set yet)
RUN SECRET_KEY=dummy python manage.py collectstatic --noinput

# 9. Run database migrations, then start Gunicorn on dynamic $PORT
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn company_management.wsgi:application --bind 0.0.0.0:$PORT"]

