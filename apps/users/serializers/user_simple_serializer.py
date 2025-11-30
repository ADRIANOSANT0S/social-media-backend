from rest_framework import serializers

from apps.users.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", "avatar"]
        read_only_fields = fields
