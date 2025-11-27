from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class AuthenticateService:

    @staticmethod
    def authenticate_user(identifier: str, password: str):
        user = authenticate(username=identifier, password=password)

        if not user:
            raise ValidationError("Invalid credentials provided.")
        return user
