"""FR-029 N2: read-only tools over one snapshot, and a ledger of what the model has really been sent.

Scope follows FR-028 "Phạm vi đọc"; the code decides it, not the model. The model sees only in-scope files.
A range counts as `delivered` when a tool result carried it and as `processed` only after the model answered
the next turn without error. Search hits never count as reading.
Secrets are masked line by line, so line numbers in what the model sees match the snapshot.
"""
from __future__ import annotations

import re

from .common import SECRET_PATTERNS

LINES_PER_READ = 200
MAX_LINE_CHARS = 400
FILES_PER_PAGE = 100
HITS_PER_SEARCH = 30

TEST_DIRS = {"tests", "test"}
MIGRATION_DIRS = {"migrations", "alembic"}
ENV_DIRS = {"node_modules", "__pycache__", "site-packages"}
CONDITIONAL_DIRS = {"scripts", "seeds", "docs", "examples", "build", "dist", "env", "venv", "testing"}
PEM = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)
TRIPLE = re.compile(r"""(?is)(password|passwd|secret|token|api_key|apikey)['"]?\s*[=:]\s*[rbu]{0,2}('{3}|"{3})(.*?)\2""")
LINE_PATTERNS = [p for p in SECRET_PATTERNS if p.pattern != PEM.pattern] + [
    # a credential-like key written as a quoted dict key, and triple-quoted values: {"password": "..."}, x = """..."""
    # also `password: str = "..."` and names like SECRET_KEY / db_password (annotation between name and =)
    re.compile(r"""(?i)(\w*(?:password|passwd|secret|token|api_key|apikey)\w*['"]?\s*(?::[^=\n]*)?[=:]\s*[rbuRBU]{0,2})"""
               r"""('{3}|"{3}|'|")(?:(?!\2).){4,}?\2"""),
]


def classify(path: str, top_names: set[str], text: str, env_roots: set[str] = frozenset()) -> tuple[str, str]:
    """(scope, reason). scope: analysis | test | migration | environment | conditional_out | manifest.
    `env_roots`: directories that hold a `pyvenv.cfg` (virtual environments, whatever their name)."""
    parts = path.split("/")
    name = parts[-1]
    dirs = parts[:-1]
    if not name.endswith(".py"):
        return "manifest", "Manifest Python, không chứa route hay lời gọi"
    if any(d.startswith(".") for d in dirs) or any(d in ENV_DIRS for d in dirs) \
            or any("/".join(dirs[:i + 1]) in env_roots for i in range(len(dirs))):
        return "environment", "Thư mục ẩn hoặc môi trường (FR-028 Phạm vi đọc)"
    if any(d in TEST_DIRS for d in dirs) or name.startswith("test_") or name.endswith("_test.py") or name == "conftest.py":
        return "test", "File kiểm thử (FR-028 Phạm vi đọc)"
    if any(d in MIGRATION_DIRS for d in dirs):
        return "migration", "File migration (FR-028 Phạm vi đọc)"
    cond = next((d for d in dirs if d in CONDITIONAL_DIRS), None)
    if cond is not None:
        own = {n for n in top_names if n != cond}
        if re.search(r"^\s*from\s+\.", text, re.M) or \
                any(re.search(rf"^\s*(?:from|import)\s+{re.escape(n)}\b", text, re.M) for n in own):
            return "analysis", f"Trong `{cond}/` nhưng import code của repository"
        return "conditional_out", f"Trong `{cond}/` và không import code của repository (FR-028 Phạm vi đọc)"
    return "analysis", "Trong phạm vi phân tích"


