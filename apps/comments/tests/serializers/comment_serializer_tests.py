from rest_framework.test import APITestCase

from apps.comments.serializers import CommentSerializer
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class CommentSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.post = PostFactory.create()

    def test_create_comment_success(self):
        """Test create comment successful."""
        data = {"content": "kkkk"}
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save(user=self.user, post=self.post)

        self.assertEqual(comment.content, data["content"])
        self.assertIsNotNone(comment.id)
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

    def test_create_comment_with_content_to_long(self):
        """Test validate raise if content is to long."""

        data = {"content": "kkkk" * 90}

        serializer = CommentSerializer(data=data)

        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.errors["content"])

    def test_comment_serializer_read_only_fields(self):
        """Test that validate the fields ['id', 'user', 'post'] is only read"""

        data = {
            "id": 7,
            "user": self.user.id,
            "post": self.post.id,
            "content": "Is very good",
        }

        serializer = CommentSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("post", serializer.validated_data)
        self.assertIn("content", serializer.validated_data)
