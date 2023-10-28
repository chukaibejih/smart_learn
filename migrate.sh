#!/usr/bin/env bash

set -o errexit  # exit when there is an error error

# provide the superuser email, or a default
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"hello@smartlearn.com"}

# enter working directory
cd /api/

# use the virtual env to run the python commands
/opt/venv/bin/python manage.py migrate --noinput

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