def masked_lines(text: str) -> list[str]:
    """Mask secrets without changing the number of lines. A multi-line private key becomes `***` on every line."""
    lines = text.split("\n")
    for m in TRIPLE.finditer(text):  # credential in a triple-quoted string that spans lines
        first, last = text.count("\n", 0, m.start(3)), text.count("\n", 0, m.end(3))
        if first == last:
            continue  # one line: LINE_PATTERNS handle it
        start_of_first = text.rfind("\n", 0, m.start(3)) + 1
        end_of_last = text.find("\n", m.end(3))
        lines[first] = text[start_of_first:m.start(3)] + "***"
        for i in range(first + 1, last):
            lines[i] = "***"
        lines[last] = "***" + text[m.end(3):end_of_last if end_of_last != -1 else len(text)]
    for m in PEM.finditer(text):
        first, last = text.count("\n", 0, m.start()), text.count("\n", 0, m.end())
        for i in range(first, last + 1):
            lines[i] = "***"
    out = []
    for line in lines:
        for p in LINE_PATTERNS:
            line = _sub(p, line)
        out.append(line)
    return out


def mask_text(text: str) -> str:
    """Mask a free text (an error message, a reason) with the same patterns, for anything published."""
    return "\n".join(masked_lines(text)) if isinstance(text, str) else text


def _sub(p, line: str) -> str:
    """Same replacement as `common.mask`, for one pattern on one line."""
    if p.groups == 3:
        return p.sub(lambda m: m.group(1) + "***" + m.group(3), line)
    if p.groups == 2:
        return p.sub(lambda m: m.group(1) + m.group(2) + "***" + m.group(2), line)
    return p.sub("***", line)


