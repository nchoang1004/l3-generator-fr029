# Dung cau truc that cua Netflix/dispatch: mot FastAPI() con duoc gan vao
# FastAPI() cha bang app.mount() cua Starlette, khong phai include_router().
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import api_router

app = FastAPI()
api = FastAPI()
frontend = FastAPI()

api.include_router(api_router)

# mount() gan thu muc tinh - khong co route nao, phai bo qua chu khong duoc
# coi day la mot chang trong cay prefix.
frontend.mount("/", StaticFiles(directory="static"), name="app")

app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
