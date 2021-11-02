#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

python manage.py migrate

python manage.py runserver 0.0.0.0:${DJANGO_BIND_PORT:-8000}
