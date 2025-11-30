import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.follows.models import Follow
from apps.posts.models import Post
from apps.users.UserFactory import UserFactory

pytestmark = pytest.mark.django_db


class TestPostListView:

    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("posts")

        # Usuários
        self.user = UserFactory.create()
        self.followed_user = UserFactory.create()
        self.unfollowed_user = UserFactory.create()

        # Seguindo
        Follow.objects.create(follower=self.user, following=self.followed_user)

        # Posts
        # Post do usuário
        Post.objects.create(
            user=self.user, blocks=[{"id": "block1", "type": "text", "data": "Hello"}]
        )
        # Post do usuário seguido
        Post.objects.create(
            user=self.followed_user,
            blocks=[{"id": "block2", "type": "text", "data": "Hi"}],
        )
        # Post do usuário não seguido (não deve aparecer)
        Post.objects.create(
            user=self.unfollowed_user,
            blocks=[{"id": "block3", "type": "text", "data": "Ignored"}],
        )

    def test_unauthenticated_user_gets_401(self):
        response = self.client.get(self.url)
        assert response.status_code == 401

    def test_authenticated_user_receives_paginated_posts(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == 200

        # A paginação do DRF retorna esses campos padrão
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

        # Deve conter só os posts do próprio usuário e dos seguidos
        post_users = {post["user"] for post in response.data["results"]}
        assert self.user.id in post_users
        assert self.followed_user.id in post_users
        assert self.unfollowed_user.id not in post_users

    def test_pagination_limit(self):
        self.client.force_authenticate(user=self.user)

        # Criar mais posts para testar paginação, por exemplo 15 posts, se page_size=10
        for i in range(15):
            Post.objects.create(
                user=self.user,
                blocks=[{"id": f"block-{i}", "type": "text", "data": f"Content {i}"}],
            )

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.data["count"] >= 16
        assert len(response.data["results"]) == 10

        response_page_2 = self.client.get(self.url + "?page=2")
        assert response_page_2.status_code == 200
        assert len(response_page_2.data["results"]) >= 6
