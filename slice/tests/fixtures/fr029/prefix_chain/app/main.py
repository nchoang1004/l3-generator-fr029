import os

from fastapi import FastAPI

from app.api import admin, health, legacy
from app.api.api import api_router
from app.config import settings
from app.sub import sub_app


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    @app.get("/")
    def root():
        return {"ok": True}

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(health.router, prefix="/public")
    app.include_router(health.router, prefix="/internal")
    app.include_router(legacy.router, prefix="/v1")
    app.include_router(admin.router, prefix=os.environ["ADMIN_PREFIX"])
    app.mount("/sub", sub_app)
    return app
