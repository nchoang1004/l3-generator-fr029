from fastapi import APIRouter

router = APIRouter(prefix="/orders")


@router.get("/{order_id}")
def read_order(order_id: int):
    return order_id
