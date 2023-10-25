#!/usr/bin/env bash

set -o errexit  # exit when there is an error error

# provide the superuser email, or a default
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"hello@ernest.com"}

cd /api/

# /opt/venv/bin/pip install -r requirements.txt

# python manage.py collectstatic --no-input
/opt/venv/bin/python manage.py migrate --noinput

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

# if [[ $CREATE_SUPERUSER ]]; then
#   /opt/venv/bin/python manage.py createsuperuser --no-input
# fi