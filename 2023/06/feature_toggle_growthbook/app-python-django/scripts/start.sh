#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

python manage.py makemigrations
python manage.py migrate
python manage.py seed_db --create-super-user

# In case you want something simpler
# python manage.py runserver 0.0.0.0:${DJANGO_BIND_PORT:-8000}

gunicorn -cpython:gunicorn_config -b 0.0.0.0:${DJANGO_BIND_PORT:-8000} app_python_django.wsgi
