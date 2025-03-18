#!/usr/bin/env bash

set -e

docker compose up -d es

RETRIES=12
DELAY=5
ES_URL="http://localhost:9200/_cat/health"

for i in $(seq 1 $RETRIES); do
    echo "Checking Elasticsearch status... (attempt $i)"
    STATUS=$(curl -sf --insecure -u elastic:elastic $ES_URL | grep -ioE 'green|yellow' || echo 'not green/yellow cluster status')
    if [[ "$STATUS" == "green" || "$STATUS" == "yellow" ]]; then
        echo "Elasticsearch is up and running."
        break
    fi
    if [ $i -eq $RETRIES ]; then
        echo "Elasticsearch did not start within the expected time."
        exit 1
    fi
    sleep $DELAY
done

curl -i --location 'http://localhost:9200/_security/user/kibana_system/_password' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic ZWxhc3RpYzplbGFzdGlj' \
--data '{
    "password": "kibada-wig-123456"
}'

docker compose up -d kibana

KIBANA_URL="http://localhost:5601/api/status"

for i in $(seq 1 $RETRIES); do
    echo "Checking Kibana status... (attempt $i)"
    STATUS=$(curl -sf -u elastic:elastic $KIBANA_URL | grep -qE 'All services are available|Looking good' && echo 'available' || echo 'not available')
    if [[ "$STATUS" == "available" ]]; then
        echo "Kibana is up and running."
        break
    fi
    if [ $i -eq $RETRIES ]; then
        echo "Kibana did not start within the expected time."
        exit 1
    fi
    sleep $DELAY
done

docker compose run --rm tf bash -c "
    cd iac && \
    terraform init && \
    terraform apply -auto-approve
"
