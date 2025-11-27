from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import DatabaseError

from apps.core.contracts import FLOW_RECOVER_EMAIL
from apps.core.services import AuthenticateService, StepValidateService
from apps.users.models import User


class EmailChangeServices:
    """
    Class EmailChangeServices include methods for validate end update email

    Methods:
        verify_code - Valide that input verify_email_code is valid.
        validate_user_credentials - Check if user is valid.
        update_email - Update that current user's email and recover_email_code.
    """

    def __init__(self, user: User):
        """The initialization class for user -> User"""

        self.user = user
        self._step_service = StepValidateService(
            user_id=user.id, flow_name="change_email", steps=FLOW_RECOVER_EMAIL
        )

    def verify_code(self, input_code: str) -> bool:
        """
        Validate that the user input code is correct.

        Args:
            input_code (str): Code entered by the user.

        Return:
            bool: True if the code is valid.

        Raises:
            ValueError: If the code is invalid.
        """
        step_name = "verify_code"

        self._step_service.validate_step(step_name=step_name)

        if not check_password(input_code, self.user.recover_email_code):
            raise ValueError("Invalid code.")

        self._step_service.set_next_step(step_name=step_name)
        return True

    def validate_user_credentials(self, username: str, password: str) -> bool:
        """
        Validate that user credential is valid.

        Args:
            password (str): Password entered by the user.
            username (str): Username entered by the user.

        Return:
            bool: True if the user's credential is valid.

        Raises:
            ValidateError: If the credentials is invalid.
        """

        step_name = "enter_credentials"

        self._step_service.validate_step(step_name=step_name)

        AuthenticateService.authenticate_user(identifier=username, password=password)

        self._step_service.set_next_step(step_name=step_name)
        return True

    def update_email(self, new_email: str) -> str:
        """
        Update user email and seve the email end new_recover_email_code in database.

        Args:
            new_email (str): Email entered by user.

        Return:
            str: Return the new code to send for user seve.
        """
        try:

            step_name = "confirm_email"

            self._step_service.validate_step(step_name=step_name)

            self.user.email = new_email
            self.user.save(update_fields=["email"])

            self._step_service.set_next_step(step_name=step_name)
        except (ValidationError, DatabaseError) as e:
            raise ValueError("Could not update email in database.") from e
        return True
