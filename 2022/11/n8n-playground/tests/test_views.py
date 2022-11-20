import base64

from uuid import uuid4

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from random_backend.apps.core.models import AuditAction


class TestViews(APITestCase):
    def test_should_save_audit_item(self):
        # Arrange
        data = {
            "correlation_id": str(uuid4()),
            "action": "CHEW",
            "metadata": {"key": "value", "nested": {"json": True}},
        }
        url = reverse("v1-audit")
        # Act
        response = self.client.post(url, data, format="json")
        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, AuditAction.objects.count())
        saved_object = AuditAction.objects.values(*list(data.keys())).first()
        self.assertEqual(data, saved_object)

    def test_should_generate_queues_details(self):
        # Arrange
        query_strings = {"fakerSeed": 0}
        url = reverse("v1-queues")
        username, password = "jafar", "iago"
        get_user_model().objects.create_superuser(username, None, password)
        headers = {"HTTP_AUTHORIZATION": f"Basic {base64.b64encode(f'{username}:{password}'.encode()).decode()}"}
        # Act
        response = self.client.get(url, query_strings, format="json", **headers)
        # Assert
        self.assertEqual(200, response.status_code)
        expected_body = [
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.high-be-what-destination"},
                "name": "high-be-what",
                "node": "travis-garcia@salt-mustache-dog-01",
                "consumers": 3,
                "messages": 31339,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.think-however-destination"},
                "name": "think-however",
                "node": "jeffrey-bailey@salt-mustache-dog-01",
                "consumers": 35,
                "messages": 76759,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.generation-cup-destination"},
                "name": "generation-cup",
                "node": "roberto-mora@salt-mustache-dog-01",
                "consumers": 33,
                "messages": 40983,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.scientist-than-destination"},
                "name": "scientist-than",
                "node": "caitlin-anderson@salt-mustache-dog-01",
                "consumers": 6,
                "messages": 26854,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.training-beautiful-destination"},
                "name": "training-beautiful",
                "node": "rebecca-henderson@salt-mustache-dog-01",
                "consumers": 91,
                "messages": 27583,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.size-may-red-maybe-destination"},
                "name": "size-may-red-maybe",
                "node": "denise-gates@salt-mustache-dog-01",
                "consumers": 55,
                "messages": 59170,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.even-majority-destination"},
                "name": "even-majority",
                "node": "michael-rivera@salt-mustache-dog-01",
                "consumers": 61,
                "messages": 37606,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.simply-best-voice-destination"},
                "name": "simply-best-voice",
                "node": "robert-grimes@salt-mustache-dog-01",
                "consumers": 63,
                "messages": 80624,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.fast-drop-however-destination"},
                "name": "fast-drop-however",
                "node": "elizabeth-williams@salt-mustache-dog-01",
                "consumers": 57,
                "messages": 43553,
                "state": "running",
                "vhost": "production",
            },
            {
                "arguments": {"x-dead-letter-routing-key": "DLQ.leader-daughter-be-destination"},
                "name": "leader-daughter-be",
                "node": "timothy-smith@salt-mustache-dog-01",
                "consumers": 35,
                "messages": 95543,
                "state": "running",
                "vhost": "production",
            },
        ]
        self.assertEqual(expected_body, response.data)
