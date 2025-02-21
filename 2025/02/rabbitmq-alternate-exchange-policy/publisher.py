import json

import pika

from settings import CustomJSONEncoder
from settings import broker_parameters


def publish_to_pika(body, headers, exchange, routing_key):
    with pika.BlockingConnection(broker_parameters) as connection:
        with connection.channel() as channel:
            properties = pika.BasicProperties(headers=headers, correlation_id=headers.get("correlation_id"))
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(body, cls=CustomJSONEncoder),
                properties=properties,
            )
