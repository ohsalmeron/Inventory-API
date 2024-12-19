def create_product_and_inventory(client):
    # Crear un nuevo producto para pruebas
    product_payload = {
        "name": "Producto Test",
        "description": "Descripción del producto test",
        "category": "Test",
        "price": 100.0,
        "sku": "TEST123"
    }
    response = client.post("/api/products/", json=product_payload)
    assert response.status_code == 201, f"Error al crear producto: {response.json()}"
    product_data = response.json()["data"]
    product_id = product_data["id"]

    # Agregar el producto al inventario de la tienda 'store1'
    inventory_payload = {
        "product_id": product_id,
        "store_id": "store1",
        "quantity": 10,
        "min_stock": 5
    }
    response = client.post("/api/inventory/", json=inventory_payload)
    assert response.status_code == 201, f"Error al agregar inventario: {response.json()}"
    return product_id


def test_create_product_and_inventory(client):
    product_id = create_product_and_inventory(client)
    # Verificar que el producto se agregó al inventario de store1
    response = client.get(f"/api/inventory/stores/store1/inventory")
    assert response.status_code == 200, f"Error al listar inventario: {response.json()}"
    inventory_data = response.json()["data"]
    product_in_store = next((item for item in inventory_data if item["product_id"] == product_id), None)
    assert product_in_store is not None, f"Producto {product_id} no encontrado en el inventario de store1"


def test_transfer_inventory_success(client):
    product_id = create_product_and_inventory(client)
    # Transferir 5 unidades del producto de store1 a store2
    transfer_payload = {
        "product_id": product_id,
        "source_store_id": "store1",
        "target_store_id": "store2",
        "quantity": 5,
        "type": "TRANSFER"
    }
    response = client.post("/api/inventory/transfer", json=transfer_payload)
    assert response.status_code == 201, f"Error al transferir inventario: {response.json()}"


def test_list_low_stock_alerts(client):
    # Crear un producto e inventario inicial
    product_id = create_product_and_inventory(client)

    # Reducir la cantidad del inventario para que caiga por debajo del stock mínimo
    inventory_update_payload = {
        "product_id": product_id,
        "store_id": "store1",
        "quantity": 3,  # Por debajo del mínimo configurado (5)
        "min_stock": 5
    }
    response = client.post("/api/inventory/", json=inventory_update_payload)
    assert response.status_code == 201, f"Error al actualizar inventario: {response.json()}"

    # Consultar alertas de inventario bajo
    response = client.get("/api/inventory/alerts")
    assert response.status_code == 200, f"Error al obtener alertas: {response.json()}"
    low_stock_data = response.json()["data"]

    # Verificar que el producto está en las alertas
    product_alert = next((item for item in low_stock_data if item["product_id"] == product_id), None)
    assert product_alert is not None, f"Producto {product_id} no está en las alertas de stock bajo"
    assert product_alert["quantity"] < 5, "La cantidad no está por debajo del mínimo configurado"
