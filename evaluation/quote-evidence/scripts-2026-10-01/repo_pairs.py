"""File pairs (a calls into b) found by calls.py and scip-python on the sample repositories. No oracle,
no AI: counts, overlap, time, crashes. Pairs inside one file are left out.

    ~/.local/opt/probe-venv/bin/python repo_pairs.py [--show <repo dir name>] [--max-files N]

Memory (the first run on 10 repositories in one process filled 15 GB): each tool on each repository runs in its
own child process, one at a time, smallest repository first, under caps (scip-python:
Node heap 3 GB, 10 minutes; pycg-ml, measured and removed on 01/10, filled the memory). Over a cap = reported as failed. Results kept in repo_pairs_cache/.
"""
import ast
import json
import subprocess
import sys
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
sys.path.insert(0, str(HERE))
import calls, flow, inventory, pyindex  # noqa: E401,E402
import resolver_bench as rb  # noqa: E402

REPOS = [p for p in (ROOT / "sample-repos").iterdir() if p.is_dir()]
CACHE = HERE / "repo_pairs_cache"
CAP_BYTES = 3 * 1024 ** 3
TIMEOUT = 600


def file_of(dotted: str, by_module: dict) -> str | None:
    parts = dotted.split(".")
    for i in range(len(parts), 0, -1):
        for j in range(i):                      # the tool may name modules from a deeper root
            hit = by_module.get(".".join(parts[j:i]))
            if hit:
                return hit
    return None


def source_root(repo: Path, scope: list) -> str:
    """The directory imports start from: the parent of the outermost package, most common over the files
    ('backend' for backend/app/..., '' for app/... at the top)."""
    from collections import Counter
    roots = Counter()
    for rel in scope:
        parts = rel.split("/")[:-1]
        i = len(parts)
        while i > 0 and (repo / "/".join(parts[:i]) / "__init__.py").exists():
            i -= 1
        roots["/".join(parts[:i])] += 1
    return roots.most_common(1)[0][0] if roots else ""


def local_modules(scope: list, root: str) -> dict:
    """Module names counted from the source root ('app.db' for project/app/db.py when the root is 'project')."""
    out = {}
    for f in scope:
        if root and f.startswith(root + "/"):
            out[rb.module_of(f[len(root) + 1:])] = f
    return out


def pairs_calls(repo: Path, scope: list) -> set:
    """Pairs from resolved calls only (call, decorator, Depends, route dependency, router registration)."""
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    return {(a, c["target"]) for a, f in facts.items() for c in f["calls"]
            if c["target"] and c["target"] != a and c["how"] in ("call", "decorator", "depends", "route_dep", "routing")}


def pairs_scip(repo: Path, scope: list, by_module: dict) -> set:
    root = source_root(repo, scope)
    base = repo / root if root else repo
    occ = rb.scip_index(base)                      # paths relative to the source root
    by_module = {**by_module, **local_modules(scope, root)}
    modules = set(by_module)
    out = set()
    for rel in scope:
        if root and not rel.startswith(root + "/"):
            continue
        local = rel[len(root) + 1:] if root else rel
        try:
            tree = ast.parse((repo / rel).read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            if isinstance(f, ast.Attribute):
                key = (local, f.end_lineno - 1, f.end_col_offset - len(f.attr))
            elif isinstance(f, ast.Name):
                key = (local, f.lineno - 1, f.col_offset)
            else:
                continue
            sym = occ.get(key)
            top = rb.scip_top(sym, modules) if sym else None
            b = by_module.get(top[0]) if top else None
            if b and b != rel:
                out.add((rel, b))
    return out


def one(repo: Path, tool: str) -> list:
    scope = inventory.scan(repo)["scope"]
    by_module = {rb.module_of(f): f for f in scope}
    fn = {"c": lambda: pairs_calls(repo, scope), "s": lambda: pairs_scip(repo, scope, by_module)}[tool]
    return sorted(map(list, fn()))


def run_cached(repo: Path, tool: str) -> dict:
    """One tool on one repository in a child process; the result is cached as JSON."""
    CACHE.mkdir(exist_ok=True)
    out = CACHE / f"{repo.name}-{tool}.json"
    if out.exists():
        return json.loads(out.read_text())
    env = {**os.environ, "NODE_OPTIONS": "--max-old-space-size=3072"}
    t = time.perf_counter()
    try:
        got = subprocess.run([sys.executable, "-B", __file__, "--one", repo.name, tool], capture_output=True,
                             text=True, timeout=TIMEOUT + 60, env=env)
        pairs = json.loads(got.stdout) if got.returncode == 0 and got.stdout.strip() else None
        error = None if pairs is not None else ((got.stderr.strip().splitlines() or ["?"])[-1][:120])
    except subprocess.TimeoutExpired:
        pairs, error = None, "timeout"
    row = {"pairs": pairs, "error": error, "seconds": round(time.perf_counter() - t)}
    out.write_text(json.dumps(row))
    return row


def main() -> None:
    if "--one" in sys.argv:
        i = sys.argv.index("--one")
        print(json.dumps(one(ROOT / "sample-repos" / sys.argv[i + 1], sys.argv[i + 2])))
        return
    show = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None
    most = int(sys.argv[sys.argv.index("--max-files") + 1]) if "--max-files" in sys.argv else 10 ** 9
    sized = sorted(((len(inventory.scan(r)["scope"]), r) for r in REPOS), key=lambda x: x[0])
    print("| Repo | file | calls.py | scip-python | chung | chỉ calls.py | chỉ scip | giây c / s |")
    print("|---|---:|---:|---:|---:|---:|---:|---|", flush=True)
    for size, repo in sized:
        if size > most:
            continue
        rows = {t: run_cached(repo, t) for t in "cs"}
        sets = {t: {tuple(x) for x in (rows[t]["pairs"] or [])} for t in "cs"}
        c, s = sets["c"], sets["s"]
        n = lambda t: f"hỏng ({rows[t]['error']})" if rows[t]["pairs"] is None else len(sets[t])
        print(f"| {repo.name[:28]} | {size} | {n('c')} | {n('s')} | {len(c & s)} | {len(c - s)} | {len(s - c)} | "
              f"{rows['c']['seconds']} / {rows['s']['seconds']} |", flush=True)
        if show and show in repo.name:
            for label, only in (("chỉ calls.py", c - s), ("chỉ scip", s - c)):
                print(f"  {label}:", *sorted(only)[:20], sep="\n    ")

if __name__ == "__main__":
    main()
