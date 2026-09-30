"""Snapshot a repository: hash every file, decide which source files are in scope.

Language-neutral. Rules are conventions shared by most repositories, never per repository.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

# Directory names skipped anywhere in the path: tooling, dependencies, tests, migrations.
EXCLUDED_DIRS = {".git", "node_modules", "venv", ".venv", "env", "__pycache__", "build", "dist",
                 "site-packages", "tests", "test", "testing", "migrations", "alembic", "docs", "examples"}
# Scripts and seed data start side flows (create the first user, send reminders): in scope only when they
# import the repository's own code; a script that imports nothing of the repository is a separate tool.
SIDE_DIRS = {"scripts", "seeds"}
IMPORT_LINE = re.compile(r"^\s*(?:from\s+(\.*)([\w.]*)\s+import|import\s+([\w.]+))", re.M)
TEST_FILE = re.compile(r"(^test_.*|.*_test|^conftest)\.py$")
LANGUAGES = {".py": "python"}          # add ".ts": "typescript" etc. when an indexer exists


def excluded_reason(rel: str) -> str | None:
    parts = rel.split("/")
    for part in parts[:-1]:
        if part in EXCLUDED_DIRS or part.startswith("."):
            return "dir:" + part
    if TEST_FILE.match(parts[-1]):
        return "test_file"
    return None


def _imports_own_code(text: str, names: set[str]) -> bool:
    for m in IMPORT_LINE.finditer(text):
        top = (m.group(2) or m.group(3) or "").split(".")[0]
        if m.group(1) or (top in names and top not in sys.stdlib_module_names):
            return True
    return False


def scan(root: Path) -> dict:
    """Return {files: {path: {sha256, bytes}}, scope: [paths], excluded: {reason: count}}."""
    root = root.resolve()
    files, scope, excluded, side = {}, [], {}, []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/"):
            continue
        raw = path.read_bytes()
        files[rel] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        if path.suffix not in LANGUAGES:
            continue
        reason = excluded_reason(rel)
        if reason:
            key = reason.split(":")[0] + ":" + reason.split(":")[-1]
            excluded[key] = excluded.get(key, 0) + 1
        elif SIDE_DIRS & set(rel.split("/")[:-1]):
            side.append(rel)
        else:
            scope.append(rel)
    names = {part for rel in scope for part in rel[:-3].split("/")}
    for rel in side:
        if _imports_own_code((root / rel).read_text(encoding="utf-8", errors="replace"), names):
            scope.append(rel)
        else:
            excluded["side:no_own_import"] = excluded.get("side:no_own_import", 0) + 1
    scope.sort()
    return {"root": str(root), "files": files, "scope": scope, "excluded": excluded}


def unchanged(snapshot: dict) -> bool:
    """True when every in-scope file still has the recorded hash."""
    root = Path(snapshot["root"])
    for rel in snapshot["scope"]:
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != snapshot["files"][rel]["sha256"]:
            return False
    return True
