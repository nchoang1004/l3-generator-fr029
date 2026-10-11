from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="Params and models")
app.include_router(router)
