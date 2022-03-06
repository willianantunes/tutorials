import re

import jwt

from django.http import HttpRequest
from jwt import DecodeError
from jwt import InvalidTokenError
from jwt import PyJWKClient
from jwt import PyJWKClientError
from rest_framework import authentication
from rest_framework import exceptions

from authentication_django_rest_framework import settings
from authentication_django_rest_framework.apps.core.api.authentication.models import TokenUser


class JWTAccessTokenAuthentication(authentication.BaseAuthentication):
    regex_bearer = re.compile(r"^[Bb]earer (.*)$")

    def __init__(self, *args, **kwargs):
        internal_extra_jwt_decode_options = kwargs.get("internal_extra_jwt_decode_options")
        if internal_extra_jwt_decode_options:
            self.internal_extra_jwt_decode_options = internal_extra_jwt_decode_options
        # Retrieving JWKS
        jwks_client = kwargs.get("internal_jwks_client")
        if jwks_client:
            self.jwks_client = jwks_client
        else:
            self.jwks_client = PyJWKClient(settings.AUTH0_TENANT_JWKS)

    def authenticate(self, request: HttpRequest):
        # Extract header
        header_authorization_value = request.headers.get("authorization")
        if not header_authorization_value:
            raise exceptions.AuthenticationFailed("Authorization header is not present")
        # Extract supposed raw JWT
        match = self.regex_bearer.match(header_authorization_value)
        if not match:
            raise exceptions.AuthenticationFailed("Authorization header must start with Bearer followed by its token")
        raw_jwt = match.groups()[-1]
        # Extract "kid"
        try:
            key_id = self.jwks_client.get_signing_key_from_jwt(raw_jwt)
        except PyJWKClientError as e:
            error_message = str(e)
            if "Unable to find a signing key" in error_message:
                raise exceptions.AuthenticationFailed("JWT does not have a valid Key ID")
            else:
                raise NotImplementedError
        except DecodeError:
            raise exceptions.AuthenticationFailed("Bearer does not contain a valid JWT")

        options = None
        extra_params = {"algorithms": ["RS256"], "audience": settings.AUTH0_MY_APPLICATION_AUDIENCE}
        # See the constructor method to understand this
        if hasattr(self, "internal_extra_jwt_decode_options"):
            options = getattr(self, "internal_extra_jwt_decode_options")
        try:
            data = jwt.decode(raw_jwt, key_id.key, **extra_params, options=options)
        except InvalidTokenError as e:
            raise exceptions.AuthenticationFailed("Bearer token is invalid")

        return TokenUser(data), data
