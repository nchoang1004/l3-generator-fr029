"""Phần đọc tĩnh trong lần chạy FR-029 (11/10/2026): bảng CSDL (FR-030), sự kiện và tác vụ nền (FR-031), thư viện và
khóa cấu hình (FR-028). Dữ kiện API vẫn chỉ do agent đề xuất (ADR-2026-006): route của bộ đọc tĩnh bị bỏ."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from l3slice.docagent import ScriptedProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

FILES = {
    "main.py": ('from fastapi import FastAPI\nfrom tasks import send_email\napp = FastAPI()\n\n\n@app.post("/users")\n'
                'def create_user():\n    send_email.delay("a@b.c")\n    return 1\n'),
    "db.py": ('from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.orm import declarative_base\n'
              'Base = declarative_base()\n\n\nclass User(Base):\n    __tablename__ = "users"\n'
              '    id = Column(Integer, primary_key=True)\n    email = Column(String(100), nullable=False)\n'),
    "worker.py": 'from celery import Celery\ncelery_app = Celery("w", broker="redis://localhost")\nimport tortoise\n',
    "tasks.py": 'from worker import celery_app\n\n\n@celery_app.task(name="email.send")\ndef send_email(to):\n    return to\n',
    "config.py": ('import os\nfrom pydantic_settings import BaseSettings\n\n\nclass Settings(BaseSettings):\n'
                  '    DB_URL: str = "postgresql://u:secretpw@db/x"\n    PAGE_SIZE: int = 20\n\n\nDEBUG = os.getenv("DEBUG")\n'
                  'DEBUG_AGAIN = os.getenv("DEBUG")\n'),
    "pyproject.toml": '[project]\nname = "demo"\ndependencies = ["fastapi==0.110.0"]\n',
    "requirements.txt": "fastapi==0.110.0\nsqlalchemy>=2\ncelery\nunused-lib==1.0\ntortoise-orm==0.25.0\n",
}
COMPONENTS = [{"name": "API", "files": ["main.py", "config.py"]}, {"name": "Data", "files": ["db.py"]},
              {"name": "Worker", "files": ["worker.py", "tasks.py"]},
              {"name": "Khác", "kind": "other", "files": ["requirements.txt", "pyproject.toml"]}]
ROUTE = {"method": "POST", "handler": "main.py::create_user", "decorator": "main.py:6-7", "application": "main.py:3",
         "path_parts": [{"kind": "decorator", "value": "/users", "at": "main.py:6"}], "params": [], "request_body": None,
         "response": None, "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [],
         "auth": {"unknown": "chưa rõ"}}


class StaticParts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tempfile.TemporaryDirectory()
        root = Path(cls.t.name)
        for rel, text in FILES.items():
            (root / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / "src" / rel).write_text(text, encoding="utf-8")
        (root / "m.json").write_text(json.dumps({"components": COMPONENTS}), encoding="utf-8")
        steps = [[("read_file", {"path": p}) for p in FILES], [("submit_findings", {"routes": [ROUTE]})], [("finish", {})]]
        cls.out = root / "out"
        cls.bundle = run_documents(root / "src", cls.out, root / "m.json", "demo", ScriptedProvider(steps))
        cls.text = (cls.out / "TAI-LIEU.md").read_text(encoding="utf-8")
        cls.paths = {a["path"]: a for a in cls.bundle["artifacts"]}

    @classmethod
    def tearDownClass(cls):
        cls.t.cleanup()

    def test_table_and_event_files_are_published(self):
        self.assertEqual(self.paths["tech-specs/DATA/schema/TBL-DEMO-DATA.md"]["status"], "ready")
        evts = sorted(p for p in self.paths if "/events/" in p)
        self.assertEqual(evts, ["tech-specs/API/events/EVT-DEMO-API-EMAIL-SEND.md",
                                "tech-specs/WORKER/events/EVT-DEMO-WORKER-EMAIL-SEND.md"])
        self.assertTrue(all(self.paths[p]["status"] == "ready" for p in evts))
        worker = (self.out / evts[1]).read_text(encoding="utf-8")
        self.assertIn("API", worker)  # the sender's component, paired through the same Celery app

    def test_readme_lists_every_contract_file(self):
        readme = (self.out / "README.md").read_text(encoding="utf-8")
        for p in ("tech-specs/DATA/schema/TBL-DEMO-DATA.md", "tech-specs/WORKER/events/EVT-DEMO-WORKER-EMAIL-SEND.md"):
            self.assertIn(f"[{p}]({p})", readme)

    def test_tai_lieu_has_tables_events_libraries_and_config(self):
        self.assertIn("### users", self.text)
        self.assertIn("| email |", self.text)
        self.assertIn("email.send", self.text)
        self.assertIn("| fastapi | ==0.110.0 | có |", self.text)
        self.assertIn("| unused-lib | ==1.0 | chưa thấy import |", self.text)
        self.assertIn("| PAGE_SIZE |", self.text)
        self.assertIn("| DB_URL |", self.text)
        self.assertNotIn("secretpw", self.text)  # a credential is never written
        self.assertIn("| tortoise-orm | ==0.25.0 | có |", self.text)  # imported as `tortoise`
        self.assertEqual(self.text.count("| DEBUG | biến môi trường |"), 1)  # one row, both places
        self.assertIn("`config.py:10`, `config.py:11`", self.text)
        self.assertEqual(self.text.count("| fastapi |"), 1)  # declared in two manifests: one row
        self.assertIn("`requirements.txt:1`, `pyproject.toml:3`", self.text)

    def test_api_facts_come_only_from_the_agent(self):
        kinds = [f["kind"] for f in self.bundle["facts"]]
        self.assertEqual(kinds.count("route"), 1)
        self.assertNotIn("request_model", kinds)
        self.assertNotIn("symbol", kinds)
        self.assertNotIn("reference", kinds)


class Robustness(unittest.TestCase):
    """fastapi_best_architecture (kiểm CSDL 12/10/2026): một gói khai hai lần theo phiên bản Python làm bộ đọc tĩnh
    văng IDENTITY_COLLISION, hỏng cả lần chạy."""

    def run_repo(self, files):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel, text in files.items():
                (root / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / "src" / rel).write_text(text, encoding="utf-8")
            (root / "m.json").write_text(json.dumps({"components": [
                {"name": "App", "files": ["main.py"]},
                {"name": "Khác", "kind": "other", "files": sorted(set(files) - {"main.py"})}]}), encoding="utf-8")
            steps = [[("read_file", {"path": "main.py"})], [("finish", {})]]
            return run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))

    def test_a_package_declared_twice_with_markers_gives_two_rows(self):
        req = ("websockets==16.1.1 ; python_version < '3.11'\nfastapi==0.110\n"
               "websockets==17.0.1 ; python_version >= '3.11'\n")
        bundle = self.run_repo({"main.py": "import websockets\n", "requirements.txt": req})
        libs = [f for f in bundle["facts"] if f["kind"] == "library"]
        lines = sorted(e["start_line"] for f in libs if f["attributes"]["name"]["value"] == "websockets"
                       for e in f["evidence"] if e["path"] == "requirements.txt")
        self.assertEqual(lines, [1, 3])

    def test_a_failure_of_the_static_reader_does_not_stop_the_run(self):
        from unittest import mock
        with mock.patch("l3slice.extract.extract", side_effect=ValueError("boom")):
            bundle = self.run_repo({"main.py": "x = 1\n"})
        self.assertIn("STATIC_READ_FAILED", [x["code"] for x in bundle["limitations"]])
        self.assertTrue(any(a["path"] == "TAI-LIEU.md" and a["status"] == "ready" for a in bundle["artifacts"]))


class Relations(unittest.TestCase):
    def test_calls_between_components_are_listed_with_an_example(self):
        files = {"api.py": ('from fastapi import FastAPI\nfrom store import save\napp = FastAPI()\n\n\n@app.post("/x")\n'
                            'def x():\n    return save()\n'),
                 "store.py": "def save():\n    return 1\n"}
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel, text in files.items():
                (root / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / "src" / rel).write_text(text, encoding="utf-8")
            (root / "m.json").write_text(json.dumps({"components": [{"name": "API", "files": ["api.py"]},
                                                                    {"name": "Store", "files": ["store.py"]}]}),
                                         encoding="utf-8")
            steps = [[("read_file", {"path": p}) for p in files], [("finish", {})]]
            bundle = run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))
            text = (root / "out" / "TAI-LIEU.md").read_text(encoding="utf-8")
        self.assertEqual(bundle["component_relations"],
                         [{"from": "API", "to": "Store", "kinds": ["calls"], "count": 1, "example": "api.py:8"}])
        self.assertIn("| API | Store | gọi hàm | 1 | `api.py:8` |", text)


if __name__ == "__main__":
    unittest.main()
