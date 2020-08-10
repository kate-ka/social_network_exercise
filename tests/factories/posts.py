import factory
from django.utils import timezone
from factory import fuzzy

from apps.posts.models import Post, Like
from .accounts import UserFactory


class PostFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText(length=200)
    text = fuzzy.FuzzyText(length=512)
    created = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    updated = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Post


class LikeFactory(factory.DjangoModelFactory):
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    created = fuzzy.FuzzyDateTime(start_dt=timezone.now())

    class Meta:
        model = Like
