from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    content = serializers.CharField(max_length=300)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
