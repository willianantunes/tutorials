# Elasticsearch Index Lifecycle Rollover

To understand it, please read the article [Index Rollover in Elasticsearch: A Beginner's Tutorial](https://www.willianantunes.com/blog/2025/03/index-rollover-in-elasticsearch-a-beginners-tutorial/).

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

If you only need to collect metrics, you can run the following command:

```shell
docker compose run --rm -e TEST_COLLECT_METRICS=1 integration-tests python -m unittest tests.agents.test_elasticsearch.TestElasticsearch.test_collect_metrics
```

## Important links

- [Tutorial: Automate rollover with ILM](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/getting-started-index-lifecycle-management.html)
- [Data streams](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/data-streams.html)
