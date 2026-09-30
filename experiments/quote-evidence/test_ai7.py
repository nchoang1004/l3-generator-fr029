"""Offline tests for ai7.py and run7.py (v7: grouping with reasons, edge check, naming) with a fake model."""
import json
import re
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ai7       # noqa: E402
import calls     # noqa: E402
import evaluate  # noqa: E402
import flow      # noqa: E402
import inventory  # noqa: E402
import llm       # noqa: E402
import pyindex   # noqa: E402
import run7      # noqa: E402

FILES = {
    "app/__init__.py": "",
    "app/main.py": "from fastapi import FastAPI\nfrom app.api.users import router\nfrom app.container import Container\n\n\n"
                   "def create_app():\n    app = FastAPI()\n    app.container = Container()\n    app.include_router(router)\n"
                   "    return app\n\n\napp = create_app()\n",
    "app/container.py": "class Container:\n    pass\n",
    "app/api/__init__.py": "",
    "app/api/users.py": "from fastapi import APIRouter, Depends\nfrom app.api.schemas import UserIn\nfrom app.deps import get_session\n"
                        "from app.domain.usecase import UserUseCase\nfrom app.domain.token import TokenUseCase\n"
                        "from app.constants import LIMIT\n\nrouter = APIRouter()\n\n\n@router.post('/users')\n"
                        "async def create(body: UserIn, usecase: UserUseCase = Depends(), session=Depends(get_session)):\n"
                        "    return await usecase.create(session, body.name, LIMIT)\n\n\n@router.post('/token')\n"
                        "async def token(tokens: TokenUseCase = Depends()):\n    return tokens.sign('x')\n",
    "app/api/schemas.py": "class UserIn:\n    name: str\n",
    "app/constants.py": "LIMIT = 10\n",
    "app/deps.py": "from app.db import SessionLocal\n\n\nasync def get_session():\n    async with SessionLocal() as session:\n"
                   "        yield session\n",
    "app/domain/__init__.py": "",
    "app/domain/usecase.py": "from abc import ABC, abstractmethod\n\n\nclass UserUseCase(ABC):\n    @abstractmethod\n"
                             "    async def create(self, session, name, limit):\n        ...\n",
    "app/domain/token.py": "from abc import ABC, abstractmethod\n\n\nclass TokenUseCase(ABC):\n    @abstractmethod\n"
                           "    def sign(self, sub):\n        ...\n",
    "app/service/__init__.py": "",
    "app/service/user.py": "from app.domain.usecase import UserUseCase\nfrom app.crud import create_user\nfrom app.dto import UserOut\n\n\n"
                           "class UserService(UserUseCase):\n    async def create(self, session, name, limit) -> UserOut:\n"
                           "        return await create_user(session, name)\n",
    "app/service/jwt.py": "from app.domain.token import TokenUseCase\n\n\nclass JwtService(TokenUseCase):\n"
                          "    def sign(self, sub):\n        return 'token-' + sub\n",
    "app/dto.py": "class UserOut:\n    id: int\n",
    "app/crud.py": "from sqlalchemy import select\nfrom app.models import User\nfrom app.constants import LIMIT\n\n\n"
                   "async def create_user(session, name):\n    session.add(User(name=name[:LIMIT]))\n"
                   "    return await session.execute(select(User))\n",
    "app/models.py": "class User:\n    __tablename__ = 'users'\n",
    "app/db.py": "from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker\n\n"
                 "engine = create_async_engine('postgresql+asyncpg://x')\nSessionLocal = async_sessionmaker(engine)\n",
    "app/clients/__init__.py": "",
    "app/clients/pay.py": "import httpx\n\n\nclass Pay:\n    def __init__(self, settings):\n"
                          "        self.client = httpx.AsyncClient(\n            timeout=5,\n            base_url=settings.PAY_URL,\n"
                          "        )\n",
    "app/tasks.py": "from app.crud import create_user\n\n\nasync def nightly(session):\n    await create_user(session, 'x')\n",
}


PLACE = {"app/api/users.py": "routes", "app/tasks.py": "logic"}     # pass 2 answers for the ambiguous files


def shown_ids(user: str) -> list[tuple[str, str, int]]:
    """(id, path as shown, line) of the code lines of a prompt: `[L3] main.py:7 code` and the overview's file lines
    `  main.py sure entry [L3]:7 code`."""
    out = []
    for row in user.splitlines():
        out += [(m[1], m[2], int(m[3])) for m in re.finditer(r"\[(L\d+)\] (\S+?):(\d+)", row)]
        m = re.match(r"\s+(\S+) [\w ]+ \[(L\d+)\]:(\d+) ", row)
        if m:
            out.append((m[2], m[1], int(m[3])))
    return out


