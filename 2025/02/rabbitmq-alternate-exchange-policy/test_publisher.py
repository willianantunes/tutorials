import time
import unittest

from datetime import datetime

from faker import Faker

from publisher import publish_to_pika
from settings import TARGET_EXCHANGE
from settings import TARGET_ROUTING_KEY


class TestPublisher(unittest.TestCase):

    def setUp(self):
        default_seed = 745574
        Faker.seed(default_seed)
        self.faker = Faker()

    def test_publish_1_message(self):
        headers = {
            "correlation-id": self.faker.uuid4(),
        }
        body = {
            "username": self.faker.name(),
            "city": self.faker.city(),
            "created_at": datetime.now(),
        }
        publish_to_pika(body, headers, TARGET_EXCHANGE, TARGET_ROUTING_KEY)

    def test_publish_100_messages(self):
        for _ in range(100):
            headers = {
                "correlation-id": self.faker.uuid4(),
            }
            body = {
                "username": self.faker.name(),
                "city": self.faker.city(),
                "created_at": datetime.now(),
            }
            publish_to_pika(body, headers, TARGET_EXCHANGE, TARGET_ROUTING_KEY)

    def test_publish_messages_indefinitely_until_keyboard_interrupt(self):
        while True:
            headers = {
                "correlation-id": self.faker.uuid4(),
            }
            body = {
                "username": self.faker.name(),
                "city": self.faker.city(),
                "created_at": datetime.now(),
            }
            time.sleep(0.2)
            publish_to_pika(body, headers, TARGET_EXCHANGE, TARGET_ROUTING_KEY)
