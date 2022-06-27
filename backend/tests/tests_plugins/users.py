import pytest

from common.db import User
from common.security.users import hash_password


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
