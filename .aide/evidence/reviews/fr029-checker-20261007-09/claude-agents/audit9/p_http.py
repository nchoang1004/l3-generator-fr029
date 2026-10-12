import boot
from boot import claims_of, http
# H2: client on app.state, handed out by an UNTYPED dependency; route file imports no HTTP library
files = {
 "main.py": "from contextlib import asynccontextmanager\nimport httpx\nfrom fastapi import FastAPI\n"
            "@asynccontextmanager\nasync def lifespan(app):\n    app.state.http = httpx.AsyncClient()\n    yield\n"
            "    await app.state.http.aclose()\napp = FastAPI(lifespan=lifespan)\n",
 "deps.py": "from fastapi import Request\ndef get_http(request: Request):\n    return request.app.state.http\n",
 "routes.py": "from fastapi import APIRouter, Depends\nfrom deps import get_http\nrouter = APIRouter()\n"
              "@router.get('/x')\nasync def x(client=Depends(get_http)):\n    r = await client.get('https://real.example/x')\n    return r.json()\n",
}
c = claims_of(files)
print("H2 suspects:", c.suspects())
print("H2 claim:", http(c, "routes.py:6", "httpx", "GET", "https://real.example/x"))
# typed variant (control)
f2 = dict(files); f2["deps.py"] = "import httpx\nfrom fastapi import Request\ndef get_http(request: Request) -> httpx.AsyncClient:\n    return request.app.state.http\n"
c = claims_of(f2)
print("H2 control typed provider suspects:", c.suspects())
# H2b: in-route access via request.app.state (control, handled?)
f3 = dict(files); f3["routes.py"] = ("from fastapi import APIRouter, Request\nrouter = APIRouter()\n"
     "@router.get('/x')\nasync def x(request: Request):\n    r = await request.app.state.http.get('https://real.example/x')\n    return r.json()\n")
c = claims_of(f3)
print("H2b request.app.state suspects:", c.suspects())

# H10: same local name `client` is httpx in one function and redis in another
src = ("import httpx\nimport redis\n\nasync def fetch():\n    async with httpx.AsyncClient() as client:\n"
       "        return await client.get('https://a.example')\n\ndef cached(key):\n    client = redis.Redis()\n"
       "    return client.get(key)\n")
c = claims_of({"h.py": src})
print("H10 suspects:", c.suspects())
print("H10 claim on redis line:", http(c, "h.py:10", "httpx", "GET", None))
