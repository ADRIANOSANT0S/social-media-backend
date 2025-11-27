from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutAPIView(APIView):
    """
    Handle user logout by deleting the user's session
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(
            {"detail": "Logged out successfully."}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
