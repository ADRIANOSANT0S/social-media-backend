from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.follows.models import Follow
from apps.users.UserFactory import UserFactory


class FollowTestCase(TestCase):
    """Test case to Follow model."""

    def setUp(self):
        self.user_a = UserFactory.create()
        self.user_b = UserFactory.create()

    def test_following_other_user(self):
        """User A should be able to follow User B."""

        follow = Follow.objects.create(follower=self.user_a, following=self.user_b)

        self.assertIsNotNone(follow.id)
        self.assertEqual(follow.follower, self.user_a)
        self.assertEqual(follow.following, self.user_b)

    def test_follower_following_himself(self):
        with self.assertRaises(ValidationError):
            Follow.objects.create(follower=self.user_a, following=self.user_a)

    def test_unique_follow_relationship(self):
        """Cannot create a duplicate follow relationship."""

        Follow.objects.create(follower=self.user_b, following=self.user_a)

        with self.assertRaises(IntegrityError):
            Follow.objects.create(follower=self.user_b, following=self.user_a)
