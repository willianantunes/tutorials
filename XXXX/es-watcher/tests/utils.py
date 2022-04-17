from contextlib import contextmanager
from uuid import uuid4

from elasticsearch import Elasticsearch


@contextmanager
def yield_temporary_index(client: Elasticsearch):
    index_name = f"salt-index-{uuid4()}"

    client.indices.create(index_name)
    yield index_name
    client.indices.delete(index_name)
