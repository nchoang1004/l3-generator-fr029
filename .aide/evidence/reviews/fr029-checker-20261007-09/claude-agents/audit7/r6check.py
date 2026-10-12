"""Vong 7: kiem lai cac muc vong 6 va bien the. Chay: cwd=slice, TMP=audit7."""
import sys
sys.path[:0] = ['.', 'tests']
from test_checker_counterexamples import claims_of, route, http, reminders  # noqa


def sus(c):
    return [s["at"] for s in c.suspects()]


print("== vong6 bien the ==")
# 1. thu tu prefix: ba muc
c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nouter = APIRouter(prefix='/o')\n"
                          "r = APIRouter(prefix='/v1')\n@r.get('/x')\ndef e():\n    return {}\n"
                          "outer.include_router(r, prefix='/m')\napp.include_router(outer, prefix='/api')\n"})
base = route("main.py::e", "main.py:5-6", "/x", application="main.py:2")
P = lambda k, v, l: {"kind": k, "value": v, "at": f"main.py:{l}"}
x = P("decorator", "/x", 5)
good = [P("include_prefix", "/api", 9), P("router_prefix", "/o", 3), P("include_prefix", "/m", 8), P("router_prefix", "/v1", 4), x]
bad = [P("include_prefix", "/api", 9), P("include_prefix", "/m", 8), P("router_prefix", "/o", 3), P("router_prefix", "/v1", 4), x]
print("order3 good", c.add_route(dict(base, path_parts=good)))
print("order3 bad (/api/m/o/v1/x)", c.add_route(dict(base, path_parts=bad)))

# 2. helper khong goi
c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\n"
                          "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\n"
                          "def attach(target, router):\n    target.include_router(router)\n"})
print("unused helper", c.add_route(route("main.py::e", "main.py:4-5", "/x", application="main.py:2")))

# 3. URL tuyet doi + config_at; bien the: url la bien tuyet doi
c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\nsettings = SimpleNamespace(URL='https://base.example')\n"
                       "c = httpx.Client(base_url=settings.URL)\nOTHER = 'https://other.example/x'\ndef e():\n    return c.get(OTHER)\n"})
print("absolute via var + config_at", c.add_http({"at": "h.py:7", "library": "httpx", "method": "GET",
                                                  "target": {"kind": "config", "value": "settings.URL", "config_at": "h.py:4"}}))

# 4. thuoc tinh client trung ten giua hai class: bien the gan tu tham so
c = claims_of({"h.py": "import httpx\nclass Remote:\n    def __init__(self):\n        self.client = httpx.Client()\n"
                       "class Cache:\n    def __init__(self, client):\n        self.client = client\n"
                       "    def e(self):\n        return self.client.get('id')\n"})
print("attr from param: suspects", sus(c), "claim", http(c, "h.py:9", "httpx", "GET", "id"))

# 5. re-export: bien the hai tang / import *
c = claims_of({"infra/transport.py": "import httpx\nwire = httpx.Client()\n",
               "infra/net/__init__.py": "from ..transport import wire\n",
               "infra/__init__.py": "from .net import wire\n",
               "routes.py": "from infra import wire\ndef e():\n    return wire.get('https://real.example')\n"})
print("reexport 2 tang", sus(c), http(c, "routes.py:3", "httpx", "GET", "https://real.example"))
c = claims_of({"infra/transport.py": "import httpx\nwire = httpx.Client()\n",
               "infra/__init__.py": "from .transport import *\n",
               "routes.py": "from infra import wire\ndef e():\n    return wire.get('https://real.example')\n"})
print("reexport star", sus(c), http(c, "routes.py:3", "httpx", "GET", "https://real.example"))

# 6. ke thua init: hai tang
c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nclass Base:\n"
                          "    def __init__(self, x_tenant: str = Header()):\n        self.x_tenant = x_tenant\n"
                          "class Mid(Base):\n    pass\nclass Tenant(Mid):\n    pass\napp = FastAPI()\n"
                          "@app.get('/x')\ndef e(v=Depends(Tenant)):\n    return {}\n"})
c.submit({"routes": [route("main.py::e", "main.py:10-11", "/x", application="main.py:9", deps=[("Tenant", "main.py:11")])]})
print("inherit 2 tang:", reminders(c)[:120])

# 7. alias pydantic: Annotated[str, Field(alias=)] va alias_generator
c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends\nfrom pydantic import BaseModel, Field\n"
                          "class Filters(BaseModel):\n    sort_by: Annotated[str, Field(alias='sortBy')] = 'name'\napp = FastAPI()\n"
                          "@app.get('/x')\ndef e(v=Depends(Filters)):\n    return {}\n"})
c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6", deps=[("Filters", "main.py:8")])]})
print("alias Annotated:", reminders(c)[:160])

# 8. partial keyword
c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nfrom functools import partial\n"
                          "def filters(skip: int = 0, limit: int = 10):\n    return limit\ntenant = partial(filters, 5)\n"
                          "app = FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)):\n    return v\n"})
c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6", deps=[("tenant", "main.py:8")])]})
print("partial pos:", reminders(c)[:200])

print("== vong5 http_bo_sot con lai ==")
c = claims_of({"h.py": "import httpx\nwire = httpx.Client()\ndef b():\n    return getattr(wire, 'get')('https://b.example')\n"})
print("getattr claim", sus(c), http(c, "h.py:4", "httpx", "GET", "https://b.example"))
c = claims_of({"h.py": "import httpx\ndef e(wire):\n    return wire.get('https://b.example')\n"
                       "def main():\n    e(httpx.Client())\n"})
print("e(wire) untyped", sus(c))
