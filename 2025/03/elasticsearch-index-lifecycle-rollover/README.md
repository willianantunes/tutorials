# Elasticsearch Index Lifecycle Rollover

TODO.

## Running the project

To run the project you must start the development environment by running the following command:

```shell
./scripts/start-development.sh
```

It does the following:

- Start the Elasticsearch service.
- Configure the password for the `kibana_system` user.
- Start the Kibana service.
- Execute the Terraform script to setup the Elasticsearch environment.

Now you are able to run the tests:

```shell
docker compose up integration-tests
```

## Important links

- [Tutorial: Automate rollover with ILM](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/getting-started-index-lifecycle-management.html)
- [Data streams](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/data-streams.html)
