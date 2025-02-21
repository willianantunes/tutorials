#!/usr/bin/env bash

set -e

python configure_alternate_exchange.py --delete-queue-by-name "listener.$TARGET_EXCHANGE"
