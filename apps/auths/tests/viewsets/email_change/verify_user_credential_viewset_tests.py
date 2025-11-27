from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.users.UserFactory import UserFactory


class VerifyUserCredentialsViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(username="testuser", password="password123")
        self.client = APIClient()
        self.url = reverse("verify-user-credentials")

    @patch(
        "apps.auths.serializers.email_change.VerifyUserCredentialsSerializer.is_valid"
    )
    def test_credentials_valid(self, mock_is_valid):
        """Test that valid credentials return 200 OK."""

        mock_is_valid.side_effect = lambda raise_exception=False: True

        data = {"username": self.user.username, "password": "password123"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Credentials verify successfully.")

    @patch(
        "apps.auths.serializers.email_change.VerifyUserCredentialsSerializer.is_valid"
    )
    def test_credentials_invalid(self, mock_is_valid):
        """Test that invalid credentials return 400 with error."""

        from rest_framework.serializers import ValidationError

        def raise_error(raise_exception=False):
            if raise_exception:
                raise ValidationError({"non_field_errors": ["Invalid credentials."]})
            return False

        mock_is_valid.side_effect = raise_error

        data = {"username": self.user.username, "password": "wrUngAs7sword"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid credentials.", str(response.data["non_field_errors"]))
