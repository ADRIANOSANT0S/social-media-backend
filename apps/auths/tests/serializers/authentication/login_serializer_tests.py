from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.auths.serializers import LoginSerializer
from apps.users.UserFactory import UserFactory


class LoginSerializerTestCase(TestCase):
    """
    Test case for the LoginSerializer.
    """

    def test_validate_with_valid_credentials(self):
        """
        Test validation with valid credentials.
        """
        plain_password = "Password12@success"
        user = UserFactory(email="email@hotmail.com")
        user.set_password(plain_password)
        user.save()

        data = {"email": user.email, "password": plain_password}

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        self.assertEqual(validated["email"], user.email)

    def test_validate_with_invalid_credentials(self):
        """
        Test validation with valid credentials.
        """
        plain_password = "Password12@success"
        user = UserFactory(email="email@hotmail.com")
        user.set_password(plain_password)
        user.save()

        data = {
            "email": "invalidEmail@gmail.com",
            "password": "invalidPassword@D33qsn89",
        }

        serializer = LoginSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Invalid credentials provided.", str(context.exception))

    def test_validate_with_empty_credentials(self):
        """
        Test validation with empty credentials.
        """
        data = {"email": "", "password": ""}

        serializer = LoginSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("This field may not be blank", str(context.exception))
