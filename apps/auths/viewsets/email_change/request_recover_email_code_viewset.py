from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.email_change import RequestRecoverEmailCodeSerializer


class RequestRecoverEmailCodeViewset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests to validate the user's recovery code.

        The request must include the `recover_email_code` field.
        Returns 200 if the code is valid, otherwise 400 with error details.
        """

        serializer = RequestRecoverEmailCodeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail": "Code verify successfully."}, status=status.HTTP_200_OK
        )
