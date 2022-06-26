import pytest
from fastapi.testclient import TestClient

from common.responses import OkResponse

url = '/logout'


@pytest.mark.usefixtures(
    'mock__crud__user_tokens__get_user_id_by_token',
    'mock__crud__user_tokens__delete'
)
def test_ok(
        default_user_auth_headers: dict[str, str],
        test_client: TestClient
):
    response = test_client.delete(url, headers=default_user_auth_headers)
    assert response.status_code == 200
    assert response.json() == OkResponse().dict()


def test_unauthorized(
        unauthorized_test_factory
):
    unauthorized_test_factory(url)
