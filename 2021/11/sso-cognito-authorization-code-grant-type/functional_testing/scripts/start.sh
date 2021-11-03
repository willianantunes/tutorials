#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

nginx -c /home/seluser/scripts/nginx.conf -g "daemon off;" &
python -m unittest discover tests
