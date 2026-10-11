from fastapi import APIRouter, Depends, HTTPException

from app import services
from app.db import get_db
from app.schemas import OrderIn, OrderOut

router = APIRouter(prefix="/orders")


@router.post("", response_model=OrderOut, status_code=201)
def create_order(payload: OrderIn, db=Depends(get_db)):
    return services.place_order(db, payload.product, payload.quantity)


@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db=Depends(get_db)):
    order = services.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404)
    return order
