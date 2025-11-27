from rest_framework import serializers

from apps.core.services.authenticate_service import AuthenticateService


class LoginSerializer(serializers.Serializer):
    """
    Serializer for the user login process.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Validate the user's credentials.
        """

        user = AuthenticateService.authenticate_user(
            identifier=data["email"], password=data["password"]
        )

        if not user:
            raise serializers.ValidationError({"detail": "Invalid Credentials."})

        data["user"] = user
        return data
