from fastapi import APIRouter

from app.hooks import registry

router = APIRouter(prefix="/orders")


@router.get("")
def list_orders():
    return []


@registry.get("/orders/cached")
def cached_orders():
    return []
