from rest_framework import serializers

from apps.likes.models import Like
from apps.users.serializers import UserSimpleSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["id", "created_at"]
