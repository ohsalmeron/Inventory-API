def test_transfer_inventory(client, seed_data):
    payload = {
        "product_id": "00000000-0000-0000-0000-000000000001",
        "source_store_id": "StoreA",
        "target_store_id": "StoreB",
        "quantity": 5,
        "type": "TRANSFER"
    }
    response = client.post("/api/inventory/transfer", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Stock transferred successfully"
