"""Python indexer: symbols, imports resolved to repository files, how imported names are used.

Where an imported name points is Pyright's answer (names.py) when it has one: it follows re-exports through any
number of __init__ files. A name Pyright cannot place keeps the file the import statement names.

Knows Python only, not any framework. Another language needs its own indexer returning the same
shape: {path: {lines, error, symbols, signals, imports, uses, external_calls}}.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path, PurePosixPath

import names

STDLIB = set(sys.stdlib_module_names)


def module_map(scope: list[str], all_files: dict) -> dict[str, list[str]]:
    """Dotted name -> files. A name may start at any directory whose parent is not a package,
    so 'backend/app/core/config.py' is reachable as 'app.core.config' but a local 'logging.py'
    inside a package never shadows the standard library 'logging'."""
    packages = {str(PurePosixPath(p).parent) for p in all_files if p.endswith("__init__.py")}
    names: dict[str, list[str]] = {}
    for rel in scope:
        parts = rel.split("/")
        mod = parts[:-1] + ([] if parts[-1] == "__init__.py" else [parts[-1][:-3]])
        for i in range(len(mod)):
            parent = "/".join(parts[:i]) or "."
            if i == 0 or parent not in packages:
                names.setdefault(".".join(mod[i:]), []).append(rel)
    return names


def _closest(candidates: list[str], rel: str) -> str:
    def shared(other: str) -> int:
        n = 0
        for a, b in zip(rel.split("/"), other.split("/")):
            if a != b:
                break
            n += 1
        return n
    return max(sorted(candidates), key=shared)


class _Resolver:
    def __init__(self, scope: list[str], all_files: dict):
        self.scope = set(scope)
        self.mods = module_map(scope, all_files)

    def absolute(self, dotted: str, rel: str) -> str | None:
        found = self.mods.get(dotted)
        return _closest(found, rel) if found else None

    def relative(self, level: int, dotted: str | None, rel: str) -> tuple[str, str | None]:
        base = PurePosixPath(rel).parent
        for _ in range(level - 1):
            base = base.parent
        path = base.joinpath(*dotted.split(".")) if dotted else base
        return str(path), next((c for c in (f"{path}.py", f"{path}/__init__.py") if c in self.scope), None)

    def at(self, path: str) -> str | None:
        return next((c for c in (f"{path}.py", f"{path}/__init__.py") if c in self.scope), None)


def _imports(tree: ast.Module, rel: str, res: _Resolver) -> list[dict]:
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                target = res.absolute(alias.name, rel)
                local = alias.asname or alias.name.split(".")[0]
                rows.append({"line": node.lineno, "local": local, "symbol": None, "target": target,
                             "external": None if target else alias.name.split(".")[0]})
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                path, module_file = res.relative(node.level, node.module, rel)
                sub = lambda name: res.at(f"{path}/{name}")
                external = None
            else:
                module_file = res.absolute(node.module or "", rel)
                sub = lambda name: res.absolute(f"{node.module}.{name}", rel)
                external = (node.module or "").split(".")[0]
            for alias in node.names:
                target = sub(alias.name) if alias.name != "*" else None
                target = target or module_file
                rows.append({"line": node.lineno, "col": alias.col_offset, "local": alias.asname or alias.name,
                             "symbol": alias.name, "target": target,
                             "external": None if target else external})
    return rows


def _use_kinds(tree: ast.Module) -> dict[int, str]:
    """Map id(Name node) -> raise | except | call | annotation | base | decorator; other loads are 'ref'."""
    kinds: dict[int, str] = {}

    def mark(node: ast.AST | None, kind: str) -> None:
        if node is None:
            return
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                kinds.setdefault(id(sub), kind)

    for node in ast.walk(tree):          # exceptions first: 'raise X(...)' is not a call to another component
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
            mark(node.exc.func, "raise")
        elif isinstance(node, ast.Raise):
            mark(node.exc, "raise")
        elif isinstance(node, ast.ExceptHandler):
            mark(node.type, "except")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for dec in node.decorator_list:
                mark(dec, "decorator")
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                mark(base, "base")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            mark(node.returns, "annotation")
            for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                mark(arg.annotation, "annotation")
        if isinstance(node, ast.AnnAssign):
            mark(node.annotation, "annotation")
        if isinstance(node, ast.Call):
            root = node.func
            while isinstance(root, ast.Attribute):
                root = root.value
            if isinstance(root, ast.Name):
                kinds.setdefault(id(root), "call")
    return kinds


def _call_root(call: ast.Call) -> str | None:
    root = call.func
    while isinstance(root, (ast.Attribute, ast.Call)):
        root = root.value if isinstance(root, ast.Attribute) else root.func
    return root.id if isinstance(root, ast.Name) else None


def _signals(tree: ast.Module, stdlib_locals: set[str]) -> tuple[list[dict], list[int]]:
    """Top-level declarations and module-level calls; setup calls into the standard library are noise."""
    symbols, lines = [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            kind = "class" if isinstance(node, ast.ClassDef) else "function"
            symbols.append({"name": node.name, "kind": kind, "line": node.lineno})
            lines.extend(d.lineno for d in node.decorator_list[:1])
            if kind == "class":
                lines.append(node.lineno)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Call):
            if _call_root(node.value) in stdlib_locals:
                continue
            lines.append(node.lineno)
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(target, ast.Name):
                symbols.append({"name": target.id, "kind": "object", "line": node.lineno})
        elif isinstance(node, (ast.Expr, ast.If)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Expr) and isinstance(sub.value, ast.Call) \
                        and _call_root(sub.value) not in stdlib_locals:
                    lines.append(sub.lineno)
    if not lines:                     # a plain script: show its first statement that is not an import
        first = next((n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom, ast.Expr))), None)
        lines = [first.lineno] if first else []
    return symbols, sorted(set(lines))


def index(root: Path, snapshot: dict) -> dict[str, dict]:
    res = _Resolver(snapshot["scope"], snapshot["files"])
    pointed = names.occurrences(root, snapshot["scope"])
    out = {}
    for rel in snapshot["scope"]:
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        entry = {"lines": text.splitlines(), "error": None, "symbols": [], "signals": [],
                 "imports": [], "uses": {}, "external_calls": []}
        out[rel] = entry
        try:
            tree = ast.parse(text, filename=rel)
        except SyntaxError as exc:
            entry["error"] = f"SyntaxError line {exc.lineno}: {exc.msg}"
            continue
        body = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
        entry["empty"] = not body
        entry["imports"] = _imports(tree, rel, res)
        entry["names"] = pointed.get(rel, {})
        for row in entry["imports"]:           # 'from pkg import X': the file that defines X, per Pyright
            hit = entry["names"].get((row["line"], row.get("col")))
            if row["symbol"] and hit:
                row["target"], row["external"] = hit[0], None
        stdlib_locals = {r["local"] for r in entry["imports"] if r["external"] in STDLIB}
        entry["symbols"], entry["signals"] = _signals(tree, stdlib_locals)
        locals_ = {row["local"]: row for row in entry["imports"]}
        kinds = _use_kinds(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in locals_:
                kind = kinds.get(id(node), "ref")
                entry["uses"].setdefault(node.id, []).append([node.lineno, kind])
                if kind == "call" and locals_[node.id]["external"]:
                    entry["external_calls"].append([node.lineno, node.id, locals_[node.id]["external"]])
        for rows in entry["uses"].values():
            rows.sort()
        entry["external_calls"].sort()
    return out

