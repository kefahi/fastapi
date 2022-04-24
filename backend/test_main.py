from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_debug_sample():
    response = client.get("/debug/sample")
    assert response.status_code == 200
    assert response.json() == {'users': ['a', 'b', 'c']}
