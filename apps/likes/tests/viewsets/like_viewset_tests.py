from rest_framework import status
from rest_framework.test import APITestCase

from apps.likes.models import Like
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class LikeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.post = PostFactory.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_toggle_creates_like_if_not_exists(self):
        """Should create a like if it does not exist when toggling."""

        url = f"/api/posts/{self.post.id}/likes/toggle/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data["post"]), self.post.id)
        self.assertEqual(int(response.data["user"]["id"]), self.user.id)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 1)

    def test_toggle_removes_like_if_exists(self):
        """Should remove a like if it exists when toggling."""

        Like.objects.create(user=self.user, post=self.post)

        url = f"/api/posts/{self.post.id}/likes/toggle/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 0)

    def test_toggle_returns_404_without_post_pk_in_url(self):
        """Should return 400 Bad Request if post_pk is missing in URL."""

        url = "/api/likes/toggle/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_likes_returns_total_and_users(self):
        """Should return total likes and users who liked a post."""

        user2 = UserFactory.create()
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=user2, post=self.post)

        url = f"/api/posts/{self.post.id}/likes/post_likes/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_likes", response.data)
        self.assertIn("users", response.data)
        self.assertEqual(response.data["total_likes"], 2)
        self.assertEqual(len(response.data["users"]), 2)

        user_ids = [u["id"] for u in response.data["users"]]
        self.assertIn(self.user.id, user_ids)

    def test_post_likes_returns_404_without_post_pk_in_url(self):
        """Should return 400 Bad Request if post_pk is missing in URL."""

        url = "/api/posts/likes/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
