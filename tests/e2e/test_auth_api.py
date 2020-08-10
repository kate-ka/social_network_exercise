import json

import pytest
from django.contrib.auth import get_user_model

from tests.factories import UserFactory

SIGN_UP_URL = "/api/auth/signup/"

SIGN_IN_URL = "/api/auth/login/"

User = get_user_model()


@pytest.mark.django_db
def test_sign_up(api_client):
    response = api_client.post(
        SIGN_UP_URL,
        data=json.dumps({"username": "foo@bar.com", "password": "qwerty"}),
        content_type="application/json",
    )

    assert response.status_code == 201

    response = response.json()

    assert User.objects.filter(username=response["username"]).exists()


@pytest.mark.django_db
def test_successful_login(api_client):
    user = UserFactory(username="foo@bar.com")
    user.set_password("qwerty")
    user.save()

    response = api_client.post(
        SIGN_IN_URL,
        data=json.dumps({"username": "foo@bar.com", "password": "qwerty"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    response = response.json()
    assert "refresh" and "access" in response


@pytest.mark.django_db
def test_unsuccessful_login(api_client):
    user = UserFactory(username="foo@bar.com")
    user.set_password("qwerty")
    user.save()

    response = api_client.post(
        SIGN_IN_URL,
        data=json.dumps({"username": "foo@bar.com", "password": "wrong password"}),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No active account found with the given credentials"
    }