class SourceTools:
    """Tools the agent may call. Nothing here writes, imports or runs repository code."""

    def __init__(self, snapshot: dict, sources: dict[str, bytes]):
        self.snapshot_id = snapshot["snapshot_id"]
        self.files = {f["path"]: f for f in snapshot["files"]}
        self.raw = {p: sources[p].decode("utf-8", errors="replace") for p in self.files}
        self.lines = {p: t.replace("\r\n", "\n").replace("\r", "\n").split("\n") for p, t in self.raw.items()}
        for p, ls in self.lines.items():  # a final newline does not make an extra line
            if len(ls) > 1 and ls[-1] == "":
                ls.pop()
            if ls == [""]:
                self.lines[p] = []
        self.shown = {p: masked_lines("\n".join(ls)) if ls else [] for p, ls in self.lines.items()}
        top = set()
        for p in self.files:  # importable top-level names, flat and src/ layouts
            parts = p.split("/")
            top.add(parts[0].removesuffix(".py"))
            if parts[0] == "src" and len(parts) > 1:
                top.add(parts[1].removesuffix(".py"))
        env_roots = {e["path"].rsplit("/", 1)[0] for e in snapshot.get("excluded", [])
                     if e["path"].endswith("pyvenv.cfg") and "/" in e["path"]}
        self.scope = {p: classify(p, top, self.raw[p], env_roots) for p in sorted(self.files)}
        # manifests are read too: the Pydantic major version decides required/nullable (A02)
        self.readable = [p for p, (s, _) in self.scope.items() if s in ("analysis", "manifest")]
        # line -> state per file: "delivered" | "processed"; "cut" lines are delivered only partly
        self.state: dict[str, dict[int, str]] = {p: {} for p in self.readable}
        self.cut: dict[str, set[int]] = {p: set() for p in self.readable}
        self.receipts: list[dict] = []
        self.pending: list[int] = []  # receipt indexes waiting for the model's next answer

    # ---- tools

    def list_files(self, cursor: int = 0) -> dict:
        cursor = cursor if isinstance(cursor, int) and cursor >= 0 else 0
        page = self.readable[cursor:cursor + FILES_PER_PAGE]
        nxt = cursor + FILES_PER_PAGE if cursor + FILES_PER_PAGE < len(self.readable) else None
        out = {"files": [{"path": p, "lines": len(self.lines[p]), "scope": self.scope[p][0]} for p in page],
               "next_cursor": nxt}
        if cursor == 0:
            out["not_readable"] = self.not_readable()
        return out

    def read_file(self, path: str, start_line: int = 1, end_line: int | None = None) -> dict:
        if path not in self.state:
            reason = self.scope[path][1] if path in self.scope else "Không có trong snapshot"
            return {"error": f"Không đọc được {path}: {reason}"}
        n = len(self.lines[path])
        if n == 0:
            self.receipts.append({"path": path, "start": 0, "end": 0})
            self.pending.append(len(self.receipts) - 1)
            return {"receipt": len(self.receipts) - 1, "path": path, "start_line": 0, "end_line": 0, "total_lines": 0,
                    "text": "(file rỗng)"}
        if not isinstance(start_line, int) or start_line < 1 or start_line > n:
            return {"error": f"start_line phải trong 1..{n}"}
        end = n if end_line is None else end_line
        if not isinstance(end, int) or end < start_line:
            return {"error": "end_line phải ≥ start_line"}
        end = min(end, n, start_line + LINES_PER_READ - 1)
        out, cut = [], []
        for i in range(start_line, end + 1):
            text = self.shown[path][i - 1]
            if len(text) > MAX_LINE_CHARS:
                text = text[:MAX_LINE_CHARS] + " …[dòng bị cắt]"
                cut.append(i)
            out.append(f"{i:>5}| {text}")
        for i in range(start_line, end + 1):
            self.state[path].setdefault(i, "delivered")
        self.cut[path].update(cut)
        self.receipts.append({"path": path, "start": start_line, "end": end})
        self.pending.append(len(self.receipts) - 1)
        res = {"receipt": len(self.receipts) - 1, "path": path, "start_line": start_line, "end_line": end,
               "total_lines": n, "text": "\n".join(out)}
        if end < n:
            res["note"] = f"Còn dòng {end + 1}–{n} chưa đọc"
        if cut:
            res["cut_lines"] = cut
        return res

    def search_text(self, query: str, cursor: int = 0) -> dict:
        if not isinstance(query, str) or not query or len(query) > 200:
            return {"error": "query phải là chuỗi 1–200 ký tự"}
        cursor = cursor if isinstance(cursor, int) and cursor >= 0 else 0
        hits = [{"path": p, "line": i + 1} for p in self.readable for i, line in enumerate(self.shown[p])
                if query in line]
        page = hits[cursor:cursor + HITS_PER_SEARCH]
        nxt = cursor + HITS_PER_SEARCH if cursor + HITS_PER_SEARCH < len(hits) else None
        return {"hits": page, "next_cursor": nxt, "note": "Kết quả tìm kiếm không tính là đã đọc"}

    # ---- ledger

    def model_answered(self):
        """Call after a valid model reply: everything delivered before it is now processed."""
        for idx in self.pending:
            r = self.receipts[idx]
            for i in range(r["start"], r["end"] + 1):
                if i:
                    self.state[r["path"]][i] = "processed"
        self.pending = []

    def was_delivered(self, path: str, start: int, end: int) -> bool:
        st = self.state.get(path)
        return st is not None and all(i in st for i in range(start, end + 1))

    def coverage(self) -> dict:
        files = []
        for p in self.readable:
            n, st = len(self.lines[p]), self.state[p]
            done = sum(1 for v in st.values() if v == "processed")
            gaps = _ranges([i for i in range(1, n + 1) if st.get(i) != "processed"])
            files.append({"path": p, "lines": n, "processed_lines": done, "missing": gaps,
                          "cut_lines": sorted(self.cut[p]),
                          "status": "empty" if n == 0 else ("processed" if not gaps else
                                                            ("partial" if done else "unread"))})
        complete = all(f["status"] in ("processed", "empty") and not f["cut_lines"] for f in files)
        return {"complete": complete, "files": files, "not_readable": self.not_readable()}

    def not_readable(self) -> list[dict]:
        return [{"path": p, "scope": s, "reason": r} for p, (s, r) in self.scope.items() if p not in self.state]

    def unread(self) -> list[dict]:
        return [{"path": f["path"], "missing": f["missing"]} for f in self.coverage()["files"] if f["missing"]]


def _ranges(nums: list[int]) -> list[list[int]]:
    out = []
    for n in nums:
        if out and out[-1][1] == n - 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out
