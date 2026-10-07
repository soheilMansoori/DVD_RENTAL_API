from app.actor.model import Actor


def test_create_actor(client):
    response = client.post(
        "/actors/", json={"first_name": "soheil", "last_name": "mansoori"}
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == "soheil"


def test_get_all_actors(client, db_session):
    actor = Actor(first_name="test", last_name="user")
    db_session.add(actor)
    db_session.commit()

    response = client.get("/actors/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["first_name"] == "test"


def test_search_actors(client, db_session):
    a1 = Actor(first_name="soheil", last_name="programmer")
    a2 = Actor(first_name="mohsen", last_name="developer")
    db_session.add_all([a1, a2])
    db_session.commit()

    response = client.get("/actors/search?q=soheil")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["first_name"] == "soheil"


def test_update_actor(client, db_session):
    actor = Actor(first_name="old", last_name="name")
    db_session.add(actor)
    db_session.commit()

    response = client.patch(
        f"/actors/{actor.id}", json={"first_name": "new_first_name"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "new_first_name"


def test_delete_actor(client, db_session):
    actor = Actor(first_name="delete", last_name="actor")
    db_session.add(actor)
    db_session.commit()

    response = client.delete(f"/actors/{actor.id}")
    assert response.status_code == 204

    check = db_session.query(Actor).filter(Actor.id == actor.id).first()
    assert check is None
