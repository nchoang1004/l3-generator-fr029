from fastapi import APIRouter

from app.api.items import router as items_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(items_router, prefix="/items")
