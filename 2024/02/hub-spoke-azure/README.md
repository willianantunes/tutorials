# Hub-spoke network topology on Azure

Work in progress.

## Running the code

Configure the required environment variables in docker-compose.yml and run the following command:

```shell
docker compose run --rm docker-client-tf-did bash
```

To create the infrastructure, run the following command:

```shell
terraform init
terraform apply
```

You can also execute:

```shell
tfsec .
terrascan scan --iac-type terraform
```