def point(user: str, ref: str) -> str:
    """The id of the shown line `path:line ...` names, as the model answers; "L999" when that line is not shown."""
    path, line = ref.split(" ")[0].rsplit(":", 1)
    return next((i for i, shown, n in shown_ids(user) if n == int(line) and path.endswith(shown)), "L999")


def placer(user: str, bad=frozenset()) -> dict:
    """Answers a pass-2 request from the files it lists, following PLACE, pointing at the first line shown for
    each file; files in `bad` point at a line of another file."""
    rows, folder, ids = [], "", {}
    for line in user.splitlines():
        head = re.match(r"# (.*)/$", line)
        entry = re.match(r"([\w.\-]+\.py)(?: \||$)", line)
        if head:
            folder = "" if head[1] == "." else head[1] + "/"
        elif entry:
            path = folder + entry[1]
            ids[path] = re.findall(r"\[(L\d+)\]", line)
            rows.append(path)
        elif rows and re.match(r"\s+\[L\d+\]", line):
            ids[rows[-1]] += re.findall(r"\[(L\d+)\]", line)
    out = []
    for n, path in enumerate(rows):
        other = [i for p in rows if p != path for i in ids[p]]
        reason = (other[0] if other else "L999") if path in bad else ids[path][0]
        out.append({"file": path, "block": PLACE[path], "reason": reason})
    return {"files": out}


def edge_judge(user: str, kind: str) -> dict:
    rows, cur = [], None
    for line in user.splitlines():
        head = re.match(r"## (P\d+):", line)
        found = re.match(r"\[(L\d+)\] \S+?:\d+\| \S", line)
        if head:
            cur = {"id": head[1], "kind": kind, "reason": None}
            rows.append(cur)
        elif found and cur and cur["reason"] is None:
            cur["reason"] = found[1]
    return {"pairs": rows}


def namer(user: str) -> dict:
    """Answers a naming request from its text; block `app` points at an id that was not shown."""
    blocks, edges, exts, cur = [], [], [], None
    for line in user.splitlines():
        head = re.match(r"## (\w+) \(", line)
        found = re.match(r"\[(L\d+)\] ", line)
        edge = re.match(r"(E\d+) -> (\w+)", line)
        ext = re.match(r"(X\d+) ", line)
        if head:
            cur = {"key": head[1], "name": "khối " + head[1], "role": "Làm việc", "role_line": None}
            blocks.append(cur)
        elif edge:
            edges.append({"id": edge[1], "label": "" if edge[2] == "database" else "gọi xử lý"})
        elif ext:
            exts.append({"id": ext[1], "name": "Payment API"})
        elif found and cur and cur["role_line"] is None:
            cur["role_line"] = found[1]
    for b in blocks:
        if b["key"] == "app":
            b["role_line"] = "L999"
    return {"blocks": blocks, "edges": edges, "externals": exts}


TOP_GOOD = {"blocks": [
    {"name": "app", "layer": "entry", "paths": ["app/main.py", "app/container.py"], "reason": "app/main.py:7 app = FastAPI()"},
    {"name": "routes", "layer": "api", "paths": ["app/api/", "./app/deps.py"],
     "reason": "app/api/users.py:11 @router.post('/users')"},
    {"name": "logic", "layer": "service", "paths": ["app/domain", "app/service/", "app/dto.py", "app/tasks.py"],
     "reason": "app/service/user.py:6 class UserService(UserUseCase):"},
    {"name": "data", "layer": "data", "paths": ["app/crud.py", "app/models.py"],
     "reason": "app/crud.py:8 return await session.execute(select(User))"},
    {"name": "database", "layer": "infra", "paths": ["app/db.py"],
     "reason": "app/db.py:3 engine = create_async_engine('postgresql+asyncpg://x')"},
    {"name": "pay", "layer": "infra", "paths": ["app/clients/"], "reason": "app/clients/pay.py:6 self.client = httpx.AsyncClient("}],
    "shared": ["app/constants.py"]}
