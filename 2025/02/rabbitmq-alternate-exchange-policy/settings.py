import datetime
import decimal
import json
import os
import uuid

from logging import Formatter

import pika

BROKER_HOST = os.getenv("BROKER_HOST")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv("BROKER_PASSWORD")
BROKER_VHOST = os.getenv("BROKER_VHOST")

TARGET_EXCHANGE = os.getenv("TARGET_EXCHANGE")
TARGET_ROUTING_KEY = os.getenv("TARGET_ROUTING_KEY")

CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE")

credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
broker_parameters = pika.ConnectionParameters(BROKER_HOST, BROKER_PORT, BROKER_VHOST, credentials)


class CustomJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and UUIDs.
    https://github.com/django/django/blob/65c46d6932c0956d2988d13ec3d9ab3ef9d96d61/django/core/serializers/json.py#L85
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r.removesuffix("+00:00") + "Z"
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)
        else:
            return super().default(o)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": Formatter,
            "format": "%(asctime)s - level=%(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "pika": {
            "level": os.getenv("PIKA_LOG_LEVEL", "WARN"),
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
