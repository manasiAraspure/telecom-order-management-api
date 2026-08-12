from pydantic import BaseModel, EmailStr
from datetime import datetime


class SubscriberBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    latitude: str
    longitude: str


class SubscriberCreate(SubscriberBase):
    """What the client sends when creating a subscriber."""
    pass


class SubscriberResponse(SubscriberBase):
    """What the API sends back."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  