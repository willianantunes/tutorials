# Load Testing Unleash: A Guide Using Locust

To understand it, please read the article TBD.

## Project details

Steps:

```shell
kind create cluster --config iac/kind-config.yaml
kubectl create namespace development
kubectl config set-context --current --namespace=development
# Create DB and UNLEASH
kubectl apply -f iac/0-db-dump.yaml
kubectl apply -f iac/1-db-deployment.yaml
kubectl logs -f deployment/db-postgres-deployment
kubectl apply -f iac/2-unleash-deployment.yaml
kubectl logs -f deployment/unleash-deployment
# Create LOCUST MASTER
# You can http://localhost:8089/ when it's ready
docker-compose build performance-testing
kind load docker-image load-testing-unleash-locust_performance-testing:latest
kubectl apply -f iac/3-locust-master-deployment.yaml
kubectl logs -f deployment/locust-master
# Create LOCUST SLAVE
kubectl apply -f iac/4-locust-worker-deployment.yaml
kubectl logs -f deployment/locust-worker --all-containers=true --tail=10
# Delete resources
kind delete cluster
```

To troubleshoot:

```shell
kubectl get events -w
kubectl -n development run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash
nmap db-postgres-service.development.svc.cluster.local -PS5432
nmap unleash-service.development.svc.cluster.local -PS4242
```
