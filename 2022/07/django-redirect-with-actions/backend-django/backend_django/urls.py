from django.contrib import admin
from django.urls import path

from backend_django.apps.core import views
from backend_django.apps.core.api.v1 import api_views as api_views_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    # Pages
    path("", views.index, name="index"),
    path("login-auth-code", views.initiate_login_flow, name="login-auth-code-flow"),
    path("logout", views.logout, name="logout"),
    path("terms", views.terms, name="terms"),
    # APIs
    path("api/v1/response-oidc", api_views_v1.handle_response_oidc, name="v1/response-oidc"),
    path("api/v1/user-info", api_views_v1.retrieve_user_info, name="v1/user-info"),
    path("api/v1/terms", api_views_v1.handle_terms, name="v1/terms"),
]
