from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

from app_python_django.apps.core.models import Category
from app_python_django.apps.core.models import Ingredient
from app_python_django.apps.core.models import Profile


class Command(BaseCommand):
    help = "Seed database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--create-super-user", action="store_true", dest="create_super_user", help="Create default super user"
        )
        parser.add_argument(
            "-u", dest="admin_username", type=str, default="admin", help="Super user username. Defaults to: admin "
        )
        parser.add_argument(
            "-p",
            dest="admin_password",
            type=str,
            default="admin",
            help="Super user password. Defaults to: admin",
        )
        parser.add_argument(
            "--hide-super-user-password", action="store_true", dest="hide_password", help="Hide admin password output"
        )
        parser.add_argument(
            "--only-super-user", action="store_true", dest="only_super_user", help="Try to create super user only"
        )
        parser.add_argument("--seed", type=int, default=0, help="Seed provided to Faker")

    def handle(self, *args, **options):
        self.create_super_user = options["create_super_user"]
        self.admin_username = options["admin_username"].strip()
        self.admin_password = options["admin_password"].strip()
        self.hide_password = options["hide_password"]
        self.only_super_user = options["only_super_user"]
        self.seed = options["seed"]

        if self.create_super_user == True:
            user_model = get_user_model()
            if user_model.objects.filter(username=self.admin_username).count() == 0:
                log_output = f"Creating ADMIN username {self.admin_username}"
                if not self.hide_password:
                    self.stdout.write(f"{log_output} and password {self.admin_password}")
                else:
                    self.stdout.write(log_output)
                get_user_model().objects.create_superuser(self.admin_username, None, self.admin_password)
            else:
                self.stdout.write("Super user already exists")

        if not self.only_super_user:
            Faker.seed(self.seed)
            faker = Faker()

            if Category.objects.all().count() == 0:
                self.stdout.write("Creating 4 categories")
                category_1 = Category.objects.create(name="Salt")
                category_2 = Category.objects.create(name="Fat")
                Category.objects.create(name="Acid")
                Category.objects.create(name="Heat")
                self.stdout.write("Creating 4 ingredients")
                Ingredient.objects.create(name="Prates", category=category_1)
                Ingredient.objects.create(name="Baltazar", category=category_2)
                Ingredient.objects.create(name="Cumin", category=category_1)
                Ingredient.objects.create(name="Chive", category=category_2)
                self.stdout.write("Creating profiles")
                [Profile.objects.create(**faker.simple_profile()) for _ in range(20)]
            else:
                self.stdout.write("There are data registered already")
