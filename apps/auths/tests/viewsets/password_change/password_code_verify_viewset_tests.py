import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.auths.services.password_change_services import PasswordChangeService
from apps.users.UserFactory import UserFactory  # seu factory


@pytest.mark.django_db
class TestPasswordCodeVerifyView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = "/api/auths/password/verify-code/"
        self.user = UserFactory.create()
        self.valid_code = "ABC123"

    def fake_get_json(self, key):
        if key == f"password_reset_code:{self.valid_code}":
            return self.user.id
        if key == f"password_reset:{self.user.id}":
            return {"code": self.valid_code, "attempts": 0, "blocked_until": None}
        return None

    def test_post_valid_code(self, monkeypatch):
        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            self.fake_get_json,
        )
        monkeypatch.setattr(
            PasswordChangeService,
            "verify_code",
            lambda self, code: True,
        )

        response = self.client.post(self.url, {"code": self.valid_code}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "detail" in response.data
        assert response.data["user_id"] == self.user.id

    def test_post_invalid_code(self, monkeypatch):
        def fake_get_json_invalid(key):
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json_invalid,
        )

        response = self.client.post(self.url, {"code": "WRONG1"}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.data
        assert "Invalid or expired code." in response.data["code"][0]

    def test_post_missing_code(self):
        response = self.client.post(self.url, {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.data
        assert "This field is required." in response.data["code"][0]
