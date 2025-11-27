from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.UserFactory import UserFactory


class PasswordVerifyEmailViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(email="user@test.com")
        self.url = reverse("password-verify-email")

    @patch(
        "apps.auths.services.password_change_services.PasswordChangeService.verify_email"
    )
    @patch(
        "apps.auths.services.password_change_services.PasswordChangeService.get_code_from_redis"
    )
    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_password_verify_email_success(
        self, mock_send, mock_get_code, mock_verify_email
    ):
        """
        Test that verify email successfully
        """

        mock_verify_email.return_value = self.user
        mock_get_code.return_value = {"code": "123456"}
        mock_send.return_value = 1

        data = {"email": self.user.email}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"], "Password reset code sent successfully."
        )

        mock_verify_email.assert_called_once()
        mock_send.assert_called_once()
        mock_get_code.assert_called_once()

    @patch(
        "apps.auths.services.password_change_services.PasswordChangeService.verify_email"
    )
    @patch(
        "apps.auths.services.password_change_services.PasswordChangeService.get_code_from_redis"
    )
    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_password_verify_email_send_failure(
        self, mock_send, mock_get_code, mock_verify_email
    ):
        mock_get_code.return_value = {"code": "123456"}
        mock_send.side_effect = Exception("Falha no envio")
        mock_verify_email.return_value = self.user

        data = {"email": self.user.email}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)

        mock_send.assert_called_once()
        mock_get_code.assert_called_once()
        mock_verify_email.assert_called_once()
