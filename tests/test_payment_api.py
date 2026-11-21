from app.payment.model import Payment


def test_create_payment(client, customer, staff, rental):
    response = client.post(
        "/payments",
        json={
            "customer_id": customer.id,
            "staff_id": staff.id,
            "rental_id": rental.id,
            "amount": "4.99",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["customer_id"] == customer.id
    assert data["staff_id"] == staff.id
    assert data["rental_id"] == rental.id
    assert data["amount"] == "4.99"
    assert "payment_date" in data


def test_create_payment_customer_not_found(client, staff, rental):
    response = client.post(
        "/payments",
        json={
            "customer_id": 9999,
            "staff_id": staff.id,
            "rental_id": rental.id,
            "amount": "4.99",
        },
    )
    assert response.status_code == 404


def test_create_payment_staff_not_found(client, customer, rental):
    response = client.post(
        "/payments",
        json={
            "customer_id": customer.id,
            "staff_id": 9999,
            "rental_id": rental.id,
            "amount": "4.99",
        },
    )
    assert response.status_code == 404


def test_create_payment_rental_not_found(client, customer, staff):
    response = client.post(
        "/payments",
        json={
            "customer_id": customer.id,
            "staff_id": staff.id,
            "rental_id": 9999,
            "amount": "4.99",
        },
    )
    assert response.status_code == 404


def test_get_all_payments(client, payment):
    response = client.get("/payments")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_payment_by_id(client, payment):
    response = client.get(f"/payments/{payment.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == payment.id
    assert "customer_id" in data
    assert "staff_id" in data
    assert "rental_id" in data
    assert "amount" in data
    assert "payment_date" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_payment_not_found(client):
    response = client.get("/payments/999")
    assert response.status_code == 404


def test_update_payment(client, payment, customer, staff, rental):
    response = client.put(
        f"/payments/{payment.id}",
        json={
            "customer_id": customer.id,
            "staff_id": staff.id,
            "rental_id": rental.id,
            "amount": "9.99",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == payment.id
    assert data["amount"] == "9.99"


def test_update_payment_not_found(client, customer, staff, rental):
    response = client.put(
        "/payments/999",
        json={
            "customer_id": customer.id,
            "staff_id": staff.id,
            "rental_id": rental.id,
            "amount": "9.99",
        },
    )
    assert response.status_code == 404


def test_patch_payment(client, payment):
    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "amount": "7.50",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == payment.id
    assert data["amount"] == "7.50"


def test_patch_payment_not_found(client):
    response = client.patch(
        "/payments/999",
        json={"amount": "7.50"},
    )
    assert response.status_code == 404


def test_delete_payment(client, payment, db_session):
    response = client.delete(f"/payments/{payment.id}")
    assert response.status_code == 204

    deleted = db_session.get(Payment, payment.id)
    assert deleted is None


def test_delete_payment_not_found(client):
    response = client.delete("/payments/999")
    assert response.status_code == 404
