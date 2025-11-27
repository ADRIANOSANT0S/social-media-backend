import pytest
from django.core.exceptions import ValidationError

from apps.core.services.authenticate_service import AuthenticateService
from apps.users.UserFactory import UserFactory


@pytest.mark.django_db
class TestAuthenticateServices:

    # ==============================================
    # Test cases for valid credentials validation.
    # ==============================================
    def test_user_with_valid_credential(self):
        """Test that user input valid credentials."""

        email = "email@gmail.com"
        password = "*uin74na@nda"
        user = UserFactory(email=email, password=password, username="username")

        # Authenticate with email
        user_returned1 = AuthenticateService.authenticate_user(
            identifier=user.email, password=password
        )

        # Authenticate with username
        user_returned2 = AuthenticateService.authenticate_user(
            identifier=user.username, password=password
        )

        user.full_clean()
        assert user_returned1 == user
        assert user_returned2 == user

    # ==============================================
    # Test cases for invalid credential validation.
    # ==============================================
    def test_user_with_invalid_credential(self):
        """Test that user input invalid credentials."""

        email = "email@gmail.com"
        password = "*uin74na@nda"
        UserFactory(email="email.oi@invalid.com", password=password)

        with pytest.raises(ValidationError) as context:
            AuthenticateService.authenticate_user(identifier=email, password=password)
        assert "Invalid credentials provided." in str(context.value)
