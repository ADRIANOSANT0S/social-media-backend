from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.UserFactory import User, UserFactory


class UserModelTestCases(TestCase):
    """Test cases for the User model."""

    def validate_field_with_values(
        self, field_name: str, values: list, factory_class=UserFactory
    ):
        """
        Helper to validate multiple values for a given field.

        Args:
            field_name (str): Is the name of field. Example (e.g.,'age').
            values (list): Is the list of that should trigger ValidationError,
            factory_class (class, optional): Factory use to create a new instances. Defaults to UserFactory.
        """

        for value in values:
            user = factory_class.build(**{field_name: value})
            user.full_clean()
            self.assertEqual(getattr(user, field_name), value)

    def validate_raises_with_value(
        self, field_name: str, values: list, factory_class=UserFactory
    ):
        """
        Helper to validate multiple values raised for a given field.

        Args:
            field_name (str): Is the name of field. Example (e.g.,'age').
            values (list): Is the list of that should trigger ValidationError,
            factory_class (class, optional): Factory use to create a new instances. Defaults to UserFactory.
        """

        for value in values:
            user = factory_class.build(**{field_name: value})
            with self.assertRaises(ValidationError) as context:
                user.full_clean()
            self.assertIn(field_name, context.exception.message_dict)

    # ==============================================
    # Test cases for name validation.
    # ==============================================
    def test_name_required(self):
        """Test that user is required"""

        user = UserFactory.build(name=None)

        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("name", context.exception.message_dict)

    def test_name_valid(self):
        """Test user with valid name"""

        valid_names = ["jw", "name lastname", "full S.", "English's name"]

        self.validate_field_with_values("name", valid_names)

    def test_name_invalid(self):
        """Test that name is invalid (too short or invalid characters)"""
        invalid_names = ["", None, "a", "n" * 101]

        self.validate_raises_with_value("name", invalid_names)

    # ==============================================
    # Test cases for age validation.
    # ==============================================
    def test_age_required(self):
        """Test that age is required"""
        user = UserFactory.build(age=None)

        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("age", context.exception.message_dict)

    def test_age_valid(self):
        """Test That aga is valid."""

        valid_ages = [18, 25, 99, 70]
        self.validate_field_with_values("age", valid_ages)

    def test_invalid_age(self):
        """Test that age is invalid."""

        invalid_ages = [17, 125, 9, 7, 101, None, "Eighteen"]

        self.validate_raises_with_value("age", invalid_ages)

    # ==============================================
    # Test cases for email validation.
    # ==============================================
    def test_email_valid(self):
        """Test that email is valid."""

        valid_emails = [
            "email@gmail.com",
            "email.person@hotmail.com",
            "email@mydomain.oi",
        ]
        self.validate_field_with_values("email", valid_emails)

    def test_email_invalid(self):
        """Test that emails is invalid."""

        invalid_emails = ["email", "@oi.com", "email@.", "invalid.email@today@", None]
        self.validate_raises_with_value("email", invalid_emails)

    def test_email_unique(self):
        """Test that email is unique."""

        user1 = UserFactory.build(email="duplicate@email.com")
        user1.full_clean()
        user1.save()

        user2 = UserFactory.build(email="duplicate@email.com")

        with self.assertRaises(ValidationError) as context:
            user2.full_clean()
        self.assertIn("email", context.exception.message_dict)

    # ==============================================
    # Test cases for password validation.
    # ==============================================
    def test_password_hashed(self):
        """Test that password is saved hashed."""

        password = "password@3gna27!"
        user = UserFactory.build(password=password)
        user.full_clean()

        self.assertNotEqual(user.password, password)

    def test_is_password_invalidated_default_false(self):
        """Test that password is invalided"""

        user = UserFactory()
        self.assertFalse(user.is_password_invalidated)

    # ==============================================
    # Test cases for avatar validation.
    # ==============================================
    def test_avatar_valid(self):
        """Test that user is valid."""

        valid_user = [
            None,
            "http://path-of-picture.svg",
            "https://my-pictures-is-here.png",
        ]

        self.validate_field_with_values("avatar", valid_user)

    def test_avatar_invalid(self):
        """Test that user is invalid"""

        invalid_avatas = [
            "/avatar.png",
            "sub-domain.invalid.com",
            "api.my-invalid-picture.png",
        ]
        self.validate_raises_with_value("avatar", invalid_avatas)

    # ==============================================
    # Test cases for username validation.
    # ==============================================
    def test_username_required(self):
        """Test that username is required."""
        user = UserFactory.build(username=None)

        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("username", context.exception.message_dict)

    def test_username_valid(self):
        """Test that username is valid."""

        valid_usernames = ["us1", "my_username", "user_name123", "user123"]
        self.validate_field_with_values("username", valid_usernames)

    def test_username_invalid(self):
        """Test that username is invalid."""

        invalid_usernames = [None, " ", "US", "n" * 16]
        self.validate_raises_with_value("username", invalid_usernames)

    def test_username_unique(self):
        """Test that user is unique."""
        user1 = UserFactory.build(username="duplicate_user")
        user1.full_clean()
        user1.save()

        user2 = UserFactory.build(username="duplicate_user")

        with self.assertRaises(ValidationError) as context:
            user2.full_clean()

        self.assertIn("username", context.exception.message_dict)

    # ==============================================
    # Test cases for banner validation.
    # ==============================================
    def test_banner_default_value(self):
        """Test that banner with default value."""

        user = User.objects.create(
            name="user1",
            age=18,
            email="user@email.oi",
            password="1aui8shf$brw",
            username="user_name",
        )

        self.assertIsNone(user.banner)

    def test_banner_valid(self):
        """Test that banner url is valid."""

        user = UserFactory()
        user.full_clean()

    def test_banner_invalid(self):
        """Test that banner invalid."""

        user = UserFactory(banner="/picture.svg")
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("banner", context.exception.message_dict)

    # ==============================================
    # Test cases for bio validation.
    # ==============================================
    def test_bio_default_value(self):
        user = User.objects.create(
            name="user1",
            age=18,
            email="user@email.oi",
            password="1aui8shf$brw",
            username="user_name",
        )

        self.assertIsNone(user.bio)

    def test_bio_valid(self):
        """Test that bio raises ValidationError if too long."""
        user = User(
            name="John",
            email="john@example.com",
            password="123456",
            bio="x" * 150,  # ultrapassa 150 chars
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_bio_invalid(self):
        """Test that bio raises ValidationError if too long."""
        user = User(
            name="John",
            email="john@example.com",
            password="123456",
            bio="x" * 200,  # ultrapassa 150 chars
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    # ==============================================
    # Test cases for lang validation.
    # ==============================================
    def test_lang_default_value(self):
        """Test that lang with default value."""
        user = User.objects.create(
            name="Mike",
            age=22,
            email="mike@gmail.com",
            password="StrongPassword1@!",
            username="mike22",
            lang="en",
        )

        self.assertEqual(user.lang, "en")

    def test_lang_valid(self):
        """Test that lang is valid."""
        # List of valid languages codes.
        valid_langs = ["en", "es", "pt"]

        self.validate_field_with_values("lang", valid_langs)

    def test_lang_invalid(self):
        """Test that lang is invalid."""
        # List of invalid languages codes.
        invalid_langs = ["fr", 123, "de", None, "#@"]
        self.validate_raises_with_value("lang", invalid_langs)

    # ==============================================
    # Test cases for create account validation.
    # ==============================================
    def test_user_creation_valid(self):
        """Test that should be create a valid user."""
        user = UserFactory()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(str(user), f"{user.name} ID: {user.id}")

    def test_user_creation_invalid(self):
        """Test that create invalid user."""

        user = User(
            name="",
            age=17,
            email="email.oi",
            password="",
            avatar="url.avatar",
            username="US",
            banner="url.banner",
            bio="bio" * 80,
            lang="fr",
        )

        invalid_fields = [
            "name",
            "age",
            "email",
            "avatar",
            "username",
            "banner",
            "bio",
            "lang",
        ]

        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        errors = context.exception.message_dict

        for field in invalid_fields:
            self.assertIn(field, errors)
