from rest_framework import serializers

from apps.auths.services.email_change_services import EmailChangeServices
from apps.core.utils.validation_helpers import run_validation
from apps.users.models import User


class UpdateEmailSerializer(serializers.ModelSerializer):
    """Serializer for updating user email."""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def update(self, instance, validate_data):
        new_email = validate_data["email"]

        service = EmailChangeServices(user=instance)
        run_validation(lambda _: service.update_email(new_email), new_email)

        return instance
