from app.address.model import Address


def test_create_address(client, city):
    response = client.post(
        "/addresses",
        json={
            "address": "gohardasht street 9",
            "district": "karaj center",
            "phone": "09121234567",
            "city_id": city.id,
            "address2": "building number 12 floor 3",
            "postal_code": "31456",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["address"] == "gohardasht street 9"
    assert data["district"] == "karaj center"
    assert data["city_id"] == city.id


def test_create_address_city_not_found(client):
    response = client.post(
        "/addresses",
        json={
            "address": "gohardasht street 9",
            "district": "karaj center",
            "phone": "09121234567",
            "city_id": 9999,
        },
    )
    assert response.status_code == 404


def test_get_all_addresses(client, address):
    response = client.get("/addresses")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_address_by_id(client, address):
    response = client.get(f"/addresses/{address.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == address.id
    assert "address" in data
    assert "district" in data
    assert "phone" in data
    assert "city_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_address_not_found(client):
    response = client.get("/addresses/999")
    assert response.status_code == 404


def test_update_address(client, address, city):
    response = client.put(
        f"/addresses/{address.id}",
        json={
            "address": "new gohardasht street 15",
            "district": "azadi square",
            "phone": "09351234567",
            "city_id": city.id,
            "address2": "unit 8 second floor",
            "postal_code": "31890",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == address.id
    assert data["address"] == "new gohardasht street 15"
    assert data["district"] == "azadi square"
    assert data["phone"] == "09351234567"


def test_update_address_not_found(client, city):
    response = client.put(
        "/addresses/999",
        json={
            "address": "some long enough address",
            "district": "some district",
            "phone": "09120000000",
            "city_id": city.id,
        },
    )
    assert response.status_code == 404


def test_patch_address(client, address):
    response = client.patch(
        f"/addresses/{address.id}",
        json={
            "address": "patched address street",
            "phone": "09121112233",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == address.id
    assert data["address"] == "patched address street"
    assert data["phone"] == "09121112233"


def test_patch_address_not_found(client):
    response = client.patch(
        "/addresses/999",
        json={"address": "whatever long enough"},
    )
    assert response.status_code == 404


def test_delete_address(client, address, db_session):
    response = client.delete(f"/addresses/{address.id}")
    assert response.status_code == 204

    deleted = db_session.get(Address, address.id)
    assert deleted is None


def test_delete_address_not_found(client):
    response = client.delete("/addresses/999")
    assert response.status_code == 404
