from django.urls import path

from product_a import settings
from product_a.apps.core import views
from product_a.apps.core.api import api_views
from product_a.apps.core.api.v1 import api_views as api_views_v1
from product_a.apps.core.services.oidc_provider import OIDCProvider

OIDCProvider.configure_class_properties(
    settings.AWS_COGNITO_PROVIDED_DOMAIN,
    settings.AWS_COGNITO_APP_CLIENT_ID,
    settings.AWS_COGNITO_APP_CLIENT_SECRET,
    settings.AWS_COGNITO_APP_SCOPES,
)
OIDCProvider.configure_oidc_configuration_document()

urlpatterns = [
    # Pages
    path("", views.index, name="index"),
    path("login-auth-code", views.initiate_login_flow, name="login-auth-code-flow"),
    # http://localhost:8000/logout
    path("logout", views.logout, name="logout"),
    # APIs
    path("health-check", api_views.health_check, name="health-check"),
    # http://localhost:8000/api/v1/response-oidc
    path("api/v1/response-oidc", api_views_v1.handle_response_oidc, name="v1/response-oidc"),
    path("api/v1/user-info", api_views_v1.retrieve_user_info, name="v1/user-info"),
]
