from typing import Any, Dict, List
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.users.models import User
from apps.users.viewsets.user_register_viewset import UserRegisterViewSet


class UserRegisterViewSetTests(TestCase):
    def setUp(self):
        self.code = "ABc123456780"
        self.factory = APIRequestFactory()
        self.view = UserRegisterViewSet.as_view({"post": "create"})
        self.valid_data = {
            "name": "John",
            "age": 18,
            "email": "john@example.com",
            "password": "StrongPass123!",
            "username": "johndoe",
            "avatar": "https://image.svg",
            "banner": "http://image.svg",
            "bio": "a" * 150,
            "recover_email_code": self.code,
        }

    # ==============================================
    # Test cases for create a user.
    # ==============================================
    @patch("apps.users.viewsets.user_register_viewset.EmailMultiAlternatives.send")
    @patch("apps.users.viewsets.user_register_viewset.CodeService.set_code")
    def test_create_user_valid(self, mock_set_code, mock_send_email):
        """Test creating a user successfully."""

        # Mock the generate code.
        mock_set_code.return_value = self.code

        self.valid_data = {
            "name": "John",
            "age": 18,
            "email": "john@example.com",
            "password": "StrongPass123!",
            "username": "johndoe",
            "avatar": "https://image.svg",
            "banner": "http://image.svg",
            "bio": "a" * 150,
            "recover_email_code": self.code,
        }

        request = self.factory.post(
            "api/users/register/", self.valid_data, format="json"
        )
        response = self.view(request)
        response.render()
        print(response.data)

        # Checa status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the user was create successfully in the database.
        user = User.objects.get(email="john@example.com")
        self.assertIsNotNone(user)
        self.assertNotEqual(user.recover_email_code, self.code)

    @patch("apps.users.viewsets.user_register_viewset.EmailMultiAlternatives.send")
    @patch("apps.users.viewsets.user_register_viewset.CodeService.set_code")
    def test_create_user_invalid(self, mock_set_code, mock_send_email):
        """Test creating an invalid user with invalid data fails."""

        self.invalid_code = "Invalid2"

        mock_set_code.return_value = self.invalid_code

        invalid_cases: List[Dict[str, Any]] = [
            {"field": "name", "value": "J@hn$%"},
            {"field": "age", "value": -1},
            {"field": "email", "value": "invalid-email"},
            {"field": "password", "value": "123"},
            {"field": "avatar", "value": "/invalid-avatar.svg"},
            {"field": "banner", "value": "/invalid-banner.svg"},
            {"field": "bio", "value": "a" * 151},
            {"field": "recover_email_code", "value": self.invalid_code},
            {"field": "lang", "value": "de"},
        ]

        for case in invalid_cases:
            invalid_data = self.valid_data.copy()
            invalid_data[case["field"]] = case["value"]

            request = self.factory.post(
                "api/users/register/", invalid_data, format="json"
            )
            response = self.view(request)
            response.render()

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(case["field"], response.data)

            # Check that send_email was't called.
            mock_send_email.assert_not_called()

    # ==============================================
    # Test cases for existent fields.
    # ==============================================
    @patch("apps.users.viewsets.user_register_viewset.EmailMultiAlternatives.send")
    @patch("apps.users.viewsets.user_register_viewset.CodeService.set_code")
    def test_create_user_email_and_username_exists(
        self, mock_set_code, mock_send_email
    ):
        """Test creating a user with existing email and username fails."""

        mock_set_code.return_value = self.code

        # Create a user.
        User.objects.create_user(
            name="john",
            age=21,
            email="john@example.com",
            password="StrongPass123!",
            username="johndoe",
            avatar="https://image.svg",
            banner="http://image.svg",
            bio="This is a bio.",
            lang="en",
        )

        request = self.factory.post(
            "api/users/register/", self.valid_data, format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("username", response.data)

        # Check that send_email was't called.
        mock_send_email.assert_not_called()

    # ==============================================
    # Test cases for send email.
    # ==============================================
    @patch("apps.users.viewsets.user_register_viewset.EmailMultiAlternatives.send")
    @patch("apps.users.viewsets.user_register_viewset.CodeService.set_code")
    def test_create_user_email_send_success(self, mock_set_code, mock_send_email):
        """Test creating a send email successfully."""

        mock_set_code.return_value = self.code

        request = self.factory.post(
            "api/users/register/", self.valid_data, format="json"
        )
        response = self.view(request)
        response.render()

        # Send email to user successfully
        mock_send_email.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("details", response.data)
        self.assertEqual(response.data["details"], "Account created successfully.")

    @patch("apps.users.viewsets.user_register_viewset.EmailMultiAlternatives.send")
    @patch("apps.users.viewsets.user_register_viewset.CodeService.set_code")
    def test_create_user_email_send_fail(self, mock_set_code, mock_send_email):
        """Test creating a send email fail."""

        mock_set_code.return_value = self.code

        # Create a email raise
        mock_send_email.side_effect = Exception("SMTP Error.")

        request = self.factory.post(
            "api/users/register/", self.valid_data, format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Could not send email. Please try again later."
        )
