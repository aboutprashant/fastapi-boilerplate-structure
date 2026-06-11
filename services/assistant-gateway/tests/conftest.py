import jwt
import pytest
from fastapi.testclient import TestClient

from gateway.core.config import Settings
from gateway.main import create_app

TEST_JWT_SECRET = "test-secret-with-at-least-32-bytes"


@pytest.fixture()
def client() -> TestClient:
    settings = Settings(environment="test", jwt_secret=TEST_JWT_SECRET)
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def auth_header() -> dict[str, str]:
    payload = {
        "organization_uuid": "org-1",
        "user_uuid": "user-1",
        "user_email": "user@example.com",
        "role": "project_user",
        "project_uuids": ["project-a"],
    }
    token = jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}