TOP_BAD = {"blocks": [
    TOP_GOOD["blocks"][0], TOP_GOOD["blocks"][1], TOP_GOOD["blocks"][2],
    {"name": "crud", "layer": "data", "paths": ["app/crud.py"], "reason": "app/crud.py:1 from sqlalchemy import select"},
    {"name": "models", "layer": "data", "paths": ["app/models.py", "app/nothing/"], "reason": "app/models.py:1 class User:"},
    {"name": "dto", "layer": "data", "paths": ["app/dto.py"], "reason": "app/dto.py:1 class UserOut:"},
    TOP_GOOD["blocks"][4],
    {"name": "pay", "layer": "infra", "paths": ["app/clients/", "app/db.py"], "reason": "app/main.py:7 app = FastAPI()"}],
    "shared": ["app/constants.py", "app/db.py"]}
# routes keep only deps.py, so users.py (sure api) sits in the service block through app/api/; tasks.py has no path
TOP_PARTIAL = {"blocks": [
    TOP_GOOD["blocks"][0], {**TOP_GOOD["blocks"][1], "paths": ["app/deps.py"]},
    {**TOP_GOOD["blocks"][2], "paths": ["app/domain/", "app/service/", "app/dto.py", "app/api/"]},
    *TOP_GOOD["blocks"][3:]], "shared": ["app/constants.py"]}


class FakeLLM:
    def __init__(self, bad=frozenset(), fail=(), edge_kind="pass", top=()):
        self.bad, self.fail, self.edge_kind, self.top, self.calls = bad, set(fail), edge_kind, list(top), []

    def json(self, system, user, schema, *, step, max_tokens, effort="medium"):
        self.calls.append({"step": step, "user": user, "total_tokens": 0, "max_tokens": max_tokens, "effort": effort,
                           "prompt": llm.estimate(system + user)})
        if step in self.fail:
            raise llm.ModelError(f"{step}: fake failure")
        if step.startswith("top"):
            if not self.top:
                return {}
            answer = json.loads(json.dumps(self.top.pop(0)))
            for b in answer["blocks"]:          # a reason written as `path:line code` becomes the id of that line
                if " " in str(b.get("reason")):
                    b["reason"] = point(user, b["reason"])
            return answer
        if step.startswith("place"):
            return placer(user, self.bad)
        if step.startswith("edges"):
            return edge_judge(user, self.edge_kind)
        return namer(user)


ORACLE = {"components": {"entry": ["app/main.py", "app/container.py"], "api": ["app/api/", "app/deps.py"],
                         "logic": ["app/service/", "app/domain/", "app/dto.py"], "data": ["app/crud.py", "app/models.py"],
                         "db": ["app/db.py"], "common": ["app/constants.py"]},
          "shared": ["common"], "externals": {"database": ["database"]},
          "required": [["entry", "api", "x"], ["api", "logic", "x"], ["logic", "data", "x"], ["data", "db", "x"],
                       ["db", "ext:database", "x"]],
          "acceptable": []}


