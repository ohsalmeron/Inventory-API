from sqlalchemy import Column, String, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(Text)
    price = Column(Numeric)
    sku = Column(String, unique=True, nullable=False)
