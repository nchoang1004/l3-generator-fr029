"""Phần thêm của route (11/10/2026): lỗi có thể trả về, tags, deprecated, mô tả do AI viết. Model đề xuất, bộ kiểm
đòi bằng chứng; ví dụ thật: Teamhide đổi CustomException thành JSON qua exception_handler, service ném lỗi 400/401/404."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from openapi_spec_validator import validate as validate_openapi  # noqa: E402

from l3slice.docagent import ScriptedProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402
from test_checker_counterexamples import claims_of  # noqa: E402

EXC = ('class CustomException(Exception):\n    code = 400\n    error_code = "BAD"\n\n\n'
       'class NotFound(CustomException):\n    code = 404\n\n\nclass Silent(CustomException):\n    pass\n')
SERVICE = ('from exc import NotFound, Silent\nfrom fastapi import HTTPException\n\n\ndef find(i):\n    if i < 0:\n'
           '        raise NotFound()\n    if i == 0:\n        raise HTTPException(status_code=409, detail="x")\n    return i\n\n\n'
           'def unused():\n    raise Silent()\n')
MAIN = ('from fastapi import FastAPI, Request\nfrom fastapi.responses import JSONResponse\nfrom exc import CustomException\n'
        'from service import find\napp = FastAPI()\n\n\n@app.exception_handler(CustomException)\n'
        'async def handle(request: Request, exc: CustomException):\n    return JSONResponse(status_code=exc.code, content={})\n\n\n'
        '@app.get("/items/{i}", tags=["items"], deprecated=True)\ndef get_item(i: int):\n    """Đọc một item."""\n'
        '    return find(i)\n')
FILES = {"exc.py": EXC, "service.py": SERVICE, "main.py": MAIN}
NOT_FOUND = {"status": 404, "exception": "NotFound", "raised_at": "service.py:7", "status_at": "exc.py:7"}
CONFLICT = {"status": 409, "exception": "HTTPException", "raised_at": "service.py:9"}


def route(**extra):
    r = {"method": "GET", "handler": "main.py::get_item", "decorator": "main.py:13-14", "application": "main.py:5",
         "path_parts": [{"kind": "decorator", "value": "/items/{i}", "at": "main.py:13"}],
         "params": [{"name": "i", "in": "path", "type": "integer", "required": True, "nullable": False, "at": "main.py:14"}],
         "request_body": None, "response": None, "status": {"codes": [200], "rule": "fastapi.default_status_200"},
         "dependencies": [], "auth": {"unknown": "chưa rõ"}}
    r.update(extra)
    return r


def errors_of(files, item):
    return " ".join(e for x in claims_of(files).submit({"routes": [item]})["errors"] for e in x["errors"])


class Errors(unittest.TestCase):
    def test_reachable_raises_with_their_status_are_accepted(self):
        self.assertEqual(errors_of(FILES, route(errors=[NOT_FOUND, CONFLICT])), "")

    def test_a_status_the_subclass_overrides_is_refused(self):
        self.assertIn("errors[0]", errors_of(FILES, route(errors=[dict(NOT_FOUND, status=400, status_at="exc.py:2")])))

    def test_a_raise_the_handler_never_reaches_is_refused(self):
        silent = {"status": 400, "exception": "Silent", "raised_at": "service.py:14", "status_at": "exc.py:2"}
        self.assertIn("errors[0].raised_at", errors_of(FILES, route(errors=[silent])))

    def test_http_exception_status_must_be_the_one_written(self):
        self.assertIn("errors[0].status", errors_of(FILES, route(errors=[dict(CONFLICT, status=404)])))

    def test_without_an_exception_handler_the_status_is_not_proven(self):
        bare = dict(FILES, **{"main.py": MAIN.replace("@app.exception_handler(CustomException)", "# no handler")})
        self.assertIn("exception_handler", errors_of(bare, route(errors=[NOT_FOUND])))

    def test_a_line_without_the_raise_is_refused(self):
        self.assertIn("errors[0].raised_at", errors_of(FILES, route(errors=[dict(NOT_FOUND, raised_at="service.py:5")])))


class StatusThroughInit(unittest.TestCase):
    """orderflow (chấm held-out 12/10/2026): mã truyền qua super().__init__(..., status_code=404), handler dùng
    exc.status_code. Bộ kiểm chỉ nhận `code = 404` nên từ chối nhầm, cả route bị loại ở lần nộp đầu."""

    ERR = ('class AppError(Exception):\n    def __init__(self, message, status_code: int = 400):\n'
           '        super().__init__(message)\n        self.status_code = status_code\n\n\n'
           'class NotFoundError(AppError):\n    def __init__(self, message="x"):\n'
           '        super().__init__(message, status_code=404)\n')
    SVC = 'from err import NotFoundError\n\n\ndef find(i):\n    raise NotFoundError()\n'
    MAIN = ('from fastapi import FastAPI\nfrom fastapi.responses import JSONResponse\nfrom err import AppError\n'
            'from svc import find\napp = FastAPI()\n\n\n@app.exception_handler(AppError)\n'
            'async def h(request, exc: AppError):\n    return JSONResponse(status_code=exc.status_code, content={})\n\n\n'
            '@app.get("/items/{i}")\ndef get_item(i: int):\n    return find(i)\n')

    def item(self, status, status_at):
        return route(errors=[{"status": status, "exception": "NotFoundError", "raised_at": "svc.py:5",
                              "status_at": status_at}], deprecated=None)

    def test_status_passed_to_the_base_init_is_accepted(self):
        files = {"err.py": self.ERR, "svc.py": self.SVC, "main.py": self.MAIN}
        self.assertEqual(errors_of(files, self.item(404, "err.py:9")), "")

    def test_a_different_status_or_the_base_default_is_refused(self):
        files = {"err.py": self.ERR, "svc.py": self.SVC, "main.py": self.MAIN}
        self.assertIn("errors[0].status_at", errors_of(files, self.item(409, "err.py:9")))
        self.assertIn("errors[0].status_at", errors_of(files, self.item(400, "err.py:2")))  # overridden by the subclass


class TagsDeprecatedSummary(unittest.TestCase):
    def test_written_values_are_accepted(self):
        item = route(tags={"value": ["items"], "at": "main.py:13"}, deprecated={"at": "main.py:13"},
                     summary={"text": "Đọc một item theo id", "at": "main.py:15"})
        self.assertEqual(errors_of(FILES, item), "")

    def test_values_not_in_the_source_are_refused(self):
        self.assertIn("tags", errors_of(FILES, route(tags={"value": ["admin"], "at": "main.py:13"})))
        self.assertIn("deprecated", errors_of(FILES, route(deprecated={"at": "main.py:14"})))
        self.assertIn("summary", errors_of(FILES, route(summary={"text": "x", "at": "main.py:5"})))


EX_MAIN = ('from fastapi import FastAPI, Body\nfrom pydantic import BaseModel\napp = FastAPI()\n\n\n'
           'class Out(BaseModel):\n    a: int\n    model_config = {"json_schema_extra": {"examples": [{"a": 2}]}}\n\n\n'
           '@app.post("/x", response_model=Out)\ndef x(payload: dict = Body(..., example={"a": 1})):\n    return payload\n'
           'SAMPLE = {"examples": [{"z": 0}]}\n')


def ex_route(**extra):
    r = {"method": "POST", "handler": "main.py::x", "decorator": "main.py:11-12", "application": "main.py:3",
         "path_parts": [{"kind": "decorator", "value": "/x", "at": "main.py:11"}], "params": [],
         "request_body": {"models": [], "type": "object", "param": "payload", "media_type": "application/json",
                          "required": True, "embedded": False, "at": "main.py:12"},
         "response": {"model": "main.py::Out", "array": False, "at": "main.py:11"},
         "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [], "auth": {"unknown": "chưa rõ"}}
    r.update(extra)
    return r


class Examples(unittest.TestCase):
    def test_literal_examples_in_the_handler_or_a_used_model_are_kept(self):
        c = claims_of({"main.py": EX_MAIN})
        self.assertEqual(c.submit({"routes": [ex_route(examples=[{"at": "main.py:12"}, {"at": "main.py:8"}])]})["errors"], [])
        [r] = c.routes.values()
        self.assertEqual([x["value"] for x in r["examples"]], [{"a": 1}, [{"a": 2}]])

    def test_shown_in_tai_lieu(self):
        out_model = {"id": "main.py::Out", "at": "main.py:6",
                     "fields": [{"name": "a", "alias": None, "type": "integer", "required": True, "nullable": False,
                                 "at": "main.py:7"}]}
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "src").mkdir()
            (root / "src/main.py").write_text(EX_MAIN, encoding="utf-8")
            (root / "m.json").write_text(json.dumps({"components": [{"name": "App", "files": ["main.py"]}]}),
                                         encoding="utf-8")
            steps = [[("read_file", {"path": "main.py"})],
                     [("submit_findings", {"models": [out_model], "routes": [ex_route(examples=[{"at": "main.py:12"}])]})],
                     [("finish", {})]]
            run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))
            text = (root / "out" / "TAI-LIEU.md").read_text(encoding="utf-8")
        self.assertIn('- Ví dụ (từ code): `{"a": 1}`', text)

    def test_lines_without_an_example_or_outside_the_route_are_refused(self):
        msg = errors_of({"main.py": EX_MAIN}, ex_route(examples=[{"at": "main.py:13"}]))
        self.assertIn("examples[0]", msg)
        msg = errors_of({"main.py": EX_MAIN}, ex_route(examples=[{"at": "main.py:14"}]))  # literal, but not this route's
        self.assertIn("examples[0]", msg)


class Published(unittest.TestCase):
    def test_openapi_and_tai_lieu_show_them(self):
        item = route(errors=[NOT_FOUND, CONFLICT], tags={"value": ["items"], "at": "main.py:13"},
                     deprecated={"at": "main.py:13"}, summary={"text": "Đọc một item theo id", "at": "main.py:15"})
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for rel, text in FILES.items():
                (root / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / "src" / rel).write_text(text, encoding="utf-8")
            (root / "m.json").write_text(json.dumps({"components": [{"name": "App", "files": sorted(FILES)}]}),
                                         encoding="utf-8")
            steps = [[("read_file", {"path": p}) for p in FILES], [("submit_findings", {"routes": [item]})], [("finish", {})]]
            bundle = run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))
            api_art = next(a for a in bundle["artifacts"] if a["kind"] == "api")
            self.assertEqual(api_art["status"], "ready", api_art.get("error"))
            api = (root / "out" / api_art["path"]).read_text(encoding="utf-8")
            text = (root / "out" / "TAI-LIEU.md").read_text(encoding="utf-8")
        doc = json.loads(re.findall(r"^```json\n(.*?)^```", api, re.M | re.S)[0])
        validate_openapi(doc)
        op = doc["paths"]["/items/{i}"]["get"]
        self.assertEqual(sorted(op["responses"]), ["200", "404", "409"])
        self.assertEqual((op["tags"], op["deprecated"]), (["items"], True))
        self.assertIn("Lỗi có thể trả về: 404 — NotFound", text)
        self.assertIn("| 200, 404*, 409* |", text)
        self.assertIn("Mô tả (AI viết): Đọc một item theo id", text)
        self.assertIn("- Nhóm (tags): items", text)


if __name__ == "__main__":
    unittest.main()
