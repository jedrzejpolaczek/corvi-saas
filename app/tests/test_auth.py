from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    r = client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret"})
    assert r.status_code in (200, 201)
    r = client.post("/auth/login", json={"email": "alice@example.com", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
