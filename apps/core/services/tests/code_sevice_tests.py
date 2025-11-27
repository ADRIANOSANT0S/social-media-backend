import pytest
from django.contrib.auth.hashers import check_password as check_code

from apps.users.UserFactory import UserFactory

from ..code_service import CodeService


@pytest.mark.django_db
class TestCodeService:
    def setup_method(self):
        self.user = UserFactory()
        self.code_service = CodeService(self.user)

    def test_set_code_with_default_length(self):
        """Test that set_code generate a code of the default length (12)"""

        code = self.code_service.set_code()
        assert len(code) == 12

    def test_set_code_with_custom_length(self):
        """Test that set_code generate a code of the specified length"""

        code = self.code_service.set_code(30)
        assert len(code) == 30

    def test_set_code_with_invalid_length(self):
        """Test that ValidateError is raise for invalid  code length."""

        invalid_codes = [5, 65]

        for length in invalid_codes:
            with pytest.raises(ValueError) as except_info:
                self.code_service.set_code(length)

            assert str(except_info.value) == "Length must be between 6 and 64."

    def test_set_code_is_hashed_successful(self):
        """Test That code is hashed correctly."""

        code = self.code_service.set_code()
        self.user.save()
        self.user.refresh_from_db()

        print("the user hash is: ", self.user.recover_email_code)
        assert self.user.recover_email_code != code
        assert self.user.recover_email_code
        assert check_code(code, self.user.recover_email_code) is True
