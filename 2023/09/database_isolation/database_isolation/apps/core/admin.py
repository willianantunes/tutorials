from django.contrib import admin

from database_isolation.apps.core.models import Account
from database_isolation.apps.core.models import Transfer
from database_isolation.support.django_helpers import CustomModelAdminMixin


@admin.register(Account)
class AccountAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Transfer)
class TransferAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
