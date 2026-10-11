from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import clients
from app.db import Order, get_db

router = APIRouter()


@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    return {"id": order.id if order else None}


@router.post("/rates/refresh")
def refresh_rates():
    return clients.fetch_rates().json()


@router.post("/orders/{order_id}/reserve")
async def reserve(order_id: int, sku: str):
    response = await clients.reserve_stock(sku)
    return {"order": order_id, "status": response.status_code}
