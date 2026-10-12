import boot
from boot import claims_of, route, part, truth, reminders
# DP1: router-level dependencies (FastAPI docs Bigger Applications)
src = ("from typing import Annotated\nfrom fastapi import FastAPI, APIRouter, Depends, Header\n"
       "def get_token_header(x_token: Annotated[str, Header()]):\n    return x_token\n"
       "router = APIRouter(dependencies=[Depends(get_token_header)])\n"
       "@router.get('/items')\ndef items():\n    return []\n"
       "app = FastAPI()\napp.include_router(router)\n")
c = claims_of({"main.py": src})
r = route("main.py::items", "main.py:6-7", "/items", application="main.py:9")
print("DP1 add_route:", c.add_route(r))
print("DP1 reminders:", repr(reminders(c)))
print("DP1 all open problems:", [p for p in c.open_problems([]) if 'Route' in p])
print("truth DP1:", truth({"main.py": src}))
# DP1b: include_router(..., dependencies=[...])
src2 = src.replace("router = APIRouter(dependencies=[Depends(get_token_header)])", "router = APIRouter()").replace(
    "app.include_router(router)", "app.include_router(router, dependencies=[Depends(get_token_header)])")
c = claims_of({"main.py": src2}); c.add_route(r)
print("DP1b reminders:", repr(reminders(c)), "| truth:", truth({"main.py": src2}))
# DP2: Annotated alias in handler signature, dependency omitted by agent
src3 = ("from typing import Annotated\nfrom fastapi import FastAPI, Depends\n"
        "def pagination(page: int = 1, size: int = 50):\n    return page, size\n"
        "PageDep = Annotated[tuple, Depends(pagination)]\n"
        "app = FastAPI()\n@app.get('/items')\ndef items(p: PageDep):\n    return []\n")
c = claims_of({"main.py": src3})
r3 = route("main.py::items", "main.py:7-8", "/items", application="main.py:6")
print("DP2 add_route (deps=[]):", c.add_route(r3))
print("DP2 reminders:", repr(reminders(c)), [p for p in c.open_problems([]) if 'Route' in p])
c = claims_of({"main.py": src3})
print("DP2 with dep declared:", c.add_route(dict(r3, dependencies=[{"name": "pagination", "at": "main.py:8"}])), repr(reminders(c)))
print("truth DP2:", truth({"main.py": src3}))
# control: same dependency inline Depends -> reminder of missing dependency
src4 = src3.replace("def items(p: PageDep):", "def items(p=Depends(pagination)):")
c = claims_of({"main.py": src4}); c.add_route(r3)
print("control inline:", [p for p in c.open_problems([]) if 'Route' in p])
