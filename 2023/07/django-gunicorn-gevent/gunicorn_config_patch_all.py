import psycogreen.gevent

# https://github.com/psycopg/psycogreen/blob/39a258cb4040b88b60a7600f6942e651a28db9a7/README.rst#module-psycogreengevent
psycogreen.gevent.patch_psycopg()

import os

print("Patch all!")

# https://docs.gunicorn.org/en/stable/settings.html
bind = os.environ.get("DJANGO_BIND_ADDRESS", "0.0.0.0") + ":" + os.environ.get("DJANGO_BIND_PORT", "8000")
backlog = int(os.getenv("GUNICORN_BACKLOG", "2048"))
workers = int(os.getenv("GUNICORN_WORKERS", "1"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gevent")
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", "50"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "300"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "2"))
threads = int(os.getenv("GUNICORN_THREADS", "1"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "0"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "10"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))

errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
accesslog = "-"
access_log_format = (
    f'{{"message": "%(r)s", "status": %(s)s, '
    f'"length": "%(b)s", "referer": "%(f)s", "user_agent": "%(a)s", '
    f'"time": %(L)s, "date": "%(t)s"}}'
)
