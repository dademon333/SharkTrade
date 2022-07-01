from unittest import mock

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from auth.schemas import LoginErrorResponse
from common import crud
from common.db import User


class LoginForm(BaseModel):
    username: str
    password: str


url = '/login'


@pytest.mark.usefixtures(
    'default_mock__crud__users_get_by_username_or_email',
    'mock__crud__user_tokens__create'
)
def test_ok(
        default_user_token: str,
        default_user_password: str,
        default_user: User,
        test_client: TestClient
):
    body = LoginForm(
        username=default_user.username,
        password=default_user_password
    )
    response = test_client.post(url, data=body.dict())
    assert response.status_code == 200
    assert response.json()['access_token'] == default_user_token
    assert response.json()['token_type'] == 'bearer'
    # noinspection PyUnresolvedReferences
    crud.user_tokens.create.assert_called_once_with(
        default_user.id,
        mock.ANY
    )


@pytest.mark.usefixtures(
    'default_mock__crud__users_get_by_username_or_email',
    'mock__crud__user_tokens__create'
)
def test_wrong_password(
        default_user: User,
        test_client: TestClient
):
    body = LoginForm(
        username=default_user.username,
        password='aabb'
    )
    response = test_client.post(url, data=body.dict())
    assert response.status_code == 403
    assert response.json() == LoginErrorResponse().dict()


@pytest.mark.usefixtures(
    'default_mock__crud__users_get_by_username_or_email',
    'mock__crud__user_tokens__create'
)
def test_unknown_user(
        test_client: TestClient
):
    body = LoginForm(
        username='1',
        password='aabb'
    )
    response = test_client.post(url, data=body.dict())
    assert response.status_code == 403
    assert response.json() == LoginErrorResponse().dict()
