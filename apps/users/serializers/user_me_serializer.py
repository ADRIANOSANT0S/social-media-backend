from rest_framework import serializers

from ..models import User


class UserMeSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user profile information."""

    avatar = serializers.URLField(required=False, allow_null=True)
    banner = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = User
        base_fields = [
            "id",
            "name",
            "age",
            "avatar",
            "username",
            "banner",
            "bio",
            "lang",
        ]
        fields = base_fields
        read_only_fields = base_fields
