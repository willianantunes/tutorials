import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apiview_django_rest_framework.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from apiview_django_rest_framework.apps.core.api.v1.serializers import UserAttributesSerializer

_logger = logging.getLogger(__name__)


class UserManagementAttributesAPIView(APIView):
    authentication_classes = [JWTAccessTokenAuthentication]

    def post(self, request):
        user_id = request.user.id
        _logger.debug("The following user is trying to refresh his attributes: %s", user_id)
        serializer = UserAttributesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO: Save new properties

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.user.id
        _logger.debug("The following user is trying to retrieve his attributes: %s", user_id)
        # TODO: retrieve properties
        user_details = {}
        body = {
            "name": user_details.get("name"),
            "given_name": user_details.get("given_name"),
            "family_name": user_details.get("family_name"),
            "user_metadata": user_details.get("user_metadata"),
        }
        return Response(body, status=status.HTTP_200_OK)
