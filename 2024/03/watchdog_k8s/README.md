# Monitoring K8S resources

Work in progress.

## Project details

Initiate your own cluster:

```shell
kind create cluster --config kind-config.yaml
kubectl create namespace development
kubectl config set-context --current --namespace=development
```

Install `cert-manager` through Helm (to make api version `cert-manager.io/v1` available):

```shell
helm repo add jetstack https://charts.jetstack.io --force-update
helm repo update
helm install \                                               
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.2 \
  --set installCRDs=true \
  --set prometheus.enabled=false
```

Run the application:

```shell
docker compose build remote-interpreter
kind load docker-image watchdog_k8s-remote-interpreter:latest
kubectl apply -f k8s/ 
```

Sample log of a Pod created by the CronJob:

```
{"message": "Checking certificate: development|develop-wigi-com-br", "correlation_id": "ec13ecd1-708c-42db-8eca-c1bc26b09628", "name": "watchdog_k8s.handler", "levelname": "INFO", "lineno": 33, "pathname": "/app/watchdog_k8s/handler.py", "asctime": "2024-02-16 18:09:03,890", "taskName": null}
{"message": "Certificate development|develop-wigi-com-br does not have a renewalTime", "correlation_id": "ec13ecd1-708c-42db-8eca-c1bc26b09628", "name": "watchdog_k8s.handler", "levelname": "ERROR", "lineno": 42, "pathname": "/app/watchdog_k8s/handler.py", "asctime": "2024-02-16 18:09:03,905", "taskName": null}
{"message": "Checking certificate: development|develop-willianantunesi-com-br", "correlation_id": "ec13ecd1-708c-42db-8eca-c1bc26b09628", "name": "watchdog_k8s.handler", "levelname": "INFO", "lineno": 33, "pathname": "/app/watchdog_k8s/handler.py", "asctime": "2024-02-16 18:09:03,905", "taskName": null}
{"message": "Certificate development|develop-willianantunesi-com-br does not have a renewalTime", "correlation_id": "ec13ecd1-708c-42db-8eca-c1bc26b09628", "name": "watchdog_k8s.handler", "levelname": "ERROR", "lineno": 42, "pathname": "/app/watchdog_k8s/handler.py", "asctime": "2024-02-16 18:09:03,910", "taskName": null}
{"message": "Some certificates are either about to expire or invalid. Please fix them ASAP", "correlation_id": "ec13ecd1-708c-42db-8eca-c1bc26b09628", "name": "watchdog_k8s.handler", "levelname": "ERROR", "lineno": 50, "pathname": "/app/watchdog_k8s/handler.py", "asctime": "2024-02-16 18:09:03,910", "taskName": null}
Stream closed EOF for development/watchdog-k8s-cronjob-28468449-4v95d (watchdog-k8s)
```

In this laboratory `renewalTime` won't be available, so the CronJob will fail. To make it run without errors, you can complete the `cert-manager` configuration to make it work with Let's Encrypt.
