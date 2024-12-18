from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    sku: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None

class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True
