from unittest.mock import patch

from django.test import TestCase

from apps.auths.serializers.email_change import VerifyUserCredentialsSerializer
from apps.users.UserFactory import UserFactory


class VerifyUserCredentialsSerializerTestCase(TestCase):

    def setUp(self):
        self.password = "uin&ytr$gue4"
        self.user = UserFactory.create(username="testuser")
        self.user.set_password(self.password)
        self.user.save()

    def test_user_with_valid_credentials_return_true(self):
        """Test that valid username and password pass serializer validation."""

        data = {"username": self.user.username, "password": self.password}

        with patch(
            "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
            return_value=True,
        ):
            serializer = VerifyUserCredentialsSerializer(instance=self.user, data=data)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(serializer.validated_data["username"], self.user.username)

    def test_user_with_invalid_credentials_return_false(self):
        """Test that invalid username or password fails serializer validation."""

        data = {"username": self.user.username, "password": "wrongpassword"}

        with patch(
            "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
            return_value=True,
        ):
            serializer = VerifyUserCredentialsSerializer(instance=self.user, data=data)
            self.assertFalse(serializer.is_valid())
            assert "Invalid credentials provided." in str(
                serializer.errors["non_field_errors"]
            )
