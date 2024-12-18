import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.product import Product
from app.models.inventory import Inventory

# Create a test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Set up and tear down the database
@pytest.fixture(scope="function")
def seed_data():
    db = SessionLocal()
    try:
        # Add a product
        product = Product(
            id="00000000-0000-0000-0000-000000000001",
            name="Test Product",
            description="A product for testing",
            category="Electronics",
            price=100.0,
            sku="TESTSKU123"
        )
        db.add(product)
        db.commit()  # Commit product to make it available for FK references

        # Add inventory
        inventory = Inventory(
            id="00000000-0000-0000-0000-000000000002",
            product_id=product.id,  # Ensure FK references an existing product
            store_id="StoreA",
            quantity=50,
            min_stock=10
        )
        db.add(inventory)
        db.commit()  # Commit inventory
    finally:
        db.close()
