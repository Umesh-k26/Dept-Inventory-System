from fastapi.testclient import TestClient
from main import app
from utils.auth import get_email, override_get_email
import pytest


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


if __name__ == "__main__":
    app.dependency_overrides[get_email] = override_get_email
    pytest.main()
    app.dependency_overrides = {}
