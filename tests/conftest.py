import pytest

from .factories import PostFactory, UserFactory, LikeFactory


@pytest.fixture()
def post():
    yield PostFactory()


@pytest.fixture()
def user():
    user = UserFactory()
    user.set_password("123456")
    user.save()

    yield user


@pytest.fixture()
def like():
    yield LikeFactory
