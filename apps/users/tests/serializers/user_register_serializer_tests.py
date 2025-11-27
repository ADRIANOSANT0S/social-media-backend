from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.core.contracts import LANGUAGES
from apps.users.serializers import UserRegisterSerializer
from apps.users.UserFactory import UserFactory


class UserRegisterSerializerTests(TestCase):
    """
    Test cases for the UserRegisterSerializer.
    """

    def setUp(self):
        """
        Set up the serializer instance for testing.
        """
        self.serializer = UserRegisterSerializer()

    # ==============================================
    # Test cases for first name validation.
    # ==============================================
    def test_validate_name_valid(self):
        """
        Test that a valid first name passes validation
        """
        valid_name = "John'N"
        validated_name = self.serializer.validate_name(valid_name)
        self.assertEqual(validated_name, valid_name)

    def test_validate_name_invalid(self):
        """
        Test that a invalid first name passes validation.
        """

        # List of invalid name
        invalid_name = [
            "",
            "1John",
            "John@Doe",
            "John Doe!",
            "John-Doe#",
            "John_Doe",
            "j",
            "name" * 101,
        ]

        for invalid_name in invalid_name:
            with self.assertRaises(ValidationError):
                self.serializer.validate_name(invalid_name)

    # ==============================================
    # Test cases for age validation.
    # ==============================================
    def test_validate_age_valid(self):
        """
        Test that a valid age passes validation.
        """

        valid_age = 25
        validate_age = self.serializer.validate_age(valid_age)
        self.assertEqual(validate_age, valid_age)

    def test_validate_age_invalid(self):
        """
        Test that an invalid age raises a ValidationError.
        """

        # List of invalid ages.
        invalid_ages = [-1, 0, 17, 101, "abc", "12.5", "18 years", "eighteen"]
        for invalid_age in invalid_ages:
            with self.assertRaises(ValidationError):
                self.serializer.validate_age(invalid_age)

    # ==============================================
    # Test cases for email validation.
    # ==============================================
    def test_validate_email_valid(self):
        """
        Test that a valid email passes validation.
        """

        valid_email = "email23@gmail.com"
        validate_email = self.serializer.validate_email(valid_email)
        self.assertEqual(validate_email, valid_email)

    def test_validate_email_invalid(self):
        """
        Test that an invalid email raises a ValidationError.
        """

        # List of invalid emails.
        invalid_emails = [
            "plainaddress",
            "missingatsign.com",
            "@missingusername.com",
            "username@.com",
            "username@domain..com",
            "username@domain,com",
        ]

        for invalid_email in invalid_emails:
            with self.assertRaises(ValidationError):
                self.serializer.validate_email(invalid_email)

    def test_validate_email_already_exists(self):
        """
        Test that an email that already exists raises a ValidationError.
        """

        email = "email@gmail.com"

        UserFactory(email=email)

        serializer = UserRegisterSerializer(
            data={
                "email": email,
                "username": "testuser",
                "name": "Test",
                "password": "ValidPassword123!",
                "age": 30,
                "banner": "https://example.com/banner.png",
                "bio": "This bio is valid.",
                "lang": "es",
            }
        )

        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert serializer.errors["email"] == ["Email already exists."]

    # ==============================================
    # Test cases for password validation.
    # ==============================================
    def test_validate_password_valid(self):
        """
        Test that a validated password passes validation.
        """

        valid_password = "ValidPassword123!"
        validate_password = self.serializer.validate_password(valid_password)
        self.assertEqual(validate_password, valid_password)

    def test_validate_password_invalid(self):
        """
        Test that an invalid password raises a ValidationError.
        """

        # List of invalid passwords.
        invalid_passwords = [
            "short",
            "nouppercase123!",
            "NOLOWERCASE123!",
            "NoSpecialChar123",
            "NoNumber!",
            "ValidPasswordButTooLong" * 10,
        ]

        for invalid_password in invalid_passwords:
            with self.assertRaises(ValidationError):
                self.serializer.validate_password(invalid_password)

    # ==============================================
    # Test cases for avatar validation.
    # ==============================================
    def test_validate_avatar_valid_url(self):
        """
        Test that a valid avatar URL passes validation.
        """

        valid_url = "https://example.com/avatar.png"
        result = self.serializer.validate_avatar(valid_url)
        self.assertEqual(result, valid_url)

    def test_validate_avatar_empty_string(self):
        """
        Test that an empty staring avatar return None.
        """

        result = self.serializer.validate_avatar("")
        self.assertIsNone(result)

    def test_validate_avatar_invalid_url(self):
        """
        Test that an invalid avatar URL raises a ValidationError.
        """

        with self.assertRaises(ValidationError):
            self.serializer.validate_avatar("ftp://invalid-url.com")

    def test_validate_avatar_invalid_type(self):
        """
        Test that an invalid avatar type raises a ValidationError.
        """

        with self.assertRaises(ValidationError):
            self.serializer.validate_avatar({"url": "https://example.com"})

    # ==============================================
    # Test cases for username validation.
    # ==============================================
    def test_validate_username_valid(self):
        """
        Test that a valid username passes validation.
        """

        # List of valid usernames.
        valid_usernames = ["john_doe", "JaneDoe123", "user_name_valid", "validUser11"]
        for username in valid_usernames:
            validate_username = self.serializer.validate_username(username)
            self.assertEqual(validate_username, username)

    def test_validate_username_invalid(self):
        """
        Test that an invalid username raises a ValidationError.
        """

        # List of invalid usernames.
        invalid_usernames = [
            "ab",
            "1John@",
            "John@Doe",
            "John Doe!",
            "John-Doe#",
            "John+Doe",
            "j" * 16,
            "user name with spaces",
            "user!name@invalid",
        ]

        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                self.serializer.validate_username(username)

    def test_validate_username_already_exists(self):
        """
        Test that a username that already exists raises a ValidationError.
        """

        username = "existing_user"

        UserFactory(username=username)

        serializer = UserRegisterSerializer(
            data={
                "username": username,
            }
        )

        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert serializer.errors["username"] == ["Username already exists."]

    # ==============================================
    # Test cases for banner validation.
    # ==============================================
    def test_validate_banner_valid_url(self):
        """
        Test that a valid banner URL passes validation.
        """

        valid_url = "https://example.com/banner.png"
        result = self.serializer.validate_banner(valid_url)
        self.assertEqual(result, valid_url)

    def test_validate_banner_empty_string(self):
        """
        Test that an empty staring banner return None.
        """

        result = self.serializer.validate_banner("")
        self.assertIsNone(result)

    def test_validate_banner_invalid_url(self):
        """
        Test that an invalid banner URL raises a ValidationError.
        """

        with self.assertRaises(ValidationError):
            self.serializer.validate_banner("ftp://invalid-url.com")

    def test_validate_banner_invalid_type(self):
        """
        Test that an invalid banner type raises a ValidationError.
        """

        with self.assertRaises(ValidationError):
            self.serializer.validate_banner({"url": "https://example.com"})

    # ==============================================
    # Test cases for bio validation.
    # ==============================================
    def test_validate_bio_valid(self):
        """
        Test that a valid bio passes validation.
        """

        # List of valid bios.
        valid_bios = [
            "This is a sample bio.",
            "Hello! I'm a good person",
            None,
            "A" * 150,
        ]

        for bio in valid_bios:
            validate_bio = self.serializer.validate_bio(bio)
            self.assertEqual(validate_bio, bio)

    def test_validate_bio_invalid(self):
        """
        Test that an invalid bio raises a ValidationError.
        """

        # List of invalid bios.
        invalid_bio = "b" * 151
        with self.assertRaises(ValidationError) as cm:
            self.serializer.validate_bio(invalid_bio)

        exception = cm.exception
        self.assertIn("Bio must be at most 150 characters.", exception.detail)

    # ==============================================
    # Test cases for lang validation.
    # ==============================================
    def test_validate_default_lang(self):
        """
        Test that the default lang 'en' is set when lang is None or empty
        """

        default_lang_inputs = [None, ""]
        for lang in default_lang_inputs:
            validate_lang = self.serializer.validate_lang(lang)
            self.assertEqual(validate_lang, "en")

    def test_validate_lang_valid(self):
        """
        Test that a valid lang passes validation.
        """

        for lang in LANGUAGES:
            validate_lang = self.serializer.validate_lang(lang)
            self.assertEqual(validate_lang, lang)

    def test_validate_lang_invalid(self):
        """
        Test that an invalid lang raises a ValidationError.
        """

        invalid_langs = ["fr", "de", "it", 12]
        for lang in invalid_langs:
            with self.assertRaises(ValidationError) as cm:
                self.serializer.validate_lang(lang)
            exception = cm.exception
            self.assertIn(
                f"Language must be one of the following: {LANGUAGES}.", exception.detail
            )

    # ==============================================
    # Test cases for creating a user.
    # ==============================================
    def test_create_user_valid(self):
        """
        Test that a user can be created with valid data.
        """

        user_factory = UserFactory.build()

        user_data = {
            "name": user_factory.name,
            "age": user_factory.age,
            "email": user_factory.email,
            "password": user_factory.password,
            "avatar": user_factory.avatar,
            "username": user_factory.username,
            "banner": user_factory.banner,
            "bio": user_factory.bio,
            "lang": user_factory.lang,
            "recover_email_code": user_factory.recover_email_code,
        }

        serializer = UserRegisterSerializer(data=user_data)
        if not serializer.is_valid():
            print(serializer.errors)
        # self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Assert that the user was created successfully.
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.age == user_data["age"]
        assert user.email == user_data["email"]
        assert user.check_password(user_data["password"])
        assert user.avatar == user_data["avatar"]
        assert user.username == user_data["username"]
        assert user.banner == user_data["banner"]
        assert user.bio == user_data["bio"]
        assert user.lang == user_data["lang"]
        assert user.recover_email_code == user_data["recover_email_code"]

    def test_create_user_invalid(self):
        """
        Test that creating a user with invalid data raises a ValidationError.
        """

        user_data = {
            "name": "",
            "age": 17,
            "email": "email@invalid",
            "password": "short",
            "avatar": {},
            "username": "",
            "banner": "/image",
            "bio": [],
            "lang": "fr",
            "recover_email_code": "1245",
        }

        serializer = UserRegisterSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

        errors = serializer.errors
        self.assertIn("name", errors)
        self.assertIn("age", errors)
        self.assertIn("email", errors)
        self.assertIn("password", errors)
        self.assertIn("avatar", errors)
        self.assertIn("username", errors)
        self.assertIn("banner", errors)
        self.assertIn("bio", errors)
        self.assertIn("lang", errors)
        self.assertIn("recover_email_code", errors)
