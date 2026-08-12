import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class OrderStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    FEASIBILITY_CHECKED = "FEASIBILITY_CHECKED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVATED = "ACTIVATED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False)
    plan_name = Column(String(100), nullable=False)          
    status = Column(Enum(OrderStatus), default=OrderStatus.REQUESTED, nullable=False)
    feasibility_result = Column(String(255), nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    subscriber = relationship("Subscriber", backref="orders")