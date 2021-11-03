import logging
import uuid

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from product_b.apps.core.services.oidc_provider import OIDCProvider

logger = logging.getLogger(__name__)


def index(request):
    logged_user = request.session.get("user")
    context = {}

    if logged_user:
        logout_request_path = _build_uri(request, "logout")
        final_logout_uri = OIDCProvider.build_logout_url(logout_request_path)
        context["logout_uri"] = final_logout_uri

    return render(request, "core/pages/home.html", context)


def logout(request):
    request.session.flush()
    redirect_uri = _build_uri(request, "index")
    return redirect(redirect_uri)


def initiate_login_flow(request):
    redirect_uri = _build_uri(request, "v1/response-oidc")
    logger.info("Built redirect URI: %s", redirect_uri)
    logger.info("Building flow session details...")
    some_state = str(uuid.uuid4())
    # So we can retrieve it later
    request.session["authorization-code"] = {"state": some_state, "redirect_uri": redirect_uri}
    # Then we redirect the user
    auth_uri = OIDCProvider.build_authorization_url(redirect_uri, some_state)
    return redirect(auth_uri)


def _build_uri(request, view_name):
    location_redirect = reverse(view_name)
    uri = request.build_absolute_uri(location_redirect)
    return _apply_gambiarra(uri)


def _apply_gambiarra(uri):
    # Know more what I had to do this here: https://www.willianantunes.com/blog/2021/11/sso-with-cognito-through-the-authorization-code-grant-type/
    uri = uri.replace("product-a", "localhost")
    return uri.replace("product-b", "localhost")
