from time import sleep

from django.db.utils import IntegrityError
from rest_framework.test import APITestCase

from apps.comments.comment_factory import CommentFactory
from apps.comments.models import Comment
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class CommentModelTestCase(APITestCase):

    def setUp(self):
        self.comment = CommentFactory.create()
        self.user = UserFactory.create()
        self.post = PostFactory.create()

    def test_comment_creation(self):
        """Should create Comment instance with valid user, post, and content."""

        self.assertIsNotNone(self.comment.id)
        self.assertIsNotNone(self.comment.user)
        self.assertIsNotNone(self.comment.post)
        self.assertTrue(len(self.comment.content) > 0)

    def test_comment_creation_without_user_raises_error(self):
        """Should raise an error when creating Comment without a user."""

        with self.assertRaises(IntegrityError):
            CommentFactory.create(user=None, post=self.post, content="kkkkk")

    def test_comment_creation_without_post_raises_error(self):
        """Should raise an error when creating Comment without a post."""
        with self.assertRaises(IntegrityError):
            CommentFactory(user=self.user, post=None, content="Good post")

    def test_comment_creation_without_content_raises_error(self):
        """Should raise an error when creating Comment without content."""
        with self.assertRaises(IntegrityError):
            CommentFactory(user=self.user, post=self.post, content=None)

    def test_comment_ordering_by_created_at_descending(self):
        """Should order comments by 'created_at' descending by default."""
        comment_a = CommentFactory.create()
        sleep(0.01)
        comment_b = CommentFactory.create()

        comments = Comment.objects.all()

        self.assertEqual(comments[0], comment_b)
        self.assertEqual(comments[1], comment_a)

    def test_comment_str_method_returns_expected_string(self):
        """Should return the correct string representation from __str__."""

        comment = CommentFactory.create()
        expected_str = f"Comment by {comment.user} on post {comment.post.id}"
        self.assertEqual(str(comment), expected_str)

    def test_comment_timestamps_are_auto_populated(self):
        """Should automatically populate created_at and updated_at fields."""
        comment = CommentFactory()

        self.assertIsNotNone(comment.created_at)

    def test_comment_updated_at_changes_on_save(self):
        """Should update 'updated_at' field when comment is saved again."""
        comment = CommentFactory.create()
        old_updated_at = comment.updated_at

        comment.content = "New content"
        comment.save()

        comment.refresh_from_db()
        new_updated_at = comment.updated_at

        self.assertNotEqual(old_updated_at, new_updated_at)
