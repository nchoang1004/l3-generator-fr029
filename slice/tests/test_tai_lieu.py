"""TAI-LIEU.md: một file đọc chính cho người (cách A, người dùng chọn 11/10/2026), và kiểm loại component của membership.

Các file cũ (README, file API, result.json) giữ nguyên; TAI-LIEU.md sinh từ cùng dữ kiện.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from l3slice.docagent import ScriptedProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402
from test_docagent import FINDINGS, run, script  # noqa: E402


class OneReadableFile(unittest.TestCase):
    def setUp(self):
        self.t, self.out, self.bundle = run(ScriptedProvider(script(bad=False)))
        self.addCleanup(self.t.cleanup)
        self.text = (self.out / "TAI-LIEU.md").read_text(encoding="utf-8")

    def test_is_published_with_the_other_files(self):
        art = next(a for a in self.bundle["artifacts"] if a["path"] == "TAI-LIEU.md")
        self.assertEqual((art["kind"], art["status"]), ("readme", "ready"))

    def test_has_the_sections_in_order(self):
        heads = [line for line in self.text.splitlines() if line.startswith("## ")]
        self.assertEqual(heads, ["## 1. Danh sách endpoint", "## 2. Chi tiết từng endpoint", "## 3. Model dữ liệu",
                                 "## 4. Bảng CSDL", "## 5. Sự kiện và tác vụ nền", "## 6. Cấu trúc code",
                                 "## 7. Gọi HTTP ra ngoài", "## 8. Thư viện", "## 9. Cấu hình",
                                 "## 10. Middleware và xử lý lỗi toàn cục", "## 11. Chưa biết và giới hạn",
                                 "## Phụ lục: file cho máy"])

    def test_inferred_reasons_are_written_once_as_notes(self):
        section = self.text.split("\n## 2.")[1].split("\n## 3.")[0]
        self.assertIn("suy luận [1]", section)
        self.assertEqual(section.count("Decorator không khai status_code"), 1)  # once, in the notes

    def test_endpoints_models_and_calls_are_there_in_plain_words(self):
        self.assertIn("| 1 | POST | /api/v1/items/ | ItemIn | ItemOut | 201 |", self.text)
        self.assertIn("| GET | /api/v1/items/{item_id} |", self.text)
        self.assertIn("| verbose | query | boolean | không |", self.text)  # parameter: place, type, required
        self.assertIn("| price | number | không | có |", self.text)  # model field: required no, nullable yes
        self.assertIn("https://audit.example.com/log", self.text)
        self.assertIn("`app/api/items.py:9`", self.text)  # where a route is declared

    def test_no_machine_noise(self):
        for noise in ("fact:", "ev:", "True", "False", "fastapi.default_status_200", "```json"):
            self.assertNotIn(noise, self.text)

    def test_status_and_limits_are_stated(self):
        self.assertIn("| Tình trạng | Đủ |", self.text)
        self.assertIn("app/main.py:13", self.text)  # route registered without a decorator: a limitation
        self.assertIn("[tech-specs/MUC-HANG/api/API-FR029-E2E-MUC-HANG-v1.md]", self.text)


SRC = {"main.py": 'from fastapi import FastAPI\napp = FastAPI()\n\n\n@app.get("/x")\ndef x():\n    return 1\n',
       "pkg/__init__.py": "",
       "tests/test_x.py": "def test_x():\n    assert True\n"}
X_ROUTE = {"method": "GET", "handler": "main.py::x", "decorator": "main.py:5-6", "application": "main.py:2",
           "path_parts": [{"kind": "decorator", "value": "/x", "at": "main.py:5"}], "params": [], "request_body": None,
           "response": None, "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [],
           "auth": {"unknown": "chưa rõ"}}


def run_repo(components):
    t = tempfile.TemporaryDirectory()
    root = Path(t.name)
    for rel, text in SRC.items():
        (root / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / "src" / rel).write_text(text, encoding="utf-8")
    (root / "m.json").write_text(json.dumps({"components": components}), encoding="utf-8")
    findings = {"routes": [X_ROUTE], "file_roles": [{"file": "main.py", "role": "Điểm vào", "at": "main.py:2"}]}
    steps = [[("read_file", {"path": "main.py"})], [("submit_findings", findings)], [("finish", {})]]
    bundle = run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))
    return t, root / "out", bundle


class PartialRun(unittest.TestCase):
    def test_lines_left_unconfirmed_are_listed_and_the_status_has_no_code(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        root = Path(t.name)
        (root / "src").mkdir()
        (root / "src/main.py").write_text(SRC["main.py"], encoding="utf-8")
        (root / "m.json").write_text(json.dumps({"components": [{"name": "App", "files": ["main.py"]}]}), encoding="utf-8")
        steps = [[("read_file", {"path": "main.py"})], [("finish", {})]]  # the route is never submitted
        run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider(steps))
        text = (root / "out/TAI-LIEU.md").read_text(encoding="utf-8")
        status = next(line for line in text.splitlines() if line.startswith("| Tình trạng"))
        self.assertIn("Chưa đủ", status)
        self.assertNotRegex(status, r"[A-Z_]{6,}:")
        self.assertIn("`main.py:5`", text.split("## 6.")[1])


class ComponentKinds(unittest.TestCase):
    def test_missing_kind_of_a_test_only_component_is_read_from_the_scope(self):
        t, out, bundle = run_repo([{"name": "App", "files": ["main.py", "pkg/__init__.py"]},
                                   {"name": "tests", "files": ["tests/test_x.py"]}])
        self.addCleanup(t.cleanup)
        kinds = {c["name"]: c["kind"] for c in bundle["components"]}
        self.assertEqual(kinds, {"App": "normal", "tests": "test"})
        readme = (out / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("### tests", readme)
        self.assertIn("`pkg/__init__.py` — file rỗng, không có vai trò", readme)
        self.assertNotIn("tests/test_x.py", (out / "TAI-LIEU.md").read_text(encoding="utf-8"))

    def test_an_explicit_normal_kind_on_test_files_is_reported(self):
        t, out, bundle = run_repo([{"name": "App", "kind": "normal", "files": ["main.py", "pkg/__init__.py"]},
                                   {"name": "tests", "kind": "normal", "files": ["tests/test_x.py"]}])
        self.addCleanup(t.cleanup)
        self.assertEqual({c["name"]: c["kind"] for c in bundle["components"]}, {"App": "normal", "tests": "normal"})
        self.assertIn("MEMBERSHIP_KIND_SUSPECT", [x["code"] for x in bundle["limitations"]])


class Presentation(unittest.TestCase):
    """Chỗ khó đọc thấy ở đầu ra Teamhide khi agent Claude đóng vai model (12/10/2026)."""

    def test_error_statuses_are_listed_once_and_column_types_are_short(self):
        from l3slice.tailieu import _column_type, _status_codes
        a = {"status_codes": {"state": "known", "value": [200]},
             "errors": {"state": "known", "value": [{"status": 400}, {"status": 400}, {"status": 401}]}}
        self.assertEqual(_status_codes(a), "200, 400*, 401*")
        unknown = {"state": "unknown", "reason": "Chưa xác định SQL dialect từ source; khai trong code: String(255)"}
        self.assertEqual(_column_type(unknown), "String(255) (chưa quy ra kiểu SQL)")
        self.assertEqual(_column_type({"state": "known", "value": "VARCHAR(255)"}), "VARCHAR(255)")

    def test_foreign_key_reads_as_table_dot_column(self):
        from l3slice.tailieu import _fk_text
        self.assertEqual(_fk_text({"state": "known", "value": {"table": "orders", "column": "id"}}), "orders.id")
        self.assertEqual(_fk_text({"state": "not_applicable", "reason": "Không khai ForeignKey"}), "—")


class Cli(unittest.TestCase):
    def test_document_command_in_oneshot_mode_writes_tai_lieu(self):
        import os
        import subprocess
        from test_docagent import FIX, MEMBERSHIP
        with tempfile.TemporaryDirectory() as t:
            script = Path(t) / "s.json"
            script.write_text(json.dumps([[{"name": "submit_findings", "arguments": FINDINGS}]]), encoding="utf-8")
            env = dict(os.environ, PYTHONPATH=str(HERE.parent), PYTHONIOENCODING="utf-8")
            proc = subprocess.run([sys.executable, "-m", "l3slice", "document", "--source", str(FIX), "--output",
                                   str(Path(t) / "out"), "--membership", str(MEMBERSHIP), "--script", str(script),
                                   "--mode", "oneshot", "--checkpoint", str(Path(t) / "ck.json"), "--json"],
                                  capture_output=True, text=True, encoding="utf-8", env=env)
            result = json.loads(proc.stdout)
            self.assertEqual(result["agent"]["mode"], "oneshot")
            self.assertIn("TAI-LIEU.md", [f["path"] for f in result["files"]])
            self.assertTrue((Path(t) / "ck.json").exists())


if __name__ == "__main__":
    unittest.main()
