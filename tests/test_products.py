def test_create_product(client):
    payload = {
        "name": "New Product",
        "description": "A new product",
        "category": "Electronics",
        "price": 200.0,
        "sku": "NEW12345"
    }
    response = client.post("/api/products/", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Product created successfully"

def test_get_products(client, seed_data):
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
