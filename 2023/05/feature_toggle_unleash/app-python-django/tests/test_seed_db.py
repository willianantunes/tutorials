from io import StringIO

import pytest

from django.core.management import call_command

from app_python_django.apps.core.models import Category
from app_python_django.apps.core.models import Ingredient
from app_python_django.apps.core.models import Profile


@pytest.mark.django_db
def test_should_seed_db_without_super_user():
    out = StringIO()

    call_command("seed_db", stdout=out)

    assert out.getvalue() == "Creating 4 categories\nCreating 4 ingredients\nCreating profiles\n"
    assert Category.objects.all().count() == 4
    assert Ingredient.objects.all().count() == 4
    assert Profile.objects.all().count() == 20
