from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.follows.serializers import FollowCreateSerializer
from apps.users.UserFactory import UserFactory


class FollowCreateSerializerTestCase(APITestCase):
    """Test suite for FollowCreateSerializer."""

    def setUp(self):
        self.user_a = UserFactory.create()
        self.user_b = UserFactory.create()

    def _get_request_with_user(self, user):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/")
        force_authenticate(request, user=user)
        return Request(request)

    def test_valid_follow_creation(self):
        """Test creating a follow relationship successfully."""

        data = {"following_id": self.user_b.id}

        serializer = FollowCreateSerializer(
            data=data,
            context={"request": self._get_request_with_user(self.user_a)},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        follow = serializer.save()
        self.assertEqual(follow.follower, self.user_a)
        self.assertEqual(follow.following, self.user_b)

    def test_user_cannot_follow_himself(self):
        """Test user cannot follow himself."""

        data = {"following_id": self.user_a.id}

        serializer = FollowCreateSerializer(
            data=data,
            context={"request": self._get_request_with_user(self.user_a)},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("following_id", serializer.errors)
        self.assertEqual(
            serializer.errors["following_id"][0],
            "User cannot follow himself.",
        )
