#!/bin/bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

# Without `-h localhost` given I want to use the Unix socket
psql -U unleash -w development < /tmp/postgresql-dump/unleash-db.dump.sql
