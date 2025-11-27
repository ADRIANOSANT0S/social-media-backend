from rest_framework import serializers

from apps.auths.services import PasswordChangeService
from apps.core.utils import run_validation
from apps.users.models import User


class PasswordVerifyEmailSerializer(serializers.Serializer):
    """
    Serializer to request a password reset code via email.
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            service = PasswordChangeService(user=user)
            self.context["user"] = user

            return run_validation(lambda _: service.verify_email, value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

    def get_user_data(self):
        user = self.context.get("user")

        if not user:
            return None
        return {"email": user.email, "name": user.name}
