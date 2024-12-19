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

@pytest.fixture
def seed_inventory(db_session, seed_products):
    inventory_data = [
        {
            "id": str(uuid.uuid4()),
            "product_id": seed_products[0].id,  # Relacionar con un producto existente
            "store_id": "store1",
            "quantity": 20,
            "min_stock": 5
        },
        {
            "id": str(uuid.uuid4()),
            "product_id": seed_products[1].id,
            "store_id": "store1",
            "quantity": 3,  # Stock bajo
            "min_stock": 10
        }
    ]
    inventories = [Inventory(**data) for data in inventory_data]
    db_session.add_all(inventories)
    db_session.commit()
    return inventory_data