import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.follows.models import Follow
from apps.posts.models import Post
from apps.users.UserFactory import UserFactory

pytestmark = pytest.mark.django_db


class TestPostListView:
    """Test suite for the Post list view."""

    def setup_method(self):
        """Setup base state with users, follow relationships, and posts."""

        self.client = APIClient()
        self.url = reverse("posts")

        self.user = UserFactory.create()
        self.followed_user = UserFactory.create()
        self.unfollowed_user = UserFactory.create()

        # User follows only followed_user
        Follow.objects.create(follower=self.user, following=self.followed_user)

        # Posts from user and followed_user should appear
        Post.objects.create(
            user=self.user,
            blocks=[{"id": "block1", "type": "text", "data": "Hello"}],
        )
        Post.objects.create(
            user=self.followed_user,
            blocks=[{"id": "block2", "type": "text", "data": "Hi"}],
        )

        # Post from an unfollowed user should NOT appear
        Post.objects.create(
            user=self.unfollowed_user,
            blocks=[{"id": "block3", "type": "text", "data": "Ignored"}],
        )

    def test_unauthenticated_user_gets_401(self):
        """Test that unauthenticated requests return 401."""
        response = self.client.get(self.url)
        assert response.status_code == 401

    def test_authenticated_user_receives_paginated_posts(self):
        """Test response structure and that only posts from self and followed users are returned."""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        assert response.status_code == 200

        # Pagination structure
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

        # Ensure posts come from the correct users
        post_users = {post["user"] for post in response.data["results"]}

        assert self.user.id in post_users
        assert self.followed_user.id in post_users
        assert self.unfollowed_user.id not in post_users

    def test_pagination_limit(self):
        """Test that pagination returns the correct number of results per page."""

        self.client.force_authenticate(user=self.user)

        # Create multiple posts to overflow pagination limit
        for i in range(15):
            Post.objects.create(
                user=self.user,
                blocks=[{"id": f"block-{i}", "type": "text", "data": f"Content {i}"}],
            )

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["count"] >= 16  # base posts + new posts

        # Default page size should be 10
        assert len(response.data["results"]) == 10

        # Second page should contain remaining items
        response_page_2 = self.client.get(self.url + "?page=2")

        assert response_page_2.status_code == 200
        assert len(response_page_2.data["results"]) >= 6
