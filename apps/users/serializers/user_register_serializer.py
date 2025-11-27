from rest_framework import serializers

from apps.core.utils.validation_helpers import run_validation

from ..models import User
from ..services.user_service import (
    validate_age,
    validate_avatar,
    validate_banner,
    validate_bio,
    validate_email,
    validate_lang,
    validate_name,
    validate_password,
    validate_recover_email_code,
    validate_username,
)


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    name = serializers.CharField(required=True, min_length=2, max_length=100)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    username = serializers.CharField(required=True)
    banner = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    lang = serializers.CharField(required=False, default="en")

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "age",
            "email",
            "password",
            "avatar",
            "username",
            "banner",
            "bio",
            "lang",
            "recover_email_code",
        ]

    def validate_name(self, value):
        return run_validation(validate_name, value)

    def validate_age(self, value):
        return run_validation(validate_age, value)

    def validate_email(self, value):
        return run_validation(validate_email, value)

    def validate_password(self, value):
        return run_validation(validate_password, value)

    def validate_avatar(self, value):
        return run_validation(validate_avatar, value)

    def validate_username(self, value):
        return run_validation(validate_username, value)

    def validate_banner(self, value):
        return run_validation(validate_banner, value)

    def validate_bio(self, value):
        return run_validation(validate_bio, value)

    def validate_lang(self, value):
        return run_validation(validate_lang, value)

    def validate_recover_email_code(self, value):
        return run_validation(validate_recover_email_code, value)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
