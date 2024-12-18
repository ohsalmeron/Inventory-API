def test_create_movement(client, seed_data):
    payload = {
        "product_id": "00000000-0000-0000-0000-000000000001",
        "source_store_id": "StoreA",
        "target_store_id": "StoreB",
        "quantity": 10,
        "type": "TRANSFER"
    }
    response = client.post("/api/movements/", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Movement created successfully"  # Mensaje actualizado
