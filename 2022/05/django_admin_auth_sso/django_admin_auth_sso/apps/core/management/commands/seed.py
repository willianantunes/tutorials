from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q


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

        should_configure_groups = not Group.objects.exists()
        if should_configure_groups:
            permissions_related_to_core_project = Permission.objects.filter(content_type__app_label="core")
            # Permissions for SUPPORT, VIEWER and BUSINESS
            support_permissions = permissions_related_to_core_project
            viewer_permissions = permissions_related_to_core_project.filter(name__contains="view")
            name_contains_delete_or_add = Q(name__contains="delete") | Q(name__contains="add")
            business_permissions = permissions_related_to_core_project.exclude(name_contains_delete_or_add)
            # Permissions for DEVELOPER
            permissions_related_to_user_and_group = Permission.objects.filter(content_type__app_label="auth")
            permissions_related_to_admin = Permission.objects.filter(content_type__app_label="admin")
            can_only_view_user_and_group = permissions_related_to_user_and_group.filter(name__contains="view")
            can_only_view_admin = permissions_related_to_admin.filter(name__contains="view")
            developer_permissions = can_only_view_user_and_group | support_permissions | can_only_view_admin
            # Group creation
            with transaction.atomic():
                viewer, support, business, developer = (
                    Group.objects.create(name="viewer"),
                    Group.objects.create(name="support"),
                    Group.objects.create(name="business"),
                    Group.objects.create(name="developer"),
                )
                viewer.permissions.set(viewer_permissions)
                viewer.save()
                support.permissions.set(support_permissions)
                support.save()
                business.permissions.set(business_permissions)
                business.save()
                developer.permissions.set(developer_permissions)
                developer.save()
            self.stdout.write("Groups have been created!")


def _create_super_user(username, password):
    return get_user_model().objects.create_superuser(username, None, password)
