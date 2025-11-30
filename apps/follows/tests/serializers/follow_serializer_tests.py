from django.test import TestCase

from apps.follows.models import Follow
from apps.follows.serializers import FollowSerializer
from apps.users.UserFactory import UserFactory


class FollowSerializerTestCase(TestCase):
    def setUp(self):
        self.user_a = UserFactory.create(username="user_a")
        self.user_b = UserFactory.create(username="user_b")

        self.follow = Follow.objects.create(follower=self.user_a, following=self.user_b)

    def test_follow_serializer_output(self):
        """Test that the serializer returns the correct fields and nested user data."""

        serializer = FollowSerializer(instance=self.follow)
        data = serializer.data

        # Top-level fields
        self.assertIn("id", data)
        self.assertIn("follower", data)
        self.assertIn("following", data)
        self.assertIn("created_at", data)

        follower_data = data["follower"]
        following_data = data["following"]

        expected_user_fields = {"id", "username", "name", "avatar"}

        # Nested fields
        self.assertEqual(set(follower_data.keys()), expected_user_fields)
        self.assertEqual(set(following_data.keys()), expected_user_fields)

        # Follower assertions
        self.assertEqual(follower_data["id"], self.user_a.id)
        self.assertEqual(follower_data["username"], self.user_a.username)
        self.assertEqual(follower_data["name"], self.user_a.name)
        self.assertEqual(follower_data["avatar"], self.user_a.avatar)

        # Following assertions
        self.assertEqual(following_data["id"], self.user_b.id)
        self.assertEqual(following_data["username"], self.user_b.username)
        self.assertEqual(following_data["name"], self.user_b.name)
        self.assertEqual(following_data["avatar"], self.user_b.avatar)
