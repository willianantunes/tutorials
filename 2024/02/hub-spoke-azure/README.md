# Hub-spoke network topology on Azure

Work in progress.

## Prerequisites

- [Create a service principal on Azure](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret).
- Configure the following environment variables in `docker-compose.yml` file:
  - ARM_CLIENT_ID
  - ARM_CLIENT_SECRET
  - ARM_TENANT_ID
  - ARM_SUBSCRIPTION_ID

## Running the Terraform code

Run the following command to start the container:

```shell
docker compose run --rm docker-client-tf-did bash
```

To create the infrastructure, run the following command:

```shell
terraform init
terraform apply
```

## Running static code analysers

```shell
tfsec .
terrascan scan --iac-type terraform
```

## Authenticating on Azure CLI

Inside the container, run the following command:

```shell
```shell
az login \
--service-principal \
-t $ARM_TENANT_ID \
-u $ARM_CLIENT_ID \
-p $ARM_CLIENT_SECRET
```

Now, for example, you can list SKU's available to create virtual machines by running:

```shell
az vm list-skus --location westus2 --output table
```
