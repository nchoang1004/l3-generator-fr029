from fastapi import APIRouter, Depends

from app.services.order import OrderService

router = APIRouter(prefix="/orders")


def get_service() -> OrderService:
    return OrderService()


@router.post("/{order_id}/confirm")
def confirm_order(order_id: int, svc: OrderService = Depends(get_service)):
    return svc.confirm(order_id)
