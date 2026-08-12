from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    subscriber_id: int
    plan_name: str


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    feasibility_result: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    subscriber_id: int
    plan_name: str
    status: OrderStatus
    feasibility_result: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True