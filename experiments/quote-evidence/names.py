"""What each name in the repository refers to, from Pyright (through scip-python). No AI.

    occurrences(root, scope) -> {path: {(line, col): (target path, top-level name)}}

line and col are 1-based / 0-based as in the ast module. Only names that point at a definition inside the
repository are kept; the target is the file holding that definition and the top-level name is the function,
class or variable of that file (a method counts as its class; a module reference gives None). Names Pyright
cannot place (libraries that are not installed, local variables) are left out, so the caller keeps its own view.

Pyright follows Python's own rules: imports and re-exports through any number of __init__ files, `import *`,
aliases, inheritance across files, string annotations, a parameter hiding an imported name, attribute types
inferred from assignments and return types. calls.py keeps what Pyright does not know: libraries, sessions, I/O,
and what FastAPI does with the names it is given.

Needs Node and scip-python (~/.local/opt/scip) and the scip CLI (~/.local/opt/scip-cli); paths can be set with
L3_SCIP_PYTHON, L3_SCIP, L3_NODE_BIN.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

HOME = Path.home()
SCIP_PYTHON = Path(os.environ.get("L3_SCIP_PYTHON", HOME / ".local/opt/scip/node_modules/.bin/scip-python"))
SCIP = Path(os.environ.get("L3_SCIP", HOME / ".local/opt/scip-cli/scip"))
NODE_BIN = Path(os.environ.get("L3_NODE_BIN", HOME / ".cache/pyright-python/nodeenv/bin"))
TIMEOUT = 900
NODE_HEAP_MB = 3072


def source_root(root: Path, scope: list[str]) -> str:
    """Where imports start: the parent of the outermost package, most common over the files ('backend' for
    backend/app/..., '' when packages sit at the top)."""
    roots = Counter()
    for rel in scope:
        parts = rel.split("/")[:-1]
        i = len(parts)
        while i > 0 and (root / "/".join(parts[:i]) / "__init__.py").exists():
            i -= 1
        roots["/".join(parts[:i])] += 1
    return roots.most_common(1)[0][0] if roots else ""


def _top(symbol: str) -> str | None:
    """'scip-python python repo 0 `app.db`/Repo#get().' -> 'Repo'; a module ('.../__init__:') -> None."""
    desc = symbol.split(" ", 4)[4]
    rest = desc.split("`/", 1)[1] if desc.startswith("`") else desc.split("/", 1)[1]
    name = ""
    for ch in rest:
        if ch in "#().:[":
            break
        name += ch
    return None if name in ("", "__init__") else name


def _index(base: Path) -> dict:
    """The scip index of `base`, printed as JSON."""
    with tempfile.TemporaryDirectory() as tmp:
        env_file, out = Path(tmp) / "env.json", Path(tmp) / "index.scip"
        env_file.write_text("[]")              # no installed packages: libraries stay unresolved, on purpose
        env = {**os.environ, "PATH": f"{NODE_BIN}:{os.environ.get('PATH', '')}",
               "NODE_OPTIONS": f"--max-old-space-size={NODE_HEAP_MB}"}
        run = subprocess.run([str(SCIP_PYTHON), "index", "--quiet", "--project-name", "repo", "--project-version",
                              "0", "--environment", str(env_file), "--cwd", str(base), "--output", str(out)],
                             capture_output=True, text=True, timeout=TIMEOUT, env=env)
        if not out.exists():
            raise RuntimeError(f"scip-python failed: {(run.stderr or run.stdout).strip()[-300:]}")
        printed = subprocess.run([str(SCIP), "print", "--json", str(out)], capture_output=True, text=True,
                                 timeout=TIMEOUT, check=True)
        return json.loads(printed.stdout)


def occurrences(root: Path, scope: list[str]) -> dict:
    root = Path(root).resolve()
    src = source_root(root, scope)
    base = root / src if src else root
    prefix = f"{src}/" if src else ""
    data = _index(base)
    where = {}                                  # symbol -> repository path of the file defining it
    docs = []
    for doc in data.get("documents", []):
        rel = prefix + doc["relative_path"]
        docs.append((rel, doc.get("occurrences", [])))
        for o in doc.get("occurrences", []):
            if o.get("symbol_roles", 0) & 1 and not o["symbol"].startswith("local"):
                where.setdefault(o["symbol"], rel)
    in_scope = set(scope)
    out = {}
    for rel, occ in docs:
        if rel not in in_scope:
            continue
        rows = out.setdefault(rel, {})
        for o in occ:
            target = where.get(o["symbol"])
            if o.get("symbol_roles", 0) & 1 or target not in in_scope:
                continue                        # a definition, a library, or a name Pyright could not place
            line, col = o["range"][0] + 1, o["range"][1]
            rows[(line, col)] = (target, _top(o["symbol"]))
    return out
