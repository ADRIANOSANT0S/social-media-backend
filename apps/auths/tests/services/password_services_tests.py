from unittest.mock import MagicMock

import pytest

from apps.auths.services import PasswordChangeService
from apps.users.UserFactory import UserFactory


@pytest.fixture
def user():
    return UserFactory.create(email="email@gm.com")


@pytest.fixture
def password_change_service(user):
    service = PasswordChangeService(user=user)
    service._step_service.validate_step = MagicMock()
    service._step_service.set_next_step = MagicMock()
    return service


@pytest.mark.django_db
class TestPasswordChangeService:
    def test_verify_email_generates_code_and_saves_redis(
        self, password_change_service, monkeypatch, user
    ):
        """
        Test that verify_email generates a code and saves it in Redis.
        """

        mock_redis_set = MagicMock()
        monkeypatch.setattr(
            "apps.auths.services.password_change_services.redis_set_json",
            mock_redis_set,
        )

        returned_user = password_change_service.verify_email(user.email)

        assert returned_user.id == user.id
        mock_redis_set.assert_called_once()
        key_used = mock_redis_set.call_args[0][0]
        assert str(user.id) in key_used

    def test_verify_email_raises_error_for_invalid_email_format(
        self, password_change_service
    ):
        """
        Test that verify_email raises ValueError when the email format is invalid.
        """

        with pytest.raises(ValueError, match="Invalid email format."):
            password_change_service.verify_email("invalid-email")

    def test_verify_email_raises_error_for_wrong_email(self, password_change_service):
        """
        Test that verify_email raises ValueError when the email does not exist.
        """
        with pytest.raises(ValueError, match="Email not found."):
            password_change_service.verify_email("another@gm.com")

    def test_verify_code_success(self, password_change_service, monkeypatch):
        """
        Test the verify_code returns True when the code is valid.
        """

        monkeypatch.setattr(
            "apps.auths.services.password_change_services.redis_get_json",
            lambda key: {"code": "Uh8yd7", "attempts": 0, "blocked_until": None},
        )
        mock_r_delete = MagicMock()
        monkeypatch.setattr(
            "apps.auths.services.password_change_services.r.delete", mock_r_delete
        )

        assert password_change_service.verify_code("Uh8yd7") is True
        mock_r_delete.assert_called_once()

    def test_verify_code_invalid(self, password_change_service, monkeypatch):
        """
        Test that verify_code raise ValuerError when the code is invalid.
        """

        monkeypatch.setattr(
            "apps.auths.services.password_change_services.redis_get_json",
            lambda key: {"code": "Uh8yd7", "attempts": 0, "blocked_until": None},
        )
        with pytest.raises(ValueError, match="Invalid code."):
            password_change_service.verify_code("0Q0y00")

    def test_update_password_changes_user_password(self, password_change_service, user):
        """
        Test that update_password updates the user's password in the database.
        """

        old_password_hash = user.password
        password_change_service.update_password("NewStrongPass123!")

        user.refresh_from_db()
        assert user.password != old_password_hash
        assert user.check_password("NewStrongPass123!")
