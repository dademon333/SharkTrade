import pytest
from fastapi.testclient import TestClient

from main import app

pytest_plugins = [
    'tests_plugins.users',
    'tests_plugins.tests_factories',

    'tests_plugins.mocks.factories',
    'tests_plugins.mocks.crud.users',
    'tests_plugins.mocks.crud.user_tokens',
]


@pytest.fixture(name='test_client')
def client() -> TestClient:
    return TestClient(app)
