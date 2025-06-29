from fastapi.testclient import TestClient


from .main import app

client = TestClient(app)

def test_service_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status" : "Active"}

#TODO : new event and status endpoints - mock db