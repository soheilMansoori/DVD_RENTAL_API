from app.staff.model import Staff


def test_create_staff(client, address, store):
    response = client.post(
        "/staffs",
        json={
            "username": "soheil",
            "password": "strongpassword123",
            "first_name": "Soheil",
            "last_name": "Mansoori",
            "email": "soheil@example.com",
            "address_id": address.id,
            "store_id": store.id,
            "active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["first_name"] == "Soheil"
    assert data["last_name"] == "Mansoori"
    assert data["email"] == "soheil@example.com"
    assert data["address_id"] == address.id
    assert data["store_id"] == store.id
    assert data["username"] == "soheil"


def test_create_staff_address_not_found(client, store):
    response = client.post(
        "/staffs",
        json={
            "first_name": "Soheil",
            "last_name": "Mansoori",
            "address_id": 9999,
            "email": "soheil@example.com",
            "store_id": store.id,
            "active": True,
            "username": "soheil",
            "password": "strongpassword123",
        },
    )
    assert response.status_code == 404


def test_create_staff_store_not_found(client, address):
    response = client.post(
        "/staffs",
        json={
            "first_name": "Soheil",
            "last_name": "Mansoori",
            "address_id": address.id,
            "email": "soheil@example.com",
            "store_id": 9999,
            "active": True,
            "username": "soheil",
            "password": "strongpassword123",
        },
    )
    assert response.status_code == 404


def test_get_all_staffs(client, staff):
    response = client.get("/staffs")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_staff_by_id(client, staff):
    response = client.get(f"/staffs/{staff.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == staff.id
    assert "first_name" in data
    assert "last_name" in data
    assert "email" in data
    assert "username" in data
    assert "address_id" in data
    assert "store_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_staff_not_found(client):
    response = client.get("/staffs/999")
    assert response.status_code == 404


def test_update_staff(client, staff, address, store):
    response = client.put(
        f"/staffs/{staff.id}",
        json={
            "first_name": "Updated",
            "last_name": "Staff",
            "address_id": address.id,
            "email": "updated@example.com",
            "store_id": store.id,
            "active": False,
            "username": "updated_user",
            "password": "newpassword123",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == staff.id
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Staff"
    assert data["email"] == "updated@example.com"
    assert data["username"] == "updated_user"
    assert data["active"] is False


def test_update_staff_not_found(client, address, store):
    response = client.put(
        "/staffs/999",
        json={
            "first_name": "Whatever",
            "last_name": "Whatever",
            "address_id": address.id,
            "email": "whatever@example.com",
            "store_id": store.id,
            "active": True,
            "username": "whatever",
            "password": "password123",
        },
    )
    assert response.status_code == 404


def test_patch_staff(client, staff):
    response = client.patch(
        f"/staffs/{staff.id}",
        json={
            "first_name": "Patched",
            "email": "patched@example.com",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == staff.id
    assert data["first_name"] == "Patched"
    assert data["email"] == "patched@example.com"


def test_patch_staff_not_found(client):
    response = client.patch(
        "/staffs/999",
        json={"first_name": "whatever"},
    )
    assert response.status_code == 404


def test_delete_staff(client, staff, db_session):
    response = client.delete(f"/staffs/{staff.id}")
    assert response.status_code == 204

    deleted = db_session.get(Staff, staff.id)
    assert deleted is None


def test_delete_staff_not_found(client):
    response = client.delete("/staffs/999")
    assert response.status_code == 404
