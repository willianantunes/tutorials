from django.contrib import admin

from random_backend.apps.core.models import AuditAction
from random_backend.support.django_helpers import CustomModelAdminMixin


@admin.register(AuditAction)
class AuditActionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["correlation_id"]
