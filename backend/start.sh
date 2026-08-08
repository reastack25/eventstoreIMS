#!/bin/bash
set -e

echo "Running migrations..."
flask db upgrade

echo "Starting gunicorn on port $PORT..."
exec gunicorn --bind "0.0.0.0:$PORT" --workers 2 --timeout 120 "app:create_app()"
