from fastapi import APIRouter

import settings
from items import router as items_router

api_router = APIRouter(prefix=settings.API_PREFIX)
api_router.include_router(items_router)
