import pytest
from fastapi.testclient import TestClient

from main import app

pytest_plugins = [
    'tests.tests_plugins.users',
    'tests.tests_plugins.tests_factories',

    'tests.tests_plugins.mocks.factories',
    'tests.tests_plugins.mocks.crud.users',
    'tests.tests_plugins.mocks.crud.user_tokens',
]


@pytest.fixture(name='test_client')
def client() -> TestClient:
    return TestClient(app)
