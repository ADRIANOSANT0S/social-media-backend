from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.comments.comment_factory import CommentFactory
from apps.comments.models import Comment
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class CommentViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.post = PostFactory.create()
        self.list_url = reverse("post-comments-list", kwargs={"post_pk": self.post.pk})

    def test_list_comments_authenticated(self):
        """Authenticated user lists comments for a post"""

        CommentFactory.create_batch(3, post=self.post, user=self.user)

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data["results"]), 3)

    def test_create_comment_authenticated(self):
        """Authenticated user creates a comment on a post"""

        self.client.force_authenticate(user=self.user)

        data = {"content": "Test comment"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Comment.objects.filter(
                post=self.post, user=self.user, content=data["content"]
            ).exists()
        )

    def test_create_comment_unauthenticated(self):
        """Unauthenticated user cannot create a comment"""

        data = {"content": "Comment without login"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments_unauthenticated(self):
        """Unauthenticated user cannot list comments"""

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
