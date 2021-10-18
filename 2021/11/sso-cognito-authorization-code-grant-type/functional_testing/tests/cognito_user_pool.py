import base64
import hashlib
import hmac
import logging

from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union

import boto3
import botocore

from mypy_boto3_cognito_idp.type_defs import GetUserResponseTypeDef

from tests import settings

logger = logging.getLogger(__name__)


class UsernameExistsException(Exception):
    pass


@dataclass(frozen=True)
class UserToBeRegistered:
    email: str
    name: str
    password: str


@dataclass(frozen=True)
class UserDetails:
    username: str
    attributes: Dict[str, Union[str, int]]
    created_at: datetime
    updated_at: datetime
    enabled: bool
    status: str


@dataclass(frozen=True)
class AppClientDetails:
    id: str
    secret: str
    name: str
    created_at: datetime
    updated_at: datetime
    refresh_token_validity: int
    read_attributes: List[str]
    supported_identity_providers: List[str]
    callback_urls: List[str]
    logout_urls: List[str]
    allowed_oauth_flows: List[str]
    allowed_oauth_scopes: List[str]
    allowed_oauth_flows_user_pool_client: bool
    enable_token_revocation: bool


GrantType = Literal["ropc", "code"]


class CognitoUserPool:
    def __init__(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/index.html#sdk-features
        self.client = boto3.client(
            "cognito-idp",
            region_name=settings.AWS_COGNITO_REGION,
            aws_access_key_id=settings.AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_COGNITO_SERVICE_ACCOUNT_ACCESS_SECRET,
        )
        self.app_client_id = settings.AWS_COGNITO_APP_CLIENT_ID
        self.app_client_secret = settings.AWS_COGNITO_APP_CLIENT_SECRET
        self.user_pool_id = settings.AWS_COGNITO_USER_POOL_ID

    def create_user(self, user: UserToBeRegistered) -> None:
        # https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cognito_idp/client.html#sign_up
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.sign_up
        logger.debug("Creating user with name %s", user.name)
        user_attributes = [
            {
                "Name": "name",
                "Value": user.name,
            },
            {
                "Name": "email",
                "Value": user.email,
            },
        ]
        secret_hash = self._generete_secret_hash(user.email)
        try:
            sign_up_response_as_json = self.client.sign_up(
                ClientId=self.app_client_id,
                Username=user.email,
                Password=user.password,
                UserAttributes=user_attributes,
                SecretHash=secret_hash,
            )
            logger.debug("Sign up response: %s", sign_up_response_as_json)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "UsernameExistsException":
                raise UsernameExistsException
            else:
                raise NotImplementedError

    def confirm_user_as_admin(self, username):
        logger.debug("Confirming user with username %s", username)
        try:
            self.client.admin_confirm_sign_up(UserPoolId=self.user_pool_id, Username=username)
        except botocore.exceptions.ClientError as e:
            message = e.response["Error"]["Message"]
            exceptionType = e.response["Error"]["Code"]
            if exceptionType == "NotAuthorizedException" and "Current status is CONFIRMED" in message:
                pass
            else:
                raise e

    def retrieve_user_through_access_token(self, access_token: str) -> GetUserResponseTypeDef:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_user
        return self.client.get_user(AccessToken=access_token)

    def retrieve_user(self, username: str) -> Optional[UserDetails]:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_get_user
        try:
            response_as_json = self.client.admin_get_user(UserPoolId=self.user_pool_id, Username=username)
            return self._create_user_details(response_as_json)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] != "UserNotFoundException":
                raise NotImplementedError
        return None

    def delete_user(self, username: str) -> None:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_delete_user
        self.client.admin_delete_user(UserPoolId=self.user_pool_id, Username=username)

    def list_users(self, pagination_token: str = None, limit=50) -> Tuple[List[UserDetails], Optional[str]]:
        users = []
        params = {"UserPoolId": self.user_pool_id, "Limit": limit}

        if not pagination_token:
            logger.debug("Listing users without pagination token")
            response_as_json = self.client.list_users(**params)
        else:
            logger.debug("Listing users with pagination token")
            params["PaginationToken"] = pagination_token
            response_as_json = self.client.list_users(**params)

        for user in response_as_json["Users"]:
            built_user = self._create_user_details(user)
            users.append(built_user)

        return users, response_as_json.get("PaginationToken")

    def retrieve_user_pool_client(self, client_id: str) -> Optional[AppClientDetails]:
        try:
            response_as_json = self.client.describe_user_pool_client(UserPoolId=self.user_pool_id, ClientId=client_id)
            user_pool_client = response_as_json["UserPoolClient"]
            constructor_dict = {
                "id": user_pool_client["UserPoolId"],
                "secret": user_pool_client["ClientSecret"],
                "name": user_pool_client["ClientName"],
                "created_at": user_pool_client["CreationDate"],
                "updated_at": user_pool_client["LastModifiedDate"],
                "refresh_token_validity": user_pool_client["RefreshTokenValidity"],
                "read_attributes": user_pool_client["ReadAttributes"],
                "supported_identity_providers": user_pool_client["SupportedIdentityProviders"],
                "callback_urls": user_pool_client["CallbackURLs"],
                "logout_urls": user_pool_client["LogoutURLs"],
                "allowed_oauth_flows": user_pool_client["AllowedOAuthFlows"],
                "allowed_oauth_scopes": user_pool_client["AllowedOAuthScopes"],
                "allowed_oauth_flows_user_pool_client": user_pool_client["AllowedOAuthFlowsUserPoolClient"],
                "enable_token_revocation": user_pool_client["EnableTokenRevocation"],
            }
            return AppClientDetails(**constructor_dict)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] != "ResourceNotFoundException":
                raise NotImplementedError
        return None

    def _generete_secret_hash(self, username: str) -> str:
        # https://aws.amazon.com/premiumsupport/knowledge-center/cognito-unable-to-verify-secret-hash/
        message = bytes(username + self.app_client_id, "utf-8")
        key = bytes(self.app_client_secret, "utf-8")
        return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

    def _create_user_details(self, user_from_cognito: dict):
        username = user_from_cognito["Username"]
        created_at = user_from_cognito["UserCreateDate"]
        updated_at = user_from_cognito["UserLastModifiedDate"]
        enabled = user_from_cognito["Enabled"]
        status = user_from_cognito["UserStatus"]
        attributes = {}
        users_attributes = user_from_cognito.get("UserAttributes")
        users_attributes = users_attributes if users_attributes else user_from_cognito["Attributes"]
        for attribute in users_attributes:
            key, value = attribute["Name"], attribute["Value"]
            attributes[key] = value
        return UserDetails(username, attributes, created_at, updated_at, enabled, status)
