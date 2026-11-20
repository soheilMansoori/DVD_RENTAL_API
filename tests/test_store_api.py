from app.store.model import Store


def test_create_store(client, address, staff):
    response = client.post(
        "/stores",
        json={
            "address_id": address.id,
            "manager_staff_id": staff.id,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["address_id"] == address.id
    assert data["manager_staff_id"] == staff.id


def test_create_store_without_manager(client, address):
    response = client.post(
        "/stores",
        json={
            "address_id": address.id,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["address_id"] == address.id
    assert data["manager_staff_id"] is None


def test_create_store_address_not_found(client, staff):
    response = client.post(
        "/stores",
        json={
            "address_id": 9999,
            "manager_staff_id": staff.id,
        },
    )
    assert response.status_code == 404


def test_create_store_staff_not_found(client, address):
    response = client.post(
        "/stores",
        json={
            "address_id": address.id,
            "manager_staff_id": 9999,
        },
    )
    assert response.status_code == 404


def test_get_all_stores(client, store):
    response = client.get("/stores")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_store_by_id(client, store):
    response = client.get(f"/stores/{store.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == store.id
    assert "address_id" in data
    assert "manager_staff_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_store_not_found(client):
    response = client.get("/stores/999")
    assert response.status_code == 404


def test_update_store(client, store, address, staff):
    response = client.put(
        f"/stores/{store.id}",
        json={
            "address_id": address.id,
            "manager_staff_id": staff.id,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == store.id
    assert data["address_id"] == address.id
    assert data["manager_staff_id"] == staff.id


def test_update_store_not_found(client, address, staff):
    response = client.put(
        "/stores/999",
        json={
            "address_id": address.id,
            "manager_staff_id": staff.id,
        },
    )
    assert response.status_code == 404


def test_patch_store(client, store, staff):
    response = client.patch(
        f"/stores/{store.id}",
        json={
            "manager_staff_id": staff.id,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == store.id
    assert data["manager_staff_id"] == staff.id


def test_patch_store_not_found(client):
    response = client.patch(
        "/stores/999",
        json={"manager_staff_id": 1},
    )
    assert response.status_code == 404


def test_delete_store(client, store, db_session):
    response = client.delete(f"/stores/{store.id}")
    assert response.status_code == 204

    deleted = db_session.get(Store, store.id)
    assert deleted is None


def test_delete_store_not_found(client):
    response = client.delete("/stores/999")
    assert response.status_code == 404
