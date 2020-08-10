import factory

from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}@example.org")

    class Meta:
        model = get_user_model()
