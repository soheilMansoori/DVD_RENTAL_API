from app.film_category.model import FilmCategory


def test_get_film_categories(client, film, film_category):
    response = client.get(f"/films/{film.id}/categories")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_film_categories_film_not_found(client):
    response = client.get("/films/999/categories")
    assert response.status_code == 404


def test_add_category_to_film(client, film, category):
    response = client.post(
        f"/films/{film.id}/categories",
        json={"category_id": category.id},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["film_id"] == film.id
    assert data["category_id"] == category.id


def test_add_category_to_film_film_not_found(client, category):
    response = client.post(
        "/films/999/categories",
        json={"category_id": category.id},
    )
    assert response.status_code == 404


def test_add_category_to_film_category_not_found(client, film):
    response = client.post(
        f"/films/{film.id}/categories",
        json={"category_id": 9999},
    )
    assert response.status_code == 404


def test_add_category_to_film_already_exists(client, film, category, film_category):
    response = client.post(
        f"/films/{film.id}/categories",
        json={"category_id": category.id},
    )
    assert response.status_code == 409


def test_delete_category_from_film(client, film, category, film_category, db_session):
    response = client.delete(f"/films/{film.id}/categories/{category.id}")
    assert response.status_code == 204

    # check the relation is really deleted
    relation = db_session.get(FilmCategory, (film.id, category.id))
    assert relation is None


def test_delete_category_from_film_not_found(client, film):
    response = client.delete(f"/films/{film.id}/categories/999")
    assert response.status_code == 404


def test_delete_category_from_film_film_not_found(client, category):
    response = client.delete(f"/films/999/categories/{category.id}")
    assert response.status_code == 404
