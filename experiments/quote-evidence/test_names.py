"""Offline tests for the code reading after Pyright (names.py) came in, and for the FastAPI and standard-library
rules calls.py keeps (RUNS_FOR_YOU, on_event, Depends(session provider), a library imported under another name).
Needs Node and scip-python, as the pipeline does."""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import calls     # noqa: E402
import flow      # noqa: E402
import inventory  # noqa: E402
import pyindex   # noqa: E402

REPO = "from sqlalchemy import select\n\nclass Repo:\n    async def get(self, session):\n        return await session.execute(select(1))\n"
WORK = "import smtplib\n\ndef job(x):\n    smtplib.SMTP('mail.example.com')\n"


class NamesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, files: dict):
        root = Path(self.tmp.name) / str(len(list(Path(self.tmp.name).iterdir())))
        for rel, text in {"app/__init__.py": "", **files}.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(textwrap.dedent(text))
        idx = pyindex.index(root, inventory.scan(root))
        facts = calls.facts(idx)
        return facts, flow.analyze(idx, facts)

    def kind(self, an, a, b):
        got = an["pairs"].get((a, b))
        return got[0] if got else None

    def test_pyright_follows_re_exports_through_two_files(self):
        _, an = self.read({"app/pkg/__init__.py": "from .mid import Repo\n", "app/pkg/mid.py": "from .impl import Repo\n",
                           "app/pkg/impl.py": REPO,
                           "app/svc.py": "from app.pkg import Repo\nasync def run(session):\n    return await Repo().get(session)\n"})
        self.assertEqual(self.kind(an, "app/svc.py", "app/pkg/impl.py"), "flow")

    def test_pyright_follows_an_attribute_set_in_a_base_class_of_another_file(self):
        _, an = self.read({"app/repo.py": REPO,
                           "app/base.py": "from app.repo import Repo\nclass Base:\n    def __init__(self):\n        self.repo = Repo()\n",
                           "app/svc.py": "from app.base import Base\nclass Svc(Base):\n"
                                         "    async def run(self, session):\n        return await self.repo.get(session)\n"})
        self.assertEqual(self.kind(an, "app/svc.py", "app/repo.py"), "flow")

    def test_a_parameter_hides_an_imported_name(self):
        _, an = self.read({"app/work.py": WORK, "app/api.py": "from app.work import job\ndef h(job):\n    return job(1)\n"})
        self.assertIsNone(self.kind(an, "app/api.py", "app/work.py"))

    def test_a_function_handed_to_background_tasks_or_a_thread_is_a_flow(self):
        for code in ("from fastapi import BackgroundTasks\nfrom app.work import job\n"
                     "async def h(bg: BackgroundTasks):\n    bg.add_task(job, 1)\n",
                     "import asyncio\nfrom app.work import job\nasync def h():\n    await asyncio.to_thread(job, 1)\n",
                     "from threading import Thread\nfrom app.work import job\ndef h():\n    Thread(target=job).start()\n"):
            _, an = self.read({"app/work.py": WORK, "app/api.py": code})
            self.assertEqual(self.kind(an, "app/api.py", "app/work.py"), "flow", code)

    def test_on_event_and_add_event_handler_are_wiring(self):
        db = "async def init_db():\n    import asyncpg\n    await asyncpg.connect('postgres://x')\n"
        for code in ("from fastapi import FastAPI\nfrom app.db import init_db\napp = FastAPI()\n\n"
                     "@app.on_event('startup')\nasync def boot():\n    await init_db()\n",
                     "from fastapi import FastAPI\nfrom app.db import init_db\napp = FastAPI()\n\n"
                     "async def boot():\n    await init_db()\n\napp.add_event_handler('startup', boot)\n"):
            _, an = self.read({"app/db.py": db, "app/main.py": code})
            self.assertEqual(self.kind(an, "app/main.py", "app/db.py"), "wiring", code)

    def test_a_parameter_from_depends_on_a_session_provider_is_a_session(self):
        facts, _ = self.read({
            "app/db.py": "from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker\n"
                         "engine = create_async_engine('x')\nSessionLocal = async_sessionmaker(engine)\n"
                         "async def get_uow():\n    async with SessionLocal() as s:\n        yield s\n",
            "app/api.py": "from fastapi import Depends\nfrom sqlalchemy import select\nfrom app.db import get_uow\n"
                          "async def h(uow=Depends(get_uow)):\n    return await uow.execute(select(1))\n"})
        self.assertTrue(facts["app/api.py"]["db_use"])

    def test_a_library_imported_under_another_name_keeps_its_sign(self):
        _, an = self.read({"app/main.py": "from fastapi import FastAPI as Api\napp = Api()\n"})
        self.assertEqual(an["sure"]["app/main.py"][0], "entry")


if __name__ == "__main__":
    unittest.main()
