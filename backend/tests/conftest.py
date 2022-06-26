from typing import Callable

import pytest
from fastapi.testclient import TestClient

from common.db import User
from common.responses import UnauthorizedResponse
from common.security.users import hash_password
from main import app

pytest_plugins = [
    'tests.mocks.factories',

    'tests.mocks.crud.users',
    'tests.mocks.crud.user_tokens',
]


@pytest.fixture(name='test_client')
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def default_user(default_user_password: str) -> User:
    return User(
        id=1,
        username='user',
        password=hash_password(1, default_user_password)
    )


@pytest.fixture()
def default_user_password() -> str:
    return '12345'


@pytest.fixture()
def default_user_token() -> str:
    # Let's ignore that password should be hashed
    return 'super_secret_token'


@pytest.fixture()
def default_user_auth_headers(default_user_token: str) -> dict[str, str]:
    # Let's ignore that password should be hashed
    return {'Authorization': f'Bearer {default_user_token}'}


@pytest.fixture()
def unauthorized_test_factory(
        mock__crud__user_tokens__get_user_id_by_token,
        mock__crud__user_tokens__delete,
        test_client: TestClient
) -> Callable[[str], None]:
    def _test(url: str) -> None:
        response = test_client.delete(url)
        assert response.status_code == 401
        assert response.json() == UnauthorizedResponse().dict()
    return _test
