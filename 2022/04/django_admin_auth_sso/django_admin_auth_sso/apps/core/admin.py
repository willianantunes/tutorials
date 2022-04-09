from django.contrib import admin
from django.contrib.admin.models import LogEntry

from django_admin_auth_sso.apps.core.models import Language
from django_admin_auth_sso.apps.core.models import Tweet
from django_admin_auth_sso.support.django_helpers import CustomModelAdminMixin


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"
    list_filter = [
        "user",
        "content_type",
        "action_flag",
    ]
    search_fields = [
        "object_repr",
        "change_message",
    ]
    list_display = [
        "action_time",
        "user",
        "content_type",
        "action_flag",
    ]


@admin.register(Tweet)
class TweetAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
