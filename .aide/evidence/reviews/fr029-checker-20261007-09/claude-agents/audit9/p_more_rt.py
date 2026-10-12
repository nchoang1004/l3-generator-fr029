import boot, os, sys, asyncio, httpx
from boot import claims_of, route, reminders
dep = "from fastapi import Header\ndef common(x_tenant: str = Header()):\n    return x_tenant\n"
files = {"api/__init__.py": "", "api/v1/__init__.py": "", "api/v1/deps.py": dep,
         "api/v1/main.py": "from fastapi import FastAPI, Depends\nfrom api.v1 import deps\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(deps.common)):\n    return {}\n"}
c = claims_of(files)
c.add_route(route("api/v1/main.py::e", "api/v1/main.py:4-5", "/x", application="api/v1/main.py:3", deps=[("deps.common", "api/v1/main.py:5")]))
print("dotted dep single definition control:", repr(reminders(c)))
# runtime of H-inherit
d = os.path.join(boot.A, "tmp", "hinh"); os.makedirs(d, exist_ok=True)
open(os.path.join(d, "base.py"), "w").write("import httpx\nclass BaseAPI:\n    def __init__(self, base_url):\n        self._client = httpx.AsyncClient(base_url=base_url)\n")
open(os.path.join(d, "github.py"), "w").write("from base import BaseAPI\nclass GitHub(BaseAPI):\n    async def repos(self):\n        r = await self._client.get('https://api.github.com/repos')\n        return r.json()\n")
sys.path.insert(0, d)
import github
seen = []
g = github.GitHub("https://api.github.com")
g._client = httpx.AsyncClient(transport=httpx.MockTransport(lambda req: (seen.append((req.method, str(req.url))), httpx.Response(200, json=[]))[1]))
print("Hinh runtime:", asyncio.run(g.repos()), seen)
