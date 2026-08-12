from sqlalchemy.orm import Session
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.feasibility_service import check_feasibility
from app.models.subscriber import Subscriber


def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(**order.model_dump(), status=OrderStatus.REQUESTED)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_all_orders(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Order | None:
    db_order = get_order(db, order_id)
    if not db_order:
        return None

    update_data = order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True

def run_feasibility_check(db: Session, order_id: int) -> Order | None:
    db_order = get_order(db, order_id)
    if not db_order:
        return None

    subscriber = db.query(Subscriber).filter(Subscriber.id == db_order.subscriber_id).first()
    if not subscriber:
        return None

    result = check_feasibility(subscriber.latitude, subscriber.longitude)

    db_order.feasibility_result = result["reason"]
    db_order.status = OrderStatus.FEASIBILITY_CHECKED if result["feasible"] else OrderStatus.REJECTED

    db.commit()
    db.refresh(db_order)
    return db_order