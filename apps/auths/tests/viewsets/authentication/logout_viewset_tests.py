from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.UserFactory import UserFactory

User = get_user_model()


class LogoutAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="testuser", email="test@example.com", password="password123"
        )

        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

        self.url = "/api/auths/logout/"

    def test_logout_authenticated_user(self):
        """Test that authenticated user can logout and cookies are deleted."""

        self.client.cookies["access_token"] = self.access_token
        self.client.cookies["refresh_token"] = self.refresh_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logged out successfully.")

        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["access_token"].value, "")
        self.assertEqual(response.cookies["refresh_token"].value, "")

    def test_logout_unauthenticated_user(self):
        """Test that unauthenticated user cannot logout (returns 401)."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
