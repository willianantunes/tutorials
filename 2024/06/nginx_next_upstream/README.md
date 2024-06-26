# NGINX Next Upstream

To understand it, please read the article [NGINX on Kubernetes Made Easy: Your Local Development Sandbox](https://www.willianantunes.com/blog/2024/06/nginx-on-kubernetes-made-easy-your-local-development-sandbox/).

```shell
kind create cluster --config kind-config.yaml
kubectl create namespace development
kubectl config set-context --current --namespace=development
helm repo add ingress-nginx charts/ingress-nginx
helm repo update
helm install nginx-internal ingress-nginx/ingress-nginx --namespace development -f ./nginx-internal-values.yaml
kubectl apply -f scenario.yaml
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
