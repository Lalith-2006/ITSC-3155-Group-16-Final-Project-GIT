from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_get_menu():
    response = client.get("/menu/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_menu():
    response = client.get("/menu/search?category=vegan")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
