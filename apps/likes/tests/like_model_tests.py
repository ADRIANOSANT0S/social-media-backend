from django.db import IntegrityError
from django.test import TestCase

from apps.likes.models import Like
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class LikeModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.post = PostFactory.create(user=self.user)

    def test_create_like_success(self):
        """Test that a Like instance can be created successfully."""
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertIsNotNone(like.id)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertIsNotNone(like.created_at)

    def test_unique_constraint_user_post(self):
        """Test that the unique constraint on (user, post) is enforced."""

        Like.objects.create(user=self.user, post=self.post)

        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, post=self.post)

    def test_related_name_access(self):
        """Test that related_name 'likes' allows reverse access from User and Post."""

        like = Like.objects.create(user=self.user, post=self.post)

        self.assertIn(like, self.user.likes.all())
        self.assertIn(like, self.post.likes.all())
