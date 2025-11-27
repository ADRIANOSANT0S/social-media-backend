from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.email_change import VerifyUserCredentialsSerializer


class VerifyUserCredentialsViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyUserCredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail": "Credentials verify successfully."}, status=status.HTTP_200_OK
        )
