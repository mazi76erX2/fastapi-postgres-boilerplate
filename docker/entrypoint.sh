#!/bin/sh
set -e

# Optionally wait for PostgreSQL to be ready
# Ensure DATABASE_HOST is set in your environment (e.g. via .env or Docker Compose)
if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for PostgreSQL at $DATABASE_HOST..."
  while ! nc -z "$DATABASE_HOST" 5432; do
    sleep 0.1
  done
  echo "PostgreSQL is available."
fi

# Determine environment mode (default: production)
ENVIRONMENT=${FASTAPI_ENV:-prod}
echo "Starting container in $ENVIRONMENT mode..."

# Run the appropriate command based on the environment
if [ "$ENVIRONMENT" = "dev" ]; then
  echo "Running in development mode..."
  # In development, use auto-reload
  exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
  echo "Running in production mode..."
  # In production, you might use a production server (e.g., uvicorn or gunicorn with uvicorn workers)
  # For simplicity, we use uvicorn directly here.
  exec uvicorn main:app --host 0.0.0.0 --port 8000
fi
