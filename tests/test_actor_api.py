from app.actor.model import Actor


def test_create_actor(client):
    response = client.post(
        "/actors", json={"first_name": "soheil", "last_name": "mansoori"}
    )

    assert response.status_code == 201

    data = response.json()
    assert "first_name" in data
    assert "last_name" in data
    assert "id" in data


def test_get_all_actors(client, actor):
    response = client.get("/actors")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1


def test_get_actor_by_id(client, actor):
    response = client.get(f"/actors/{actor.id}")
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_actor_not_found(client):
    response = client.get("/actors/999")
    assert response.status_code == 404


def test_update_actor(client, actor):
    response = client.patch(f"/actors/{actor.id}", json={"first_name": "new_name"})
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == actor.id
    assert data["first_name"] == "new_name"


def test_update_actor_not_found(client):
    response = client.patch("/actors/999", json={"first_name": "whatever"})
    assert response.status_code == 404


def test_delete_actor(client, actor, db_session):
    response = client.delete(f"/actors/{actor.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Actor, actor.id)
    assert deleted is None


def test_delete_actor_not_found(client):
    response = client.delete("/actors/999")
    assert response.status_code == 404
