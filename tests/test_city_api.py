from app.city.model import City


def test_create_city(client, country):
    response = client.post(
        "/cities",
        json={
            "city": "Karaj",
            "country_id": country.id,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["city"] == "Karaj"
    assert data["country_id"] == country.id


def test_create_city_country_not_found(client):
    response = client.post(
        "/cities",
        json={
            "city": "Karaj",
            "country_id": 9999,
        },
    )
    assert response.status_code == 404


def test_get_all_cities(client, city):
    response = client.get("/cities")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_city_by_id(client, city):
    response = client.get(f"/cities/{city.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == city.id
    assert "city" in data
    assert "country_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_city_not_found(client):
    response = client.get("/cities/999")
    assert response.status_code == 404


def test_delete_city(client, city, db_session):
    response = client.delete(f"/cities/{city.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(City, city.id)
    assert deleted is None


def test_delete_city_not_found(client):
    response = client.delete("/cities/999")
    assert response.status_code == 404
