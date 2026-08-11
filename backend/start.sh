#!/bin/bash
echo "=== Starting Elroyy IMS Backend ==="
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# Try migrations but don't fail if they error
echo "=== Running migrations ==="
flask db upgrade && echo "Migrations OK" || echo "Migration failed - continuing"

# Start gunicorn
echo "=== Starting gunicorn on port $PORT ==="
exec gunicorn \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --timeout 120 \
  --log-level debug \
  --access-logfile - \
  --error-logfile - \
  "app:create_app()"
