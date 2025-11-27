from unittest.mock import patch

from django.test import TestCase
from rest_framework import serializers

from apps.auths.serializers.password_change import UpdatePasswordSerializer
from apps.users.UserFactory import UserFactory


class UpdatePasswordSerializerTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password("OldPassword123")
        self.user.save()

    @patch(
        "apps.auths.services.password_change_services.StepValidateService.validate_step"
    )
    def test_update_password_success(self, mock_validate_step):
        """Test that serializer updates password and returns user"""

        mock_validate_step.return_value = None
        data = {
            "user_id": self.user.id,
            "new_password": "NewPassw@ord123",
        }
        serializer = UpdatePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(user.id, self.user.id)
        self.assertTrue(user.check_password("NewPassw@ord123"))

    def test_update_password_user_not_found(self):
        """Test that serializer fails when user does not exist"""
        data = {
            "user_id": 9999,
            "new_password": "NewPassw@ord123",
        }
        serializer = UpdatePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.save()
        self.assertIn("User not found.", str(context.exception))
