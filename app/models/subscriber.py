from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(String(20), nullable=False)   # used later for feasibility check
    longitude = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())