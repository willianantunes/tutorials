from django.http import Http404
from rest_framework import filters
from rest_framework import viewsets

from app_python_django.apps.core.api.v1.serializers import CategorySerializer
from app_python_django.apps.core.api.v1.serializers import IngredientSerializer
from app_python_django.apps.core.api.v1.serializers import ProfileSerializer
from app_python_django.apps.core.models import Category
from app_python_django.apps.core.models import Ingredient
from app_python_django.apps.core.models import Profile
from app_python_django.apps.core.providers.feature_management import client


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "sex", "mail"]

    def initial(self, request, *args, **kwargs):
        """
        https://www.django-rest-framework.org/api-guide/views/#initialself-request-args-kwargs
        """
        enable_profile_api = client.is_enabled("ENABLE_PROFILE_API")
        if not enable_profile_api:
            raise Http404("Not available")
        super().initial(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
