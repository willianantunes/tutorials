from django.contrib import admin
from django.urls import path

from cache_django.apps.core.api.v1 import views as standard_views_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/friends", standard_views_v1.ExampleView.as_view()),
]
