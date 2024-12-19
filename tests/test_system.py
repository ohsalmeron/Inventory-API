from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Filtrar una categoria inexistente
def test_list_products_filter_no_results():
    response = client.get("/api/products/?category=nonexistent")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "No products found",
        "data": []
    }

# Obtener un producto inexistente
def test_get_product_not_found():
    response = client.get("/api/products/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {"status": "error", "message": "Product not found"}
    }

# Obtener un producto con id inválido
def test_get_product_invalid_id():
    response = client.get("/api/products/invalid-id")
    assert response.status_code == 422  # Unprocessable Entity
    assert "uuid_parsing" in str(response.json())

# Crear un producto con campos vacios
def test_create_product_missing_fields():
    response = client.post("/api/products/", json={"name": "Test Product"})
    assert response.status_code == 422
    assert "Field required" in str(response.json())

# Actualizar un producto con precio de texto
def test_create_product_invalid_price():
    response = client.post("/api/products/", json={
        "name": "Test Product",
        "category": "Test",
        "price": "invalid",
        "sku": "123"
    })
    assert response.status_code == 422
    assert "Input should be a valid number" in str(response.json())

# Actualizar un producto inexistente
def test_update_product_not_found():
    response = client.put(
        "/api/products/00000000-0000-0000-0000-000000000000",
        json={"name": "Updated Product", "category": "General", "price": 100.00}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": {"status": "error", "message": "Product not found"}
    }


# Borrar un producto inexistente
def test_delete_product_not_found():
    response = client.delete("/api/products/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {"status": "error", "message": "Product not found"}
    }

# Listar todos los productos
def test_list_products(client, seed_products):
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 9 # Verificamos que los 9 productos estén listados

# Filtrar por categoría
def test_filter_products_by_category(client, seed_products):
    response = client.get("/api/products/?category=Acero")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2  # Solo los productos de categoría "Acero"

# Filtrar por rango de precio
def test_filter_products_by_price(client, seed_products):
    response = client.get("/api/products/?price_min=100&price_max=500")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 5  # Productos dentro del rango de precio

# Obtener detalle de un producto
def test_get_product_by_id(client, seed_products):
    product_id = seed_products[0].id  # Obtener ID del primer producto
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Varilla de Acero"

# Crear un nuevo producto
def test_create_product(client):
    new_product = {
        "name": "Nuevo Producto",
        "description": "Un producto de prueba",
        "category": "General",
        "price": 100.00,
        "sku": "SKU002"
    }
    response = client.post("/api/products/", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == "Nuevo Producto"
    assert data["data"]["sku"] == new_product["sku"]  # Validar contra el SKU original


# Borrar un producto
def test_delete_product(client, seed_products):
    product_id = seed_products[0].id  # Obtener ID del primer producto
    response = client.delete(f"/api/products/{product_id}")
    assert response.status_code == 200
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 404  # Producto eliminado no debe existir

# Filtrar productos gratis
def test_filter_free_products(client, seed_products):
    response = client.get("/api/products/?price_max=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Producto Gratis"

# Categorías similares
def test_filter_similar_categories(client, seed_products):
    response = client.get("/api/products/?category=Acero")
    assert response.status_code == 200
    data = response.json()
    assert all("Acero Especial" not in p["category"] for p in data["data"])

# Duplicados prohibidos al crear
def test_create_duplicate_sku(client, seed_products):
    duplicate_product = {
        "name": "Producto Duplicado",
        "description": "Un duplicado",
        "category": "Duplicados",
        "price": 100.00,
        "sku": "VAR123".lower()
    }
    response = client.post("/api/products/", json=duplicate_product)
    assert response.status_code == 400
    assert response.json() == {
        "detail": {"status": "error", "message": "A product with this SKU already exists"}
    }

# Actualizar producto sin descripción
def test_update_product_description(client, seed_products):
    product_id = seed_products[4].id  # ID del producto gratis
    updates = {"description": "Descripción añadida", "category": "Promoción", "price": 0.0}  # Validar categoría y precio
    response = client.put(f"/api/products/{product_id}", json=updates)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["description"] == "Descripción añadida"


# Prueba de paginación
def test_pagination(client, seed_products):
    response = client.get("/api/products/?limit=3&offset=6")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 3  # Últimos 3 productos en el seed

# Filtros combinados
def test_combined_filters(client, seed_products):
    response = client.get("/api/products/?category=Acero&price_min=100&price_max=500")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2  # "Varilla de Acero" y "Lámina Galvanizada"

# Nombre o descripción extrema
def test_long_name_and_special_description(client):
    long_name = "Producto " + "A" * 245  # Nombre de 255 caracteres
    special_description = "Descripción con caracteres especiales: ©®, emojis 😃🚀"
    product = {
        "name": long_name,
        "description": special_description,
        "category": "Especial",
        "price": 999.99,
        "sku": "LONG001"
    }
    response = client.post("/api/products/", json=product)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == long_name
    assert data["data"]["description"] == special_description

# Precio negativo
def test_invalid_price(client):
    invalid_product = {
        "name": "Producto Inválido",
        "description": "Con precio negativo",
        "category": "Errores",
        "price": -100.00,
        "sku": "ERR001"
    }
    response = client.post("/api/products/", json=invalid_product)
    assert response.status_code == 422
    assert "price" in str(response.json())

# Insensibilidad del SKU
def test_sku_case_insensitivity(client, seed_products):
    duplicate_sku = {
        "name": "Producto Duplicado",
        "description": "Un duplicado en SKU insensible a mayúsculas",
        "category": "Duplicados",
        "price": 100.00,
        "sku": "var123"
    }
    response = client.post("/api/products/", json=duplicate_sku)
    assert response.status_code == 400
    assert "already exists" in str(response.json())

# Verificar Productos Sin Categoría
def test_create_product_without_category(client):
    product_without_category = {
        "name": "Producto Sin Categoría",
        "description": "No tiene categoría",
        "price": 150.00,
        "sku": "NOCAT001"
    }
    response = client.post("/api/products/", json=product_without_category)
    assert response.status_code == 422
    assert "category" in str(response.json())

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

def test_transfer_insufficient_stock(client):
    product_id = create_product_and_inventory(client)

    # Intentar transferir más cantidad de la disponible
    transfer_payload = {
        "product_id": product_id,
        "source_store_id": "store1",
        "target_store_id": "store2",
        "quantity": 15,  # Más de los 10 disponibles
        "type": "TRANSFER"
    }
    response = client.post("/api/inventory/transfer", json=transfer_payload)
    assert response.status_code == 400, f"Error esperado no ocurrió: {response.json()}"

    # Validar el mensaje de error
    assert "detail" in response.json(), "La respuesta no contiene el campo 'detail'"
    error_detail = response.json()["detail"]
    assert "message" in error_detail, "El detalle del error no contiene el campo 'message'"
    assert error_detail["message"] == f"Insufficient stock in store store1. Available: 10, Required: 15", (
        f"Mensaje de error incorrecto: {error_detail['message']}"
    )