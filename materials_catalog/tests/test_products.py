from fastapi.testclient import TestClient
import json

def test_product_filtering(client: TestClient):
    # Create a product first (with auth)
    # First get auth token
    login_response = client.post("/api/login", json={
        "email": "admin@example.com",
        "password": "secret"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create test product
    product_data = {
        "name": "Test Filter Product",
        "category": "TestCategory",
        "attributes": {
            "thickness_mm": 25.0,
            "coverage_sqm": 5.0
        }
    }
    
    response = client.post("/api/products", json=product_data, headers=headers)
    assert response.status_code == 200
    
    # Test filtering by category
    response = client.get("/api/products?category=TestCategory")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(p["category"] == "TestCategory" for p in data)

def test_unit_conversion(client: TestClient):
    # Create test product
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    
    if products:
        # Test metric (default)
        product = products[0]
        assert "thickness_mm" in product
        assert "coverage_sqm" in product
        
        # Test imperial
        response = client.get("/api/products?unit_system=imperial")
        assert response.status_code == 200
        imperial_products = response.json()
        
        if imperial_products:
            imperial_product = imperial_products[0]
            # Should still have original fields
            assert "thickness_mm" in imperial_product
            assert "coverage_sqm" in imperial_product
            # And converted fields
            assert "thickness_in" in imperial_product
            assert "coverage_sqft" in imperial_product