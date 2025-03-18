import unittest

from index_lifecycle_rollover.elasticsearch_client import retrieve_elasticsearch_tasks
from index_lifecycle_rollover.elasticsearch_client import retrieve_thread_pool


class TestElasticsearchClient(unittest.TestCase):
    def test_retrieve_elasticsearch_tasks(self):
        result = retrieve_elasticsearch_tasks()
        self.assertGreater(len(result), 0)

    def test_retrieve_thread_pool(self):
        result = retrieve_thread_pool()
        self.assertGreater(len(result), 0)
