import logging
import os

from django.conf import settings


def pytest_configure():
    logging_configuration = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "()": logging.Formatter,
                "format": "%(levelname)-8s [%(asctime)s] [%(threadName)s] %(name)s: %(message)s",
            }
        },
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "standard"}},
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["console"]},
            "django_stomp": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
            "stomp.py": {"level": "INFO", "handlers": ["console"], "propagate": False},
        },
    }

    settings.configure(
        INSTALLED_APPS=["django_stomp"],
        STOMP_SERVER_HOST=os.getenv("STOMP_SERVER_HOST", "localhost"),
        STOMP_SERVER_PORT="61613",
        STOMP_USE_SSL=False,
        STOMP_PROCESS_MSG_ON_BACKGROUND=False,
        # Enable the line below if you want to look at the log messages.
        # You'll see duplicated lines. If you change "propagate" to True, then caplog won't work anymore.
        # LOGGING=logging_configuration,
    )
