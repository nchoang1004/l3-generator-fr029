import boot, os, sys, httpx
from boot import claims_of, http
d = os.path.join(boot.A, "tmp", "h2rt"); os.makedirs(d, exist_ok=True)
open(os.path.join(d, "deps.py"), "w").write("from fastapi import Request\ndef get_http(request: Request):\n    return request.app.state.http\n")
open(os.path.join(d, "routes.py"), "w").write("from fastapi import APIRouter, Depends\nfrom deps import get_http\nrouter = APIRouter()\n"
              "@router.get('/x')\nasync def x(client=Depends(get_http)):\n    r = await client.get('https://real.example/x')\n    return r.json()\n")
sys.path.insert(0, d)
import routes
from fastapi import FastAPI
from fastapi.testclient import TestClient
seen = []
app = FastAPI(); app.include_router(routes.router)
app.state.http = httpx.AsyncClient(transport=httpx.MockTransport(lambda req: (seen.append((req.method, str(req.url))), httpx.Response(200, json={"ok": 1}))[1]))
print("H2 runtime:", TestClient(app).get("/x").json(), seen)
print("openapi params of /x:", app.openapi()["paths"]["/x"]["get"].get("parameters"))
try:
    import redis; print("redis installed", redis.__version__)
except ImportError:
    print("redis not installed")
# H10 class variant
src = ("import httpx\nimport redis\n\nclass Gateway:\n    def __init__(self):\n        self.client = httpx.AsyncClient()\n"
       "    async def pay(self):\n        return await self.client.post('https://pay.example/charge')\n\n"
       "class Cache:\n    def __init__(self, url):\n        self.client = redis.from_url(url)\n"
       "    def read(self, key):\n        return self.client.get(key)\n")
c = claims_of({"s.py": src})
print("H10b suspects:", c.suspects())
print("H10b claim on redis self.client.get:", http(c, "s.py:14", "httpx", "GET", None))
