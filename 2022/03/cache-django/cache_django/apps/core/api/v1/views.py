from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cache_django.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from cache_django.apps.core.api.authentication.models import TokenUser


class ExampleView(APIView):
    authentication_classes = [JWTAccessTokenAuthentication]

    def get(self, request):
        authenticated_user: TokenUser = request.user
        body = {
            "user": authenticated_user.id,
        }
        return Response(body, status=status.HTTP_200_OK)


class UserView(APIView):
    pass
