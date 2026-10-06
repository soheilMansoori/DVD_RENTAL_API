from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_not_found():
    response = client.get("/not_found")
    assert response.status_code == 404, "check not found status code"
    assert response.json() == {"detail": "Not Found"}, "check not found response body"
