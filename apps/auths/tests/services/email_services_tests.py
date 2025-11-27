from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import DatabaseError

from apps.auths.services import EmailChangeServices
from apps.users.UserFactory import UserFactory


@pytest.fixture
def user() -> tuple:
    """
    Fixture to create a  fake user with a hashed recover_email_code.

    Returns:
        - user (UserFactory): The created user instance.
    """

    return UserFactory.create()


@pytest.fixture
def email_change_service(user):
    """
    Fixture providing a ready-to-use EmailChangeServices instance with mocked step methods.

    Args:
        user: The user instance.

    Returns:
        EmailServicesChange: An instance of email change service with `validate_step` and `set_next_step` mocked.
    """

    service = EmailChangeServices(user=user)
    service._step_service.validate_step = MagicMock()
    service._step_service.set_next_step = MagicMock()
    return service


@pytest.mark.django_db
class TestEmailChangeService:

    def test_verify_code_valid(self, user, email_change_service):
        """
        Test that validate the user's recover_email_code is correctly.
        """
        name_step = "verify_code"

        # Store the original recover_email_code, hash it, and save to the database.
        recover_code = user.recover_email_code
        user.recover_email_code = make_password(recover_code)
        user.save()

        assert email_change_service.verify_code(recover_code) is True

        email_change_service._step_service.validate_step.assert_called_once_with(
            step_name=name_step
        )
        email_change_service._step_service.set_next_step.assert_called_once_with(
            step_name=name_step
        )

    def test_verify_code_invalid(self, email_change_service):
        """
        Test that verifying invalid user's recover_email_code is raise a ValueError.
        """

        invalid_recover_code = "W3eti2NsAQw7"

        with pytest.raises(ValueError, match="Invalid code."):
            email_change_service.verify_code(invalid_recover_code)

    def test_valid_user_credentials_pass_validation(self, user, email_change_service):
        """
        Test that the user's credentials are validated successfully.
        """

        name_step = "enter_credentials"
        password = "myNewPassword!7"

        user.set_password(password)
        user.save()

        result = email_change_service.validate_user_credentials(
            username=user.username, password=password
        )

        assert result is True
        assert user.password != password

        email_change_service._step_service.validate_step.assert_called_once_with(
            step_name=name_step
        )
        email_change_service._step_service.set_next_step.assert_called_once_with(
            step_name=name_step
        )

    def test_valid_user_credentials_pass_invalidation(self, user, email_change_service):
        """
        Test that the user's credentials invalidated is raise ValueErro.
        """

        with pytest.raises(ValidationError, match="Invalid credentials provided."):
            email_change_service.validate_user_credentials(
                username="user_invalid", password="adn7HIndUHla"
            )

    def test_update_email_success(self, user, email_change_service):
        """
        Test that the user update email correctly.
        """

        new_email = "email@gmail.com"

        result = email_change_service.update_email(new_email)
        user.refresh_from_db()

        assert user.email == new_email
        assert result is True

        email_change_service._step_service.validate_step.assert_called_once_with(
            step_name="confirm_email"
        )
        email_change_service._step_service.set_next_step.assert_called_once_with(
            step_name="confirm_email"
        )

    def test_update_email_fail(self, user, email_change_service):
        """
        Test that update_email raises ValueError when the update fails.
        """

        invalid_email = "invalid@email.com"
        error_message = "Could not update email in database."

        with patch.object(user, "save", side_effect=ValidationError("invalid")):
            with pytest.raises(ValueError, match=error_message):
                email_change_service.update_email(invalid_email)

        with patch.object(user, "save", side_effect=DatabaseError("DB fail.")):
            with pytest.raises(ValueError, match=error_message):
                email_change_service.update_email(invalid_email)
