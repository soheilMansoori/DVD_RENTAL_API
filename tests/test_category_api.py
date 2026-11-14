from app.category.model import Category


def test_create_category(client):
    response = client.post(
        "/categories",
        json={"name": "Action"},
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == "Action"


def test_get_all_categories(client, category):
    response = client.get("/categories")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_category_by_id(client, category):
    response = client.get(f"/categories/{category.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == category.id
    assert "name" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_category_not_found(client):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_delete_category(client, category, db_session):
    response = client.delete(f"/categories/{category.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Category, category.id)
    assert deleted is None


def test_delete_category_not_found(client):
    response = client.delete("/categories/999")
    assert response.status_code == 404
