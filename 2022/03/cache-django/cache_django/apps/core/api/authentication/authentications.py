import re

import jwt

from django.core.cache import cache
from django.http import HttpRequest
from jwt import DecodeError
from jwt import InvalidTokenError
from jwt import PyJWKClient
from jwt import PyJWKClientError
from rest_framework import authentication
from rest_framework import exceptions

from cache_django import settings
from cache_django.apps.core.api.authentication.models import TokenUser


class CachingJWKClient(PyJWKClient):
    cache_key = "MY_APP_NAME_JWKS"
    cache_timeout_1_day = 60 * 60 * 24

    def __init__(self, uri: str):
        super().__init__(uri)

    def fetch_data(self):
        return cache.get_or_set(self.cache_key, super().fetch_data, timeout=self.cache_timeout_1_day)


class JWTAccessTokenAuthentication(authentication.BaseAuthentication):
    regex_bearer = re.compile(r"^[Bb]earer (.*)$")

    def __init__(self, *args, **kwargs):
        internal_extra_jwt_decode_options = kwargs.get("internal_extra_jwt_decode_options")
        if internal_extra_jwt_decode_options:
            self.internal_extra_jwt_decode_options = internal_extra_jwt_decode_options
        # Retrieving JWKS Client
        jwks_client = kwargs.get("internal_jwks_client")
        if jwks_client:
            self.jwks_client = jwks_client
        else:
            self.jwks_client = CachingJWKClient(settings.AUTH0_TENANT_JWKS)

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
        except InvalidTokenError:
            raise exceptions.AuthenticationFailed("Bearer token is invalid")

        return TokenUser(data), data
