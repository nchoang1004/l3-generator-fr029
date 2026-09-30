"""Help write an oracle (rev 3) from code, not from memory of results.

    python oracle_tool.py <repo dir> <oracle.json> [--finalize]

- Lists files that belong to no component (they are left out of scoring on purpose, or were forgotten).
- Lists every import-proven edge between components with the code lines that prove it; the writer picks
  the flow edges for `required` by reading these lines.
- --finalize: writes `acceptable` = every import-proven edge that is not required and touches no shared
  component (drawing it is not wrong, it is just not part of a flow). Rows marked "hand" (written by hand),
  "wiring" (assembly: DI container, start-up, shut-down; real but not a processing flow), "pass" (a
  session/client only handed on to another component), "check" (a token/permission/session check that
  returns) or "up" (goes from a lower layer to a higher one) stay.
- Lists components that are not shared and have no valid layer, and required edges that go up a layer.
- Lists every "file:line code" (layers, required, labelled acceptable) whose code is not that line, verbatim.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import evaluate, graph, inventory, pyindex  # noqa: E402

LAYERS = ("entry", "api", "service", "data", "infra")
LABELS = ("hand", "wiring", "pass", "check", "up")


def load(repo: Path, oracle_path: Path):
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    idx = pyindex.index(repo, inventory.scan(repo))
    shared = set(oracle.get("shared", []))
    comps = {}
    for p in graph.content_files(idx):
        key = evaluate.oracle_owner(oracle, p)
        if key:
            comps.setdefault(key, {"id": key, "key": key, "shared": key in shared, "files": []})["files"].append(p)
    return oracle, idx, comps


def dump(oracle: dict) -> str:
    """One entry per line, so an oracle reads and diffs well."""
    j = lambda v: json.dumps(v, ensure_ascii=False)
    out = []
    for k, v in oracle.items():
        if isinstance(v, dict):
            out.append(f" {j(k)}: {{\n" + ",\n".join(f"  {j(a)}: {j(b)}" for a, b in v.items()) + "\n }")
        elif isinstance(v, list) and v and isinstance(v[0], list):
            out.append(f" {j(k)}: [\n" + ",\n".join(f"  {j(x)}" for x in v) + "\n ]")
        else:
            out.append(f" {j(k)}: {j(v)}")
    return "{\n" + ",\n".join(out) + "\n}\n"


def main() -> None:
    repo, path = Path(sys.argv[1]), Path(sys.argv[2])
    oracle, idx, comps = load(repo, path)
    owned = {p for c in comps.values() for p in c["files"]}
    loose = defaultdict(list)
    for p in graph.content_files(idx):
        if p not in owned:
            loose[str(PurePosixPath(p).parent)].append(PurePosixPath(p).name)
    print(f"# {len(owned)} files in {len(comps)} components; {sum(map(len, loose.values()))} files outside")
    for d, names in sorted(loose.items()):
        print(f"  outside {d}/: {' '.join(names)}")
    empty = [k for k in oracle["components"] if k not in comps]
    if empty:
        print("  components with no file:", empty)
    edges = graph.candidates(idx, comps)
    required = {(r[0], r[1]) for r in oracle.get("required", [])}
    shared = set(oracle.get("shared", []))
    print(f"# {len(edges)} import edges (R = in required, S = touches shared)")
    for e in sorted(edges.values(), key=lambda e: (e["source"], e["target"])):
        mark = ("R" if (e["source"], e["target"]) in required else " ") + \
               ("S" if e["source"] in shared or e["target"] in shared else " ")
        kinds = sorted({k for u in e["symbols"].values() for k in u})
        p, n = e["lines"][0]
        print(f" {mark} {e['source']} -> {e['target']}  [{','.join(kinds)}] {','.join(list(e['symbols'])[:4])}"
              f"  | {p}:{n} {idx[p]['lines'][n - 1].strip()[:90]}")
    missing = [r for r in oracle.get("required", []) if not r[1].startswith("ext:")
               and (r[0], r[1]) not in {(e['source'], e['target']) for e in edges.values()}]
    for r in missing:
        print(f"  required without import: {r[0]} -> {r[1]} | {r[2] if len(r) > 2 else ''}")
    no_layer = [k for k in oracle["components"]
                if k not in shared and oracle.get("layers", {}).get(k, [None])[0] not in LAYERS]
    if no_layer:
        print("  no layer:", no_layer)
    rank = {k: LAYERS.index(v[0]) for k, v in oracle.get("layers", {}).items() if v and v[0] in LAYERS}
    for r in oracle.get("required", []):
        if r[0] in rank and r[1] in rank and rank[r[1]] < rank[r[0]]:
            print(f"  upward: {r[0]} ({LAYERS[rank[r[0]]]}) -> {r[1]} ({LAYERS[rank[r[1]]]})")
    quotes = [(f"layer {k}", v[1]) for k, v in oracle.get("layers", {}).items() if len(v) > 1]
    quotes += [(f"{r[0]} -> {r[1]}", r[2]) for r in oracle.get("required", []) if len(r) > 2]
    quotes += [(f"{a[0]} -> {a[1]} ({a[2]})", a[3]) for a in oracle.get("acceptable", []) if len(a) > 3]
    for what, quote in quotes:
        m = re.match(r"(\S+):(\d+) (.*)$", quote)
        f = repo / m[1] if m else None
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines() if f and f.is_file() else []
        if not m or not 0 < int(m[2]) <= len(lines) or lines[int(m[2]) - 1].strip() != m[3].strip():
            print(f"  quote mismatch: {what} | {quote[:100]}")
    if "--finalize" in sys.argv:
        hand = [a for a in oracle.get("acceptable", []) if len(a) > 2 and a[2] in LABELS]
        auto = sorted({(e["source"], e["target"]) for e in edges.values()} - required
                      - {(a[0], a[1]) for a in hand})
        auto = [list(a) for a in auto if a[0] not in shared and a[1] not in shared]
        oracle["acceptable"] = hand + auto
        path.write_text(dump(oracle), encoding="utf-8")
        print(f"# wrote {len(auto)} code-made acceptable edges (+{len(hand)} by hand)")


if __name__ == "__main__":
    main()
