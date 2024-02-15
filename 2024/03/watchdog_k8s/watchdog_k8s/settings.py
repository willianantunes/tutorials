import os

from logging import Formatter

from pythonjsonlogger.jsonlogger import JsonFormatter

from watchdog_k8s.support import ContextFilter
from watchdog_k8s.support import getenv_or_raise_exception

CERTIFICATES_TO_BE_CHECKED = getenv_or_raise_exception("CERTIFICATES_TO_BE_CHECKED")

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
        "watchdog_k8s": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
