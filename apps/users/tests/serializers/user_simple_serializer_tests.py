from django.test import TestCase

from apps.users.serializers import UserSimpleSerializer
from apps.users.UserFactory import UserFactory


class UserSimpleSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(
            name="Rich", username="richNR", avatar="https://rich.png"
        )
        self.expected_fields = {"id", "name", "username", "avatar"}

    def test_user_simple_serializer_output_expected_fields(self):
        """UserSimpleSerializer should be outputs the expected fields."""
        serializer = UserSimpleSerializer(self.user)
        data = serializer.data

        self.assertEqual(set(data.keys()), self.expected_fields)
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["name"], self.user.name)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["avatar"], self.user.avatar)

    def test_user_me_serializer_output_unexpected_fields(self):
        """
        UserSimpleSerializer does not include unexpected fields like email or password.
        """

        serializer = UserSimpleSerializer(self.user)
        data = serializer.data

        expected_fields_with_extras = {*self.expected_fields, "password", "email"}

        self.assertNotEqual(set(data.keys()), expected_fields_with_extras)

    def test_user_simple_serializer_read_only_fields(self):
        """UserSimpleSerializer should not allow changes to read-only fields."""

        original_name = self.user.name
        original_username = self.user.username
        original_avatar = self.user.avatar

        serializer = UserSimpleSerializer(
            instance=self.user,
            data={
                "name": "Rich1",
                "username": "rich123",
                "avatar": "https://avatar.png",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()

        self.assertEqual(updated_user.name, original_name)
        self.assertEqual(updated_user.username, original_username)
        self.assertEqual(updated_user.avatar, original_avatar)

    def test_user_me_serializer_with_null_avatar(self):
        """
        Test that UserMeSerializer handles a user with a null avatar correctly.
        """

        user = UserFactory(avatar=None)
        serializer = UserSimpleSerializer(user)
        data = serializer.data

        self.assertIsNone(data["avatar"])
