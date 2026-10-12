"""Lỗi bộ kiểm FR-029 tìm ngày 11/10/2026: review code (docs/FR029-review-code-va-de-bai-20261011.md) và lượt chạy
"đọc một lần" trên Teamhide. Mỗi lỗi có ca phải bị từ chối và ca đúng phải vẫn được nhận.
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from openapi_spec_validator import validate as validate_openapi  # noqa: E402

from l3slice import render  # noqa: E402
from l3slice.docagent import ScriptedProvider  # noqa: E402
from l3slice.docfacts import Claims  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402
from test_checker_counterexamples import claims_of, main_py, reminders, route  # noqa: E402
from test_docagent import tools_for  # noqa: E402


def errors_of(claims, kind, item):
    return " ".join(e for x in claims.submit({kind: [item]})["errors"] for e in x["errors"])


class EmptyFile(unittest.TestCase):
    """1. open_problems đòi vai trò cho file rỗng, add_role lại từ chối vai trò của file rỗng."""

    def test_empty_file_needs_no_role(self):
        c = claims_of({"pkg/__init__.py": "", "pkg/main.py": "x = 1\n"})
        problems = " ".join(c.open_problems([{"name": "P", "kind": "normal", "files": ["pkg/__init__.py", "pkg/main.py"]}]))
        self.assertNotIn("pkg/__init__.py", problems)
        self.assertIn("pkg/main.py", problems)


class ProvideDependency(unittest.TestCase):
    """2. Depends(Provide[Container.x]): không tên nào được nhận, còn dependencies=[] thì lọt."""

    FILES = {"di.py": "class Provide:\n    pass\n\n\nclass Container:\n    svc = 1\n",
             "main.py": main_py("from di import Provide, Container", '@app.get("/e")',
                                "def e(s=Depends(Provide[Container.svc])):")}

    def test_target_is_named_as_written(self):
        c = claims_of(self.FILES)
        self.assertTrue(c.dependency_at("Provide[Container.svc]", ("main.py", 7, 7)))
        self.assertFalse(c.dependency_at("Provide[Container.other]", ("main.py", 7, 7)))
        self.assertEqual(errors_of(c, "routes", route("main.py::e", "main.py:6-7", "/e",
                                                      deps=[("Provide[Container.svc]", "main.py:7")])), "")
        self.assertNotIn("Provide", reminders(c))

    def test_a_call_is_named_by_its_function(self):
        c = claims_of({"perm.py": "class Perm:\n    def __init__(self, roles):\n        pass\n",
                       "main.py": main_py("from perm import Perm", '@app.get("/e")', "def e(p=Depends(Perm([1]))):")})
        self.assertEqual(errors_of(c, "routes", route("main.py::e", "main.py:6-7", "/e", deps=[("Perm", "main.py:7")])), "")
        self.assertIn("ghi tên hàm f", errors_of(c, "routes", route("main.py::e", "main.py:6-7", "/e",
                                                                    deps=[("Perm([1])", "main.py:7")])))

    def test_leaving_it_out_is_reminded(self):
        c = claims_of(self.FILES)
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e")]})
        self.assertIn("Depends(Provide[Container.svc])", reminders(c))


class DuplicateParameter(unittest.TestCase):
    """3. Tham số trùng làm OpenAPI hỏng mà file API vẫn ready."""

    def test_same_name_and_place_twice_is_refused(self):
        c = claims_of({"main.py": main_py("", '@app.get("/e")', "def e(q: int = 0, x_token: str = Header()):")})
        q = {"name": "q", "in": "query", "type": "integer", "required": False, "nullable": False, "at": "main.py:7"}
        h = {"name": "x-token", "in": "header", "type": "string", "required": True, "nullable": False, "at": "main.py:7"}
        self.assertIn("trùng", errors_of(c, "routes", dict(route("main.py::e", "main.py:6-7", "/e"), params=[q, dict(q)])))
        self.assertIn("trùng", errors_of(c, "routes", dict(route("main.py::e", "main.py:6-7", "/e"),
                                                          params=[h, dict(h, name="X-Token")])))  # HTTP header names ignore case
        self.assertEqual(errors_of(c, "routes", dict(route("main.py::e", "main.py:6-7", "/e"), params=[q, h])), "")

    def test_invalid_openapi_is_a_format_problem(self):
        doc = {"openapi": "3.1.0", "info": {"title": "t", "version": "1"}, "paths": {"/e": {"get": {
            "parameters": [{"name": "q", "in": "query", "schema": {"type": "integer"}}] * 2,
            "responses": {"200": {"description": "ok"}}}}}}
        self.assertIn("OpenAPI", render.openapi_problem("```json\n" + json.dumps(doc) + "\n```\n"))
        doc["paths"]["/e"]["get"]["parameters"] = doc["paths"]["/e"]["get"]["parameters"][:1]
        self.assertIsNone(render.openapi_problem("```json\n" + json.dumps(doc) + "\n```\n"))


LONG_TAIL = " " * 460


class CutLine(unittest.TestCase):
    """4. Giá trị nằm ở phần dòng bị cắt (model chưa thấy) vẫn được nhận."""

    def claims(self, line):
        t = tools_for({"a.py": "import httpx\n" + line + "\n"})
        t.read_file("a.py")
        t.model_answered()
        return Claims(t)

    def test_value_in_the_cut_part_is_refused(self):
        c = self.claims('httpx.get(' + LONG_TAIL + '"https://hidden.example/x")')
        self.assertTrue(c.add_http({"at": "a.py:2", "library": "httpx", "method": "GET",
                                    "target": {"kind": "literal", "value": "https://hidden.example/x"}}))

    def test_value_before_the_cut_passes(self):
        c = self.claims('httpx.get("https://seen.example/x", timeout=1)  #' + LONG_TAIL)
        self.assertEqual(c.add_http({"at": "a.py:2", "library": "httpx", "method": "GET",
                                     "target": {"kind": "literal", "value": "https://seen.example/x"}}), [])


AUTH_MAIN = ('from fastapi import FastAPI, Depends\nfrom fastapi.security import OAuth2PasswordBearer\napp = FastAPI()\n'
             'oauth = OAuth2PasswordBearer(tokenUrl="t")\n\n@app.get("/e")\ndef e(token: str = Depends(oauth), q: int = 0):\n'
             '    pass\n')


class Auth(unittest.TestCase):
    """5. Auth bịa, dẫn một dòng không liên quan, vẫn thành dữ kiện known."""

    def item(self, at):
        return dict(route("main.py::e", "main.py:6-7", "/e", deps=[("oauth", "main.py:7")]),
                    auth={"value": "OAuth2 bearer token", "at": at})

    def test_auth_on_a_line_without_security_signal_is_refused(self):
        self.assertIn("auth.at", errors_of(claims_of({"main.py": AUTH_MAIN}), "routes", self.item("main.py:3")))

    def test_auth_from_the_security_scheme_passes(self):
        self.assertEqual(errors_of(claims_of({"main.py": AUTH_MAIN}), "routes", self.item("main.py:4")), "")
        self.assertEqual(errors_of(claims_of({"main.py": AUTH_MAIN}), "routes", self.item("main.py:7")), "")


BODY_ROUTE = 'from fastapi import FastAPI, Body\napp = FastAPI()\n\n\n@app.post("/x")\ndef x(payload: dict = Body(...)):\n    return payload\n'


def body(**kw):
    return dict({"models": [], "param": "payload", "media_type": "application/json", "required": True,
                 "embedded": False, "at": "main.py:6"}, **kw)


class PlainJsonBody(unittest.TestCase):
    """6. Body JSON không có model Pydantic (dict, list[int]) không khai được."""

    def item(self, b):
        return dict(route("main.py::x", "main.py:5-6", "/x", method="POST", application="main.py:2"), request_body=b)

    def test_declared_type_is_accepted(self):
        self.assertEqual(errors_of(claims_of({"main.py": BODY_ROUTE}), "routes", self.item(body(type="object"))), "")

    def test_no_model_and_no_type_is_refused(self):
        self.assertIn("request_body", errors_of(claims_of({"main.py": BODY_ROUTE}), "routes", self.item(body())))

    def test_published_as_the_request_schema(self):
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / "src"
            src.mkdir()
            (src / "main.py").write_text(BODY_ROUTE, encoding="utf-8")
            membership = Path(t) / "m.json"
            membership.write_text(json.dumps({"components": [{"name": "Demo", "kind": "normal", "files": ["main.py"]}]}),
                                  encoding="utf-8")
            findings = {"routes": [self.item(body(type="object"))],
                        "file_roles": [{"file": "main.py", "role": "Điểm vào", "at": "main.py:2"}]}
            steps = [[("read_file", {"path": "main.py"})], [("submit_findings", findings)], [("finish", {})]]
            bundle = run_documents(src, Path(t) / "out", membership, "demo", ScriptedProvider(steps))
            self.assertEqual(bundle["agent"]["status"], "completed")
            api = next((Path(t) / "out").rglob("API-*.md")).read_text(encoding="utf-8")
            self.assertTrue(all(a["status"] == "ready" for a in bundle["artifacts"]))
        doc = json.loads(re.findall(r"^```json\n(.*?)^```", api, re.M | re.S)[0])
        validate_openapi(doc)
        op = doc["paths"]["/x"]["post"]
        self.assertEqual(op["requestBody"]["content"]["application/json"]["schema"]["type"], "object")
        self.assertTrue(op["requestBody"]["required"])


class ServiceChain(unittest.TestCase):
    """7. Đường gọi Service bịa (không có lời gọi giữa các bước) vẫn được nhận."""

    REAL = {"route.py": 'from fastapi import FastAPI\nfrom helper import helper\napp = FastAPI()\n@app.get("/x")\n'
                        'def x():\n    return helper()\n',
            "helper.py": "from db import save\ndef helper():\n    return save(None)\n",
            "db.py": "def save(db):\n    db.commit()\n"}

    def role(self, path):
        return {"file": "helper.py", "role": "Service", "at": "helper.py:" + path[1], "call_path": path}

    def test_invented_chain_is_refused(self):
        fake = {"route.py": 'from fastapi import FastAPI\napp = FastAPI()\n@app.get("/x")\ndef x(): return 1\n',
                "helper.py": "def helper(): return 2\n", "db.py": "def save(db): db.commit()\n"}
        errs = claims_of(fake).add_role({"file": "helper.py", "role": "Service", "at": "helper.py:1",
                                         "call_path": ["route.py:4", "helper.py:1", "db.py:1"]})
        self.assertIn("call_path", " ".join(errs))

    def test_real_chain_passes(self):
        self.assertEqual(claims_of(self.REAL).add_role({"file": "helper.py", "role": "Service", "at": "helper.py:3",
                                                        "call_path": ["route.py:6", "helper.py:3", "db.py:2"]}), [])

    def test_a_skipped_step_is_refused(self):
        errs = claims_of(self.REAL).add_role({"file": "helper.py", "role": "Service", "at": "helper.py:3",
                                              "call_path": ["route.py:6", "db.py:2", "helper.py:3"]})
        self.assertIn("call_path", " ".join(errs))


MODELS = ("from typing import Optional\nfrom pydantic import BaseModel, Field\n\n\nclass Tag(BaseModel):\n    label: str\n\n\n"
          "class ItemIn(BaseModel):\n    name: str\n    price: float | None = None\n    tags: list[Tag] = []\n"
          "    note: Optional[str]\n    code: int = Field(..., alias=\"c\")\n    meta: \"Meta\" = None\n")
# lines:  9 class ItemIn, 10 name, 11 price, 12 tags, 13 note, 14 code, 15 meta


def field(name, line, type_, required, nullable, **kw):
    return dict({"name": name, "alias": None, "type": type_, "required": required, "nullable": nullable,
                 "at": f"m.py:{line}"}, **kw)


class ModelFields(unittest.TestCase):
    """8. Kiểu, required, nullable của trường model không được so với source."""

    def model(self, *fields):
        return {"id": "m.py::ItemIn", "at": "m.py:9", "fields": list(fields)}

    def test_wrong_type_required_nullable_are_refused(self):
        c = claims_of({"m.py": MODELS})
        self.assertIn("type", errors_of(c, "models", self.model(field("price", 11, "boolean", False, True))))
        self.assertIn("required", errors_of(c, "models", self.model(field("price", 11, "number", True, True))))
        self.assertIn("nullable", errors_of(c, "models", self.model(field("price", 11, "number", False, False))))
        self.assertIn("required", errors_of(c, "models", self.model(field("code", 14, "integer", False, False, alias="c"))))
        self.assertIn("type", errors_of(c, "models", self.model(field("tags", 12, "array[string]", False, False))))

    def test_matching_fields_pass_and_undecidable_ones_are_left_to_the_agent(self):
        c = claims_of({"m.py": MODELS})
        good = self.model(field("name", 10, "string", True, False), field("price", 11, "number", False, True),
                          field("tags", 12, "array[m.py::Tag]", False, False),
                          field("note", 13, "string", True, True, rule="pydantic.v2_required_no_default"),
                          field("code", 14, "integer", True, False, alias="c"),
                          field("meta", 15, "object", False, True))
        self.assertEqual(errors_of(c, "models", good), "")
        # Optional without default: v1 and v2 differ; a string annotation is not read: both are not checked
        self.assertEqual(errors_of(c, "models", self.model(field("note", 13, "string", False, True))), "")

    def test_unchecked_fields_lower_the_confidence(self):
        src = ('from fastapi import FastAPI\nfrom pydantic import BaseModel\napp = FastAPI()\nclass Out(BaseModel):\n'
               '    a: int\n    b: "Later" = None\n@app.get("/x", response_model=Out)\ndef x():\n    return {}\n')
        fields = [field("a", 5, "integer", True, False), field("b", 6, "object", False, True)]
        for given, want in ((fields[:1], "exact"), (fields, "inferred")):
            with tempfile.TemporaryDirectory() as t:
                (Path(t) / "src").mkdir()
                (Path(t) / "src/main.py").write_text(src, encoding="utf-8")
                (Path(t) / "m.json").write_text(json.dumps({"components": [
                    {"name": "Demo", "kind": "normal", "files": ["main.py"]}]}), encoding="utf-8")
                findings = {"models": [{"id": "main.py::Out", "at": "main.py:4",
                                        "fields": [dict(f, at=f["at"].replace("m.py", "main.py")) for f in given]}],
                            "routes": [dict(route("main.py::x", "main.py:7-8", "/x", application="main.py:3"),
                                            response={"model": "main.py::Out", "array": False, "at": "main.py:7"})],
                            "file_roles": [{"file": "main.py", "role": "Điểm vào", "at": "main.py:3"}]}
                steps = [[("read_file", {"path": "main.py"})], [("submit_findings", findings)], [("finish", {})]]
                bundle = run_documents(Path(t) / "src", Path(t) / "out", Path(t) / "m.json", "demo",
                                       ScriptedProvider(steps))
            model = next(f for f in bundle["facts"] if f["kind"] == "model")
            self.assertEqual(model["confidence"], want)
            if want == "inferred":
                self.assertIn("b", model["confidence_reason"])


class RolePlayFindings(unittest.TestCase):
    """Tìm khi cho agent Claude đóng vai model trên tdd-docker (12/10/2026): bộ kiểm từ chối nhầm."""

    def test_prefix_literal_on_a_later_line_of_include_router(self):
        main = ('from fastapi import FastAPI\nfrom api import router\napp = FastAPI()\napp.include_router(\n'
                '    router, prefix="/summaries", tags=["s"]\n)\n')
        api = 'from fastapi import APIRouter\nrouter = APIRouter()\n\n\n@router.get("/x")\ndef x():\n    pass\n'
        item = dict(route("api.py::x", "api.py:5-6", "/x", application="main.py:3"),
                    path_parts=[{"kind": "include_prefix", "value": "/summaries", "at": "main.py:5"},
                                {"kind": "decorator", "value": "/x", "at": "api.py:5"}])
        self.assertEqual(errors_of(claims_of({"main.py": main, "api.py": api}), "routes", item), "")
        wrong = dict(item, path_parts=[{"kind": "include_prefix", "value": "/summaries", "at": "main.py:3"},
                                       item["path_parts"][1]])
        self.assertIn("path_parts[0]", errors_of(claims_of({"main.py": main, "api.py": api}), "routes", wrong))

    def test_a_callable_class_given_to_depends_reaches_its_call_method(self):
        # Teamhide: dependencies=[Depends(PermissionDependency([IsAdmin]))]; FastAPI calls PermissionDependency.__call__
        files = {"route.py": ('from fastapi import FastAPI, Depends\nfrom perm import Perm\napp = FastAPI()\n'
                              '@app.get("/x", dependencies=[Depends(Perm([1]))])\ndef x():\n    return 1\n'),
                 "perm.py": ("from db import load\n\n\nclass Perm:\n    def __init__(self, roles):\n        self.roles = roles\n\n"
                             "    async def __call__(self):\n        return load()\n"),
                 "db.py": "def load(session=None):\n    return session.get(1)\n"}
        c = claims_of(files)
        self.assertEqual(c.add_role({"file": "perm.py", "role": "Service", "at": "perm.py:9",
                                     "call_path": ["route.py:4", "perm.py:9", "db.py:2"]}), [])

    def test_a_model_made_at_run_time_is_a_schema_signal(self):
        src = ('from tortoise import fields, models\nfrom tortoise.contrib.pydantic import pydantic_model_creator\n\n\n'
               'class TextSummary(models.Model):\n    url = fields.TextField()\n\n\nSummarySchema = pydantic_model_creator(TextSummary)\n')
        c = claims_of({"m.py": src})
        self.assertEqual(c.add_role({"file": "m.py", "role": "Schema API", "at": "m.py:9"}), [])
        self.assertTrue(c.add_role({"file": "m.py", "role": "Schema API", "at": "m.py:6"}))


if __name__ == "__main__":
    unittest.main()
