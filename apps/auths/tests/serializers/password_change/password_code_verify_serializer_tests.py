import pytest

from apps.auths.serializers.password_change import PasswordCodeVerifySerializer
from apps.users.UserFactory import (  # supondo que você usa Factory para usuários
    UserFactory,
)


@pytest.mark.django_db
class TestPasswordCodeVerifySerializer:

    def fake_validate_step(self, step_name):
        pass

    def test_verify_code_success(self, monkeypatch):
        user = UserFactory.create()
        fake_data_user = {"code": "ABC123", "attempts": 0, "blocked_until": None}

        def fake_get_json(key):
            if key == "password_reset_code:ABC123":
                return user.id
            if key == f"password_reset:{user.id}":
                return fake_data_user
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json,
        )

        monkeypatch.setattr(
            "apps.auths.services.password_change_services.PasswordChangeService.verify_code",
            lambda self, code: True,
        )

        monkeypatch.setattr(
            "apps.auths.services.password_change_services.StepValidateService.validate_step",
            self.fake_validate_step,
        )

        serializer = PasswordCodeVerifySerializer(data={"code": "ABC123"})
        assert serializer.is_valid(), serializer.errors
        assert serializer.context["user"].id == user.id

    def test_verify_code_invalid_code(self, monkeypatch):
        UserFactory.create()

        def fake_get_json(key):
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json,
        )

        serializer = PasswordCodeVerifySerializer(data={"code": "WRONG1"})
        assert not serializer.is_valid()
        assert "Invalid or expired code." in serializer.errors["code"][0]

    def test_user_not_found(self, monkeypatch):
        UserFactory.create()

        def fake_get_json(key):
            if key == "password_reset_code:ABC123":
                return 999999
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json,
        )

        serializer = PasswordCodeVerifySerializer(data={"code": "ABC123"})
        assert not serializer.is_valid()
        assert "User not found." in serializer.errors["code"][0]

    def test_no_stored_data(self, monkeypatch):
        user = UserFactory.create()

        def fake_get_json(key):
            if key == "password_reset_code:ABC123":
                return user.id
            if key == f"password_reset:{user.id}":
                return None
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json,
        )

        serializer = PasswordCodeVerifySerializer(data={"code": "ABC123"})
        assert not serializer.is_valid()
        assert "Invalid or expired code." in serializer.errors["code"][0]

    def test_verify_code_service_false(self, monkeypatch):
        user = UserFactory.create()
        fake_data_user = {"code": "ABC123", "attempts": 0, "blocked_until": None}

        def fake_get_json(key):
            if key == "password_reset_code:ABC123":
                return user.id
            if key == f"password_reset:{user.id}":
                return fake_data_user
            return None

        monkeypatch.setattr(
            "apps.auths.serializers.password_change.password_code_verify_serializer.redis_get_json",
            fake_get_json,
        )

        # Força a validação do serviço a falhar
        monkeypatch.setattr(
            "apps.auths.services.password_change_services.PasswordChangeService.verify_code",
            lambda self, code: False,
        )

        serializer = PasswordCodeVerifySerializer(data={"code": "ABC123"})
        assert not serializer.is_valid()
        assert "Invalid or expired code." in serializer.errors["code"][0]
