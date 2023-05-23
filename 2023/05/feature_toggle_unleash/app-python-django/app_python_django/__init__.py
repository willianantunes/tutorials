import signal

import gevent

from UnleashClient import UnleashClient


def handle_shutdown(*args):
    from app_python_django.apps.core.providers.feature_management import retrieve_client

    client = retrieve_client()

    gevent.spawn(perform_destroy, client)


def perform_destroy(client: UnleashClient):
    try:
        client.destroy()
    except FileNotFoundError:
        pass


signal.signal(signal.SIGTERM, handle_shutdown)
