from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.subscriber import SubscriberCreate, SubscriberResponse
from app.services import subscriber_service
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/subscribers", tags=["Subscribers"])


@router.post("/", response_model=SubscriberResponse, status_code=201)
def create_subscriber(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    return subscriber_service.create_subscriber(db, subscriber)


@router.get("/", response_model=list[SubscriberResponse])
def list_subscribers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return subscriber_service.get_all_subscribers(db, skip, limit)


@router.get("/{subscriber_id}", response_model=SubscriberResponse)
def get_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    db_subscriber = subscriber_service.get_subscriber(db, subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return db_subscriber

@router.delete("/{subscriber_id}", status_code=204)
def delete_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = subscriber_service.delete_subscriber(db, subscriber_id)
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Subscriber not found")
    if result == "has_orders":
        raise HTTPException(status_code=400, detail="Cannot delete subscriber with existing orders")