#!/usr/bin/env bash

set -e

# Be careful with vm.max_map_count: https://stackoverflow.com/a/53097050
# https://www.elastic.co/docs/deploy-manage/deploy/self-managed/bootstrap-checks?version=9.0#bootstrap-checks-max-map-count

echo "Check if the ./secrets/certs directory is empty"
if [ $(ls -A -1 ./secrets/certs/ | wc -l) -eq 1 ]; then
  docker compose -f docker-compose.setup.yaml run --rm certs
fi

echo "Check if the ./secrets/keystore/ directory contains exactly one file"
if [ $(ls -A -1 ./secrets/keystore/ | wc -l) -eq 1 ]; then
   docker compose -f docker-compose.setup.yaml run --rm keystore
fi

# I don't use `-d` on purpose to see the logs
echo "Starting the Elastic Stack..."
docker compose -f docker-compose.o11y-stack.yaml up

# Useful commands when you update the YAML configuration files
# docker compose -f docker-compose.o11y-stack.yaml build apm-server
# docker compose -f docker-compose.o11y-stack.yaml exec apm-server bash
# docker compose -f docker-compose.o11y-stack.yaml exec elasticsearch bash
# docker compose -f docker-compose.o11y-stack.yaml up fleet-server
