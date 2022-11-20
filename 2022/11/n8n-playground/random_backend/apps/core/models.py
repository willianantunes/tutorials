import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class AuditAction(StandardModelMixin):
    correlation_id = models.CharField(
        max_length=36, null=False, blank=False, editable=False, verbose_name="Correlation ID"
    )
    action = models.CharField(max_length=128, null=False, blank=False, editable=False, verbose_name="Action")
    metadata = models.JSONField(null=False, blank=False, editable=False, verbose_name="Metadata")

    def __str__(self):
        return f"{self.correlation_id} / {self.action}"
