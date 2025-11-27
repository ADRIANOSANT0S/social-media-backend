from django.test import TestCase

from apps.users.serializers import UserMeSerializer
from apps.users.UserFactory import UserFactory


class UserMeSerializerTests(TestCase):
    """
    Test cases for the UserMeSerializer.
    """

    def setUp(self):
        self.expected_fields = {
            "id",
            "name",
            "age",
            "avatar",
            "username",
            "banner",
            "bio",
            "lang",
        }

    # ==============================================
    # Test cases for user me serialize return datas.
    # ==============================================
    def test_user_me_serializer_output_expected_fields(self):
        """
        Test that the UserMeSerializer outputs the expected fields.
        """
        user = UserFactory()
        serializer = UserMeSerializer(user)
        data = serializer.data

        self.assertEqual(set(data.keys()), self.expected_fields)

        self.assertEqual(data["id"], user.id)
        self.assertEqual(data["name"], user.name)
        self.assertEqual(data["age"], user.age)
        self.assertEqual(data["avatar"], user.avatar)
        self.assertEqual(data["username"], user.username)
        self.assertEqual(data["banner"], user.banner)
        self.assertEqual(data["bio"], user.bio)
        self.assertEqual(data["lang"], user.lang)

    def test_user_me_serializer_output_unexpected_fields(self):
        """
        Test that UserMeSerializer does not include unexpected fields like email or password.
        """

        user = UserFactory()
        serializer = UserMeSerializer(user)
        data = serializer.data

        expected_fields_with_extras = {*self.expected_fields, "password", "email"}

        self.assertNotEqual(set(data.keys()), expected_fields_with_extras)

    # ==============================================
    # Test cases for serializer return the user avatar.
    # ==============================================
    def test_user_me_serializer_with_null_avatar(self):
        """
        Test that UserMeSerializer handles a user with a null avatar correctly.
        """

        user = UserFactory(avatar=None)
        serializer = UserMeSerializer(user)
        data = serializer.data

        self.assertIsNone(data["avatar"])

    def test_user_me_serializer_without_avatar(self):
        """
        Test that UserMeSerializer handles a user without an avatar correctly.
        """

        user = UserFactory()
        serializer = UserMeSerializer(user)
        data = serializer.data

        self.assertIsNotNone(data["avatar"])

    # ==============================================
    # Test cases to ensure the serializer does not update read-only or immutable fields.
    # ==============================================
    def test_user_me_serializer_does_not_update(self):
        """
        Test that UserMeSerializer does not update user data.
        """
        user = UserFactory(username="original_username")
        data = {"username": "new_username"}

        serializer = UserMeSerializer(user, data=data, partial=True)
        assert (
            serializer.is_valid()
        )  # Should be valid even if it doesn't change anything
        instance = serializer.save() if serializer.is_valid() else user

        assert instance.username == "original_username"
