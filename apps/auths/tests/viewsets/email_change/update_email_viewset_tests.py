from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.UserFactory import UserFactory


class UpdateEmailViewSetTests(APITestCase):
    def setUp(self):
        self.default_code = "SE7rna9ja6ye"
        self.user = UserFactory.create(email="old@email.com")
        self.user.recover_email_code = self.default_code
        self.user.save()
        self.url = reverse("update-email")
        self.data = {
            "user_id": self.user.id,
            "email": "new@email.com",
        }

    @patch("django.core.mail.EmailMultiAlternatives")
    def test_update_email_success(self, mock_email_class):
        """Test that email is updated and email is send successfully."""
        mock_email_instance = mock_email_class.return_value
        mock_email_instance.send.return_value = True

        response = self.client.put(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.recover_email_code, None)

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_update_email_fail(self, mock_send):
        """Test that email failure is handled gracefully."""

        mock_send.side_effect = Exception("SMTP server error")

        response = self.client.put(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.recover_email_code, self.default_code)
