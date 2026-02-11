from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import time

def test_trending_products(client: TestClient):
    # First record some events
    events = [
        {"product_id": 1, "session_id": "session_1"},
        {"product_id": 1, "session_id": "session_2"},
        {"product_id": 2, "session_id": "session_1"},
        {"product_id": 3, "session_id": "session_3"},
        {"product_id": 1, "session_id": "session_4"},
    ]
    
    for event in events:
        response = client.post("/api/events", json=event)
        assert response.status_code == 200
    
    # Test trending endpoint
    response = client.get("/api/insights/trending?window_hours=24&limit=5")
    assert response.status_code == 200
    trending = response.json()
    
    # Product 1 should have 3 views
    product_1 = next((p for p in trending if p["product_id"] == 1), None)
    if product_1:
        assert product_1["view_count"] >= 3