from unittest.mock import patch

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from apps.users.UserFactory import UserFactory


class LoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.password = "TestPasswo&rd123"
        self.user.set_password(self.password)
        self.user.save()
        self.url = reverse("auth-login")

    @patch("apps.auths.viewsets.authentication.login_viewset.set_http_only_cookie")
    def test_login_success(self, mock_set_cookie):
        """Test that login returns detail and sets cookies"""

        response = self.client.post(
            self.url,
            {"email": self.user.email, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["detail"], "User create successfully")

        self.assertEqual(mock_set_cookie.call_count, 2)
        calls = [call.args[1] for call in mock_set_cookie.call_args_list]
        self.assertIn("access_token", calls)
        self.assertIn("refresh_token", calls)

    def test_login_invalid_credentials(self):
        """Test that login fails with wrong password"""

        response = self.client.post(
            self.url,
            {"email": self.user.email, "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        """Test that login fails with missing data"""

        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
