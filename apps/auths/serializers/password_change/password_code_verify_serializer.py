from rest_framework import serializers

from apps.auths.services import PasswordChangeService
from apps.core.utils import redis_get_json
from apps.users.models import User


class PasswordCodeVerifySerializer(serializers.Serializer):
    """
    Serializer to verify the temporary code from email.
    """

    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, code):
        redis_key_code = f"password_reset_code:{code}"
        user_id = redis_get_json(redis_key_code)

        if not user_id:
            raise serializers.ValidationError("Invalid or expired code.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        redis_key_user = f"password_reset:{user.id}"
        stored_data = redis_get_json(redis_key_user)

        if not stored_data:
            raise serializers.ValidationError("Invalid or expired code.")

        service = PasswordChangeService(user)
        if not service.verify_code(code):
            raise serializers.ValidationError("Invalid or expired code.")

        self.context["user"] = user
        return code

    def validate(self, attrs):
        attrs["user"] = self.context.get("user")
        if not attrs["user"]:
            raise serializers.ValidationError("User context is required.")
        return attrs
