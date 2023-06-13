#!/bin/bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

mongorestore --authenticationDatabase admin --authenticationMechanism SCRAM-SHA-1 -u root -p password --db test --archive="/tmp/mongodb-dump/growthbook-mongodump"
