from django.contrib import admin
from django.urls import path

from apiview_django_rest_framework.apps.core.api.v1 import standard_views as standard_views_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/attributes", standard_views_v1.UserManagementAttributesAPIView.as_view()),
]
