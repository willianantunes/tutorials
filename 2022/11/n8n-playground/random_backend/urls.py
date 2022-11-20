from django.contrib import admin
from django.urls import path

from random_backend.apps.core.api.v1 import views as views_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/audit", views_v1.AuditAPIView.as_view(), name="v1-audit"),
    path("api/v1/queues", views_v1.FakeBrokerQueueDetailsAPIView.as_view(), name="v1-queues"),
]
