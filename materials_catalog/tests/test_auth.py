from fastapi.testclient import TestClient

def test_register_and_login(client: TestClient):
    # Test registration
    response = client.post("/api/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    
    # Test login
    response = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"