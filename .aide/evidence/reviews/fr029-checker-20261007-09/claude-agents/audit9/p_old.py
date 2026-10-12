import boot
from boot import claims_of, http, route, part, reminders
c = claims_of({"h.py": "import httpx\nwire = httpx.Client()\ndef b():\n    return getattr(wire, 'get')('https://b.example')\n"})
print("getattr suspects:", c.suspects(), "claim:", http(c, "h.py:4", "httpx", "GET", "https://b.example"))
c = claims_of({"h.py": "import httpx\ndef e(wire):\n    return wire.get('https://real.example')\ndef main():\n    e(httpx.Client())\n"})
print("e(wire) untyped suspects:", c.suspects(), "claim:", http(c, "h.py:3", "httpx", "GET", "https://real.example"))
c = claims_of({"h.py": "import asyncio\nimport httpx\nc = httpx.Client()\nasync def e():\n    loop = asyncio.get_running_loop()\n    return await loop.run_in_executor(None, c.get, 'https://real.example')\n"})
print("run_in_executor suspects:", c.suspects(), "claim:", http(c, "h.py:6", "httpx", "GET", "https://real.example"))
# variants of round-8 fixes
c = claims_of({"h.py": "import httpx\ndef e(clients: list[httpx.Client]):\n    return clients[0].get('https://real.example')\n"})
print("list of clients indexing suspects:", c.suspects())
c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Query\n"
  "from pydantic import BaseModel, Field\nclass Filters(BaseModel):\n    tags: list[str] = Field([], alias='tag')\n"
  "def dep(f: Annotated[Filters, Query()]):\n    return f\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8", deps=[("dep", "main.py:10")])]})
print("query model list alias:", reminders(c))
