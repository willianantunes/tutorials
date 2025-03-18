import os

from logging import Formatter

from pythonjsonlogger.jsonlogger import JsonFormatter

from index_lifecycle_rollover.support import ContextFilter
from index_lifecycle_rollover.support import eval_env_as_boolean
from index_lifecycle_rollover.support import getenv_or_raise_exception

ELASTICSEARCH_HOSTS = getenv_or_raise_exception("ELASTICSEARCH_HOSTS")
ELASTICSEARCH_PORT = int(getenv_or_raise_exception("ELASTICSEARCH_PORT"))
ELASTICSEARCH_USE_SSL = eval_env_as_boolean("ELASTICSEARCH_USE_SSL", True)
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"correlation_id": {"()": ContextFilter}},
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(message)s %(correlation_id)s %(name)s %(levelname)s %(lineno)s %(pathname)s %(asctime)s",
        },
        "development": {
            "()": Formatter,
            "format": "%(asctime)s - correlation-id=%(correlation_id)s level=%(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
            "filters": ["correlation_id"],
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "index_lifecycle_rollover": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        "elasticsearch": {
            "level": os.getenv("ELASTICSEARCH_LOG_LEVEL", "WARN"),
            "handlers": ["console"],
            "propagate": False,
        },
        "elastic_transport": {
            "level": os.getenv("ELASTIC_TRANSPORT_LOG_LEVEL", "WARN"),
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
