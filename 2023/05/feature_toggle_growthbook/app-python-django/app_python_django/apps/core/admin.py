from django.contrib import admin

from app_python_django.apps.core.models import Profile
from app_python_django.apps.core.providers.feature_management import retrieve_client
from app_python_django.support.django_helpers import CustomModelAdminMixin


class CustomProfileAdminMixin:
    def get_queryset(self, request):
        client = retrieve_client()
        enable_profile_admin = client.is_on("ENABLE_PROFILE_ADMIN".lower())
        if not enable_profile_admin:
            return self.model.objects.none()
        return super().get_queryset(request)


@admin.register(Profile)
class ProfileAdmin(CustomModelAdminMixin, CustomProfileAdminMixin, admin.ModelAdmin):
    search_fields = ["mail"]
    list_filter = ["created_at", "updated_at", "sex"]
