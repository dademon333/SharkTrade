from typing import Callable

import pytest
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_factory(
        mocker: MockerFixture
) -> Callable[[str], Callable[..., None]]:
    """Currying mock factory.

    It's easier to explain on example:

    ===========================================
    # /tests/mocks/crud/users.py

    @pytest.fixture()
    def factory_mock__crud__users__get(
            mock_factory: Callable[[str], Callable[..., None]]
    ) -> Callable[..., None]:
        return mock_factory(
            'common.crud.users.get'
        )


    @pytest.fixture()
    def default_mock__crud__users_get(
            default_user: User,
            factory_mock__crud__users__get: Callable[..., None]
    ) -> None:
        factory_mock__crud__users__get(
            return_value=default_user
        )

    ===========================================
    # /tests/auth/handlers/login

    @pytest.mark.usefixtures(
        'default_mock__crud__users_get'
    )
    def test_ok(
            default_user: User,
            test_client: TestClient
    ):
        ...

    ===========================================

    So, in this case common.crud.users.get will return default_user .
    """
    def _callable(path: str) -> Callable[..., None]:
        def _factory(*args, **kwargs):
            mocker.patch(path, *args, **kwargs)
        return _factory
    return _callable
