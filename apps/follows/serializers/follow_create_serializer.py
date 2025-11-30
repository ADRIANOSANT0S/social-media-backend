from rest_framework import serializers

from apps.follows.models import Follow


class FollowCreateSerializer(serializers.ModelSerializer):
    following_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Follow
        fields = ["following_id"]

    @property
    def user(self):
        return self.context["request"].user

    def create(self, validated_data):
        following_id = validated_data["following_id"]

        return Follow.objects.create(follower=self.user, following_id=following_id)

    def validate_following_id(self, value):
        if self.user.id == value:
            raise serializers.ValidationError("User cannot follow himself.")
        return value
