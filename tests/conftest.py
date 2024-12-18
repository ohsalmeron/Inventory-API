import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.product import Product
from app.models.inventory import Inventory

# Configuración del cliente de pruebas
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Configuración de la base de datos para pruebas
@pytest.fixture(scope="function")
def db_session():
    # Use SessionLocal from your database configuration
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def seed_data(db_session):
    # Clear existing data
    db_session.query(Inventory).delete()
    db_session.query(Product).delete()

    # Seed product data
    product = Product(
        id="00000000-0000-0000-0000-000000000001",
        name="Test Product",
        description="A product for testing",
        category="Electronics",
        price=100.0,
        sku="TESTSKU123"
    )
    db_session.add(product)
    db_session.commit()

    # Seed inventory data
    inventory_a = Inventory(
        id="00000000-0000-0000-0000-000000000002",
        product_id=product.id,
        store_id="StoreA",
        quantity=50,
        min_stock=10
    )
    db_session.add(inventory_a)

    inventory_b = Inventory(
        id="00000000-0000-0000-0000-000000000003",
        product_id=product.id,
        store_id="StoreB",
        quantity=0,
        min_stock=5
    )
    db_session.add(inventory_b)
    db_session.commit()
