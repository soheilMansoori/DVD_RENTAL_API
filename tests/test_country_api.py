from app.country.model import Country


def test_create_country(client):
    response = client.post(
        "/countries",
        json={"country": "Iran"},
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["country"] == "Iran"


def test_get_all_countries(client, country):
    response = client.get("/countries")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_country_by_id(client, country):
    response = client.get(f"/countries/{country.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == country.id
    assert "country" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_country_not_found(client):
    response = client.get("/countries/999")
    assert response.status_code == 404


def test_delete_country(client, country, db_session):
    response = client.delete(f"/countries/{country.id}")
    assert response.status_code == 204

    # check it really deleted
    deleted = db_session.get(Country, country.id)
    assert deleted is None


def test_delete_country_not_found(client):
    response = client.delete("/countries/999")
    assert response.status_code == 404
