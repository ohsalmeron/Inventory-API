from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    store_id = Column(Text, nullable=False)
    quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)
