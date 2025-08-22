import pytest
from fastapi.testclient import TestClient
from corvi_api.app import app

@pytest.fixture
def client():
    return TestClient(app)
