import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apiview_django_rest_framework.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from apiview_django_rest_framework.apps.core.api.v1.serializers import UserAttributesSerializer

_logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([JWTAccessTokenAuthentication])
def refresh_user_attributes(request: Request) -> Response:
    _logger.debug("The following user is trying to refresh his attributes: %s", request.user.id)
    serializer = UserAttributesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # TODO: Save new properties

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAccessTokenAuthentication])
def retrieve_user_attributes(request: Request, user_id: str) -> Response:
    _logger.debug("The following user is trying to retrieve his attributes: %s", request.user.id)
    # TODO: retrieve properties
    user_details = {}
    body = {
        "name": user_details.get("name"),
        "given_name": user_details.get("given_name"),
        "family_name": user_details.get("family_name"),
        "user_metadata": user_details.get("user_metadata"),
    }
    return Response(body, status=status.HTTP_200_OK)
