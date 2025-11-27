import random

import factory
from django.contrib.auth import get_user_model
from faker import Faker

from apps.core.utils import generate_code

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances for testing."""

    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(lambda: fake.name()[:100].strip())
    age = factory.Faker("random_int", min=18, max=100)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "deFault@pAssword123")
    avatar = factory.Faker("image_url")
    username = factory.LazyFunction(lambda: fake.user_name()[:15].strip())
    lang = factory.LazyFunction(lambda: random.choice(["en", "pt", "es"]))
    banner = factory.Faker("image_url")
    bio = factory.LazyFunction(lambda: fake.text()[:150].strip())
    recover_email_code = factory.LazyFunction(lambda: generate_code())
    is_active = True
    is_staff = False
