from unittest.mock import patch

from django.test import TestCase

from apps.auths.serializers.email_change import UpdateEmailSerializer
from apps.users.UserFactory import UserFactory


class UpdateEmailSerializerTestCase(TestCase):
    """Test case for UpdateEmailSerializer."""

    def setUp(self):
        # Create test user
        self.user = UserFactory.create(email="teste@dominio.com")
        self.user.save()
        self.new_email = "novoemail@dominio.com"

    @patch(
        "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
        return_value=True,
    )
    @patch("apps.auths.services.email_change_services.EmailChangeServices.update_email")
    def test_update_email_success(self, mock_update_email, mock_is_step_valid):
        """Test that serializer updates email and calls the update service correctly."""
        mock_update_email.return_value = True

        data = {"email": self.new_email}
        serializer = UpdateEmailSerializer(instance=self.user, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        mock_update_email.assert_called_once_with(self.new_email)
        self.assertEqual(serializer.instance, self.user)

    @patch(
        "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
        return_value=True,
    )
    @patch("apps.auths.services.email_change_services.EmailChangeServices.update_email")
    def test_update_email_failure(self, mock_update_email, mock_is_step_valid):
        """Test that serializer fails if update service returns False."""
        mock_update_email.return_value = False

        data = {"email": self.new_email}
        serializer = UpdateEmailSerializer(instance=self.user, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        mock_update_email.assert_called_once_with(self.new_email)
        self.assertNotEqual(self.user.email, self.new_email)
