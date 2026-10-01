"""Probe the code-reading steps (inventory, pyindex, calls, flow) with tiny made-up repositories, one common code
pattern each, and count the holes per step. No AI, no sample repository, no oracle.

    python probe_holes.py [--fail]        # --fail: print only the failing cases

Each case: files, then what a reader of the code would say is true (an edge and its kind, a tier sign, an I/O
line, a file in scope). A case fails when the code says otherwise.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import calls, flow, inventory, pyindex  # noqa: E401,E402

TMP = Path(tempfile.mkdtemp(prefix="probe-"))
REPO = "from sqlalchemy import select\n\nclass Repo:\n    async def get(self, session):\n        return await session.execute(select(1))\n"
WORK = "import smtplib\n\ndef job(x):\n    smtplib.SMTP('mail.example.com')\n"
SVC = "from app.repo import Repo\n\n"
INIT = {"app/__init__.py": ""}


def build(files: dict):
    d = Path(tempfile.mkdtemp(dir=TMP))
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(textwrap.dedent(text))
    snap = inventory.scan(d)
    idx = pyindex.index(d, snap)
    facts = calls.facts(idx)
    return snap, idx, facts, flow.analyze(idx, facts)


def kind(an, a, b):
    got = an["pairs"].get((a, b))
    return got[0] if got else None


# (step, name, files, check(snap, idx, facts, an) -> bool)
CASES = [
    # [1] inventory
    ("1 inventory", "app trong thư mục env/", {"env/main.py": "from fastapi import FastAPI\napp = FastAPI()\n"},
     lambda s, i, f, a: "env/main.py" in s["scope"]),
    ("1 inventory", "app trong thư mục build/", {"build/main.py": "from fastapi import FastAPI\napp = FastAPI()\n"},
     lambda s, i, f, a: "build/main.py" in s["scope"]),
    ("1 inventory", "app trong thư mục testing/ (không phải test)",
     {"testing/main.py": "from fastapi import FastAPI\napp = FastAPI()\n"},
     lambda s, i, f, a: "testing/main.py" in s["scope"]),
    # [2] import resolution
    ("2 import", "import tương đối", {**INIT, "app/repo.py": REPO,
                                      "app/svc.py": "from .repo import Repo\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("2 import", "re-export qua __init__", {**INIT, "app/repos/__init__.py": "from .user import Repo\n",
                                            "app/repos/user.py": REPO,
                                            "app/svc.py": "from app.repos import Repo\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repos/user.py") == "flow"),
    ("2 import", "re-export 2 bước, file tên a_",
     {**INIT, "app/pkg/__init__.py": "from .mid import Repo\n", "app/pkg/mid.py": "from .impl import Repo\n",
      "app/pkg/impl.py": REPO,
      "app/a_consumer.py": "from app.pkg import Repo\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/a_consumer.py", "app/pkg/impl.py") == "flow"),
    ("2 import", "re-export 2 bước, file tên z_",
     {**INIT, "app/pkg/__init__.py": "from .mid import Repo\n", "app/pkg/mid.py": "from .impl import Repo\n",
      "app/pkg/impl.py": REPO,
      "app/z_consumer.py": "from app.pkg import Repo\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/z_consumer.py", "app/pkg/impl.py") == "flow"),
    ("2 import", "from m import *", {**INIT, "app/repo.py": REPO,
                                     "app/svc.py": "from app.repo import *\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("2 import", "import trong hàm", {**INIT, "app/repo.py": REPO,
                                      "app/svc.py": "async def run(session):\n    from app.repo import Repo\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("2 import", "src layout (src/app)", {"src/app/__init__.py": "", "src/app/repo.py": REPO,
                                          "src/app/svc.py": "from app.repo import Repo\nasync def run(session):\n    return await Repo().get(session)\n"},
     lambda s, i, f, a: kind(a, "src/app/svc.py", "src/app/repo.py") == "flow"),
    ("2 import", "crud.order.get() qua package", {**INIT, "app/crud/__init__.py": "from .order import order\n",
                                                  "app/crud/order.py": REPO + "\norder = Repo()\n",
                                                  "app/api.py": "from app import crud\nasync def h(session):\n    return await crud.order.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/crud/order.py") == "flow"),
    # [3] call resolution
    ("3 lời gọi", "self.repo = repo (tham số có kiểu)", {**INIT, "app/repo.py": REPO, "app/svc.py": SVC +
     "class Svc:\n    def __init__(self, repo: Repo):\n        self.repo = repo\n    async def run(self, session):\n        return await self.repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "chú thích dạng chuỗi 'Repo'", {**INIT, "app/repo.py": REPO, "app/svc.py": SVC +
     "class Svc:\n    def __init__(self, repo: 'Repo'):\n        self.repo = repo\n    async def run(self, session):\n        return await self.repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "Annotated[Repo, Depends()]", {**INIT, "app/repo.py": REPO, "app/api.py":
     "from typing import Annotated\nfrom fastapi import Depends\nfrom app.repo import Repo\n"
     "async def h(session, repo: Annotated[Repo, Depends()]):\n    return await repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "thuộc tính ở mức class", {**INIT, "app/repo.py": REPO, "app/svc.py": SVC +
     "class Svc:\n    repo = Repo()\n    async def run(self, session):\n        return await self.repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "thuộc tính gán ở lớp cha file khác", {**INIT, "app/repo.py": REPO,
     "app/base.py": SVC + "class Base:\n    def __init__(self):\n        self.repo = Repo()\n",
     "app/svc.py": "from app.base import Base\nclass Svc(Base):\n    async def run(self, session):\n        return await self.repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "gán tuple self.a, self.repo = ...", {**INIT, "app/repo.py": REPO, "app/svc.py": SVC +
     "class Svc:\n    def __init__(self, repo: Repo):\n        self.a, self.repo = 1, repo\n    async def run(self, session):\n        return await self.repo.get(session)\n"},
     lambda s, i, f, a: kind(a, "app/svc.py", "app/repo.py") == "flow"),
    ("3 lời gọi", "tham số trùng tên import (không được có cạnh)", {**INIT, "app/work.py": WORK,
     "app/api.py": "from app.work import job\ndef h(job):\n    return job(1)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/work.py") is None),
    # [3] tier signs
    ("3 dấu hiệu", "FastAPI as Api", {**INIT, "app/main.py": "from fastapi import FastAPI as Api\napp = Api()\n"},
     lambda s, i, f, a: a["sure"].get("app/main.py", [None])[0] == "entry"),
    ("3 dấu hiệu", "APIRouter đặt bí danh", {**INIT, "app/api.py":
     "from fastapi import APIRouter as R\nr = R()\n\n@r.get('/x')\ndef x():\n    return 1\n"},
     lambda s, i, f, a: a["sure"].get("app/api.py", [None])[0] == "api"),
    ("3 dấu hiệu", "model Tortoise (models.Model)", {**INIT, "app/models.py":
     "from tortoise import fields, models\n\nclass Item(models.Model):\n    id = fields.IntField(pk=True)\n"},
     lambda s, i, f, a: a["tier"].get("app/models.py", [None])[0] == "data"),
    ("3 dấu hiệu", "model Beanie (Document)", {**INIT, "app/models.py":
     "from beanie import Document\n\nclass Item(Document):\n    name: str\n"},
     lambda s, i, f, a: a["tier"].get("app/models.py", [None])[0] == "data"),
    # [3] session
    ("3 session", "tham số kiểu AsyncSession tên lạ", {**INIT, "app/crud.py":
     "from sqlalchemy import select\nfrom sqlalchemy.ext.asyncio import AsyncSession\n"
     "async def get(s: AsyncSession):\n    return await s.execute(select(1))\n"},
     lambda s, i, f, a: bool(f["app/crud.py"]["db_use"])),
    ("3 session", "tham số tên lạ, không kiểu, từ Depends(get_uow)", {**INIT,
     "app/db.py": "from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker\n"
                  "engine = create_async_engine('x')\nSessionLocal = async_sessionmaker(engine)\n"
                  "async def get_uow():\n    async with SessionLocal() as s:\n        yield s\n",
     "app/api.py": "from fastapi import Depends\nfrom sqlalchemy import select\nfrom app.db import get_uow\n"
                   "async def h(uow=Depends(get_uow)):\n    return await uow.execute(select(1))\n"},
     lambda s, i, f, a: bool(f["app/api.py"]["db_use"])),
    # [3] I/O
    *[("3 I/O", f"{lib}: {why}", {**INIT, "app/client.py": code}, (lambda k: lambda s, i, f, a: bool(f["app/client.py"]["io"]))(lib))
      for lib, why, code in [
          ("aiohttp", "có trong bảng (đối chứng)", "import aiohttp\nasync def g():\n    async with aiohttp.ClientSession() as s:\n        return await s.get('https://x')\n"),
          ("tortoise", "Tortoise.init(db_url)", "from tortoise import Tortoise\nasync def init():\n    await Tortoise.init(db_url='postgres://x', modules={})\n"),
          ("motor", "AsyncIOMotorClient(url)", "from motor.motor_asyncio import AsyncIOMotorClient\nclient = AsyncIOMotorClient('mongodb://x')\n"),
          ("boto3", "boto3.client('s3')", "import boto3\ns3 = boto3.client('s3')\n"),
          ("openai", "AsyncOpenAI(api_key)", "from openai import AsyncOpenAI\nclient = AsyncOpenAI(api_key='k')\n"),
          ("stripe", "stripe.Charge.create", "import stripe\ndef pay():\n    return stripe.Charge.create(amount=1)\n"),
          ("minio", "Minio(host)", "from minio import Minio\nclient = Minio('play.min.io')\n"),
          ("elasticsearch", "AsyncElasticsearch(url)", "from elasticsearch import AsyncElasticsearch\nes = AsyncElasticsearch('http://x')\n"),
      ]],
    # [4] edge kinds
    ("4 loại cạnh", "BackgroundTasks.add_task(f) là luồng", {**INIT, "app/work.py": WORK, "app/api.py":
     "from fastapi import BackgroundTasks\nfrom app.work import job\nasync def h(bg: BackgroundTasks):\n    bg.add_task(job, 1)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/work.py") == "flow"),
    ("4 loại cạnh", "asyncio.to_thread(f) là luồng", {**INIT, "app/work.py": WORK, "app/api.py":
     "import asyncio\nfrom app.work import job\nasync def h():\n    await asyncio.to_thread(job, 1)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/work.py") == "flow"),
    ("4 loại cạnh", "Thread(target=f) là luồng", {**INIT, "app/work.py": WORK, "app/api.py":
     "from threading import Thread\nfrom app.work import job\ndef h():\n    Thread(target=job, args=(1,)).start()\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/work.py") == "flow"),
    ("4 loại cạnh", "task.delay() của Celery là luồng", {**INIT,
     "app/tasks.py": "from celery import Celery\nimport smtplib\ncelery_app = Celery('x', broker='redis://x')\n\n"
                     "@celery_app.task\ndef job(x):\n    smtplib.SMTP('h')\n",
     "app/api.py": "from app.tasks import job\ndef h():\n    job.delay(1)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/tasks.py") == "flow"),
    ("4 loại cạnh", "hàm kiểm tra tên lạ (authenticate) là check", {**INIT,
     "app/auth.py": "from fastapi import HTTPException\nimport smtplib\n\ndef authenticate(token: str):\n"
                    "    if token != 'x':\n        raise HTTPException(401)\n    smtplib.SMTP('h')\n",
     "app/api.py": "from fastapi import Depends\nfrom app.auth import authenticate\n"
                   "def h(user=Depends(authenticate)):\n    return 1\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/auth.py") == "check"),
    ("4 loại cạnh", "validate_order làm nghiệp vụ thật vẫn là luồng", {**INIT, "app/repo.py": REPO,
     "app/orders.py": "from app.repo import Repo\nasync def validate_order(session):\n    return await Repo().get(session)\n",
     "app/api.py": "from app.orders import validate_order\nasync def h(session):\n    return await validate_order(session)\n"},
     lambda s, i, f, a: kind(a, "app/api.py", "app/orders.py") == "flow"),
    ("4 loại cạnh", "@app.on_event('startup') là lắp ráp", {**INIT, "app/repo.py": REPO,
     "app/db.py": "from sqlalchemy.ext.asyncio import create_async_engine\nengine = create_async_engine('x')\n"
                  "async def init_db():\n    async with engine.begin() as c:\n        await c.run_sync(lambda x: x)\n",
     "app/main.py": "from fastapi import FastAPI\nfrom app.db import init_db\napp = FastAPI()\n\n"
                    "@app.on_event('startup')\nasync def boot():\n    await init_db()\n"},
     lambda s, i, f, a: kind(a, "app/main.py", "app/db.py") in ("wiring", "pass", None)),
]


def main() -> None:
    only_fail = "--fail" in sys.argv
    by_step = {}
    for step, name, files, check in CASES:
        try:
            ok = bool(check(*build(files)))
            note = ""
        except Exception as exc:          # a crash counts as a hole
            ok, note = False, f" (lỗi: {type(exc).__name__}: {str(exc)[:60]})"
        by_step.setdefault(step, []).append(ok)
        if not ok or not only_fail:
            print(f"{'OK  ' if ok else 'SAI '} [{step}] {name}{note}")
    print("\n| Bước | Ca thử | Sai |\n|---|---:|---:|")
    for step, oks in by_step.items():
        print(f"| {step} | {len(oks)} | {oks.count(False)} |")
    total = [o for oks in by_step.values() for o in oks]
    print(f"| Tổng | {len(total)} | {total.count(False)} |")


if __name__ == "__main__":
    main()
