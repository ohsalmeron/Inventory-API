from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.movement import Movement
from app.schemas.movement import MovementCreate, MovementResponse
from uuid import UUID

router = APIRouter()

# Listar todos los movimientos
@router.get("/", response_model=dict)
def list_movements(db: Session = Depends(get_db)):
    """
    Listar todos los movimientos registrados en la base de datos.
    """
    movements = db.query(Movement).all()
    
    # Serializar los movimientos
    serialized_movements = [
        {
            "id": movement.id,
            "product_id": movement.product_id,
            "source_store_id": movement.source_store_id,
            "target_store_id": movement.target_store_id,
            "quantity": movement.quantity,
            "type": movement.type,
            "timestamp": movement.timestamp
        }
        for movement in movements
    ]
    
    return {
        "status": "success",
        "message": "Movements retrieved successfully",
        "data": serialized_movements
    }

# Crear un nuevo movimiento
@router.post("/", response_model=dict, status_code=201)
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo movimiento (ingreso, salida o transferencia).
    """
    if movement.type == "TRANSFER" and not (movement.source_store_id and movement.target_store_id):
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Transfer must include source_store_id and target_store_id"
            }
        )
    try:
        db_movement = Movement(**movement.model_dump())
        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        return {
            "status": "success",
            "message": "Movement created successfully",
            "data": {
                "id": db_movement.id,
                "product_id": db_movement.product_id,
                "source_store_id": db_movement.source_store_id,
                "target_store_id": db_movement.target_store_id,
                "quantity": db_movement.quantity,
                "type": db_movement.type,
                "timestamp": db_movement.timestamp
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to create movement",
                "error": str(e)
            }
        )

# Obtener un movimiento por ID
@router.get("/{movement_id}", response_model=dict)
def get_movement(movement_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener los detalles de un movimiento por su ID.
    """
    movement = db.query(Movement).filter(Movement.id == movement_id).first()
    if not movement:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "Movement not found"
            }
        )
    
    return {
        "status": "success",
        "message": "Movement retrieved successfully",
        "data": {
            "id": movement.id,
            "product_id": movement.product_id,
            "source_store_id": movement.source_store_id,
            "target_store_id": movement.target_store_id,
            "quantity": movement.quantity,
            "type": movement.type,
            "timestamp": movement.timestamp
        }
    }
