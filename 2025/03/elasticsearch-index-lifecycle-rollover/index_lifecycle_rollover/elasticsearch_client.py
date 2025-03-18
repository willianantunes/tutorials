import logging

from dataclasses import dataclass
from datetime import datetime

from elasticsearch import ApiError
from elasticsearch import Elasticsearch
from elasticsearch.helpers import BulkIndexError
from elasticsearch.helpers import bulk

from index_lifecycle_rollover import settings

_logger = logging.getLogger(__name__)

if "," in settings.ELASTICSEARCH_HOSTS:
    hosts = settings.ELASTICSEARCH_HOSTS.split(",")
else:
    hosts = [settings.ELASTICSEARCH_HOSTS]

connection_details = {
    "port": settings.ELASTICSEARCH_PORT,
    "use_ssl": settings.ELASTICSEARCH_USE_SSL,
}
hosts = [dict(host=host, **connection_details) for host in hosts]

basic_auth = None
if settings.ELASTICSEARCH_USERNAME:
    basic_auth = (settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD)
es_client = Elasticsearch(hosts=hosts, basic_auth=basic_auth)


def bootstrap_initial_indices(index_alias):
    index = f"{index_alias}-000001"
    try:
        es_client.indices.create(index=index, body={"aliases": {index_alias: {"is_write_index": True}}})
    except ApiError as e:
        expected_error_1 = f"alias [{index_alias}] has more than one write index" in e.body["error"]["reason"]
        expected_error_2 = "resource_already_exists_exception" == e.error
        if not expected_error_1 and not expected_error_2:
            raise


def send_to_elasticsearch(data, index_alias):
    actions = [
        {
            "_op_type": "create",  # This guarantees the action works when the target is a data stream
            "_index": index_alias,
            "_source": {
                **doc,
                "@timestamp": datetime.now().isoformat(),
            },
        }
        for doc in data
    ]
    try:
        bulk(es_client, actions)
    except BulkIndexError as e:
        if "failed to index" in str(e):
            _logger.error("Is there a new field to the document or the field type is different?")
            if len(e.errors) > 0:
                errors_details = e.errors[0]["index"]["error"]
                error_reason = errors_details.get("reason")
                error_type = errors_details.get("type")
                _logger.error("Error type is `%s`. Reason is `%s`", error_type, error_reason)
            exit(1)
        else:
            raise


@dataclass
class ThreadPoolEntry:
    node_name: str
    name: str
    active: int
    queue: int
    rejected: int


def retrieve_thread_pool() -> list[ThreadPoolEntry]:
    response = es_client.cat.thread_pool(v=True)

    entries = []
    lines = response.body.strip().split("\n")

    # Skip the header line
    for line in lines[1:]:
        # Split by whitespace and filter out empty strings
        parts = [part for part in line.split(" ") if part]

        if len(parts) >= 5:
            entry = ThreadPoolEntry(
                node_name=parts[0],
                name=parts[1],
                active=int(parts[2]),
                queue=int(parts[3]),
                rejected=int(parts[4]),
            )
            entries.append(entry)

    return entries


@dataclass
class TaskStatus:
    databases_count: int = 0
    expired_databases: int = 0
    failed_downloads: int = 0
    skipped_updates: int = 0
    successful_downloads: int = 0
    total_download_time: int = 0
    state: str = ""


@dataclass
class Task:
    id: str
    action: str
    node: str
    cancellable: bool
    cancelled: bool
    type: str
    start_time: str
    running_time: str
    running_time_in_nanos: int
    description: str = ""
    parent_task_id: str | None = None
    status: TaskStatus | None = None
    headers: dict = None


def retrieve_elasticsearch_tasks(detailed=True, human=True) -> list[Task]:
    response = es_client.tasks.list(detailed=detailed, human=human)
    tasks = []

    for node_id, node_info in response.get("nodes", {}).items():
        for task_id, task_data in node_info.get("tasks", {}).items():
            status = None
            if task_data.get("status"):
                status_data = task_data["status"]
                status = TaskStatus(
                    databases_count=status_data.get("databases_count", 0),
                    expired_databases=status_data.get("expired_databases", 0),
                    failed_downloads=status_data.get("failed_downloads", 0),
                    skipped_updates=status_data.get("skipped_updates", 0),
                    successful_downloads=status_data.get("successful_downloads", 0),
                    total_download_time=status_data.get("total_download_time", 0),
                    state=status_data.get("state", ""),
                )

            task = Task(
                id=task_id,
                action=task_data.get("action", ""),
                node=task_data.get("node", ""),
                cancellable=task_data.get("cancellable", False),
                cancelled=task_data.get("cancelled", False),
                type=task_data.get("type", ""),
                start_time=task_data.get("start_time", ""),
                running_time=task_data.get("running_time", ""),
                running_time_in_nanos=task_data.get("running_time_in_nanos", ""),
                description=task_data.get("description", ""),
                parent_task_id=task_data.get("parent_task_id"),
                status=status,
                headers=task_data.get("headers", {}),
            )
            tasks.append(task)

    return tasks
