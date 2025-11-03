#!/bin/bash
set -e

# wait for DB to be ready...
echo "Waiting for DB to be ready..."
until python - <<PY
import sys, socket, os
host = os.getenv('DB_HOST','db')
port = int(os.getenv('DB_PORT','3306'))
s = socket.socket()
try:
    s.connect((host, port))
    print("DB reachable")
except Exception as e:
    print("DB not reachable")
    sys.exit(1)
finally:
    s.close()
PY
do
    echo "DB not up yet"
    sleep 2
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

# start passed command
exec "$@"
