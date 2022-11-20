from rest_framework import serializers


class AuditSerializer(serializers.Serializer):
    correlation_id = serializers.UUIDField(required=True)
    action = serializers.CharField(max_length=128, required=True)
    metadata = serializers.JSONField(required=False)
