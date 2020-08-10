import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    yield APIClient()


@pytest.fixture()
def logged_client(user):
    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"username": user.username, "password": "123456"},
        format="json",
    )
    assert response.status_code == 200
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION="Bearer {0}".format(token))
    client.user = user

    yield client


@pytest.fixture()
def datetime_to_representation():
    """
    datetime -> isoformat like rest framework does
    """

    def _datetime_to_representation(value):
        value = value.isoformat()
        if value.endswith("+00:00"):
            value = value[:-6] + "Z"

        return value

    yield _datetime_to_representation
