from django.test import TestCase

from apps.follows.models import Follow
from apps.follows.serializers import FollowSerializer
from apps.users.UserFactory import UserFactory


class FollowSerializerTestCase(TestCase):
    def setUp(self):
        # Cria dois usuários para testes
        self.user_a = UserFactory.create(username="user_a")
        self.user_b = UserFactory.create(username="user_b")

        # Cria um follow entre user_a e user_b
        self.follow = Follow.objects.create(follower=self.user_a, following=self.user_b)

    def test_follow_serializer_output(self):
        """O serializer deve conter os campos corretos e os dados aninhados."""

        serializer = FollowSerializer(instance=self.follow)
        data = serializer.data

        # Verifica se todos os campos estão presentes
        self.assertIn("id", data)
        self.assertIn("follower", data)
        self.assertIn("following", data)
        self.assertIn("created_at", data)

        # Verifica se follower e following são dicionários com os campos do UserSimpleSerializer
        follower_data = data["follower"]
        following_data = data["following"]

        expected_user_fields = {"id", "username", "name", "avatar"}

        self.assertEqual(set(follower_data.keys()), expected_user_fields)
        self.assertEqual(set(following_data.keys()), expected_user_fields)

        # Verifica se os dados do follower estão corretos
        self.assertEqual(follower_data["id"], self.user_a.id)
        self.assertEqual(follower_data["username"], self.user_a.username)
        self.assertEqual(follower_data["name"], self.user_a.name)
        self.assertEqual(follower_data["avatar"], self.user_a.avatar)

        # Verifica se os dados do following estão corretos
        self.assertEqual(following_data["id"], self.user_b.id)
        self.assertEqual(following_data["username"], self.user_b.username)
        self.assertEqual(following_data["name"], self.user_b.name)
        self.assertEqual(following_data["avatar"], self.user_b.avatar)
