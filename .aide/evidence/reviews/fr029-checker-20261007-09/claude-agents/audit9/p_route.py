import boot
from boot import claims_of, route, part, truth
# R2: relative "from . import items" aggregator; R5: loop over routers
pkg = {
 "app/__init__.py": "",
 "app/routers/__init__.py": "",
 "app/routers/items.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/items')\n@router.get('/list')\ndef list_items():\n    return []\n",
 "app/routers/api.py": "from fastapi import APIRouter\nfrom . import items\napi_router = APIRouter()\napi_router.include_router(items.router)\n",
 "app/main.py": "from fastapi import FastAPI\nfrom app.routers.api import api_router\napp = FastAPI()\napp.include_router(api_router)\n",
}
c = claims_of(pkg)
base = route("app/routers/items.py::list_items", "app/routers/items.py:3-4", "/list", application="app/main.py:3")
print("R2 missing /items:", c.add_route(base))
c = claims_of(pkg)
print("R2 full:", c.add_route(dict(base, path_parts=[part("router_prefix", "/items", "app/routers/items.py:2"), part("decorator", "/list", "app/routers/items.py:3")])))
# absolute import control
pkg2 = dict(pkg); pkg2["app/routers/api.py"] = "from fastapi import APIRouter\nfrom app.routers import items\napi_router = APIRouter()\napi_router.include_router(items.router)\n"
c = claims_of(pkg2)
print("R2 control (absolute import) missing /items:", c.add_route(base))
print("truth R2:", truth(pkg, "app.main"))

loop = {
 "items.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/items')\n@router.get('/list')\ndef list_items():\n    return []\n",
 "users.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/users')\n@router.get('/me')\ndef me():\n    return {}\n",
 "main.py": "from fastapi import FastAPI\nimport items, users\napp = FastAPI()\nfor r in (items.router, users.router):\n    app.include_router(r, prefix='/api')\n",
}
c = claims_of(loop)
b = route("items.py::list_items", "items.py:3-4", "/list", application="main.py:3")
print("R5 missing both prefixes:", c.add_route(b))
c = claims_of(loop)
print("R5 only /items:", c.add_route(dict(b, path_parts=[part("router_prefix", "/items", "items.py:2"), part("decorator", "/list", "items.py:3")])))
print("truth R5:", truth(loop))
