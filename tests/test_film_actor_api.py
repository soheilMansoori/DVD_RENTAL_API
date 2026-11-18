from app.film_actor.model import FilmActor


def test_get_film_actors(client, film, film_actor):
    response = client.get(f"/films/{film.id}/actors")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_film_actors_film_not_found(client):
    response = client.get("/films/999/actors")
    assert response.status_code == 404


def test_add_actor_to_film(client, film, actor):
    response = client.post(
        f"/films/{film.id}/actors",
        json={"actor_id": actor.id},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["film_id"] == film.id
    assert data["actor_id"] == actor.id


def test_add_actor_to_film_film_not_found(client, actor):
    response = client.post(
        "/films/999/actors",
        json={"actor_id": actor.id},
    )
    assert response.status_code == 404


def test_add_actor_to_film_actor_not_found(client, film):
    response = client.post(
        f"/films/{film.id}/actors",
        json={"actor_id": 9999},
    )
    assert response.status_code == 404


def test_add_actor_to_film_already_exists(client, film, actor, film_actor):
    response = client.post(
        f"/films/{film.id}/actors",
        json={"actor_id": actor.id},
    )
    assert response.status_code == 409


def test_delete_actor_from_film(client, film, actor, film_actor, db_session):
    response = client.delete(f"/films/{film.id}/actors/{actor.id}")
    assert response.status_code == 204

    # check the relation is really deleted
    relation = db_session.get(FilmActor, (actor.id, film.id))
    assert relation is None


def test_delete_actor_from_film_not_found(client, film):
    response = client.delete(f"/films/{film.id}/actors/999")
    assert response.status_code == 404


def test_delete_actor_from_film_film_not_found(client, actor):
    response = client.delete(f"/films/999/actors/{actor.id}")
    assert response.status_code == 404
