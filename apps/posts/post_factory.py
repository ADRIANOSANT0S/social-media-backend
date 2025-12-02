import factory

from apps.posts.models import Post
from apps.users.UserFactory import UserFactory


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)

    blocks = [
        {"type": "text", "content": "Sample text for testing"},
        {"type": "image", "url": "http://example.com/test-image.jpg"},
        {"type": "text", "content": "Another sample text for testing"},
        {"type": "image", "url": "http://example.com/test-image2.jpg"},
    ]
