import logging

from typing import TypedDict

import jwt

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from backend_django import settings
from backend_django.apps.core.api.api_exception import ContractNotRespectedException
from backend_django.apps.core.services.oidc_provider import OIDCProvider

_logger = logging.getLogger(__name__)


@api_view(["GET"])
def handle_response_oidc(request: Request) -> Response:
    current_referer = request.headers.get("referer")
    _logger.info("Handling callback! It came from %s", current_referer)

    auth_flow_details: dict = request.session.pop("authorization-code", {})
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state or not auth_flow_details:
        raise ContractNotRespectedException
    if auth_flow_details["state"] != state:
        raise ContractNotRespectedException

    _logger.info("We have everything to contact token endpoint!")
    tokens, claims = OIDCProvider.acquire_token_by_auth_code_flow(code, auth_flow_details["redirect_uri"])

    request.session["user"] = claims
    request.session["tokens"] = tokens
    location_index = reverse("index")

    return redirect(location_index)


@api_view(["GET"])
def retrieve_user_info(request: Request) -> Response:
    tokens = request.session.get("tokens")
    access_token = tokens["access_token"]
    _logger.info("Using the following access token: %s", access_token)
    result = OIDCProvider.get_user_info(access_token)

    return Response(data=result)


class PayloadAuth0(TypedDict):
    id: str
    client_id: str
    whenTheEventStarted: str
    app_metadata: dict


@api_view(["GET"])
def handle_terms(request: Request) -> Response:
    _logger.debug("Received params: %s", request.query_params)

    # Sample input from Auth0
    # <QueryDict: {'session_token': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NTU0OTk5NzYsImlzcyI6ImFudHVuZXMudXMuYXV0aDAuY29tIiwic3ViIjoiYXV0aDB8NjJhY2VjYzczYWVlZDIwNjVkNWFmZjFhIiwiZXhwIjoxNjU1NTAwNTc2LCJpcCI6IjI4MDQ6MTRkOjFhODc6YzhkZTo4NzkzOmIyMTA6NjI5NzoyM2NiIiwiaWQiOiJhdXRoMHw2MmFjZWNjNzNhZWVkMjA2NWQ1YWZmMWEiLCJhcHBfbWV0YWRhdGEiOnt9LCJjbGllbnRfaWQiOiJXS1RzczR6NlExS1gzTEVCMk9nU1NIbTFjSFRTSkRucyIsIndoZW5UaGVFdmVudFN0YXJ0ZWQiOiIyMDIyLTA2LTE3VDIxOjA2OjE1LjY4NloifQ.-lGF10DdIeVra4jMmRRIR9_88-GxXwDU6o3wzhQscb0'], 'state': ['hKFo2SA4SHdZT2FlYmhHdmFIYTliX194TVNJUVhvclJHT29TLaFuqHJlZGlyZWN0o3RpZNkgSjFHTHpfZkxUN2RlUWVSYmhKMWNkeDRJWEsyV09UOEKjY2lk2SBXS1RzczR6NlExS1gzTEVCMk9nU1NIbTFjSFRTSkRucw']}>

    _logger.debug("Extracting required params")
    session_token = request.query_params.get("session_token")
    state = request.query_params.get("state")

    _logger.debug("Decrypting the session token")
    payload: PayloadAuth0 = jwt.decode(session_token, settings.AUTH0_JWT_SECRET, algorithms=["HS256"])

    # Sample payload
    # {
    #     "iat": 1655504851,
    #     "iss": "antunes.us.auth0.com",
    #     "sub": "auth0|62acecc73aeed2065d5aff1a",
    #     "exp": 1655505451,
    #     "ip": "2804:14d:1a87:c8de:f457:b2b7:465d:76e",
    #     "id": "auth0|62acecc73aeed2065d5aff1a",
    #     "app_metadata": {},
    #     "client_id": "WKTss4z6Q1KX3LEB2OgSSHm1cHTSJDns",
    #     "whenTheEventStarted": "2022-06-17T22:27:31.140Z",
    # }

    _logger.debug("Let's store the payload and the state so we can retrieve them later")
    request.session["state"] = state
    request.session["payload"] = payload

    return redirect(reverse("terms"))
