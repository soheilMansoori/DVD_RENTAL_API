from app.inventory.model import Inventory


def test_create_inventory(client, film, store):
    response = client.post(
        "/inventories",
        json={
            "film_id": film.id,
            "store_id": store.id,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["film_id"] == film.id
    assert data["store_id"] == store.id


def test_create_inventory_film_not_found(client, store):
    response = client.post(
        "/inventories",
        json={
            "film_id": 9999,
            "store_id": store.id,
        },
    )
    assert response.status_code == 404


def test_create_inventory_store_not_found(client, film):
    response = client.post(
        "/inventories",
        json={
            "film_id": film.id,
            "store_id": 9999,
        },
    )
    assert response.status_code == 404


def test_get_all_inventories(client, inventory):
    response = client.get("/inventories")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_inventory_by_id(client, inventory):
    response = client.get(f"/inventories/{inventory.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == inventory.id
    assert "film_id" in data
    assert "store_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_inventory_not_found(client):
    response = client.get("/inventories/999")
    assert response.status_code == 404


def test_delete_inventory(client, inventory, db_session):
    response = client.delete(f"/inventories/{inventory.id}")
    assert response.status_code == 204

    deleted = db_session.get(Inventory, inventory.id)
    assert deleted is None


def test_delete_inventory_not_found(client):
    response = client.delete("/inventories/999")
    assert response.status_code == 404
