"""Vong 7: phan vi du moi. Chay: cwd=slice, TMP=audit7."""
import sys
sys.path[:0] = ['.', 'tests']
from test_checker_counterexamples import claims_of, route, http, reminders  # noqa


def sus(c):
    return [s["at"] for s in c.suspects()]


P = lambda k, v, at: {"kind": k, "value": v, "at": at}

# A. helper dang ky co that (duoc goi) o file khac tat kiem prefix cho moi router
A = {"main.py": "from fastapi import FastAPI, APIRouter\nfrom setup import register\napp = FastAPI()\nr = APIRouter()\n"
                "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\nregister(app)\n",
     "setup.py": "from fastapi import APIRouter\nother = APIRouter()\ndef register(target):\n    target.include_router(other, prefix='/o')\n"}
c = claims_of(A)
print("A thieu /api, co helper:", c.add_route(route("main.py::e", "main.py:5-6", "/x", application="main.py:3")), c._edges_open)
A2 = dict(A, **{"setup.py": "from fastapi import APIRouter\nother = APIRouter()\n"})
A2["main.py"] = A["main.py"].replace("from setup import register\n", "from setup import other\n").replace("register(app)\n", "app.include_router(other)\n")
c = claims_of(A2)
print("A doi chung khong helper:", c.add_route(route("main.py::e", "main.py:5-6", "/x", application="main.py:3")))

# B. prefix thua lay tu dong include cua router khac
B = {"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\nadmin = APIRouter()\n"
                "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\napp.include_router(admin, prefix='/admin')\n"}
c = claims_of(B)
print("B /admin/api/x:", c.add_route(dict(route("main.py::e", "main.py:5-6", "/x", application="main.py:2"),
      path_parts=[P("include_prefix", "/admin", "main.py:9"), P("include_prefix", "/api", "main.py:8"), P("decorator", "/x", "main.py:5")])))
print("B /api/api/x:", c.add_route(dict(route("main.py::e", "main.py:5-6", "/x", application="main.py:2"),
      path_parts=[P("include_prefix", "/api", "main.py:8"), P("include_prefix", "/api", "main.py:8"), P("decorator", "/x", "main.py:5")])))

# C. gia tri prefix la literal khac tren dong (tags)
C = {"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter(prefix='/auth', tags=['authentication'])\n"
                "@r.post('/login')\ndef login():\n    return {}\napp.include_router(r, prefix='/api/v1', tags=['v1'])\n"}
c = claims_of(C)
print("C prefix=tags:", c.add_route(dict(route("main.py::login", "main.py:4-5", "/login", method="POST", application="main.py:2"),
      path_parts=[P("include_prefix", "v1", "main.py:7"), P("router_prefix", "authentication", "main.py:3"),
                  P("decorator", "/login", "main.py:4")])))

# D. router la lop con cua APIRouter (trong repo) / import doi ten
D = {"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nclass TrailingSlashRouter(APIRouter):\n    pass\n"
                "r = TrailingSlashRouter()\n@r.get('/x')\ndef e():\n    return {}\napp.include_router(r)\n"}
c = claims_of(D)
print("D subclass decorator:", c._decorator_problems(("main.py", 6, 7), "main.py::e", "GET"))
print("D subclass add_route:", c.add_route(route("main.py::e", "main.py:6-7", "/x", application="main.py:2")))
D2 = {"main.py": "from fastapi import FastAPI, APIRouter as Router\napp = FastAPI()\nr = Router()\n"
                 "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r)\n"}
print("D2 import as Router:", claims_of(D2)._decorator_problems(("main.py", 4, 5), "main.py::e", "GET"))

# E. dependencies=[] duoc nhan du handler co Depends(dep) khai header
E = {"main.py": "from fastapi import FastAPI, Depends, Header\ndef verify(x_token: str = Header()):\n    return x_token\n"
                "app = FastAPI()\n@app.get('/x')\ndef e(v=Depends(verify)):\n    return {}\n"}
c = claims_of(E)
print("E deps=[]:", c.submit({"routes": [route("main.py::e", "main.py:5-6", "/x", application="main.py:4", deps=[])]}),
      "reminders:", repr(reminders(c)))

# F. dependency la ten tham so / ten kieu tren dong
F = {"main.py": "from fastapi import FastAPI, Depends, Header\nclass Session:\n    pass\n"
                "def get_db(x_tenant: str = Header()):\n    return Session()\n"
                "app = FastAPI()\n@app.get('/x')\ndef e(db: Session = Depends(get_db)):\n    return {}\n"}
c = claims_of(F)
print("F dep=db:", c.dependency_at("db", ("main.py", 8, 8)), "dep=Session:", c.dependency_at("Session", ("main.py", 8, 8)))
print("F submit:", c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6", deps=[("db", "main.py:8")])]}),
      "reminders:", repr(reminders(c)))

# G. khoa config chi can la chuoi con cua doi so URL
G = {"h.py": "import httpx\nfrom types import SimpleNamespace\nsettings = SimpleNamespace(PAYMENT_API_URL='https://pay.example')\n"
             "def e():\n    return httpx.get(settings.PAYMENT_API_URL + '/charge')\n"}
c = claims_of(G)
for v in ("API_URL", "settings", "e"):
    print("G value", v, c.add_http({"at": "h.py:5", "library": "httpx", "method": "GET", "target": {"kind": "config", "value": v}}))

# H. config_at la self.client cua lop khac cung ten thuoc tinh
H = {"h.py": "import httpx\nfrom types import SimpleNamespace\nsettings = SimpleNamespace(USERS='https://u.example', ORDERS='https://o.example')\n"
             "class Users:\n    def __init__(self):\n        self.client = httpx.Client(base_url=settings.USERS)\n"
             "    def me(self):\n        return self.client.get('/me')\n"
             "class Orders:\n    def __init__(self):\n        self.client = httpx.Client(base_url=settings.ORDERS)\n"}
c = claims_of(H)
print("H config_at lop khac:", c.add_http({"at": "h.py:8", "library": "httpx", "method": "GET",
                                           "target": {"kind": "config", "value": "settings.ORDERS", "config_at": "h.py:11"}}))
print("H config_at dung:", c.add_http({"at": "h.py:8", "library": "httpx", "method": "GET",
                                       "target": {"kind": "config", "value": "settings.USERS", "config_at": "h.py:6"}}))

# I. client tra ve tu method roi goi ngay
I = {"h.py": "import httpx\nclass Api:\n    def _client(self):\n        return httpx.Client(base_url='https://a.example')\n"
             "    def me(self):\n        return self._client().get('/me')\n"
             "def build():\n    return httpx.Client()\ndef top():\n    return build().get('https://b.example')\n"}
c = claims_of(I)
print("I suspects (can h.py:6, h.py:10):", sus(c))

# K. URL tuong doi duoc nhan la literal du client co base_url literal
K = {"h.py": "import httpx\nc = httpx.Client(base_url='https://api.github.com')\ndef e():\n    return c.get('/users')\n"}
c = claims_of(K)
print("K literal /users:", http(c, "h.py:4", "httpx", "GET", "/users"))
