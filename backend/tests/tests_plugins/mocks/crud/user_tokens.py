from typing import Callable

import pytest
from aioredis import Redis

from common.db import User


@pytest.fixture()
def mock__crud__user_tokens__get_user_id_by_token(
        default_user: User,
        default_user_token: str,
        mock_factory: Callable[[str], Callable[..., None]]
) -> None:
    # noinspection PyUnusedLocal
    async def _mock(
            access_token: str,
            redis_cursor: Redis
    ) -> int | None:
        if access_token != default_user_token:
            return None
        return default_user.id

    mock_factory(
        'common.crud.user_tokens.get_user_id_by_token'
    )(_mock)


@pytest.fixture()
def mock__crud__user_tokens__create(
        default_user_token: str,
        mock_factory: Callable[[str], Callable[..., None]]
) -> None:
    mock_factory(
        'common.crud.user_tokens.create'
    )(return_value=default_user_token)


@pytest.fixture()
def mock__crud__user_tokens__delete(
        mock_factory: Callable[[str], Callable[..., None]]
) -> None:
    mock_factory(
        'common.crud.user_tokens.delete'
    )(return_value=None)
