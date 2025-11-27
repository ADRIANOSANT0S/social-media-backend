from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.backends import CookieJWTAuthentication
from apps.users.serializers import UserMeSerializer


class UserMeAPIView(APIView):
    """
    Return the autenticad user data for frontend.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
