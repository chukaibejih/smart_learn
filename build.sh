#!/usr/bin/env bash

set -o errexit  # exit when there is an error error

pip install -r requirements.txt

# python manage.py collectstatic --no-input
python manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input
fi
