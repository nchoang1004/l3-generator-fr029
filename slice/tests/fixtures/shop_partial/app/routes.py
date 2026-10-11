from fastapi import APIRouter

router = APIRouter(prefix="/v1")


@router.get("/orders")
def list_orders():
    return []
