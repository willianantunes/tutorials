import json
import logging.config

import pika

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from pika.spec import BasicProperties

import settings

from settings import CONSUMER_QUEUE
from settings import broker_parameters


def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    try:
        data = json.loads(body)
        print("Body", data)
        print("Properties", properties)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error processing message", e)
        ch.basic_nack(delivery_tag=method.delivery_tag)


logging.config.dictConfig(settings.LOGGING)

while True:
    try:
        with pika.BlockingConnection(broker_parameters) as connection:
            with connection.channel() as channel:
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=CONSUMER_QUEUE, on_message_callback=callback, auto_ack=False)
                try:
                    channel.start_consuming()
                except KeyboardInterrupt:
                    channel.stop_consuming()
                channel.close()
                break
    except pika.exceptions.ConnectionClosedByBroker:
        print("Do not recover if connection was closed by broker")
        break
    except pika.exceptions.AMQPChannelError:
        print("Do not recover on channel errors")
        break
    except pika.exceptions.AMQPConnectionError:
        print("Recover on all other connection errors")
        continue
