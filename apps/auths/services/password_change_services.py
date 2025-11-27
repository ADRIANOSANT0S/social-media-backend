from datetime import datetime, timedelta
from typing import Optional

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.core.config.redis import r
from apps.core.contracts import FLOW_RECOVER_PASSWORD
from apps.core.services.step_validate_service import StepValidateService
from apps.core.utils import redis_get_json, redis_set_json
from apps.core.utils.generate_code import generate_code
from apps.users.models import User
from apps.users.services.user_service import validate_password


class PasswordChangeService:
    """
    Class PasswordChangeService include all methods to change password process.
    """

    def __init__(self, user: User):
        self.user = user
        self._step_service = StepValidateService(
            user_id=user.id, flow_name="change_password", steps=FLOW_RECOVER_PASSWORD
        )

    def verify_email(self, email: str) -> User:
        """
        Verify user's email.

        Args:
            email (str): User's email

        Return:
            User: Return the user object to send the confirmation code.
        """

        step_name = "verify_identity"
        self._step_service.validate_step(step_name=step_name)

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email format.")

        if self.user.email != email.lower():
            raise ValueError("Email not found.")

        code = generate_code(6)

        redis_set_json(
            f"password_reset:{self.user.id}",
            {"code": code, "attempts": 0, "blocked_until": None},
            ex=300,
        )

        self._step_service.set_next_step(step_name=step_name)
        return self.user

    def verify_code(self, input_code: str) -> bool:
        step_name = "verify_code"
        self._step_service.validate_step(step_name=step_name)

        key = f"password_reset:{self.user.id}"
        data = redis_get_json(key)

        if not data:
            raise ValueError("No code generated or expired.")

        if data.get("blocked_until"):
            blocked_until = datetime.fromisoformat(data["blocked_until"])

            if blocked_until > datetime.now():
                raise ValueError("Code temporarily blocked. Try later.")

        if input_code != data["code"]:
            data["attempts"] += 1

            if data["attempts"] >= 3:
                data["blocked_until"] = (
                    datetime.now() + timedelta(hours=12)
                ).isoformat()

            redis_set_json(key, data, ex=300)
            raise ValueError("Invalid code.")

        self._step_service.set_next_step(step_name=step_name)
        r.delete(key)
        return True

    def get_code_from_redis(self) -> Optional[dict]:
        """
        Retrieve the code data from Redis.
        key = f"password_reset:{self.user.id}
        Returns:
            dict: The code data stored in Redis.
        """

        key = f"password_reset:{self.user.id}"
        data = redis_get_json(key)
        return data

    def update_password(self, new_password):
        """
        Update the user's password.

        Args:
        new_password: The new password.
        """
        step_name = "confirm_password"
        self._step_service.validate_step(step_name=step_name)

        validate_password(new_password)
        self.user.set_password(new_password)
        self.user.save()

        self._step_service.set_next_step(step_name=step_name)
