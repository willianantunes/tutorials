from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from database_isolation.apps.core.models import Account


class SeedTest(TestCase):
    def test_should_seed(self):
        out = StringIO()
        with self.assertNumQueries(13):
            call_command("seed", stdout=out)

        self.assertIsNotNone(out.getvalue())
        self.assertEquals(1, User.objects.filter(username="admin").count())
        self.assertEquals(10, Account.objects.count())
