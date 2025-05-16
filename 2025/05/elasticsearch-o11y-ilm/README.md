# Elastic Observability: Dealing with Index Lifecycle Management (ILM)

TODO.

## Running the project

Execute the command below to start the services:

```shell
./start.sh
```

Let's expose the APM server and Elasticsearch services using a [tunneling tool](https://github.com/anderspitman/awesome-tunneling?tab=readme-ov-file). Let's use `localtunnel`:

```shell
# APM SERVER
lt --port 8200 --subdomain salt-licker-wig-apm
# ELASTICSEARCH
lt --port 9200 --local-https --allow-invalid-cert --subdomain salt-licker-cockatiel-elasticsearch
```

If the subdomain is already taken, remove the flag or change the subdomain to something else. Don't forget to update the ENV variables.

TIP: Use `ngrok` to capture the traffic and see the requests being sent to the APM server. You can use the command `ngrok http http://localhost:8200` to expose the APM server or `ngrok http https://localhost:9200` to expose the Elasticsearch service.

Create your Kubernetes cluster and install some components:

```shell
kind create cluster --config kind-config.yaml

kubectl create namespace development && kubectl create namespace o11y && kubectl create namespace proxies && \
kubectl config set-context --current --namespace=development

helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ && \
helm repo update && \
helm upgrade --install metrics-server metrics-server/metrics-server \
-f k8s/metrics-server-values.yaml --namespace kube-system --version 3.11.0

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx && \
helm repo update && \
helm upgrade --install nginx-internal ingress-nginx/ingress-nginx \
-f k8s/nginx-internal-values.yaml --namespace proxies --version 4.12.2

helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts && \
helm repo update && \
kubectl apply -f k8s/otel-collector-apps-secret.yaml && \
helm upgrade --install otel-collector-apps open-telemetry/opentelemetry-collector \
-f k8s/otel-collector-apps-values.yaml --namespace o11y --version 0.125.0

kubectl apply -f k8s/letter-b.yaml
```

Generate an Api Key accessing the page:

- https://localhost:5601/app/observabilityOnboarding/kubernetes/?category=kubernetes

Decode it from Base64 format and put its RAW value in the `k8s/elastic-agent-secret.yaml` file. Now you are ready to install the Elastic Agent:

```shell
helm repo add elastic https://helm.elastic.co && \
helm repo update && \
kubectl apply -f k8s/elastic-agent-secret.yaml && \
helm upgrade --install elastic-agent elastic/elastic-agent --version 9.0.1 \
-f k8s/elastic-agent-values.yaml --namespace o11y
```

If you want to install `kube-state-metrics` isolated, you can do it with the command below:

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
# https://github.com/kubernetes/kube-state-metrics?tab=readme-ov-file#helm-chart
helm install kube-state-metrics prometheus-community/kube-state-metrics \
-f k8s/kube-state-metrics-values.yaml --namespace o11y
```

## Generating telemetry data and managing indices

Call the `letter-b` service to generate telemetry data:

```shell
curl --request POST \                                                                                            
--url http://127.0.0.1:8080/api/v1/users/attributes \
--header 'Content-Type: application/json' \
--data '{
    "full_name": "'"Sal Paradise $(date +%Y-%m-%dT%H:%M:%S)"'",
    "given_name": "Sal",
    "family_name": "Paradise",
    "user_metadata":
    {
        "city": "são paulo",
        "state": "SP",
        "birthday": "1965-01-13",
        "gender": "male"
    }
}'
```

Access its ADMIN using the credentials `admin:admin`:

- http://localhost:8080/admin/login/?next=/admin/

Create metrics of fake services by executing the command below:

```shell
docker compose run --rm remote-interpreter python -m \
elastic_o11y_ilm.send_metrics --fake-services-count 100
```

Generate a reporting informing the indices and how much storage and how many shards are being used:

```shell
docker compose run --rm remote-interpreter python -m \
elastic_o11y_ilm.shard_report
```

Delete data streams based on a string pattern:

```shell
docker compose run --rm remote-interpreter python -m \
elastic_o11y_ilm.data_stream_deletion --pattern "metrics-apm.app*"
```

Migrate indices and delete the old ones:

```shell
docker compose run --rm remote-interpreter python -m \
elastic_o11y_ilm.migrate_indices --dest-index "metrics-apm.app.all-default" \
--pattern "metrics-apm.app.*" \
--conflict-decision "abort"
```

## Creating snapshots using Minio (S3)

Expose the Minio Web Console:

```shell
lt --port 9000 --subdomain salted-meat-minio-repo
```

The file `setup/keystore.sh` configure the following keys:

```shell
s3.client.minio.access_key
s3.client.minio.secret_key
```

The client name is `minio`. We'll use it to create the repository connection. The Terraform provider `elastic/elasticstack` does not support its creation because it doesn't support some properties, so we need to create it manually. Execute the following in the [Dev Tools](https://localhost:5601/app/dev_tools):

```shell
PUT _snapshot/minio
{
  "type": "s3",
   "settings": {
      "bucket": "elasticsearch-bucket",
      "client": "minio",
      "endpoint": "salted-meat-minio-repo.loca.lt:443",
      "path_style_access": "true",
      "protocol": "https"
   }
}
```

You'll receive `{"acknowledged":true}` as a response. Uncomment the resource `elasticstack_elasticsearch_snapshot_lifecycle.o11y_nightly_snapshots` and create the Terraform infrastructure:

```shell
docker compose run --rm tf bash -c "
    cd iac && \
    terraform init && \
    terraform apply -auto-approve
"
```

You are ready to go!

## Cleaning up

Destroy/stop everything:

```shell
kind delete cluster --name kind
docker compose down --remove-orphans -t 0
```

Don't forget to stop the tunnels.

## Project links

Use the credential `elastic:elastic` to log in:

- Infrastructure Inventory: https://localhost:5601/app/metrics/inventory

## Useful commands

```shell
helm repo list
helm search repo metrics-server -l
helm search repo ingress-nginx -l
helm search repo open-telemetry -l
helm search repo open-telemetry -l
helm search repo elastic -l

helm show chart elastic/elastic-agent --version 9.0.1
helm pull elastic/elastic-agent --version 9.0.1
docker compose run --rm tf bash -c "
    cd iac && \
    terraform init && \
    terraform apply -auto-approve
"
```

## Useful docs to understand concepts

- [APM: Index lifecycle management](https://www.elastic.co/docs/solutions/observability/apm/index-lifecycle-management).
- [Fleet: Data streams](https://www.elastic.co/docs/reference/fleet/data-streams).