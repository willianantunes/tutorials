#!/usr/bin/env bash

# # https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

locust --locustfile auth0_fluentd_load_testing/locustfile.py \
  --headless \
  --users 100 \
  --spawn-rate 5 \
  --run-time 30s \
  --csv locust_report \
  --csv-full-history \
  --only-summary