class Ai7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "repo"
        for rel, text in FILES.items():
            (cls.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (cls.root / rel).write_text(text, encoding="utf-8")
        cls.idx = pyindex.index(cls.root, inventory.scan(cls.root))
        cls.facts = calls.facts(cls.idx)
        cls.an = flow.analyze(cls.idx, cls.facts)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def group(self, fake=None):
        fake = fake or FakeLLM(top=[TOP_PARTIAL, TOP_PARTIAL])     # pass 1 finds a problem and asks again
        g = ai7.group(fake, self.idx, self.facts, self.an)
        return g, {p: k for k, files in g["blocks"].items() for p in files}, fake

    def test_files_by_path_then_ambiguous_ones_by_the_model(self):
        g, owner, fake = self.group()
        self.assertEqual([c["step"] for c in fake.calls], ["top-1", "top-2", "place-1"])
        self.assertEqual(sorted(owner), sorted(p for p, e in self.idx.items() if not e.get("empty")))
        self.assertEqual(g["ambiguous"], {"no_path": ["app/tasks.py"], "sure_above": ["app/api/users.py"]})
        self.assertEqual((owner["app/api/users.py"], owner["app/tasks.py"]), ("routes", "logic"))
        self.assertEqual(owner["app/api/schemas.py"], "logic")                # by path, not ambiguous
        self.assertEqual(g["reasons"]["app/tasks.py"], {"file": "app/tasks.py", "line": 4,
                                                        "text": "async def nightly(session):"})
        self.assertEqual(sorted(g["reasons"]), ["app/api/users.py", "app/tasks.py"])
        self.assertEqual(g["block_reasons"]["app"], {"file": "app/main.py", "line": 7, "text": "app = FastAPI()"})
        # routes points at users.py, which its paths no longer hold: code picks a line of deps.py
        self.assertEqual(g["block_reasons"]["routes"]["file"], "app/deps.py")
        self.assertEqual((g["by_rule"], g["issues"]), ([], [
            "top: evidence picked by code (the model's line missing or outside the block): routes",
            "top: 1 problems left after the retry"]))

    def test_block_layer_sure_files_first_then_given(self):
        top = json.loads(json.dumps(TOP_GOOD))
        top["blocks"][3]["layer"] = "service"                                  # data block, models.py is sure data
        g, _, _ = self.group(FakeLLM(top=[top]))
        self.assertEqual(g["layer"], {"app": "entry", "routes": "api", "logic": "service", "data": "data",
                                      "database": "infra", "pay": "infra", "shared": "shared"})
        self.assertEqual(g["layer_differs"], [{"block": "data", "highest": "data", "given": "service"}])

    def test_request_shows_blocks_and_file_profiles(self):
        _, _, fake = self.group()
        text = fake.calls[-1]["user"]
        self.assertTrue(text.startswith("Blocks:\napp (entry): app/container.py, app/main.py\n"))
        self.assertIn("logic (service): app/api/, app/domain/, app/dto.py, app/service/\n", text)
        self.assertIn("\nshared: app/constants.py\n", text)
        self.assertRegex(text, r"users\.py \| layer: api \(sure\) \[L\d+\] 11: @router\.post\('/users'\)")
        self.assertRegex(text, r"tasks\.py \| defines nightly \| reaches [^\n]*\n  \[L\d+\] 4\| async def")
        self.assertNotRegex(text, r"users\.py \| [^\n]*\n  \[L\d+\] \d+\|")   # no code lines for a sure file
        for by_path in ("schemas.py", "crud.py", "db.py", "constants.py"):
            self.assertNotRegex(text, rf"(?m)^{re.escape(by_path)} ")

    def test_reason_not_in_that_file_is_rejected(self):
        g, owner, _ = self.group(FakeLLM(top=[TOP_PARTIAL], bad={"app/tasks.py", "app/api/users.py"}))
        self.assertEqual(owner["app/api/users.py"], "logic")                   # keeps its path
        self.assertEqual(owner["app/tasks.py"], "app_service")   # logic is api now (users.py): no service block in app/
        self.assertEqual(g["reasons"], {})
        self.assertEqual(sorted(g["by_rule"]), ["app/api/users.py", "app/tasks.py"])
        self.assertIn("place-1: 2 answers rejected (unknown file or block, a sure file shared, or reason not a "
                      "line of that file)", g["issues"])

    def test_lines_turn_ids_back_into_exact_code(self):
        lines = ai7.Lines(self.idx)
        self.assertEqual((lines.tag("app/db.py", 3), lines.tag("app/main.py", 7), lines.tag("app/db.py", 3)),
                         ("L1", "L2", "L1"))
        self.assertEqual(lines.show("app/db.py", 3), "[L1] app/db.py:3| engine = create_async_engine('postgresql+asyncpg://x')")
        self.assertEqual(lines.quote("L1"), {"file": "app/db.py", "line": 3,
                                             "text": "engine = create_async_engine('postgresql+asyncpg://x')"})
        self.assertEqual(lines.quote("[L2]")["line"], 7)
        self.assertIsNone(lines.quote("L2", ["app/db.py"]))                    # a line outside the given files
        self.assertIsNone(lines.quote("L9"))
        self.assertIsNone(lines.quote("app/db.py:3 engine"))                   # code text is not an id
        self.assertEqual(lines.schema(), {"type": "string", "enum": ["L1", "L2"]})
        mark = lines.mark()
        lines.tag("app/crud.py", 8)
        lines.reset(mark)
        self.assertEqual(lines.schema()["enum"], ["L1", "L2"])

    def test_failed_request_falls_back(self):
        g, owner, _ = self.group(FakeLLM(top=[TOP_PARTIAL], fail={"place-1"}))
        self.assertTrue(any(i.startswith("place-1 failed") for i in g["issues"]))
        self.assertEqual(g["layer"][owner["app/api/users.py"]], "api")    # a sure layer lifts its block
        self.assertEqual(g["layer"][owner["app/db.py"]], "infra")

    def test_no_answer_from_pass_1_the_code_draft_is_the_grouping(self):
        g, owner, fake = self.group(FakeLLM(top=[]))
        self.assertEqual([c["step"] for c in fake.calls], ["top-1"])
        self.assertEqual(g["top"]["source"], "draft")
        self.assertIn("top: no answer from the model; the code draft is the grouping", g["issues"])
        self.assertEqual(sorted(owner), sorted(p for p, e in self.idx.items() if not e.get("empty")))
        self.assertEqual({p: owner[p] for p in ("app/main.py", "app/container.py", "app/api/users.py", "app/deps.py",
                                                "app/crud.py", "app/db.py", "app/clients/pay.py", "app/constants.py")},
                         {"app/main.py": "app", "app/container.py": "app", "app/api/users.py": "api",
                          "app/deps.py": "api", "app/crud.py": "data", "app/db.py": "database",
                          "app/clients/pay.py": "http", "app/constants.py": ai7.SHARED})
        self.assertEqual(g["block_reasons"]["database"]["line"], 3)

    def test_no_answer_and_no_draft_places_every_file_by_rule(self):
        g = ai7.group(FakeLLM(top=[]), self.idx, self.facts, self.an, use_draft=False)
        owner = {p: k for k, files in g["blocks"].items() for p in files}
        self.assertIn("top: no blocks; every file placed by rule", g["issues"])
        self.assertEqual(owner["app/constants.py"], ai7.SHARED)
        self.assertEqual(g["layer"][owner["app/db.py"]], "infra")

    def test_pass_1_prompt_holds_the_draft_unless_asked_not_to(self):
        with_draft, without = FakeLLM(top=[TOP_GOOD]), FakeLLM(top=[TOP_GOOD])
        ai7.top_blocks(with_draft, self.idx, self.facts, self.an)
        ai7.top_blocks(without, self.idx, self.facts, self.an, use_draft=False)
        self.assertRegex(with_draft.calls[0]["user"], r"Draft by code \(name \(layer\): paths \| evidence id\):\n"
                                                      r"api \(api\): app/deps\.py, app/api/ \| \[L\d+\]\n")
        self.assertNotIn("Draft by code", without.calls[0]["user"])

    def test_reasoning_effort_per_step(self):
        fake = FakeLLM(top=[TOP_PARTIAL, TOP_PARTIAL])
        g = ai7.group(fake, self.idx, self.facts, self.an)
        ai7.describe(fake, self.idx, self.facts, self.an, g)
        self.assertEqual({c["step"].split("-")[0]: c["effort"] for c in fake.calls},
                         {"top": "medium", "place": "low", "name": "low"})

    def test_block_cap_is_reported(self):
        with unittest.mock.patch.dict(ai7.CAP, {"infra": 1}):
            g, _, _ = self.group(FakeLLM(top=[TOP_GOOD]))
        self.assertIn("2 infra blocks, above 1", g["issues"])

    def test_batches_follow_the_directory_tree(self):
        g = ai7._Grouping(self.idx, self.facts, self.an, {"blocks": {}, "shared": []})
        files = sorted(p for p, e in self.idx.items() if not e.get("empty"))
        cost = lambda ps: sum(llm.estimate(g.entry(p)) + ai7.ANSWER_PER_FILE for p in ps)
        overhead = ai7.REASONING + llm.estimate(ai7.PLACE_SYSTEM + "Blocks:\n" + g.block_list()) + 50
        domain = [p for p in files if p.startswith("app/domain/")]
        with unittest.mock.patch.object(ai7, "LIMIT", overhead + max(cost(domain), cost(["app/crud.py"])) + 1):
            batches = g.batches(files)
        self.assertGreater(len(batches), 1)
        self.assertEqual(sum(any(p in b for p in domain) for b in batches), 1)   # a small directory stays whole
        self.assertEqual(sorted(p for b in batches for p in b), sorted(files))

    def test_edge_check_draws_only_flow_with_checked_reason(self):
        g, _, _ = self.group()
        fake = FakeLLM(edge_kind="flow")
        out = ai7.check_edges(fake, self.idx, self.facts, self.an, g)
        self.assertEqual([c["step"] for c in fake.calls], ["edges-1"])
        self.assertIn("## P1: routes (api) -> database (infra)", fake.calls[0]["user"])  # deps.py hands a session on
        self.assertIn("app/deps.py:5| async with SessionLocal() as session:", fake.calls[0]["user"])
        self.assertEqual(out["edges"], {("routes", "database"): ["app/deps.py", 4]})
        self.assertTrue(all(d["checked"] for d in out["decisions"]))
        self.assertEqual(ai7.check_edges(FakeLLM(edge_kind="pass"), self.idx, self.facts, self.an, g)["edges"], {})

    def test_names_labels_quotes_and_externals(self):
        fake = FakeLLM(top=[TOP_GOOD])
        g, _, _ = self.group(fake)
        out = ai7.describe(fake, self.idx, self.facts, self.an, g, {("routes", "database"): ["app/deps.py", 5]})
        comps = {c["key"]: c for c in out["components"]}
        self.assertEqual(comps["routes"]["name"], "Khối routes")
        self.assertEqual(comps["app"]["role"], "")                        # quote not on that line: role dropped
        self.assertEqual(comps["logic"]["role"], "Làm việc")
        self.assertEqual(out["quotes"], {"returned": 6, "valid": 5})
        ids = {c["key"]: c["id"] for c in out["components"]}
        edges = {(e["source"], e["target"]): e["label"] for e in out["edges"]}
        self.assertEqual(edges[(ids["routes"], ids["logic"])], "gọi xử lý")
        self.assertEqual(edges[(ids["data"], ids["database"])], "gọi")    # empty label, no called name: code label
        self.assertIn((ids["routes"], ids["database"]), edges)            # drawn after the edge check
        self.assertNotIn((ids["routes"], ids["data"]), edges)
        names = {x["name"]: [e["source"] for e in x["edges"]] for x in out["externals"]}
        self.assertEqual(names, {"Database": [ids["database"]], "Payment API": [ids["pay"]]})
        sent = "\n".join(c["user"] for c in fake.calls if c["step"].startswith("name"))
        self.assertIn("base_url=settings.PAY_URL", sent)

    def test_run7_end_to_end_scored(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            summary = run7.run(self.root, out, FakeLLM(top=[TOP_GOOD]), ORACLE)
            data = json.loads((out / "graph.json").read_text(encoding="utf-8"))
            self.assertEqual(data["meta"]["pipeline"], "v7")
            self.assertEqual(data["meta"]["block_reasons"]["database"]["file"], "app/db.py")
            self.assertTrue((out / "diagram.mmd").exists() and (out / "score.json").exists())
            self.assertEqual(summary["score"]["internal"], {"precision": 1.0, "precision_strict": 1.0, "recall": 1.0})
            self.assertEqual(summary["score"]["external"]["recall"], 1.0)
            with self.assertRaises(FileExistsError):
                run7.run(self.root, out, FakeLLM(), None)

    def test_overview_router_tree_and_directory_lines(self):
        text, units, issues = ai7.overview(self.idx, self.facts, self.an, 3_000)
        self.assertEqual(issues, [])
        self.assertEqual(sorted(units), ["app/", "app/api/", "app/clients/", "app/domain/", "app/service/"])
        self.assertIn("app/main.py\n  -> app/api/users.py: [L1] app/main.py:9 app.include_router(router)\n", text)
        lines = {row.split(" ")[1]: row for row in text.splitlines() if re.match(r"D\d+ ", row)}
        self.assertTrue(lines["app/"].startswith("D1 app/ 9 files | constants.py, container.py, crud.py,"))
        self.assertIn("sure entry x1: [L2] main.py:7 app = FastAPI() |", lines["app/"])
        # a cut line ends in "…"; the same line keeps one id wherever it is shown
        self.assertIn("io database: [L4] db.py:3 engine = create_async_engine('postgresql+asyncpg:/… |", lines["app/"])
        self.assertIn("\n  db.py sure infra [L4]:3 engine = create_async_engine(", text)
        self.assertTrue(lines["app/clients/"].endswith("io http: [L13] pay.py:6 self.client = httpx.AsyncClient("))
        self.assertTrue(lines["app/api/"].endswith("| -> D1, D4 | <- D1 (include)"))   # a plain call has no label
        self.assertTrue(lines["app/domain/"].endswith("| <- D2"))
        # one line per file under its directory: a line of its code, what it shows, where it calls
        self.assertIn("\n  users.py sure api [L11]:11 @router.post('/users') | -> D1, D4\n", text)
        self.assertIn("\n  tasks.py defines [L10]:4 async def nightly(session):\n", text)

    def test_overview_drops_file_lines_then_merges_deep_directories_to_fit(self):
        overview = lambda limit: ai7.overview(self.idx, self.facts, self.an, limit)
        full = llm.estimate(overview(10_000)[0])
        text, units, issues = overview(full - 1)                   # file lines lose their calls first
        self.assertEqual((len(units), issues), (5, ["overview: file lines without their calls to fit"]))
        self.assertIn("\n  users.py sure api [L11]:11 @router.post('/users')\n", text)
        bare = llm.estimate(overview(llm.estimate(text) - 1)[0])    # then they go
        self.assertIn("overview: file lines left out to fit", overview(bare)[2])
        text, units, issues = overview(bare - 1)                    # then directories merge
        self.assertLess(len(units), 5)
        self.assertEqual(sorted(p for ps in units.values() for p in ps), sorted(ai7.graph.content_files(self.idx)))
        self.assertTrue(any(i.startswith("overview: sub-directories shown as their parent: app/") for i in issues))
        text, units, issues = overview(10)                          # merged up to the repo root
        self.assertEqual(list(units), ["./"])
        self.assertTrue(any("above 10" in i for i in issues))
        self.assertIn("D1 ./ 16 files in 5 dirs | sub-dirs app/ | sure entry x1: [L2] app/main.py:7", text)

    def test_router_tree_skips_prefix_and_other_keywords(self):
        files = {"main.py": "from fastapi import FastAPI\nfrom api import router\nfrom config import PREFIX\n\n"
                            "app = FastAPI()\napp.include_router(router, prefix=PREFIX)\n",
                 "api.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n",
                 "config.py": "PREFIX = '/x'\n"}
        with tempfile.TemporaryDirectory() as tmp:
            for rel, body in files.items():
                (Path(tmp) / rel).write_text(body, encoding="utf-8")
            idx = pyindex.index(Path(tmp), inventory.scan(Path(tmp)))
            tree = ai7._router_tree(idx, calls.facts(idx), ai7.Lines(idx))
        self.assertEqual(tree, ["main.py", "  -> api.py: [L1] main.py:6 app.include_router(router, prefix=PREFIX)"])

    def test_top_blocks_checked_answer_kept(self):
        fake = FakeLLM(top=[TOP_GOOD])
        out = ai7.top_blocks(fake, self.idx, self.facts, self.an)
        self.assertEqual([c["step"] for c in fake.calls], ["top-1"])
        self.assertEqual((out["found"], out["left"], out["issues"], out["source"], out["evidence_by_code"]),
                         ([], [], [], "model", []))
        self.assertEqual(out["blocks"]["routes"]["paths"], ["app/api/", "app/deps.py"])      # "./" dropped
        self.assertEqual(out["blocks"]["logic"]["paths"][0], "app/domain/")                  # a directory gets "/"
        self.assertEqual(out["blocks"]["data"]["reason"],
                         {"file": "app/crud.py", "line": 8, "text": "return await session.execute(select(User))"})
        self.assertEqual(out["shared"], ["app/constants.py"])
        self.assertLessEqual(fake.calls[0]["prompt"], ai7.TOP_PROMPT)
        self.assertEqual(fake.calls[0]["max_tokens"], ai7.LIMIT - fake.calls[0]["prompt"])

    def test_top_blocks_problems_sent_back_once(self):
        fake = FakeLLM(top=[TOP_BAD, TOP_GOOD])
        out = ai7.top_blocks(fake, self.idx, self.facts, self.an)
        self.assertEqual([c["step"] for c in fake.calls], ["top-1", "top-2"])
        found = "\n".join(out["found"])
        for text in ("block models: path 'app/nothing/' holds no file of the repository",
                     "path app/db.py given to two blocks: database, pay",
                     "3 data blocks, above the limit of 2",
                     "block models (data) is called only by block crud (data): a block that only serves one block joins it; "
                     "line app/crud.py:",
                     "data block dto has no file with a model, a query or a database call"):
            self.assertIn(text, found)
        retry = fake.calls[1]
        self.assertIn("Problems found by code, with the facts:\n- ", retry["user"])
        self.assertRegex(retry["user"], r"\ndto \(data\): app/dto\.py \| L\d+\n")   # the first answer, with ids
        self.assertIn("Draft by code", retry["user"])
        self.assertLessEqual(retry["prompt"], ai7.LIMIT - ai7.TOP_ANSWER)
        self.assertEqual((out["left"], out["evidence_by_code"]), ([], []))
        self.assertEqual(sorted(out["blocks"]), ["app", "data", "database", "logic", "pay", "routes"])

    def test_top_blocks_bad_evidence_is_picked_by_code_not_dropped(self):
        out = ai7.top_blocks(FakeLLM(top=[TOP_BAD, TOP_BAD]), self.idx, self.facts, self.an)
        # pay points at main.py (another block); crud at a line never shown: code picks a line of each block
        self.assertEqual(sorted(out["evidence_by_code"]), ["crud", "pay"])
        self.assertEqual(out["blocks"]["pay"]["reason"]["file"], "app/clients/pay.py")
        self.assertEqual(out["blocks"]["crud"]["reason"], {"file": "app/crud.py", "line": 8,
                                                           "text": "return await session.execute(select(User))"})
        self.assertEqual(out["blocks"]["models"]["reason"], {"file": "app/models.py", "line": 1,
                                                             "text": "class User:"})   # the model's own line
        self.assertNotIn("dto", out["blocks"])     # its only path was given to logic first: no file of its own
        self.assertEqual(len(out["left"]), len(out["found"]))

    def test_shared_with_io_or_sure_layer_is_a_problem(self):
        blocks = {"database": {"layer": "infra", "paths": ["app/clients/"], "reason": {}}}
        found = ai7._violations(self.idx, self.facts, self.an, blocks, ["app/db.py", "app/api/"])
        self.assertIn("shared holds app/db.py, sure infra: shared is support without I/O; line app/db.py:3 "
                      "engine = create_async_engine(", "\n".join(found))
        self.assertIn("shared holds app/api/users.py, sure api", "\n".join(found))

    def test_two_api_blocks_registered_by_one_file_is_a_problem(self):
        files = {"main.py": "from fastapi import FastAPI\nimport a\nimport b\n\napp = FastAPI()\n"
                            "app.include_router(a.router)\napp.include_router(b.router)\n",
                 "a.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n\n\n@router.get('/a')\ndef get_a():\n    return 1\n",
                 "b.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n\n\n@router.get('/b')\ndef get_b():\n    return 2\n"}
        with tempfile.TemporaryDirectory() as tmp:
            for rel, body in files.items():
                (Path(tmp) / rel).write_text(body, encoding="utf-8")
            idx = pyindex.index(Path(tmp), inventory.scan(Path(tmp)))
        facts = calls.facts(idx)
        blocks = {"app": {"layer": "entry", "paths": ["main.py"]}, "a_api": {"layer": "api", "paths": ["a.py"]},
                  "b_api": {"layer": "api", "paths": ["b.py"]}}
        found = ai7._violations(idx, facts, flow.analyze(idx, facts), blocks, [])
        self.assertEqual(found, ["api blocks a_api and b_api are both registered by main.py: split api blocks only for a "
                                 "different way in; line main.py:6 app.include_router(a.router)"])

    def test_dry_run_estimates_every_request(self):
        est = run7.dry_run(self.root)
        self.assertTrue({"top-1", "name-1"} <= set(est["prompt_tokens"]))
        self.assertEqual(est["largest_request"], ai7.LIMIT)          # every answer gets the room left
        self.assertGreaterEqual(est["answer_room"]["top-1"], ai7.TOP_ANSWER)
        self.assertEqual(est["not_sent"], [])
        self.assertEqual(est["pass2_worst"]["requests"], 1)

    def test_flow_score_credits_a_diagram_drawn_another_way(self):
        comp = lambda cid, files, shared=False: {"id": cid, "files": files, "shared": shared}
        run = {"components": [comp("C1", ["app/main.py", "app/container.py"]), comp("C2", ["app/api/users.py"]),
                              comp("C3", ["app/api/schemas.py", "app/deps.py"]),          # api split in two
                              comp("C4", ["app/service/user.py", "app/domain/usecase.py", "app/dto.py",
                                          "app/crud.py", "app/models.py"]),                # logic and data merged
                              comp("C5", ["app/db.py"]), comp("C6", ["app/constants.py"], True)],
               "edges": [{"source": a, "target": b} for a, b in (("C1", "C2"), ("C2", "C4"), ("C4", "C5"),
                                                                 ("C2", "C3"))],
               "externals": [], "file_lines": {}}
        f = evaluate.flow_score(run, ORACLE)
        self.assertEqual((f["flow_recall"], f["merged"], f["missed"]), (0.75, 1, []))   # logic -> data hidden in C4
        self.assertEqual((f["flow_precision"], f["right"], f["neutral"], f["wrong"]), (1.0, 3, 1, []))
        self.assertLess(f["ari"], 1)
        same = {"components": [comp(k, [p for p in ai7.graph.content_files(self.idx)
                                        if evaluate.oracle_owner(ORACLE, p) == k]) for k in ORACLE["components"]],
                "edges": [], "externals": []}
        self.assertEqual(evaluate.flow_score(same, ORACLE)["ari"], 1.0)

    def test_request_with_too_little_answer_room_is_not_sent(self):
        fake, issues = FakeLLM(), []
        with unittest.mock.patch.object(ai7, "LIMIT", 2_500):
            self.assertEqual(ai7._json(fake, "s" * 3_000, "", {}, "top-1", ai7.TOP_ANSWER, issues), {})
        self.assertEqual((fake.calls, issues), ([], ["top-1: not sent, answer room 1499 below the 2000 needed"]))


if __name__ == "__main__":
    unittest.main()
