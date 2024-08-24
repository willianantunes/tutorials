# Observability with Elastic

This is based on the repository [lizozom/docker-elastic-observability-with-apm](https://github.com/lizozom/docker-elastic-observability-with-apm).

## Running the project

1. Execute the command below to start the services:

```shell
./start.sh
```

2. Use Ngrok to expose the Kibana service with the command `ngrok http https://localhost:9200`. Let's say Ngrok generated the URL `https://4aeb-2804-14c-160-9316-00-ef15.ngrok-free.app`. Configure it in the `elastic-agent-standalone-kubernetes.yml` with the following command:

```shell
sed -i 's|http://localhost:9200|https://4aeb-2804-14c-160-9316-00-ef15.ngrok-free.app:443|g' k8s/elastic-agent-standalone-kubernetes.yml
```

3. Initialize terraform with `terraform init` and apply the configuration with `terraform apply`. After that, execute the command `terraform output -json api_key_k8s_kind | jq -r '.encoded' | base64 -d` and copy the output, for example, `hQWMi5EBhUCAyqbLKnVv:CLAvDR_AQeOqe0yo5RJHTQ`. Configure it in the `elastic-agent-standalone-kubernetes.yml` with the following command:

```shell
sed -i 's|YOUR_API_KEY|hQWMi5EBhUCAyqbLKnVv:CLAvDR_AQeOqe0yo5RJHTQ|g' k8s/elastic-agent-standalone-kubernetes.yml
```

4. Create your Kubernetes cluster with the following commands:

```shell
kind create cluster --config kind-config.yaml
kubectl create namespace development
kubectl config set-context --current --namespace=development
```

5. Apply the configuration with the following command:

```shell
kubectl apply -f k8s/elastic-agent-standalone-kubernetes.yml
```

6. Check out the logs using `k8s`. You should be able to see all the pods in the Inventory page of the Observability section in Kibana.

- https://localhost:5601/app/metrics/inventory

## Destroying the project

Stop the terminal running the `./start.sh` script and run the following commands:

```shell
kind delete cluster && \
docker compose down --remove-orphans -t 0 && \
docker volume rm elastic_elasticsearch-data
```

## Tips

- If you Terraform raises an error saying Kibana returned 409, you can remove the created volume with the command `docker volume rm elastic_elasticsearch-data`. The command `docker compose down --remove-orphans -t 0` won't do it for you. When it's done, you can run `docker compose up` again.

## Links

- [Application performance monitoring (APM)](https://www.elastic.co/guide/en/observability/current/apm.html)
- [Monitor Kubernetes: Observe the health and performance of your Kubernetes deployments](https://www.elastic.co/guide/en/observability/current/monitor-kubernetes.html#monitor-k8s-update-agent-config)
