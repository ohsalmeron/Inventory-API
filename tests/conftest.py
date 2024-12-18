import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.product import Product
from app.models.inventory import Inventory

# Configuración del cliente de pruebas
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Configuración de la base de datos para pruebas
@pytest.fixture(scope="function", autouse=True)
def db_session():
    # Crear una sesión para la base de datos
    session = SessionLocal()
    
    # Limpiar la base de datos antes de cada test
    session.query(Product).delete()
    session.commit()

    yield session  # Proveer la sesión para los tests

    # Rollback después de cada test
    session.rollback()
    session.close()

# Poblar la base de datos con productos de prueba
@pytest.fixture(scope="function")
def seed_products(db_session):
    products = [
        Product(
            name="Varilla de Acero",
            description="Varilla corrugada para refuerzo",
            category="Acero",
            price=120.50,
            sku="VAR123"
        ),
        Product(
            name="Lámina Galvanizada",
            description="Lámina de acero para techos",
            category="Acero",
            price=350.75,
            sku="LAM456"
        ),
        Product(
            name="Perfil IPR",
            description="Perfil estructural tipo IPR",
            category="Estructuras",
            price=1500.00,
            sku="IPR789"
        ),
        Product(
            name="Placa de Acero",
            description="Placa de acero para construcción",
            category="Placas",
            price=2000.00,
            sku="PLA101"
        ),
        # Casos adicionales
        Product(
            name="Producto Gratis",
            description=None,
            category="Promoción",
            price=0.00,
            sku="FREE001"
        ),
        Product(
            name="Producto Premium",
            description="Producto con precio alto",
            category="Lujo",
            price=99999.99,
            sku="PREM001"
        ),
        Product(
            name="Producto Similar",
            description="Producto con SKU diferente",
            category="General",
            price=100.00,
            sku="sku001"
        ),
        Product(
            name="Producto Similar",
            description="Producto con SKU diferente",
            category="General",
            price=100.00,
            sku="SKU001"
        ),
        Product(
            name="Producto Substring",
            description="Un producto con categoría como substring",
            category="Acero Especial",
            price=500.00,
            sku="SUB001"
        )
    ]
    db_session.add_all(products)
    db_session.commit()
    return products

@pytest.fixture(scope="function")
def seed_inventory(db_session, seed_products):
    inventories = [
        Inventory(
            product_id=seed_products[0].id,  # Varilla de Acero
            store_id="store1",
            quantity=10,
            min_stock=5
        ),
        Inventory(
            product_id=seed_products[1].id,  # Lámina Galvanizada
            store_id="store1",
            quantity=15,
            min_stock=10
        ),
        Inventory(
            product_id=seed_products[2].id,  # Perfil IPR
            store_id="store1",
            quantity=5,
            min_stock=3
        ),
        Inventory(
            product_id=seed_products[3].id,  # Placa de Acero
            store_id="store2",
            quantity=2,
            min_stock=5
        ),
        Inventory(
            product_id=seed_products[4].id,  # Producto Gratis
            store_id="store2",
            quantity=0,
            min_stock=1
        ),
        Inventory(
            product_id=seed_products[5].id,  # Producto Premium
            store_id="store2",
            quantity=1,
            min_stock=0
        )
    ]
    db_session.add_all(inventories)
    db_session.commit()

    # Log para verificar
    print("Seed Inventory Data:")
    for inv in inventories:
        print(f"Product ID: {inv.product_id}, Store ID: {inv.store_id}, Quantity: {inv.quantity}, Min Stock: {inv.min_stock}")

    return inventories
