from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Order


def save_order(db: Session, product: str, quantity: int) -> Order:
    order = Order(product=product, quantity=quantity)
    db.add(order)
    db.commit()
    return order


def find_order(db: Session, order_id: int) -> Order | None:
    return db.scalars(select(Order).where(Order.id == order_id)).first()
