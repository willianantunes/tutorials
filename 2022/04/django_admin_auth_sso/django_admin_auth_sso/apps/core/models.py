import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Tweet(StandardModelMixin):
    screen_name = models.CharField(max_length=16, null=False, blank=False)
    when_tweet_was_created = models.DateTimeField(null=False, blank=False)
    tweet_id = models.PositiveBigIntegerField(null=False, blank=False)

    def __str__(self):
        return self.tweet_id


class Language(StandardModelMixin):
    language_tag = models.CharField(max_length=20, null=False, blank=False, unique=True)
    language = models.CharField(max_length=50, null=True, blank=True, verbose_name="Language")
    accent_or_dialect = models.CharField(max_length=50, null=True, blank=True, verbose_name="Accent/Dialect")
    family = models.CharField(max_length=50, null=True, blank=True, verbose_name="Family")

    def __str__(self):
        return self.language_tag
