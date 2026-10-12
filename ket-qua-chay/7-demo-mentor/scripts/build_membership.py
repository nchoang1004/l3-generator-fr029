"""Membership for the L3 CLI from one of Khiem's v8 graphs. Blocks keep Khiem's files and names.
A file of the L3 snapshot that no block holds goes, by a fixed rule, to the block holding most files of its
directory, then of the parent directory, ... (not the root); with none, to a block named after its top folder ("Ngoài sơ đồ: x").

    python build_membership.py <repo dir> <graph.json> <out.json> [<prefix of graph paths to drop, e.g. backend/>]
"""
import collections
import json
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, "D:/VSF/l3-generator-l3/slice")
from l3slice import snapshot  # noqa: E402

repo, graph, out = sys.argv[1:4]
cut = sys.argv[4] if len(sys.argv) > 4 else ""
snap, _ = snapshot.take(Path(repo))
files = [f["path"] for f in snap["files"]]
g = json.load(open(graph, encoding="utf-8"))
blocks = {c["name"]: [p[len(cut):] for p in c["files"] if p.startswith(cut) and p[len(cut):] in files] for c in g["components"]}
owner = {p: n for n, ps in blocks.items() for p in ps}
extra = collections.defaultdict(list)
for p in files:
    if p in owner:
        continue
    d, placed = PurePosixPath(p).parent, None
    while placed is None and str(d) not in (".", ""):  # never climb to the root: a root file says nothing of tests/
        near = collections.Counter(owner[q] for q in owner if PurePosixPath(q).parent == d)
        if near:
            placed = sorted(near.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        else:
            d = d.parent
    if placed:
        blocks[placed].append(p)
    else:
        top = p.split("/")[0] if "/" in p else "(gốc)"
        extra[f"Ngoài sơ đồ: {top}"].append(p)
comps = [{"name": n, "files": sorted(ps)} for n, ps in blocks.items() if ps] + \
        [{"name": n, "files": sorted(ps)} for n, ps in sorted(extra.items())]
json.dump({"partition_version": "fixture-membership-v1", "components": comps,
           "_ghi_chu": f"Khối lấy từ {graph}; file Khiêm không xếp được gán theo luật trong build_membership.py"},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(files)} file L3, {len(owner)} file Khiêm đã xếp, {len(comps)} khối:",
      ", ".join(f"{c['name']} ({len(c['files'])})" for c in comps))
