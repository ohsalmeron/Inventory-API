def test_create_product(client):
    payload = {
        "name": "Test Product",
        "description": "A test product",
        "category": "Electronics",
        "price": 200.0,
        "sku": "TEST123"
    }
    response = client.post("/api/products/", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test Product"
    assert data["sku"] == "TEST123"
