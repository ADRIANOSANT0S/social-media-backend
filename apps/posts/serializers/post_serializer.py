from uuid import uuid4

from rest_framework import serializers

from apps.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "blocks", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_blocks(self, blocks: dict) -> None:
        if not blocks or len(blocks) == 0:
            raise serializers.ValidationError("Post must contain at least one block.")

        for block in blocks:
            if "id" not in block:
                block["id"] = str(uuid4())
        return blocks
