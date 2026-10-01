"""Compare call resolvers on the PyCG micro-benchmark (119 small programs, answers written by the PyCG authors).

    ~/.local/opt/probe-venv/bin/python resolver_bench.py [--detail]

Resolvers: calls.py (this pipeline, Pyright inside since 01/10), Jedi (goto on every call), scip-python (Pyright
alone: the definition each use of a name points to). pycg-ml was measured on 01/10 (0,97 / 0,95) and removed:
it fails on Python 3.14 syntax and ran out of memory on lnbits.
Level compared: (file, top-level name) -> (file, top-level name). That is the level the pipeline needs; a method
counts as its class, a nested function as the function holding it, module code as "<module>". Calls into the
standard library or builtins are left out. No AI.
"""
import ast
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import calls, inventory, pyindex  # noqa: E401,E402
import jedi  # noqa: E402

BENCH = Path.home() / ".local/opt/pycg-benchmark/snippets"


def module_of(rel: str) -> str:
    parts = rel[:-3].split("/")
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def tops(path: Path) -> dict:
    """{top-level name: kind}, plus {method name: class} for the fallback of calls.py."""
    tree = ast.parse(path.read_text())
    names, methods = {}, {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names[n.name] = "def"
        elif isinstance(n, ast.ClassDef):
            names[n.name] = "class"
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.setdefault(m.name, n.name)
    return names, methods


def top_of_dotted(name: str, modules: set) -> tuple | None:
    """'pkg.mod.A.f' -> ('pkg.mod', 'A'); 'main' -> ('main', '<module>'); None outside the case."""
    parts = name.split(".")
    for i in range(len(parts), 0, -1):
        mod = ".".join(parts[:i])
        if mod in modules:
            return (mod, parts[i] if i < len(parts) else "<module>")
    return None


def truth(case: Path, modules: set) -> set:
    cg = json.loads((case / "callgraph.json").read_text())
    out = set()
    for caller, callees in cg.items():
        a = top_of_dotted(caller, modules)
        for callee in callees:
            b = top_of_dotted(callee, modules)
            if a and b and a != b:
                out.add((a, b))
    return out


def by_calls(case: Path, files: list, modules: set) -> set:
    snap = inventory.scan(case)
    idx = pyindex.index(case, snap)
    facts = calls.facts(idx)
    info = {rel: tops(case / rel) for rel in files}
    out = set()
    for rel, f in facts.items():
        for c in f["calls"]:
            if c["how"] not in ("call", "decorator") or not c["target"] or c["target"] not in info:
                continue
            names, methods = info[c["target"]]
            sym = next((s for s in (c["symbol"], c["last"]) if s in names), None) \
                or methods.get(c["symbol"]) or methods.get(c["last"])
            if not sym:
                continue
            caller = c["func"].split(".")[0] if c["func"] != "<module>" else "<module>"
            a, b = (module_of(rel), caller), (module_of(c["target"]), sym)
            if a != b:
                out.add((a, b))
    return out


def by_jedi(case: Path, files: list, modules: set) -> set:
    project = jedi.Project(case)
    out = set()
    for rel in files:
        path = case / rel
        code = path.read_text()
        tree = ast.parse(code)
        script = jedi.Script(code, path=path, project=project)
        owner = {}
        for n in tree.body:
            name = n.name if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else "<module>"
            for sub in ast.walk(n):
                owner.setdefault(id(sub), name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            if isinstance(f, ast.Attribute):
                line, col = f.end_lineno, f.end_col_offset - len(f.attr)
            elif isinstance(f, ast.Name):
                line, col = f.lineno, f.col_offset
            else:
                continue
            try:
                found = script.goto(line, col, follow_imports=True)
            except Exception:
                continue
            for d in found:
                if not d.module_path or case not in Path(d.module_path).parents or not d.full_name:
                    continue
                b = top_of_dotted(d.full_name, modules)
                a = (module_of(rel), owner.get(id(node), "<module>"))
                if b and a != b:
                    out.add((a, b))
    return out


SCIP_PY = Path.home() / ".local/opt/scip/node_modules/.bin/scip-python"
SCIP = Path.home() / ".local/opt/scip-cli/scip"
NODE = Path.home() / ".cache/pyright-python/nodeenv/bin"


def scip_index(case: Path) -> dict:
    """{(rel, line0, col0): symbol} for every occurrence that is not a definition, from scip-python (Pyright)."""
    import os
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    env_file = tmp / "env.json"
    env_file.write_text("[]")
    env = {**os.environ, "PATH": f"{NODE}:{os.environ['PATH']}"}
    subprocess.run([str(SCIP_PY), "index", "--quiet", "--project-name", "repo", "--project-version", "0",
                    "--environment", str(env_file), "--cwd", str(case), "--output", str(tmp / "index.scip")],
                   capture_output=True, text=True, timeout=600, env=env)
    printed = subprocess.run([str(SCIP), "print", "--json", str(tmp / "index.scip")], capture_output=True,
                             text=True, timeout=300)
    out = {}
    for doc in json.loads(printed.stdout).get("documents", []):
        for o in doc.get("occurrences", []):
            if o.get("symbol_roles", 0) & 1:          # a definition, not a use
                continue
            line, col = o["range"][0], o["range"][1]
            out[(doc["relative_path"], line, col)] = o["symbol"]
    return out


def scip_top(symbol: str, modules: set) -> tuple | None:
    """'scip-python python repo 0 pkg.mod/A#f().' -> ('pkg.mod', 'A'); other packages (stdlib) -> None."""
    parts = symbol.split(" ")
    if len(parts) < 5 or parts[2] != "repo":
        return None
    desc = " ".join(parts[4:])
    if desc.startswith("`"):                      # a dotted name with dashes is quoted
        mod, _, rest = desc[1:].partition("`/")
    else:
        mod, _, rest = desc.partition("/")
    mod = mod.removesuffix(".__init__")
    parts_mod = mod.split(".")                    # named from the project root: match on the longest tail
    mod = next((".".join(parts_mod[i:]) for i in range(len(parts_mod)) if ".".join(parts_mod[i:]) in modules),
               None)
    if mod is None:
        return None
    name = ""
    for ch in rest:
        if ch in "#().[:":
            break
        name += ch
    return (mod, name or "<module>") if name != "__init__" else (mod, "<module>")


def by_scip(case: Path, files: list, modules: set) -> set:
    occ = scip_index(case)
    out = set()
    for rel in files:
        tree = ast.parse((case / rel).read_text())
        owner = {}
        for n in tree.body:
            name = n.name if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else "<module>"
            for sub in ast.walk(n):
                owner.setdefault(id(sub), name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            if isinstance(f, ast.Attribute):
                key = (rel, f.end_lineno - 1, f.end_col_offset - len(f.attr))
            elif isinstance(f, ast.Name):
                key = (rel, f.lineno - 1, f.col_offset)
            else:
                continue
            sym = occ.get(key)
            b = scip_top(sym, modules) if sym else None
            a = (module_of(rel), owner.get(id(node), "<module>"))
            if b and a != b:
                out.add((a, b))
    return out


def main() -> None:
    detail = "--detail" in sys.argv
    tools = {"calls.py": by_calls, "Jedi": by_jedi, "scip-python": by_scip}
    per_cat = defaultdict(lambda: {t: [0, 0, 0] for t in tools})       # hit, wrong, missed
    for cat in sorted(p for p in BENCH.iterdir() if p.is_dir()):
        for case in sorted(p for p in cat.iterdir() if (p / "callgraph.json").exists()):
            files = sorted(p.relative_to(case).as_posix() for p in case.rglob("*.py"))
            modules = {module_of(r) for r in files}
            want = truth(case, modules)
            for name, fn in tools.items():
                try:
                    got = fn(case, files, modules)
                except Exception as exc:
                    got = set()
                    if detail:
                        print(f"  {name} crashed on {cat.name}/{case.name}: {exc}")
                hit, wrong, missed = len(got & want), len(got - want), len(want - got)
                row = per_cat[cat.name][name]
                row[0] += hit
                row[1] += wrong
                row[2] += missed
                if detail and (wrong or missed):
                    print(f"{name:8} {cat.name}/{case.name}: thiếu {sorted(want - got)} thừa {sorted(got - want)}")
    f2 = lambda x: f"{x:.2f}".replace(".", ",")
    print("| Nhóm | " + " | ".join(f"{t}: P / R" for t in tools) + " |")
    print("|---|" + "---|" * len(tools))
    total = {t: [0, 0, 0] for t in tools}
    for cat, rows in per_cat.items():
        cells = []
        for t in tools:
            h, w, m = rows[t]
            for i, v in enumerate((h, w, m)):
                total[t][i] += v
            cells.append(f"{f2(h / (h + w)) if h + w else '-'} / {f2(h / (h + m)) if h + m else '-'}")
        print(f"| {cat} | " + " | ".join(cells) + " |")
    print("| **Tổng** | " + " | ".join(
        f"**{f2(h / (h + w)) if h + w else '-'} / {f2(h / (h + m)) if h + m else '-'}** (đúng {h}, thừa {w}, thiếu {m})"
        for h, w, m in (total[t] for t in tools)) + " |")


if __name__ == "__main__":
    main()
