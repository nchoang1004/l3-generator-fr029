from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from app.routers import orders

app = FastAPI(title="Exclusions")
app.include_router(orders.router)


def health():
    return {"ok": True}


async def plain(request):
    return PlainTextResponse("ok")


async def ws_echo(websocket):
    await websocket.accept()
    await websocket.close()


app.add_api_route("/health", health, methods=["GET"])
app.add_route("/plain", plain)
app.add_websocket_route("/ws", ws_echo)
