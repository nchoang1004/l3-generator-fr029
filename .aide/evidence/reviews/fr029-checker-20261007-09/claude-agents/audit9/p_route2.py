import boot
from boot import claims_of, route, part, truth
# FastAPI docs "Bigger Applications": from .routers import items (module given, level=1)
pkg = {
 "app/__init__.py": "",
 "app/routers/__init__.py": "",
 "app/routers/items.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/items')\n@router.get('/list')\ndef list_items():\n    return []\n",
 "app/main.py": "from fastapi import FastAPI\nfrom .routers import items\napp = FastAPI()\napp.include_router(items.router)\n",
}
c = claims_of(pkg)
base = route("app/routers/items.py::list_items", "app/routers/items.py:3-4", "/list", application="app/main.py:3")
print("docs pattern missing /items:", c.add_route(base))
# from . import items in same package as main
pkg3 = {
 "app/__init__.py": "",
 "app/items.py": pkg["app/routers/items.py"],
 "app/main.py": "from fastapi import FastAPI\nfrom . import items\napp = FastAPI()\napp.include_router(items.router)\n",
}
c = claims_of(pkg3)
b3 = route("app/items.py::list_items", "app/items.py:3-4", "/list", application="app/main.py:3")
print("from . import items (main) missing /items:", c.add_route(b3))
print("truth:", truth(pkg3, "app.main"))
