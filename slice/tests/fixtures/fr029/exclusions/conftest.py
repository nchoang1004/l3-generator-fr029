import pytest
from fastapi import FastAPI

from app.routers import internal


@pytest.fixture
def debug_app():
    app = FastAPI()
    app.include_router(internal.router, prefix="/internal")
    return app
