import httpx

from app.db import SessionLocal
from app.models.order import Order


class OrderService:
    def confirm(self, order_id: int):
        db = SessionLocal()
        order = db.query(Order).get(order_id)
        httpx.post("https://payment.internal/charge", json={"id": order_id})
        order.status = "confirmed"
        db.commit()
