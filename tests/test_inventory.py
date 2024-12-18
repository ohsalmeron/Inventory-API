def test_create_inventory(client):
    # Crear un producto primero
    product_payload = {
        "name": "Test Product",
        "description": "A test product",
        "category": "Electronics",
        "price": 200.0,
        "sku": "UNIQUE_SKU123"  # Cambiar a un SKU único
    }
    product_response = client.post("/api/products/", json=product_payload)
    assert product_response.status_code == 201
