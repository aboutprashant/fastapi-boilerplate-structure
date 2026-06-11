import jwt
import pytest
from fastapi.testclient import TestClient

from kb.core.config import Settings
from kb.main import create_app

TEST_JWT_SECRET = "test-secret-with-at-least-32-bytes"


@pytest.fixture()
def client(tmp_path) -> TestClient:
    settings = Settings(
        environment="test",
        database_url=f"sqlite+aiosqlite:///{tmp_path}/kb.db",
        jwt_secret=TEST_JWT_SECRET,
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


def make_token(projects: list[str], role: str = "project_user") -> str:
    payload = {
        "organization_uuid": "org-1",
        "user_uuid": "user-1",
        "user_email": "user@example.com",
        "role": role,
        "project_uuids": projects,
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")


@pytest.fixture()
def auth_header() -> dict[str, str]:
    return {"Authorization": f"Bearer {make_token(['project-a', 'project-b'], 'org_admin')}"}
