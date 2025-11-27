from datetime import datetime, timezone

from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.serializers import LoginSerializer
from apps.core.utils import set_http_only_cookie


class LoginAPIView(APIView):
    """
    LoginApiViewSet is responsible for handling user login requests.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle Post request for user login.
        """

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        access_expires = (
            datetime.now(timezone.utc) + refresh_token.access_token.lifetime
        )
        refresh_expires = datetime.now(timezone.utc) + refresh_token.lifetime

        response = JsonResponse(
            {"detail": "User create successfully"},
            status=status.HTTP_200_OK,
        )

        set_http_only_cookie(response, "access_token", access_token, access_expires)

        set_http_only_cookie(response, "refresh_token", refresh_token, refresh_expires)

        return response
