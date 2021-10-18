import logging

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from product_a.apps.core.api.api_exception import ContractNotRespectedException
from product_a.apps.core.services.oidc_provider import OIDCProvider

logger = logging.getLogger(__name__)


@api_view(["GET"])
def handle_response_oidc(request: Request) -> Response:
    current_referer = request.headers.get("referer")
    logger.info("Handling callback! It came from %s", current_referer)

    auth_flow_details = request.session.pop("authorization-code", {})
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state or not auth_flow_details:
        raise ContractNotRespectedException
    if auth_flow_details["state"] != state:
        raise ContractNotRespectedException

    logger.info("We have everything to contact token endpoint!")
    tokens, claims = OIDCProvider.acquire_token_by_auth_code_flow(code, auth_flow_details["redirect_uri"])

    request.session["user"] = claims
    request.session["tokens"] = tokens
    location_index = reverse("index")

    return redirect(location_index)


@api_view(["GET"])
def retrieve_user_info(request: Request) -> Response:
    tokens = request.session.get("tokens")
    result = OIDCProvider.get_user_info(tokens["access_token"])
    return Response(data=result)
