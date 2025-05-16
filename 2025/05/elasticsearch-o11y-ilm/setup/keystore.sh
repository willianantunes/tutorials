#!/usr/bin/env bash

set -e

echo "Setting bootstrap password..."
(echo "$ELASTIC_PASSWORD" | elasticsearch-keystore add -x 'bootstrap.password')

# ----- Setting Secrets

## Add Additional Config
# 1- Copy the below commented block, uncomment it, and replace <name>, <key>, and <KEY_ENV_VALUE>.
# 2- Pass <KEY_ENV_VALUE> to setup container in `docker-compose-setup.yml`

## Setting <name>
#echo "Setting <name>..."
#(echo "$<KEY_ENV_VALUE>" | elasticsearch-keystore add -x '<key>')


# ----- Setting S3 Secrets

echo "Configuring S3 Access Key and Secret Key..."
(echo -n "root" | elasticsearch-keystore add 's3.client.minio.access_key' --stdin)
(echo -n "password" | elasticsearch-keystore add 's3.client.minio.secret_key' --stdin)