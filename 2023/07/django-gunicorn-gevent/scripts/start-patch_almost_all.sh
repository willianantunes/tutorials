#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

python manage.py makemigrations
python manage.py migrate

gunicorn -cpython:gunicorn_config_patch_almost_all -b 0.0.0.0:${DJANGO_BIND_PORT:-$PORT} django_gunicorn_gevent.wsgi
