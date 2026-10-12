import boot
from boot import claims_of, http, route, part, reminders, truth
# H-inherit: client built in base class of another file; subclass file imports no HTTP lib
files = {"base.py": "import httpx\nclass BaseAPI:\n    def __init__(self, base_url):\n        self._client = httpx.AsyncClient(base_url=base_url)\n",
         "github.py": "from base import BaseAPI\nclass GitHub(BaseAPI):\n    async def repos(self):\n        r = await self._client.get('https://api.github.com/repos')\n        return r.json()\n"}
c = claims_of(files)
print("Hinh suspects:", c.suspects())
print("Hinh claim:", http(c, "github.py:4", "httpx", "GET", "https://api.github.com/repos"))
f2 = dict(files); f2["github.py"] = "import httpx\n" + files["github.py"]
c = claims_of(f2)
print("Hinh (subclass imports httpx) suspects:", c.suspects(), "claim:", http(c, "github.py:5", "httpx", "GET", "https://api.github.com/repos"))
# same-file inheritance control
c = claims_of({"a.py": files["base.py"] + files["github.py"].split("\n", 1)[1]})
print("same-file control suspects:", c.suspects())
# stream / request sanity
c = claims_of({"h.py": "import httpx\nasync def f():\n    async with httpx.AsyncClient() as c:\n        async with c.stream('GET', 'https://a.example/big') as r:\n            pass\n        await c.request('POST', 'https://a.example/p')\n"})
print("stream:", http(c, "h.py:4", "httpx", "GET", "https://a.example/big"), "request:", http(c, "h.py:6", "httpx", "POST", "https://a.example/p"))
# dotted dependency with the same name in two modules
dep = "from fastapi import Header\ndef common(x_tenant: str = Header()):\n    return x_tenant\n"
files = {"api/__init__.py": "", "api/v1/__init__.py": "", "api/v2/__init__.py": "",
         "api/v1/deps.py": dep, "api/v2/deps.py": dep.replace("x_tenant", "x_org"),
         "api/v1/main.py": "from fastapi import FastAPI, Depends\nfrom api.v1 import deps\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(deps.common)):\n    return {}\n"}
c = claims_of(files)
print("dotted dep add_route:", c.add_route(route("api/v1/main.py::e", "api/v1/main.py:4-5", "/x", application="api/v1/main.py:3", deps=[("deps.common", "api/v1/main.py:5")])))
print("dotted dep reminders:", repr(reminders(c)))
print("truth:", truth(files, "api.v1.main"))
