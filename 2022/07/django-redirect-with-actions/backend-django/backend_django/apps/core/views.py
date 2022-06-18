import logging
import uuid

from datetime import timedelta

import jwt

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from backend_django import settings
from backend_django.apps.core.services.oidc_provider import OIDCProvider
from backend_django.settings import AUTH0_CONTINUE_ENDPOINT
from backend_django.support.http_utils import build_url_with_query_strings

logger = logging.getLogger(__name__)


def index(request):
    logged_user = request.session.get("user")
    context = {}

    if logged_user:
        logout_request_path = _build_uri(request, "logout")
        final_logout_uri = OIDCProvider.build_logout_url(logout_request_path)
        # Enriching output
        context["logout_uri"] = final_logout_uri
        context = {
            "logout_uri": final_logout_uri,
        }

    return render(request, "core/pages/home.html", context)


def logout(request):
    request.session.flush()
    redirect_uri = _build_uri(request, "index")
    return redirect(redirect_uri)


def terms(request):
    if request.method == "POST":
        state = request.session["state"]
        payload_from_auth0 = request.session["payload"]
        payload = {
            "iat": timezone.now(),
            "sub": payload_from_auth0["sub"],
            "iss": settings.AUTH0_DOMAIN,
            "exp": timezone.now() + timedelta(seconds=30),
            "state": state,
            "other": {
                "termsAcceptanceHistory": [
                    {
                        "version": 1,
                        "registeredAt": timezone.now().isoformat(),
                    }
                ]
            },
        }
        jwt_to_be_set = jwt.encode(payload, settings.AUTH0_JWT_SECRET, algorithm="HS256")
        # Sample: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTU1MDc2MDYsInN1YiI6ImF1dGgwfDYyYWNlY2M3M2FlZWQyMDY1ZDVhZmYxYSIsImlzcyI6ImFudHVuZXMudXMuYXV0aDAuY29tIiwiZXhwIjoxNjU1NTA3NjM2LCJzdGF0ZSI6ImhLRm8yU0JxVTBaemJsTktNbmhHUzBOaFVtazRTWE4zWVU1MU5YTktiRVJzV1VreWFLRnVxSEpsWkdseVpXTjBvM1JwWk5rZ1ltVTBUMWh4VkRGM2RsRTFNM1pwZDJocVExZGFZelp0Y0dWNmFIVmpUbFdqWTJsazJTQkpTMGhQUVc1Vlp6SlVWVUZrT1RoTVVuZE1WbE54V2pWU2RFRTFZM2RNWWciLCJvdGhlciI6eyJ0ZXJtc0FjY2VwdGFuY2VIaXN0b3J5IjpbeyJ2ZXJzaW9uIjoxLCJyZWdpc3RlcmVkQXQiOiIyMDIyLTA2LTE3VDIzOjEzOjI2LjcwOTQ3MyswMDowMCJ9XX19.r2_bn7DYjMY4K2j-pSXvBd05w0dAkycUbBZPjG2Gu5Q
        logger.debug("Created JWT: %s", jwt_to_be_set)
        params = {
            "state": state,
            "data": jwt_to_be_set,
        }
        return redirect(build_url_with_query_strings(AUTH0_CONTINUE_ENDPOINT, params))

    return render(request, "core/pages/terms.html")


def initiate_login_flow(request):
    redirect_uri = _build_uri(request, "v1/response-oidc")
    logger.info("Building flow session details...")
    some_state = str(uuid.uuid4())
    # So we can retrieve it later
    request.session["authorization-code"] = {"state": some_state, "redirect_uri": redirect_uri}
    # Then we redirect the user
    auth_uri = OIDCProvider.build_authorization_url(redirect_uri, some_state)
    return redirect(auth_uri)


def _build_uri(request, view_name):
    location_redirect = reverse(view_name)
    return request.build_absolute_uri(location_redirect)
