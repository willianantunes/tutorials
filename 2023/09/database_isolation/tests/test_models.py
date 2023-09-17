from decimal import Decimal

from django.test import TestCase

from database_isolation.apps.core.models import Account
from database_isolation.apps.core.models import Transfer


class ModelTest(TestCase):
    def test_models(self):
        with self.assertNumQueries(3):
            account_a = Account.objects.create(username="wig", balance=Decimal("100.0"))
            account_b = Account.objects.create(username="midna", balance=Decimal("100.0"))
            Transfer.objects.create(from_account=account_b, to_account=account_a, amount=Decimal("10.0"))
