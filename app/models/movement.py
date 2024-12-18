from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class Movement(Base):
    __tablename__ = "movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    source_store_id = Column(Text, nullable=True)
    target_store_id = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(Text, CheckConstraint("type IN ('IN', 'OUT', 'TRANSFER')"), nullable=False)
