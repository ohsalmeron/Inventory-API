from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional
from uuid import UUID

class InventoryBase(BaseModel):
    product_id: UUID
    store_id: str
    quantity: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    min_stock: Optional[int] = None

class InventoryResponse(InventoryBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class InventoryByStoreResponse(BaseModel):
    product_id: UUID4
    name: str
    description: Optional[str]
    category: str
    price: float
    sku: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)
