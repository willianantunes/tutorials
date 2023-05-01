from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from app_python_django.apps.core import views
from app_python_django.apps.core.api.v1 import views as v1_views

router = routers.DefaultRouter()
router.register("profile", v1_views.ProfileViewSet, basename="Profile")
router.register("category", v1_views.CategoryViewSet, basename="Category")
router.register("ingredient", v1_views.IngredientViewSet, basename="Ingredient")

urlpatterns = [
    # Pages
    path("admin/", admin.site.urls, name="admin"),
    path("", views.index, name="index"),
    # APIs forms
    path("forms/v1/profiles", views.manage_profiles, name="forms_v1_manage_profiles"),
    # APIs
    path("api/v1/", include(router.urls)),
]
