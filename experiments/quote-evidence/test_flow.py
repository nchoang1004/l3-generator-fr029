"""Offline tests for calls.py and flow.py (v7, code-only steps). No AI, no network."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import calls     # noqa: E402
import flow      # noqa: E402
import inventory  # noqa: E402
import pyindex   # noqa: E402

FILES = {
    "app/__init__.py": "",
    "app/main.py": "import asyncio\nfrom contextlib import asynccontextmanager\nfrom fastapi import FastAPI\n"
                   "from app.api.routes import router\nfrom app.db import create_tables\nfrom app.cache import start_cache\n"
                   "from app.worker import run_worker\n\n\n@asynccontextmanager\nasync def lifespan(app):\n"
                   "    await create_tables()\n    start_cache()\n    asyncio.create_task(run_worker())\n    yield\n\n\n"
                   "app = FastAPI(lifespan=lifespan)\napp.include_router(router)\n",
    "app/api/__init__.py": "",
    "app/api/routes.py": "from fastapi import APIRouter, Depends\nfrom app.services.orders import OrderService\n"
                         "from app.auth import get_current_user\nfrom app.helpers import slugify_title\n\n"
                         "router = APIRouter()\n\n\n@router.post('/orders', dependencies=[Depends(get_current_user)])\n"
                         "async def create(title: str, service: OrderService = Depends(OrderService)):\n"
                         "    return await service.place(slugify_title(title))\n",
    "app/auth.py": "def get_current_user():\n    return None\n",
    "app/helpers.py": "import re\n\n\ndef slugify_title(t):\n    return re.sub(r'\\W+', '-', t)\n",
    "app/services/__init__.py": "",
    "app/services/orders.py": "from app.db import SessionLocal\nfrom app.repo import crud_orders\nfrom app.reports import count\n\n\n"
                              "class OrderService:\n    async def place(self, slug):\n"
                              "        async with SessionLocal() as db:\n"
                              "            await count(db)\n            return await crud_orders.create(db=db, slug=slug)\n",
    "app/repo.py": "from fastcrud import FastCRUD\nfrom app.models import Order\n\ncrud_orders = FastCRUD(Order)\n",
    "app/reports.py": "async def count(session):\n    return await session.execute('select 1')\n",
    "app/models.py": "from sqlalchemy.orm import DeclarativeBase\n\n\nclass Base(DeclarativeBase):\n    pass\n\n\n"
                     "class Order(Base):\n    __tablename__ = 'orders'\n",
    "app/db.py": "from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker\n\n"
                 "engine = create_async_engine('postgresql+asyncpg://x')\nSessionLocal = async_sessionmaker(engine)\n\n\n"
                 "async def create_tables():\n    async with engine.begin() as conn:\n        await conn.run_sync(print)\n",
    "app/cache.py": "from redis.asyncio import Redis\n\nclient = None\n\n\ndef start_cache():\n    global client\n"
                    "    client = Redis(host='localhost')\n",
    "app/worker.py": "import asyncio\nfrom app.services.orders import OrderService\n\n\nasync def run_worker():\n"
                     "    while True:\n        await asyncio.sleep(1)\n        await OrderService().place('x')\n",
    "app/container.py": "from dependency_injector.providers import Factory\nfrom app.services.orders import OrderService\n\n"
                        "service = Factory(OrderService)\n",
    "app/plugins.py": "from importlib import import_module\n\n\ndef load(name):\n"
                      "    module = import_module(f'app.plug.{name}')\n    return getattr(module, 'router', None)\n",
    "app/plug/__init__.py": "",
    "app/plug/one.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n",
    "app/plug/two.py": "def other():\n    return 2\n",
    "run.py": "import uvicorn\n\nif __name__ == '__main__':\n    uvicorn.run('app.main:app')\n",
    "app/events.py": "import asyncpg\n\n\nasync def connect(app):\n    app.state.pool = await asyncpg.create_pool('x')\n",
    "app/getpool.py": "def pool(request):\n    return request.app.state.pool\n",
    "app/finish.py": "async def finish(session, order):\n    await session.commit()\n    await session.refresh(order)\n"
                     "    return await session.get(type(order), 1)\n",
    "app/raw.py": "async def rows(db):\n    return await db.fetchall(f\"SELECT * FROM {'orders'}\")\n",
    "app/legacy.py": "def all_orders(session, Order):\n    return session.query(Order).all()\n",
}


class FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        for rel, text in FILES.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        cls.idx = pyindex.index(root, inventory.scan(root))
        cls.facts = calls.facts(cls.idx)
        cls.an = flow.analyze(cls.idx, cls.facts)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def kind(self, a, b):
        return self.an["pairs"].get((f"app/{a}.py", f"app/{b}.py"), [None])[0]

    def test_tiers_from_signs(self):
        tier = {p: t[0] for p, t in self.an["tier"].items()}
        self.assertEqual(tier["app/main.py"], "entry")               # FastAPI(
        self.assertEqual(tier["app/worker.py"], "entry")             # background loop
        self.assertEqual(tier["app/api/routes.py"], "api")
        self.assertEqual(tier["app/services/orders.py"], "service")  # no sign, called from api
        self.assertEqual(tier["app/models.py"], "data")              # __tablename__
        self.assertEqual(tier["app/repo.py"], "data")                # FastCRUD object queries for it
        self.assertEqual(tier["app/db.py"], "infra")                 # creates the engine
        self.assertEqual(tier["app/cache.py"], "infra")
        self.assertEqual(tier["app/helpers.py"], "shared")           # no I/O

    def test_sure_signs_only(self):
        sure = {p: t[0] for p, t in self.an["sure"].items()}
        self.assertEqual(sure, {"app/main.py": "entry", "app/api/routes.py": "api", "app/models.py": "data",
                                "app/db.py": "infra"})   # FastAPI(, @router.post, __tablename__, create_async_engine
        # hints only: uvicorn.run, a background loop, a Redis client, asyncpg pool, FastCRUD, SQL text, APIRouter()
        for p in ("run.py", "app/worker.py", "app/cache.py", "app/events.py", "app/repo.py", "app/raw.py",
                  "app/plug/one.py"):
            self.assertNotIn(p, sure)
            self.assertIn(p, self.an["tier"])

    def test_data_sign_needs_a_query(self):
        tier = {p: t[:3] for p, t in self.an["tier"].items()}
        self.assertNotEqual(tier["app/finish.py"][0], "data")          # commit, refresh, get: no query written
        self.assertEqual(tier["app/raw.py"][::2], ["data", "SQL"])
        self.assertEqual(tier["app/legacy.py"][::2], ["data", "query("])
        self.assertEqual(self.kind("finish", "db"), "flow")            # the session use still reaches the engine

    def test_call_kinds(self):
        self.assertEqual(self.kind("main", "api/routes"), "flow")    # include_router
        self.assertEqual(self.kind("main", "db"), "wiring")          # inside lifespan
        self.assertEqual(self.kind("main", "cache"), "wiring")
        self.assertEqual(self.kind("main", "worker"), "wiring")
        self.assertEqual(self.kind("api/routes", "services/orders"), "flow")
        self.assertEqual(self.kind("api/routes", "auth"), "check")   # dependencies=[...]
        self.assertEqual(self.kind("api/routes", "helpers"), "helper")
        self.assertEqual(self.kind("services/orders", "db"), "pass")  # opens a session, hands it on
        self.assertEqual(self.kind("container", "services/orders"), "wiring")

    def test_edges_without_import(self):
        self.assertEqual(self.kind("repo", "db"), "flow")            # FastCRUD(Order) gets the session
        self.assertEqual(self.kind("reports", "db"), "flow")         # session.execute on a parameter
        self.assertEqual(self.kind("plugins", "plug/one"), "flow")   # import_module + getattr(router)
        self.assertIsNone(self.kind("plugins", "plug/two"))
        self.assertEqual(self.an["pairs"][("run.py", "app/main.py")][0], "flow")   # "app.main:app"
        self.assertEqual(self.kind("getpool", "events"), "pass")     # app.state.pool

    def test_walk_from_entry_points(self):
        reached = self.an["reached"]
        for p in ("api/routes", "services/orders", "repo", "db", "reports"):
            self.assertIn(f"app/{p}.py", reached)
        self.assertNotIn("app/cache.py", reached)                    # set up at start-up, never used

    def test_block_edges_drop_inside_shared_and_up(self):
        an = {"pairs": {("a.py", "b.py"): ["flow", 1], ("b.py", "a.py"): ["flow", 2], ("a.py", "c.py"): ["flow", 3],
                        ("a.py", "d.py"): ["flow", 4], ("a.py", "e.py"): ["check", 5]}}
        owner = {"a.py": "api", "b.py": "data", "c.py": "api", "d.py": "common", "e.py": "data2"}
        rank = {"api": 1, "data": 3, "data2": 3}
        self.assertEqual(flow.block_edges(an, owner, {"common"}, rank), {("api", "data"): ["a.py", 1]})


if __name__ == "__main__":
    unittest.main()
