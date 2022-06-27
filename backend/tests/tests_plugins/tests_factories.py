from typing import Callable

import pytest
from fastapi.testclient import TestClient

from common.responses import UnauthorizedResponse


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
