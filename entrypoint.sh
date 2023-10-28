#!/bin/bash
# creating a default application port to run on
APP_PORT=${PORT:-8080}
cd /api/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm smart_learning.wsgi:application --bind "0.0.0.0:$APP_PORT"