def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_not_found(client):
    response = client.get("/not_found")
    assert response.status_code == 404, "check not found status code"
    assert response.json() == {"detail": "Not Found"}, "check not found response body"
