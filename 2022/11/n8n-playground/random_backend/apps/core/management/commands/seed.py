from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database"

    def add_arguments(self, parser):
        parser.add_argument("--create-super-user", action="store_true")
        parser.add_argument("-u", type=str, default="admin")
        parser.add_argument("-p", type=str, default="admin")

    def handle(self, *args, **options):
        self.create_super_user = options["create_super_user"]
        self.admin_username = options["u"].strip()
        self.admin_password = options["p"].strip()

        if self.create_super_user:
            if get_user_model().objects.filter(username=self.admin_username).count() == 0:
                self.stdout.write(f"Creating ADMIN username {self.admin_username}")
                _create_super_user(self.admin_username, self.admin_password)
            else:
                self.stdout.write("Super user already exists")


def _create_super_user(username, password):
    return get_user_model().objects.create_superuser(username, None, password)
