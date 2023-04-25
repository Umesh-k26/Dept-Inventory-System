from fastapi.testclient import TestClient
from main import app
from utils.auth import get_email, override_get_email
import pytest


client = TestClient(app)


if __name__ == "__main__":
    app.dependency_overrides[get_email] = override_get_email
    pytest.main()
    app.dependency_overrides = {}
