import re

import jwt

from jwt import PyJWKClient
from rest_framework import authentication
from rest_framework import exceptions

from apiview_django_rest_framework import settings
from apiview_django_rest_framework.apps.core.api.authentication.models import TokenUser

regex_bearer = re.compile(r"^[Bb]earer (.*)$")


class JWTAccessTokenAuthentication(authentication.BaseAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__()
        internal_extra_jwt_decode_options = kwargs.get("internal_extra_jwt_decode_options")
        if internal_extra_jwt_decode_options:
            self.internal_extra_jwt_decode_options = internal_extra_jwt_decode_options
        jwks_client = kwargs.get("internal_jwks_client")
        if jwks_client:
            self.jwks_client = jwks_client
        else:
            # TODO: Add cache to avoid consulting openid-configuration all the time
            self.jwks_client = self._provide_jwks_client()

    def authenticate(self, request):
        # Extract header
        header_authorization_value: str = request.META.get("HTTP_AUTHORIZATION")
        if not header_authorization_value:
            raise exceptions.AuthenticationFailed("Authorization header is not present")
        # Extract raw JWT
        match = regex_bearer.match(header_authorization_value)
        if not match:
            raise exceptions.AuthenticationFailed("Authorization header must start with Bearer followed by its token")
        raw_jwt = match.groups()[-1]

        # TODO: Add exception layer so we can raise proper exceptions
        # Evaluate if raw_jwt is indeed a JWT to avoid 5XX
        signing_key = self.jwks_client.get_signing_key_from_jwt(raw_jwt)

        options = {"algorithms": ["RS256"], "audience": settings.AUTH0_MY_APPLICATION_AUDIENCE}
        if hasattr(self, "internal_extra_jwt_decode_options"):
            options = options | getattr(self, "internal_extra_jwt_decode_options")
        data = jwt.decode(raw_jwt, signing_key.key, **options)

        return TokenUser(data), data

    @staticmethod
    def _provide_jwks_client():
        return PyJWKClient(settings.AUTH0_TENANT_JWKS)
