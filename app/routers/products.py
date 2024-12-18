from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from uuid import UUID
from typing import Optional, List

router = APIRouter()

# Listar todos los productos con filtros y paginación
@router.get("/", response_model=dict)
def list_products(
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    stock_min: Optional[int] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    # Filtros por categoría y precio
    if category:
        query = query.filter(Product.category == category)
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    # Filtro de stock mínimo
    if stock_min is not None:
        query = query.join(Inventory, Product.id == Inventory.product_id) \
                     .group_by(Product.id) \
                     .having(func.sum(Inventory.quantity) >= stock_min)

    products = query.offset(offset).limit(limit).all()
    return {
        "status": "success",
        "message": "Products retrieved successfully",
        "data": [ProductResponse.model_validate(product).model_dump() for product in products]
    }

# Obtener un producto por ID
@router.get("/{product_id}", response_model=dict)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Product not found"}
        )
    return {
        "status": "success",
        "message": "Product retrieved successfully",
        "data": ProductResponse.model_validate(product).model_dump()
    }

# Crear un nuevo producto
@router.post("/", response_model=dict, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Validar SKU único
    if db.query(Product).filter(Product.sku == product.sku).first():
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "A product with this SKU already exists"}
        )
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {
        "status": "success",
        "message": "Product created successfully",
        "data": ProductResponse.model_validate(db_product).model_dump()
    }

# Actualizar un producto existente
@router.put("/{product_id}", response_model=dict)
def update_product(product_id: UUID, updates: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Product not found"}
        )
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return {
        "status": "success",
        "message": "Product updated successfully",
        "data": ProductResponse.model_validate(db_product).model_dump()
    }

# Eliminar un producto
@router.delete("/{product_id}", response_model=dict, status_code=200)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Product not found"}
        )
    db.delete(db_product)
    db.commit()
    return {"status": "success", "message": "Product deleted successfully"}
