import os
import unittest

from unittest.mock import patch

from elasticsearch import NotFoundError

from index_lifecycle_rollover.agents.elasticsearch import collect_metrics
from index_lifecycle_rollover.elasticsearch_client import Task
from index_lifecycle_rollover.elasticsearch_client import TaskStatus
from index_lifecycle_rollover.elasticsearch_client import ThreadPoolEntry
from index_lifecycle_rollover.elasticsearch_client import es_client


def delete_data_stream(name):
    try:
        es_client.indices.delete_data_stream(name=name)
    except NotFoundError:
        pass


TEST_COLLECT_METRICS = int(os.getenv("TEST_COLLECT_METRICS", 0))


class TestElasticsearch(unittest.TestCase):
    def setUp(self):
        self.mock_thread_pool_data = [
            ThreadPoolEntry(
                node_name="node1",
                name="search",
                active=2,
                queue=0,
                rejected=0,
            ),
            ThreadPoolEntry(
                node_name="node1",
                name="write",
                active=1,
                queue=1,
                rejected=0,
            ),
        ]
        self.mock_tasks_data = [
            Task(
                id="123",
                action="cluster:monitor/tasks/lists",
                node="node1",
                cancellable=True,
                cancelled=False,
                type="transport",
                start_time="1234567890",
                running_time="1.2s",
                running_time_in_nanos=1200000000,
                status=TaskStatus(
                    databases_count=10,
                    expired_databases=1,
                    failed_downloads=0,
                    skipped_updates=2,
                    successful_downloads=7,
                    total_download_time=5000,
                    state="RUNNING",
                ),
            )
        ]
        if TEST_COLLECT_METRICS == 0:
            delete_data_stream("es-thread-pool")
            delete_data_stream("es-tasks")

    @unittest.skipIf(TEST_COLLECT_METRICS == 0, "Should be executed manually")
    def test_collect_metrics(self):
        collect_metrics()

    @patch("index_lifecycle_rollover.agents.elasticsearch.retrieve_thread_pool")
    @patch("index_lifecycle_rollover.agents.elasticsearch.retrieve_elasticsearch_tasks")
    def test_save_metrics_when_metrics_are_present(self, mock_tasks, mock_thread_pool):
        # Arrange
        mock_thread_pool.return_value = self.mock_thread_pool_data
        mock_tasks.return_value = self.mock_tasks_data
        # Act
        collect_metrics()
        # Assert
        es_client.indices.refresh(index="es-thread-pool")
        es_client.indices.refresh(index="es-tasks")
        thread_pool_data = es_client.search(index="es-thread-pool")
        tasks_data = es_client.search(index="es-tasks")
        self.assertEqual(thread_pool_data["hits"]["total"]["value"], len(self.mock_thread_pool_data))
        self.assertEqual(tasks_data["hits"]["total"]["value"], len(self.mock_tasks_data))
        thread_pool_hits = thread_pool_data["hits"]["hits"]
        for i, thread_pool in enumerate(self.mock_thread_pool_data):
            source = thread_pool_hits[i]["_source"]
            self.assertEqual(source["node_name"], thread_pool.node_name)
            self.assertEqual(source["name"], thread_pool.name)
            self.assertEqual(source["active"], thread_pool.active)
            self.assertEqual(source["queue"], thread_pool.queue)
            self.assertEqual(source["rejected"], thread_pool.rejected)
            self.assertIn("@timestamp", source)
        task_hits = tasks_data["hits"]["hits"]
        for i, task in enumerate(self.mock_tasks_data):
            source = task_hits[i]["_source"]
            self.assertEqual(source["id"], task.id)
            self.assertEqual(source["action"], task.action)
            self.assertEqual(source["node"], task.node)
            self.assertEqual(source["running_time_milliseconds"], int(task.running_time_in_nanos // 1_000_000))
            self.assertEqual(source["running_time_string"], task.running_time)
            self.assertEqual(source["cancellable"], task.cancellable)
            self.assertEqual(source["description"], task.description)
            self.assertEqual(source["parent_task_id"], task.parent_task_id)
            self.assertIn("@timestamp", source)
