# NGINX Next Upstream

Have your own NGINX playground environment on localhost Kubernetes! Learn how it works, invoke automation, and many more!

```shell
kind create cluster --config kind-config.yaml
kubectl create namespace development
kubectl config set-context --current --namespace=development
helm repo add ingress-nginx charts/ingress-nginx
helm repo update
helm install nginx-internal ingress-nginx/ingress-nginx --namespace development -f ./nginx-internal-values.yaml --dry-run
```

You can use the following command to access the service directly without the Ingress: 

```shell
kubectl proxy
curl -i http://localhost:8001/api/v1/namespaces/development/services/env-web-server-service:8080/proxy/
```

Wait a few minutes, and you should be able to access `http://localhost:8000/`. Delete the cluster when you are done by running:

```shell
kind delete cluster
```
