#!/bin/sh

echo "Waiting for PostgreSQL..."
until python - <<'PY'
import os, socket, sys
host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
s = socket.socket()
try:
    s.settimeout(2)
    s.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    s.close()
PY
do
  sleep 2
done
echo "PostgreSQL is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
