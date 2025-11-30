import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.follows.models import Follow
from apps.users.UserFactory import UserFactory

pytestmark = pytest.mark.django_db


class TestFollowView:

    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("follows")

        # Usuário autenticado
        self.user = UserFactory.create(
            username="main",
        )

        # Outros usuários
        self.follower1 = UserFactory.create(
            username="f1",
        )

        self.follower2 = UserFactory.create(
            username="f2",
        )

        self.following1 = UserFactory.create(
            username="g1",
        )

        # followers → user
        Follow.objects.create(follower=self.follower1, following=self.user)
        Follow.objects.create(follower=self.follower2, following=self.user)

        # user → following
        Follow.objects.create(follower=self.user, following=self.following1)

    # ------------------------------------------------------

    def test_unauthenticated_user_returns_401(self):
        response = self.client.get(self.url)
        assert response.status_code == 401

    # ------------------------------------------------------

    def test_authenticated_user_receives_200(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "followers" in response.data
        assert "following" in response.data

    # ------------------------------------------------------

    def test_followers_count_is_correct(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert len(response.data["followers"]) == 2

    # ------------------------------------------------------

    def test_following_count_is_correct(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert len(response.data["following"]) == 1

    # ------------------------------------------------------

    def test_followers_payload_structure(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        follower_item = response.data["followers"][0]

        assert "id" in follower_item
        assert "follower" in follower_item
        assert "following" in follower_item
        assert "created_at" in follower_item

        # Verifica se retorna username e imagem
        assert "username" in follower_item["follower"]
        assert "avatar" in follower_item["follower"]

    # ------------------------------------------------------

    def test_following_payload_structure(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        following_item = response.data["following"][0]

        assert "id" in following_item
        assert "follower" in following_item
        assert "following" in following_item
        assert "created_at" in following_item

        assert "username" in following_item["following"]
        assert "avatar" in following_item["following"]
