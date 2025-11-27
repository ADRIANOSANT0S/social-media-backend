from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return JsonResponse(
                {"detail": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            response = JsonResponse({"access": access_token})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=token.access_token.lifetime.total_seconds(),
            )
            return response
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
