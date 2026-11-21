from app.rental.model import Rental


def test_create_rental(client, inventory, customer, staff):
    response = client.post(
        "/rentals",
        json={
            "inventory_id": inventory.id,
            "customer_id": customer.id,
            "staff_id": staff.id,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["inventory_id"] == inventory.id
    assert data["customer_id"] == customer.id
    assert data["staff_id"] == staff.id
    assert "rental_date" in data
    assert data["return_date"] is None


def test_create_rental_inventory_not_found(client, customer, staff):
    response = client.post(
        "/rentals",
        json={
            "inventory_id": 9999,
            "customer_id": customer.id,
            "staff_id": staff.id,
        },
    )
    assert response.status_code == 404


def test_create_rental_customer_not_found(client, inventory, staff):
    response = client.post(
        "/rentals",
        json={
            "inventory_id": inventory.id,
            "customer_id": 9999,
            "staff_id": staff.id,
        },
    )
    assert response.status_code == 404


def test_create_rental_staff_not_found(client, inventory, customer):
    response = client.post(
        "/rentals",
        json={
            "inventory_id": inventory.id,
            "customer_id": customer.id,
            "staff_id": 9999,
        },
    )
    assert response.status_code == 404


def test_get_all_rentals(client, rental):
    response = client.get("/rentals")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_rental_by_id(client, rental):
    response = client.get(f"/rentals/{rental.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == rental.id
    assert "inventory_id" in data
    assert "customer_id" in data
    assert "staff_id" in data
    assert "rental_date" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_rental_not_found(client):
    response = client.get("/rentals/999")
    assert response.status_code == 404


def test_update_rental(client, rental, inventory, customer, staff):
    response = client.put(
        f"/rentals/{rental.id}",
        json={
            "inventory_id": inventory.id,
            "customer_id": customer.id,
            "staff_id": staff.id,
            "return_date": "2026-11-21T15:00:00",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == rental.id
    assert data["inventory_id"] == inventory.id
    assert data["customer_id"] == customer.id
    assert data["staff_id"] == staff.id
    assert data["return_date"] is not None


def test_update_rental_not_found(client, inventory, customer, staff):
    response = client.put(
        "/rentals/999",
        json={
            "inventory_id": inventory.id,
            "customer_id": customer.id,
            "staff_id": staff.id,
            "return_date": None,
        },
    )
    assert response.status_code == 404


def test_patch_rental(client, rental):
    response = client.patch(
        f"/rentals/{rental.id}",
        json={
            "return_date": "2026-11-21T16:30:00",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == rental.id
    assert data["return_date"] is not None


def test_patch_rental_not_found(client):
    response = client.patch(
        "/rentals/999",
        json={"return_date": "2026-11-21T16:30:00"},
    )
    assert response.status_code == 404


def test_delete_rental(client, rental, db_session):
    response = client.delete(f"/rentals/{rental.id}")
    assert response.status_code == 204

    deleted = db_session.get(Rental, rental.id)
    assert deleted is None


def test_delete_rental_not_found(client):
    response = client.delete("/rentals/999")
    assert response.status_code == 404
