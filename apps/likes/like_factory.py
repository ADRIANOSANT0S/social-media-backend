import factory

from apps.likes.models import Like
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class LikeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
