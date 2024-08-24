#!/usr/bin/env bash

set -e

# Be careful with vm.max_map_count: https://stackoverflow.com/a/53097050

# Check if the ./secrets/certs directory is empty
if [ $(ls -A -1 ./secrets/certs/ | wc -l) -eq 1 ]; then
   docker compose -f docker-compose.setup.yaml run --rm certs
fi

# Check if the ./secrets/keystore/ directory contains exactly one file
if [ $(ls -A -1 ./secrets/keystore/ | wc -l) -eq 1 ]; then
   docker compose -f docker-compose.setup.yaml run --rm keystore
fi

# I don't use `-d` on purpose to see the logs
docker compose -f docker-compose.yaml up
