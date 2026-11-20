from app.language.model import Language


def test_create_language(client):
    response = client.post(
        "/languages",
        json={"name": "English"},
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == "English"


def test_get_all_languages(client, language):
    response = client.get("/languages")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_language_by_id(client, language):
    response = client.get(f"/languages/{language.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == language.id
    assert "name" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_language_not_found(client):
    response = client.get("/languages/999")
    assert response.status_code == 404


def test_delete_language(client, language, db_session):
    response = client.delete(f"/languages/{language.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Language, language.id)
    assert deleted is None


def test_delete_language_not_found(client):
    response = client.delete("/languages/999")
    assert response.status_code == 404
