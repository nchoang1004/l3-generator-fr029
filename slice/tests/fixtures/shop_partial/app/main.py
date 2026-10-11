import os

from fastapi import FastAPI

from app.routes import router

app = FastAPI()
app.include_router(router, prefix=os.environ["API_PREFIX"])
