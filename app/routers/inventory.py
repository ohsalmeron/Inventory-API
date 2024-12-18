from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.inventory import Inventory
from app.models.movement import Movement
from app.models.product import Product
from app.schemas.movement import MovementCreate
from app.schemas.inventory import InventoryCreate, InventoryByStoreResponse
from uuid import UUID
from datetime import datetime
from typing import List

router = APIRouter()

# Crear inventario
@router.post("/", response_model=dict, status_code=201)
def create_inventory(item: InventoryCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo registro de inventario.
    """
    try:
        db_item = Inventory(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return {
            "status": "success",
            "message": "Inventory record created successfully",
            "data": {
                "id": db_item.id,
                "product_id": db_item.product_id,
                "store_id": db_item.store_id,
                "quantity": db_item.quantity,
                "min_stock": db_item.min_stock
            }
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to create inventory record"
            }
        )

# Listar inventario por tienda
@router.get("/stores/{store_id}/inventory", response_model=dict)
def list_inventory_by_store(store_id: str, db: Session = Depends(get_db)):
    """
    Listar inventario para una tienda específica.
    """
    inventory = (
        db.query(
            Inventory.product_id,
            Product.name,
            Product.description,
            Product.category,
            Product.price,
            Product.sku,
            Inventory.quantity
        )
        .join(Product, Inventory.product_id == Product.id)
        .filter(Inventory.store_id == store_id)
        .all()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"No inventory found for store {store_id}"
            }
        )

    # Serializar resultados
    serialized_inventory = [
        {
            "product_id": row.product_id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "price": row.price,
            "sku": row.sku,
            "quantity": row.quantity
        }
        for row in inventory
    ]

    return {
        "status": "success",
        "message": f"Inventory retrieved successfully for store {store_id}",
        "data": serialized_inventory
    }

# Alertas de stock bajo
@router.get("/alerts", response_model=dict)
def get_stock_alerts(db: Session = Depends(get_db)):
    """
    Listar productos con stock por debajo del mínimo definido (min_stock).
    """
    alerts = (
        db.query(
            Inventory.product_id,
            Product.name,
            Product.description,
            Product.category,
            Product.price,
            Product.sku,
            Inventory.quantity
        )
        .join(Product, Inventory.product_id == Product.id)
        .filter(Inventory.quantity < Inventory.min_stock)
        .all()
    )

    if not alerts:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "No stock alerts found"
            }
        )

    # Serializar resultados
    serialized_alerts = [
        {
            "product_id": row.product_id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "price": row.price,
            "sku": row.sku,
            "quantity": row.quantity
        }
        for row in alerts
    ]

    return {
        "status": "success",
        "message": "Low stock alerts retrieved successfully",
        "data": serialized_alerts
    }

# Transferencia de productos entre tiendas
@router.post("/transfer", response_model=dict, status_code=201)
def transfer_product(transfer: MovementCreate, db: Session = Depends(get_db)):
    """
    Transferir stock entre tiendas.
    """
    if transfer.type != "TRANSFER":
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Invalid movement type for transfer"
            }
        )

    # Validar stock en tienda origen
    source_inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == transfer.product_id,
            Inventory.store_id == transfer.source_store_id
        )
        .first()
    )

    if not source_inventory or source_inventory.quantity < transfer.quantity:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Insufficient stock in source store"
            }
        )

    try:
        # Restar stock en tienda origen
        source_inventory.quantity -= transfer.quantity

        # Sumar stock en tienda destino
        target_inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == transfer.product_id,
                Inventory.store_id == transfer.target_store_id
            )
            .first()
        )

        if target_inventory:
            target_inventory.quantity += transfer.quantity
        else:
            # Si no existe en la tienda destino, crear un nuevo registro
            new_inventory = Inventory(
                product_id=transfer.product_id,
                store_id=transfer.target_store_id,
                quantity=transfer.quantity,
                min_stock=0
            )
            db.add(new_inventory)

        # Crear registro de movimiento
        db_movement = Movement(
            product_id=transfer.product_id,
            source_store_id=transfer.source_store_id,
            target_store_id=transfer.target_store_id,
            quantity=transfer.quantity,
            type="TRANSFER",
            timestamp=datetime.utcnow()
        )
        db.add(db_movement)

        db.commit()
        db.refresh(db_movement)

        return {
            "status": "success",
            "message": "Stock transferred successfully",
            "data": {
                "product_id": db_movement.product_id,
                "source_store_id": db_movement.source_store_id,
                "target_store_id": db_movement.target_store_id,
                "quantity": db_movement.quantity,
                "timestamp": db_movement.timestamp
            }
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "An error occurred during the transfer process"
            }
        )
