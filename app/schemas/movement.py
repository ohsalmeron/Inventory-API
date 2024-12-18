from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class MovementBase(BaseModel):
    product_id: UUID
    source_store_id: Optional[str] = None
    target_store_id: Optional[str] = None
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")
    type: str = Field(..., pattern="^(IN|OUT|TRANSFER)$", description="Type must be IN, OUT, or TRANSFER")

class MovementCreate(MovementBase):
    pass

class MovementResponse(MovementBase):
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True
