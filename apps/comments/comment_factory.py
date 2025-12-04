import factory

from apps.comments.models import Comment
from apps.posts.post_factory import PostFactory
from apps.users.UserFactory import UserFactory


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    content = factory.Faker("text", max_nb_chars=300)
