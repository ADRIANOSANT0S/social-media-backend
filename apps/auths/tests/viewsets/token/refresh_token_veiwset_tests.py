from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.UserFactory import UserFactory


class RefreshTokenAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.url = "/api/auths/refresh-token/"

        self.refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.refresh)

    def test_refresh_token_success(self):
        """Test that valid refresh token returns a new access token and sets cookie."""

        self.client.cookies["refresh_token"] = self.refresh_token
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("access_token", response.cookies)
        self.assertEqual(
            response.cookies["access_token"].value, response.json()["access"]
        )

    def test_refresh_token_missing(self):
        """Test that missing refresh token returns 401."""

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "No refresh token")

    def test_refresh_token_invalid(self):
        """Test that invalid refresh token returns 401."""

        self.client.cookies["refresh_token"] = "invalidtoken123"
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is invalid", response.json()["detail"])
