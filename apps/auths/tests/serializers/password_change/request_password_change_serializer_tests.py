import pytest

from apps.auths.serializers.password_change import PasswordVerifyEmailSerializer
from apps.users.UserFactory import UserFactory


@pytest.mark.django_db
class TestRequestPasswordChangeSerializer:
    def test_verify_valid_email(self):
        """Test that valid email passes validation and returns correct user data."""
        user = UserFactory.create(email="email@gm.com")

        serializer = PasswordVerifyEmailSerializer(data={"email": user.email})

        assert serializer.is_valid()

        user_data = serializer.get_user_data()

        assert user_data["email"] == user.email
        assert user_data["name"] == user.name

    def test_verify_invalid_email(self):
        """Test that invalid email fails validation and returns no user data."""
        not_found_email = "invalid.account@gm.com"

        serializer = PasswordVerifyEmailSerializer(data={"email": not_found_email})

        assert not serializer.is_valid()
        assert "User not found." in str(serializer.errors["email"])

        user_data = serializer.get_user_data()
        assert user_data is None
