from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from database_isolation.apps.core.models import Account


class Command(BaseCommand):
    help = "Seed the database"

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=0, help="Seed provided to Faker")

    def handle(self, *args, **options):
        self.seed = options["seed"]

        if get_user_model().objects.filter(username="admin").count() == 0:
            self.stdout.write("Creating ADMIN username admin")
            get_user_model().objects.create_superuser("admin", None, "admin")
        else:
            self.stdout.write("Super user already exists")

        if Account.objects.count() == 0:
            self.stdout.write("Generating sample data...")
            Faker.seed(self.seed)
            faker = Faker()
            initial_balance = Decimal("1000.0")
            for _ in range(10):
                Account.objects.create(username=faker.simple_profile()["username"], balance=initial_balance)
                initial_balance += Decimal("1000.0")
