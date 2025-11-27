from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.users.UserFactory import UserFactory


class RequestRecoverEmailCodeViewsetTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.url = reverse("verify-recover-email-code")

    @patch(
        "apps.auths.serializers.email_change.RequestRecoverEmailCodeSerializer.is_valid"
    )
    def test_recover_code_valid(self, mock_is_valid):
        """Test that valid recover code returns 200."""

        mock_is_valid.return_value = True
        mock_is_valid.side_effect = lambda raise_exception=False: True

        data = {"recover_email_code": "validcode123"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Code verify successfully.")

    @patch(
        "apps.auths.serializers.email_change.RequestRecoverEmailCodeSerializer.is_valid"
    )
    def test_recover_code_invalid(self, mock_is_valid):
        """Test that invalid recover code returns 400."""

        def raise_error(raise_exception=False):
            from rest_framework.serializers import ValidationError

            if raise_exception:
                raise ValidationError({"recover_email_code": ["Invalid code."]})
            return False

        mock_is_valid.side_effect = raise_error

        data = {"recover_email_code": "wrongcode"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid code.", str(response.data["recover_email_code"]))
