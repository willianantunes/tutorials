import json

from dataclasses import dataclass
from uuid import uuid4

from django_stomp.builder import build_listener
from django_stomp.builder import build_publisher


@dataclass(frozen=True)
class Message:
    headers: dict
    body: dict


def publish_to_destination(destination, body, headers=None, persistent=True, attempts=1):
    with build_publisher(f"random-publisher-{uuid4()}").auto_open_close_connection() as publisher:
        publisher.send(body=body, queue=destination, headers=headers, persistent=persistent, attempt=attempts)


def get_latest_message_from_destination_using_test_listener(destination) -> Message:
    """
    Gets the latest message using the test listener utility. It does not ack the message on the destination queue.

    [!]: It makes a test hang forever if a message never arrives at the destination.
    """
    evaluation_consumer = build_listener(destination, is_testing=True)
    test_listener = evaluation_consumer._test_listener
    evaluation_consumer.start(wait_forever=False)

    # may wait forever if the msg never arrives
    test_listener.wait_for_message()
    received_message = test_listener.get_latest_message()

    headers = received_message[0]
    body = json.loads(received_message[1])

    return Message(headers, body)
