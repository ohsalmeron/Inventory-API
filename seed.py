from app.database import SessionLocal
from app.models.product import Product
from app.models.inventory import Inventory

# Crear sesión
session = SessionLocal()

# Poblar la base de datos con productos de prueba
products = [
    Product(name="Varilla de Acero", description="Varilla corrugada para refuerzo", category="Acero", price=120.50, sku="VAR123"),
    Product(name="Lámina Galvanizada", description="Lámina de acero para techos", category="Acero", price=350.75, sku="LAM456"),
    Product(name="Perfil IPR", description="Perfil estructural tipo IPR", category="Estructuras", price=1500.00, sku="IPR789"),
    Product(name="Placa de Acero", description="Placa de acero para construcción", category="Placas", price=2000.00, sku="PLA101"),
]
session.add_all(products)
session.commit()

# Agregar inventario
inventories = [
    Inventory(product_id=products[0].id, store_id="store1", quantity=10, min_stock=5),
    Inventory(product_id=products[1].id, store_id="store1", quantity=15, min_stock=10),
    Inventory(product_id=products[2].id, store_id="store1", quantity=5, min_stock=3),
    Inventory(product_id=products[3].id, store_id="store2", quantity=2, min_stock=5),
]
session.add_all(inventories)
session.commit()

print("Seed data applied successfully!")
session.close()
