from typing import Callable

import pytest

from common.db import User


@pytest.fixture()
def factory_mock__crud__users__get_by_username_or_email(
        mock_factory: Callable[[str], Callable[..., None]]
) -> Callable[..., None]:
    return mock_factory(
        'common.crud.users.get_by_username_or_email'
    )


@pytest.fixture()
def none_mock__crud__users__get_by_username_or_email(
        factory_mock__crud__users__get_by_username_or_email: Callable[..., None]  # noqa
) -> None:
    factory_mock__crud__users__get_by_username_or_email(
        return_value=None
    )


@pytest.fixture()
def default_mock__crud__users_get_by_username_or_email(
        default_user: User,
        factory_mock__crud__users__get_by_username_or_email: Callable[..., None]  # noqa
) -> None:
    factory_mock__crud__users__get_by_username_or_email(
        return_value=default_user
    )
