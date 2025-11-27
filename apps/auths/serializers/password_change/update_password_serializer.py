from rest_framework import serializers

from apps.auths.services import PasswordChangeService
from apps.core.utils import run_validation
from apps.users.models import User


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer to update the user's password after code verification.
    """

    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=12)

    def validate(self, attrs):
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(id=self.validated_data["user_id"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        service = PasswordChangeService(user=user)
        run_validation(service.update_password, self.validated_data["new_password"])

        return user
