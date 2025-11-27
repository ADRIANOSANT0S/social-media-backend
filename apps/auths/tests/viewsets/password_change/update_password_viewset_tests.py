from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.auths.serializers.password_change.update_password_serializer import (
    UpdatePasswordSerializer,
)
from apps.auths.services.password_change_services import PasswordChangeService
from apps.users.UserFactory import UserFactory


@pytest.mark.django_db
class TestUpdatePasswordView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = reverse("update-password")
        self.user = UserFactory.create()

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_update_password_success(self, mock_send, client, monkeypatch):

        def fake_update_password(self, password):
            return True

        monkeypatch.setattr(
            PasswordChangeService, "update_password", fake_update_password
        )

        data = {"user_id": self.user.id, "new_password": "umaSenhaSegura123!"}

        serializer = UpdatePasswordSerializer(data=data)
        assert serializer.is_valid()

        saved_user = serializer.save()
        assert saved_user == self.user

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_update_password_failure(self, mock_send, monkeypatch):
        def fake_save_raises(self):
            raise Exception("DB error")

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.UpdatePasswordSerializer.save",
            fake_save_raises,
        )

        data = {
            "user_id": self.user.id,
            "new_password": "StrongPassword123!",
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "detail" in response.data
        assert "Could not update password" in response.data["detail"]
        mock_send.assert_not_called()

    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_update_password_invalid_data(self, monkeypatch):
        def raise_error(*args, **kwargs):
            raise Exception("Simulated failure")

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.UpdatePasswordSerializer.save",
            raise_error,
        )
        data = {
            "user_id": self.user.id,
            "new_password": "",
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "new_password" in response.data
