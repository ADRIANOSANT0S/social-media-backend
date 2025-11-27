from rest_framework import serializers

from apps.core.services.authenticate_service import AuthenticateService
from apps.core.utils.validation_helpers import run_validation
from apps.users.models import User


class VerifyUserCredentialsSerializer(serializers.ModelSerializer):
    """Serializer for verifying user credentials."""

    username = serializers.CharField(required=True, max_length=15)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        run_validation(
            lambda _: AuthenticateService.authenticate_user(
                identifier=username, password=password
            ),
            attrs,
        )

        return attrs
