from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="HTTP calls")
app.include_router(router)
