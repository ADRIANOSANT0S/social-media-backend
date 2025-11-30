from rest_framework.test import APITestCase

from apps.posts.serializers import PostSerializer


class PostSerializerTestCase(APITestCase):
    """Test case for PostSerializer."""

    def setUp(self) -> None:
        self.valid_blocks = [
            {"type": "text", "content": "This is a test post."},
            {"type": "image", "url": "http://example.com/image.jpg"},
        ]

    def test_validate_blocks_success(self):
        """Should validate blocks and assign ids where missing."""

        data = {"blocks": self.valid_blocks}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        validated_blocks = serializer.validated_data["blocks"]

        # Check that all blocks have an 'id'
        for block in validated_blocks:
            self.assertIn("id", block)
            self.assertIsInstance(block["id"], str)

    def test_validate_blocks_empty_list(self):
        """Should raise ValidationError for empty blocks list."""

        data = {"blocks": []}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("blocks", serializer.errors)

    def test_validate_blocks_none(self):
        """Should raise ValidationError for None blocks."""

        data = {"blocks": None}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("blocks", serializer.errors)
