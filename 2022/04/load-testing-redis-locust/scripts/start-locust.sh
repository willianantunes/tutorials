#!/usr/bin/env bash

# # https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

locust --locustfile load_testing_redis_locust/locustfile.py \
  --headless \
  --users 25 \
  --spawn-rate 5 \
  --run-time 30s \
  --csv locust_report \
  --csv-full-history \
  --only-summary
