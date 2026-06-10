import pytest
from fastapi.testclient import TestClient

from rag_api.core.config import Settings
from rag_api.main import create_app


@pytest.fixture()
def client() -> TestClient:
    settings = Settings(environment="test")
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
