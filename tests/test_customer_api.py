from app.customer.model import Customer


def test_create_customer(client, address, store):
    response = client.post(
        "/customers",
        json={
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


def test_create_customer_address_not_found(client, store):
    response = client.post(
        "/customers",
        json={
            "first_name": "Soheil",
            "last_name": "Mansoori",
            "email": "soheil@example.com",
            "address_id": 9999,
            "store_id": store.id,
            "active": True,
        },
    )
    assert response.status_code == 404


def test_create_customer_store_not_found(client, address):
    response = client.post(
        "/customers",
        json={
            "first_name": "Soheil",
            "last_name": "Mansoori",
            "email": "soheil@example.com",
            "address_id": address.id,
            "store_id": 9999,
            "active": True,
        },
    )
    assert response.status_code == 404


def test_get_all_customers(client, customer):
    response = client.get("/customers")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_customer_by_id(client, customer):
    response = client.get(f"/customers/{customer.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == customer.id
    assert "first_name" in data
    assert "last_name" in data
    assert "email" in data
    assert "address_id" in data
    assert "store_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_customer_not_found(client):
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_update_customer(client, customer, address, store):
    response = client.put(
        f"/customers/{customer.id}",
        json={
            "first_name": "Updated",
            "last_name": "Customer",
            "email": "updated@example.com",
            "address_id": address.id,
            "store_id": store.id,
            "active": False,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == customer.id
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Customer"
    assert data["email"] == "updated@example.com"
    assert data["active"] is False


def test_update_customer_not_found(client, address, store):
    response = client.put(
        "/customers/999",
        json={
            "first_name": "Whatever",
            "last_name": "Whatever",
            "email": "whatever@example.com",
            "address_id": address.id,
            "store_id": store.id,
            "active": True,
        },
    )
    assert response.status_code == 404


def test_patch_customer(client, customer):
    response = client.patch(
        f"/customers/{customer.id}",
        json={
            "first_name": "Patched",
            "email": "patched@example.com",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == customer.id
    assert data["first_name"] == "Patched"
    assert data["email"] == "patched@example.com"


def test_patch_customer_not_found(client):
    response = client.patch(
        "/customers/999",
        json={"first_name": "whatever"},
    )
    assert response.status_code == 404


def test_delete_customer(client, customer, db_session):
    response = client.delete(f"/customers/{customer.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Customer, customer.id)
    assert deleted is None


def test_delete_customer_not_found(client):
    response = client.delete("/customers/999")
    assert response.status_code == 404
