from fastapi import FastAPI

from app.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")


def ping():
    return {"ok": True}


app.add_api_route("/ping", ping)
