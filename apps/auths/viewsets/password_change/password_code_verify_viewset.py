from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.password_change import PasswordCodeVerifySerializer


class PasswordCodeVerifyView(APIView):
    """Viewset to verify password change code."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordCodeVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            {
                "detail": "Code verified successfully.",
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )
