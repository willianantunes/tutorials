#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

python manage.py makemigrations
python manage.py migrate
python manage.py seed --create-super-user

# If you want to run your server through HTTPS
# python manage.py runserver_plus --cert-file tmp-localhost.crt 0.0.0.0:${DJANGO_BIND_PORT:-8010}

python manage.py runserver 0.0.0.0:${DJANGO_BIND_PORT:-8010}
