import inspect
import logging

from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Set
from typing import TypedDict

import jwt
import requests

from jwt import PyJWKClient
from requests.auth import HTTPBasicAuth

from backend_django.support.http_utils import build_url_with_query_strings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OIDCConfigurationDocument:
    # Endpoints
    authorization_endpoint: str
    token_endpoint: str
    device_authorization_endpoint: str
    userinfo_endpoint: str
    mfa_challenge_endpoint: str
    jwks_uri: str
    registration_endpoint: str
    revocation_endpoint: str
    # Metadata
    issuer: str
    scopes_supported: List[str]
    response_types_supported: List[str]
    code_challenge_methods_supported: List[str]
    response_modes_supported: List[str]
    subject_types_supported: List[str]
    id_token_signing_alg_values_supported: List[str]
    token_endpoint_auth_methods_supported: List[str]
    claims_supported: List[str]
    request_uri_parameter_supported: bool

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


class JWTPublicKey(TypedDict):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str
    x5t: Optional[str]
    x5c: Optional[str]


class JWTPublicKeys(TypedDict):
    keys: List[JWTPublicKey]


class OIDCProvider:
    oidc_configuration_document: OIDCConfigurationDocument
    jwt_public_keys: JWTPublicKeys
    jwt_public_keys_algorithms: Set[str]
    jwks_client: PyJWKClient

    domain = str
    app_client_key = str
    app_client_secret = str
    scopes = str

    @classmethod
    def configure_class_properties(cls, domain, app_key, app_secret, scopes: List[str]):
        cls.domain = domain
        cls.app_client_key = app_key
        cls.app_client_secret = app_secret
        cls.scopes = scopes

    @classmethod
    def configure_oidc_configuration_document(cls):
        document = requests.get(f"https://{cls.domain}/.well-known/openid-configuration").json()
        cls.oidc_configuration_document = OIDCConfigurationDocument.from_dict(document)
        cls.jwks_client = PyJWKClient(f"https://{cls.domain}/.well-known/jwks.json")

    @classmethod
    def build_authorization_url(cls, redirect_uri: str, state: str, params: Optional[dict] = None):
        # https://auth0.com/docs/api/authentication#authorization-code-flow
        # https://auth0.com/docs/login/authentication/add-login-auth-code-flow#authorize-user
        auth_url = cls.oidc_configuration_document.authorization_endpoint
        provided_params = {
            "state": state,
            "client_id": cls.app_client_key,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls.scopes),
            # https://auth0.com/docs/brand-and-customize/i18n/universal-login-internationalization
            # Instead of passing the parameter below, I changed the tenant itself!
            # "ui_locales": "pt-BR",
        }
        if params:
            provided_params = provided_params | params

        logger.debug("Building authorization URL...")
        return build_url_with_query_strings(auth_url, provided_params)

    @classmethod
    def acquire_token_by_auth_code_flow(cls, code: str, redirect_uri: str):
        # https://auth0.com/docs/api/authentication#authenticate-user
        # https://auth0.com/docs/authorization/flows/call-your-api-using-the-authorization-code-flow#request-tokens
        token_endpoint = cls.oidc_configuration_document.token_endpoint
        app_credentials = HTTPBasicAuth(cls.app_client_key, cls.app_client_secret)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": cls.app_client_key,
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls.scopes),
        }
        response = requests.post(token_endpoint, headers=headers, data=body, auth=app_credentials)
        content = response.json()
        id_token = content["id_token"]
        claims = cls._retrieve_claims(id_token)
        return content, claims

    @classmethod
    def _retrieve_claims(cls, id_token: str) -> dict:
        key_id = cls.jwks_client.get_signing_key_from_jwt(id_token)
        options = {"verify_aud": False}
        return jwt.decode(id_token, key_id.key, ["RS256"], options)

    @classmethod
    def build_logout_url(cls, return_to):
        # https://auth0.com/docs/api/authentication#logout
        logout_endpoint = f"https://{cls.domain}/v2/logout"
        params = {
            "returnTo": return_to,
            "client_id": cls.app_client_key,
        }
        logger.debug("Building logout URL...")
        return build_url_with_query_strings(logout_endpoint, params)

    @classmethod
    def get_user_info(cls, access_token: str):
        # https://auth0.com/docs/api/authentication#user-profile
        userinfo_endpoint = cls.oidc_configuration_document.userinfo_endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        result = requests.get(userinfo_endpoint, headers=headers)
        body = result.json()

        return body
