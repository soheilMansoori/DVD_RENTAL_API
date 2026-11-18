from app.film.model import Film


def test_create_film(client, language):
    response = client.post(
        "/films",
        json={
            "title": "The Matrix",
            "description": "A computer hacker learns about the true nature of reality",
            "release_year": 1999,
            "language_id": language.id,
            "rental_duration": 3,
            "rental_rate": 4.99,
            "length": 136,
            "replacement_cost": 19.99,
            "rating": "R",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == "The Matrix"
    assert data["language_id"] == language.id
    assert data["release_year"] == 1999


def test_create_film_language_not_found(client):
    response = client.post(
        "/films",
        json={
            "title": "The Matrix",
            "description": "A computer hacker learns about the true nature of reality",
            "release_year": 1999,
            "language_id": 9999,
            "rental_duration": 3,
            "rental_rate": 4.99,
            "length": 136,
            "replacement_cost": 19.99,
            "rating": "R",
        },
    )
    assert response.status_code == 404


def test_get_all_films(client, film):
    response = client.get("/films")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_film_by_id(client, film):
    response = client.get(f"/films/{film.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == film.id
    assert "title" in data
    assert "language_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_film_not_found(client):
    response = client.get("/films/999")
    assert response.status_code == 404


def test_update_film(client, film, language):
    response = client.put(
        f"/films/{film.id}",
        json={
            "title": "The Matrix Reloaded",
            "description": "Neo and the rebel leaders fight against the machines",
            "release_year": 2003,
            "language_id": language.id,
            "rental_duration": 5,
            "rental_rate": 5.99,
            "length": 138,
            "replacement_cost": 24.99,
            "rating": "R",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == film.id
    assert data["title"] == "The Matrix Reloaded"
    assert data["release_year"] == 2003
    assert data["rental_rate"] == 5.99


def test_update_film_not_found(client, language):
    response = client.put(
        "/films/999",
        json={
            "title": "Whatever",
            "description": "Some description that is long enough",
            "release_year": 2000,
            "language_id": language.id,
            "rental_duration": 3,
            "rental_rate": 4.99,
            "length": 120,
            "replacement_cost": 19.99,
            "rating": "PG",
        },
    )
    assert response.status_code == 404


def test_patch_film(client, film):
    response = client.patch(
        f"/films/{film.id}",
        json={
            "title": "Patched Film Title",
            "rental_rate": 3.99,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == film.id
    assert data["title"] == "Patched Film Title"
    assert data["rental_rate"] == 3.99


def test_patch_film_not_found(client):
    response = client.patch(
        "/films/999",
        json={"title": "whatever"},
    )
    assert response.status_code == 404


def test_delete_film(client, film, db_session):
    response = client.delete(f"/films/{film.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Film, film.id)
    assert deleted is None


def test_delete_film_not_found(client):
    response = client.delete("/films/999")
    assert response.status_code == 404
