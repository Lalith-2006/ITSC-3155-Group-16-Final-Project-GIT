from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()



def test_get_orders():
    response = client.get("/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
