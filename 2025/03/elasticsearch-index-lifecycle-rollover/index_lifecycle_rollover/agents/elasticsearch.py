import logging

from index_lifecycle_rollover.elasticsearch_client import retrieve_elasticsearch_tasks
from index_lifecycle_rollover.elasticsearch_client import retrieve_thread_pool
from index_lifecycle_rollover.elasticsearch_client import send_to_elasticsearch

_logger = logging.getLogger(__name__)


class Calopsita:

    def __init__(self):
        super().__init__()


def collect_metrics():
    _logger.info("Like Dev Tools `GET _cat/thread_pool?v`")
    threads = retrieve_thread_pool()
    _logger.info("Threads found %s", len(threads))
    documents = [
        {
            "node_name": thread.node_name,
            "name": thread.name,
            "active": thread.active,
            "queue": thread.queue,
            "rejected": thread.rejected,
        }
        for thread in threads
        if thread.active > 0 or thread.queue > 0 or thread.rejected > 0
    ]
    _logger.info("Number of threads that are active, in queue or rejected %s", len(documents))
    index_alias = "es-thread-pool"
    send_to_elasticsearch(documents, index_alias)

    _logger.info("Like Dev Tools `GET /_tasks?pretty=true&human=true&detailed=true`")
    tasks = retrieve_elasticsearch_tasks()
    _logger.info("Tasks found %s", len(tasks))
    five_ms_in_nanos = 5_000_000
    documents = [
        {
            "node": task.node,
            "id": task.id,
            "action": task.action,
            "running_time_milliseconds": int(task.running_time_in_nanos // 1_000_000),
            "running_time_string": task.running_time,
            "cancellable": task.cancellable,
            "parent_task_id": task.parent_task_id,
            "description": task.description,
        }
        for task in tasks
        if task.running_time_in_nanos > five_ms_in_nanos
    ]
    _logger.info("Number of tasks that are running %s", len(documents))
    index_alias = "es-tasks"
    send_to_elasticsearch(documents, index_alias)
