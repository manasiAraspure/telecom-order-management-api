from sqlalchemy.orm import Session
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate
from app.models.order import Order


def create_subscriber(db: Session, subscriber: SubscriberCreate) -> Subscriber:
    db_subscriber = Subscriber(**subscriber.model_dump())
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


def get_subscriber(db: Session, subscriber_id: int) -> Subscriber | None:
    return db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()


def get_all_subscribers(db: Session, skip: int = 0, limit: int = 100) -> list[Subscriber]:
    return db.query(Subscriber).offset(skip).limit(limit).all()


def delete_subscriber(db: Session, subscriber_id: int) -> str:
    db_subscriber = get_subscriber(db, subscriber_id)
    if not db_subscriber:
        return "not_found"

    has_orders = db.query(Order).filter(Order.subscriber_id == subscriber_id).first()
    if has_orders:
        return "has_orders"

    db.delete(db_subscriber)
    db.commit()
    return "deleted"