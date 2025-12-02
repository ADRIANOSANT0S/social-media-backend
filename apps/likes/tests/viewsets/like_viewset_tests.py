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

        response = self.client.post("/api/likes/toggle/", {"post_id": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data["post"]), self.post.id)
        self.assertEqual(int(response.data["user"]["id"]), self.user.id)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 1)

    def test_toggle_removes_like_if_exists(self):
        """Should remove a like if it exists when toggling."""

        Like.objects.create(user=self.user, post=self.post)

        response = self.client.post("/api/likes/toggle/", {"post_id": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 0)

    def test_toggle_returns_400_without_post_id(self):
        """Should return 400 Bad Request if post_id is missing in toggle."""

        response = self.client.post("/api/likes/toggle/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("post_id", response.data["detail"].lower())

    def test_post_likes_returns_total_and_users(self):
        """Should return total likes and users who liked a post."""

        # Cria likes de outros usuários para o post
        user2 = UserFactory.create()
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=user2, post=self.post)

        response = self.client.get(f"/api/likes/post_likes/?post_id={self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("total_likes", response.data)
        self.assertIn("users", response.data)

        self.assertEqual(response.data["total_likes"], 2)
        self.assertEqual(len(response.data["users"]), 2)

        # Verifica se o usuário atual está na lista
        user_ids = [u["id"] for u in response.data["users"]]
        self.assertIn(self.user.id, user_ids)

    def test_post_likes_returns_400_without_post_id(self):
        """Should return 400 Bad Request if post_id is missing in post_likes."""

        response = self.client.get("/api/likes/post_likes/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("post_id", response.data["detail"].lower())
