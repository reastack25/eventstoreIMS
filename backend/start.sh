#!/bin/bash
echo "Starting gunicorn..."
exec gunicorn \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --timeout 60 \
  "app:create_app()"
