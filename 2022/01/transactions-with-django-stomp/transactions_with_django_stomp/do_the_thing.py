import logging

from typing import Tuple

from django_stomp.builder import build_publisher
from django_stomp.services.consumer import Payload

logger = logging.getLogger(__name__)

xyz_destination = "/queue/xyz"
acme_destination = "/queue/acme"


def retrieve_events_to_be_dispatched(message: dict) -> Tuple[dict, dict]:
    event_to_xyz = {
        "who_did_the_thing_id": message["owner_id"],
        "title": message["title"],
    }
    event_to_acme = {
        "who_did_the_thing_id": message["owner_id"],
        "is_salt_addicted": message["salt_addicted"],
        "registered_at": message["registered_at"],
    }
    return event_to_xyz, event_to_acme


def build_news_and_dispatch_them(payload: Payload):
    """
    Payload body example:
    {
        "owner_id": "dcf6e27d-9331-406e-9bc2-ce973a761dfd",
        "title": "All right, so I'm back in high school, standing in the middle of the cafeteria",
        "salt_addicted": True,
        "registered_at": "2022-01-22T19:07:16.979"
    }
    """
    # Never do this in real production code. I did this just for the sake of the article.

    logger.debug("Creating messages to XYZ and ACME")
    message_to_xyz, message_to_acme = retrieve_events_to_be_dispatched(payload.body)

    logger.debug("Let's inform XYZ and ACME")
    publisher = build_publisher("news")
    with publisher.auto_open_close_connection(), publisher.do_inside_transaction():
        publisher.send(message_to_xyz, xyz_destination)
        publisher.send(message_to_acme, acme_destination)

    logger.debug("All the events have been sent")
    payload.ack()
