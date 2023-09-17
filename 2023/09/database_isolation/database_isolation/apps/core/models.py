import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Account(StandardModelMixin):
    username = models.CharField(null=False, max_length=128, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=4)


class Transfer(StandardModelMixin):
    from_account = models.ForeignKey(Account, related_name="transfer_from_account", on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name="transfer_to_account", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_transfer_between_accounts",
                fields=["from_account", "to_account"],
            ),
        ]
