import os

from es_watcher.support import eval_env_as_boolean
from es_watcher.support import getenv_or_raise_exception

ELASTICSEARCH_HOST = getenv_or_raise_exception("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = int(getenv_or_raise_exception("ELASTICSEARCH_PORT"))
ELASTICSEARCH_USE_SSL = eval_env_as_boolean("ELASTICSEARCH_USE_SSL", False)
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
