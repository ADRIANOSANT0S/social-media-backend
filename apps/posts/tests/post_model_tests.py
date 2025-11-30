import time

from django.test import TestCase

from apps.posts.models import Post
from apps.users.UserFactory import UserFactory


class MotelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.blocks = [
            {"id": 1, "type": "text", "content": "This is a test post."},
            {"id": 2, "type": "image", "url": "http://example.com/image.jpg"},
        ]

    # ==============================================
    # Test cases for create post.
    # ==============================================
    def test_create_post_successfully(self):
        """Post should be created with valid user and block data."""

        post = Post.objects.create(user=self.user, blocks=self.blocks)
        self.assertIsNotNone(post.id)
        self.assertEqual(post.blocks, self.blocks)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_create_post_with_blocks_invalid(self):
        """Post creation should fail with blocks data invalid."""

        invalid_blocks = [None, "invalid block", ""]
        for block in invalid_blocks:
            with self.assertRaises(Exception):
                Post.objects.create(user=self.user, blocks=block)

    def test_create_post_without_user(self):
        """Post creation should fail with invalid user."""

        with self.assertRaises(Exception):
            Post.objects.create(user=None, blocks=self.blocks)

    def test_validate_post_ordering(self):
        """Post should be ordered by created_at descending."""

        post1 = Post.objects.create(user=self.user, blocks=self.blocks)
        time.sleep(0.01)
        post2 = Post.objects.create(user=self.user, blocks=self.blocks)

        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)
