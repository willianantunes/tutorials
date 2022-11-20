import logging

from django.utils.text import slugify
from faker import Faker
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from random_backend.apps.core.api.v1.serializers import AuditSerializer
from random_backend.apps.core.models import AuditAction

_logger = logging.getLogger(__name__)


class AuditAPIView(APIView):
    def post(self, request):
        deserializer = AuditSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        audit_attributes = deserializer.validated_data

        _logger.debug("An incoming request made with correlation %s", audit_attributes["correlation_id"])
        AuditAction(**audit_attributes).save()

        return Response(status=status.HTTP_200_OK)


class FakeBrokerQueueDetailsAPIView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        queues_number = int(request.query_params.get("numberOfQueuesToGenerate", 10))
        faker_seed = request.query_params.get("fakerSeed", None)
        _logger.debug(f"Queues number and faker seed: {queues_number} / {faker_seed}")
        faker = Faker()
        faker.seed_instance(faker_seed)

        _logger.debug("Building fake queues details...")
        queues = []
        for _ in range(0, queues_number):
            name = faker.slug()
            queue_name = f"{name}-destination"
            dead_letter_queue_name = f"DLQ.{queue_name}"
            queue_details = {
                "arguments": {
                    "x-dead-letter-routing-key": dead_letter_queue_name,
                },
                "name": name,
                "node": f"{slugify(faker.name())}@salt-mustache-dog-01",
                "consumers": faker.random_int(min=0, max=100),
                "messages": faker.random_int(min=0, max=100_000),
                "state": "running",
                "vhost": "production",
            }
            queues.append(queue_details)

        return Response(queues, status=status.HTTP_200_OK)
