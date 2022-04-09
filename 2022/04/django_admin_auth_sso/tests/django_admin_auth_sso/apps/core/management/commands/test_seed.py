from io import StringIO

import pytest

from django.contrib.auth.models import Group
from django.core.management import call_command


@pytest.mark.django_db
class TestUserManagement:
    def test_should_create_groups_when_no_group_exist(self):
        out = StringIO()
        call_command("seed", stdout=out)

        assert out.getvalue() == "Groups have been created!\n"
        assert Group.objects.count() == 4
        assert Group.objects.get(name="viewer").permissions.count() == 2
        assert Group.objects.get(name="business").permissions.count() == 4
        assert Group.objects.get(name="support").permissions.count() == 8
        assert Group.objects.get(name="developer").permissions.count() == 12
