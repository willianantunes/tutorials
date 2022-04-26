import pytest

from elasticsearch.helpers import bulk

from es_watcher.elasticsearch_client import es_client
from resources.sample_entries import auth0_log_events_samples
from tests.utils import yield_temporary_index


@pytest.fixture
def bulk_insert_auth0_log_events():
    with yield_temporary_index(es_client) as index_name:
        # https://www.elastic.co/guide/en/elasticsearch/reference/8.1/mapping-fields.html#mapping-fields
        actions = [{"_index": index_name, "_source": document} for document in auth0_log_events_samples]
        bulk(es_client, actions)
        # https://www.elastic.co/guide/en/elasticsearch/reference/8.1/indices-refresh.html
        es_client.indices.refresh(index_name)
        yield index_name


def test_should_query_with_match_all(bulk_insert_auth0_log_events):
    # Arrange
    index_name = bulk_insert_auth0_log_events
    # Act
    # https://www.elastic.co/guide/en/elasticsearch/reference/8.1/query-dsl-match-all-query.html
    query = {"query": {"match_all": {}}}
    results = es_client.search(index=index_name, body=query)
    # Assert
    assert results["hits"]["total"] == {"value": 10, "relation": "eq"}
