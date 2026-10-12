import asyncio
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.cache import get_snapshot
from app.config import settings
from app.refresh import refresh_loop, refresh_once
from app.routers import fx


@asynccontextmanager
async def lifespan(app: FastAPI):
    await refresh_once()
    stop = asyncio.Event()
    task = asyncio.create_task(refresh_loop(stop))
    try:
        yield
    finally:
        stop.set()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="FX-Service", version="0.1.0", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "message": "invalid request parameters"}},
    )


@app.exception_handler(redis.RedisError)
async def redis_error_handler(request: Request, exc: redis.RedisError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "RATES_UNAVAILABLE",
                "message": "rate store temporarily unavailable",
            }
        },
    )


app.include_router(fx.router)


@app.get("/healthz")
def healthz() -> JSONResponse:
    snap = get_snapshot(settings.base_currency)
    if snap is None:
        return JSONResponse(
            status_code=503,
            content={"status": "no_data", "rates_age_seconds": None},
        )
    return JSONResponse(
        status_code=200,
        content={"status": "ok", "rates_age_seconds": snap.age_seconds()},
    )
