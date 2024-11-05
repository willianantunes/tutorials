# Rundeck playground environment on Kubernetes

Wanna ride on Rundeck 🏇?

Have your own [Rundeck playground environment on localhost Kubernetes](https://www.willianantunes.com/blog/2022/05/rundeck-playground-environment-on-kubernetes/)! Learn how it works, invoke automation, and many more!

## Project details

Learn more in [this blog post](https://bit.ly/3PByXcj).

```shell
cd rundeck-custom-image && docker build -t rundeck-k8s . && cd ..
kind create cluster --config kind-config.yaml
kubectl create namespace support-tools
kubectl config set-context --current --namespace=support-tools
kind load docker-image rundeck-k8s:latest
kubectl apply -f k8s-manifests/0-database.yaml
kubectl apply -f k8s-manifests/1-permissions.yaml
kubectl apply -f k8s-manifests/2-secrets-and-configmap.yaml
kubectl logs -f deployment/db-postgres-deployment
kubectl apply -f k8s-manifests/3-service-and-deployment.yaml
kubectl logs -f deployment/rundeck-k8s-deployment
kubectl exec -it deploy/rundeck-k8s-deployment -- bash
```

Wait a few minutes, and you should be able to access `http://localhost:8000/`. Use `admin` for username and password.

```shell
kind delete cluster
```

Set the context you had been using before the ride:

```shell
kubectl config current-context
kubectl config get-contexts
kubectl config use-context YOUR_PREVIOUS_CONTEXT
```

Explore the Rundeck container:

```shell
docker run -it --rm --entrypoint bash rundeck-k8s
```
