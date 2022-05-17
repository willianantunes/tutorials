#!/usr/bin/env bash

# # https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

locust -f auth0_fluentd_load_testing/locustfile.py



