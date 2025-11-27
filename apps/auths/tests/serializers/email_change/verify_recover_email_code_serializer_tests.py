from unittest.mock import patch

import pytest
from django.contrib.auth.hashers import make_password

from apps.auths.serializers.email_change import RequestRecoverEmailCodeSerializer
from apps.users.UserFactory import UserFactory


@pytest.mark.django_db
class TestRequestRecoverEmailCodeSerializer:

    @patch(
        "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
        return_value=True,
    )
    @patch("apps.core.services.step_validate_service.r.get")
    @patch("apps.core.services.step_validate_service.r.set")
    def test_validate_with_valid_code(self, mock_set, mock_get, mock_validate_step):
        """Test that valid recover code passes validation."""

        code = "AE7fna3kne9u"

        user = UserFactory.create()
        user.recover_email_code = make_password(code)
        user.save()

        mock_get.return_value = None

        serializer = RequestRecoverEmailCodeSerializer(
            instance=user, data={"recover_email_code": code}
        )

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["recover_email_code"] is True

    @patch(
        "apps.core.services.step_validate_service.StepValidateService.is_step_valid",
        return_value=True,
    )
    @patch("apps.core.services.step_validate_service.r.get")
    @patch("apps.core.services.step_validate_service.r.set")
    def test_validate_with_invalid_code(self, mock_set, mock_get, mock_validate_step):
        """Test that invalid recover code fails validation."""

        valid_code = "AE7fna3kne9u"
        invalid_code = "wrongcode123"

        user = UserFactory.create()
        user.recover_email_code = make_password(valid_code)
        user.save()

        mock_get.return_value = None

        serializer = RequestRecoverEmailCodeSerializer(
            instance=user, data={"recover_email_code": invalid_code}
        )

        assert not serializer.is_valid()
        assert "Invalid code." in str(serializer.errors["recover_email_code"])
