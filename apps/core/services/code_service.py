from django.contrib.auth.hashers import make_password

from apps.users.models import User

from ..utils.generate_code import generate_code


class CodeService:
    def __init__(self, user: User):
        self.user = user

    def set_code(self, length: int = 12) -> str:
        """
        Generate code and set code in user's database.

        Args:
            length (int): Is the length of code generate. Default 12

        Return:
            str: The generated code (plain text; stored hashed in the user object).

        Note:
            The called is responsible for saving the user object to persist the code.
        """

        if length < 6 or length > 64:
            raise ValueError("Length must be between 6 and 64.")

        code = generate_code(length)
        self.user.recover_email_code = make_password(code)

        return code
