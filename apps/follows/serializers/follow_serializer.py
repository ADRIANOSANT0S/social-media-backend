from rest_framework import serializers

from apps.follows.models import Follow
from apps.users.serializers import UserSimpleSerializer


class FollowSerializer(serializers.ModelSerializer):
    """Serializer to return list of followers and following."""

    follower = UserSimpleSerializer(read_only=True)
    following = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["id", "created_at"]
