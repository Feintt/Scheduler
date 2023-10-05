#!/bin/sh

# Wait for the database to be ready
# This step is optional but can help in environments where the
# database container takes longer to start.
while ! nc -z db 5432; do
  sleep 1
done

# Run migrations
python manage.py migrate

# Start server
exec "$@"
