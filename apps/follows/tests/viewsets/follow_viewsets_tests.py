import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.follows.models import Follow
from apps.users.UserFactory import UserFactory

pytestmark = pytest.mark.django_db


class TestFollowView:
    """Test suite for the Follow view."""

    def setup_method(self):
        """Setup test data before each test."""
        self.client = APIClient()
        self.url = reverse("follows")

        self.user = UserFactory.create(username="main")

        self.follower1 = UserFactory.create(username="f1")
        self.follower2 = UserFactory.create(username="f2")

        self.following1 = UserFactory.create(username="g1")

        # Followers → user
        Follow.objects.create(follower=self.follower1, following=self.user)
        Follow.objects.create(follower=self.follower2, following=self.user)

        # User → following
        Follow.objects.create(follower=self.user, following=self.following1)

    def test_unauthenticated_user_returns_401(self):
        """Test that unauthenticated requests return 401."""
        response = self.client.get(self.url)
        assert response.status_code == 401

    def test_authenticated_user_receives_200(self):
        """Test that authenticated users receive status 200 and correct response structure."""
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "followers" in response.data
        assert "following" in response.data

    def test_followers_count_is_correct(self):
        """Test that followers count matches what is stored in the database."""
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert len(response.data["followers"]) == 2

    def test_following_count_is_correct(self):
        """Test that following count matches what is stored in the database."""
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        assert len(response.data["following"]) == 1

    def test_followers_payload_structure(self):
        """Test that each follower object contains the correct fields and nested user details."""
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        follower_item = response.data["followers"][0]

        # Top-level fields
        assert "id" in follower_item
        assert "follower" in follower_item
        assert "following" in follower_item
        assert "created_at" in follower_item

        # Nested user fields
        assert "username" in follower_item["follower"]
        assert "avatar" in follower_item["follower"]

    def test_following_payload_structure(self):
        """Test that each following object contains the correct fields and nested user details."""
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        following_item = response.data["following"][0]

        # Top-level fields
        assert "id" in following_item
        assert "follower" in following_item
        assert "following" in following_item
        assert "created_at" in following_item

        # Nested user fields
        assert "username" in following_item["following"]
        assert "avatar" in following_item["following"]
