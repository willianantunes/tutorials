import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class Profile(StandardModelMixin):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    mail = models.EmailField(null=False, blank=False)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Category(StandardModelMixin):
    name = models.CharField(max_length=100, unique=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    distributed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(StandardModelMixin):
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="ingredients", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
