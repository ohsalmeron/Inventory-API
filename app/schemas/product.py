from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: Optional[float] = Field(ge=0, description="El precio debe ser mayor o igual a 0")
    sku: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None

class ProductResponse(ProductBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
