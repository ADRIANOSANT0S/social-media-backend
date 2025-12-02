from rest_framework import serializers
from rest_framework.test import APITestCase

from apps.likes.like_factory import LikeFactory
from apps.likes.serializers import LikeSerializer
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class LikeSerializerTestCase(APITestCase):
    def setUp(self):
        self.user_a = UserFactory.create()
        self.user_b = UserFactory.create()

    def test_like_serializer_returns_expected_fields(self):
        """Should serialize all expected fields from a Like instance."""

        post = PostFactory.create(user=self.user_a)
        like = LikeFactory.create(user=self.user_a, post=post)

        serializer = LikeSerializer(instance=like)
        data = serializer.data

        expected_keys = {"id", "user", "post", "created_at"}
        self.assertTrue(expected_keys.issubset(data.keys()))

        self.assertIsInstance(data["user"], dict)

        self.assertEqual(data["post"], post.id)
        self.assertIsNotNone(data["created_at"])

    def test_like_serializer_user_and_post_are_read_only(self):
        """Should treat 'user' and 'post' fields as read-only in the serializer."""

        post = PostFactory.create(user=self.user_a)
        like = LikeFactory.create(user=self.user_a, post=post)

        input_data = {
            "user": 999,
            "post": 999,
        }

        serializer = LikeSerializer(instance=like, data=input_data, partial=True)
        is_valid = serializer.is_valid()

        self.assertTrue(
            is_valid, "Serializer should ignore read-only fields and be valid"
        )
        self.assertNotIn("user", serializer.validated_data)
        self.assertNotIn("post", serializer.validated_data)

    def test_like_serializer_meta_read_only_fields(self):
        """Should define 'id' and 'created_at' as read-only meta fields."""

        serializer = LikeSerializer()
        fields = serializer.get_fields()

        self.assertTrue(fields["id"].read_only, "'id' field should be read_only")
        self.assertTrue(
            fields["created_at"].read_only, "'created_at' field should be read_only"
        )

    def test_like_serializer_post_is_pk_field(self):
        """Should use PrimaryKeyRelatedField for the 'post' field."""

        serializer = LikeSerializer()
        post_field = serializer.fields["post"]

        self.assertIsInstance(post_field, serializers.PrimaryKeyRelatedField)

    def test_like_serializer_does_not_include_unexpected_fields(self):
        """Should not expose any fields beyond ['id', 'user', 'post', 'created_at']."""

        post = PostFactory.create(user=self.user_a)
        like = LikeFactory.create(user=self.user_a, post=post)

        serializer = LikeSerializer(instance=like)
        data = serializer.data

        allowed_fields = {"id", "user", "post", "created_at"}
        self.assertEqual(set(data.keys()), allowed_fields)
