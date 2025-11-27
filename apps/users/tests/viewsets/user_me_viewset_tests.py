from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.users.UserFactory import UserFactory
from apps.users.viewsets.user_me_viewset import UserMeAPIView


class UserMeViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserMeAPIView.as_view()
        self.user = UserFactory()

    # ==============================================
    # Test cases for user authentication.
    # ==============================================
    def test_user_me_authenticated(self):
        """Test that the authenticated user data is returned correctly."""
        request = self.factory.get("/api/users/me/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_data = response.data["user"]
        expected_fields = {
            "id",
            "name",
            "age",
            "avatar",
            "username",
            "banner",
            "bio",
            "lang",
        }
        self.assertEqual(set(user_data.keys()), expected_fields)
        self.assertEqual(user_data["id"], self.user.id)
        self.assertEqual(user_data["username"], self.user.username)

    def test_user_me_unauthenticated(self):
        """Test  that the unauthenticated request are rejected."""

        request = self.factory.get("/api/users/me/")
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
