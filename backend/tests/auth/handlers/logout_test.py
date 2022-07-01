from typing import Callable
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from common import crud
from common.responses import OkResponse

url = '/logout'


@pytest.mark.usefixtures(
    'mock__crud__user_tokens__get_user_id_by_token',
    'mock__crud__user_tokens__delete'
)
def test_ok(
        default_user_token: str,
        default_user_auth_headers: dict[str, str],
        test_client: TestClient
):
    response = test_client.delete(url, headers=default_user_auth_headers)
    assert response.status_code == 200
    assert response.json() == OkResponse().dict()
    # noinspection PyUnresolvedReferences
    crud.user_tokens.delete.assert_called_once_with(
        default_user_token,
        mock.ANY
    )


def test_unauthorized(
        unauthorized_test_factory: Callable[[str], None]
):
    unauthorized_test_factory(url)
