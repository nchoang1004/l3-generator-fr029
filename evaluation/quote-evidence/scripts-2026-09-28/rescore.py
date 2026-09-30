"""Score existing runs against the oracle before the hand-drawing sync (oracle/rev3/) and the current one
(rev 4, synced to oracle/ve-tay/*.md). No AI call. Internal edges, the pipeline's own drawing.
Tokens: meta.tokens of the run; 0 means every response came from the cache."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import evaluate  # noqa: E402

RUNS = [("rhoboro", "v4-rhoboro", "rhoboro-async-fastapi-sqlalchemy.json"),
        ("teamhide", "v3-teamhide", "teamhide-fastapi-boilerplate.json"),
        ("boilerplate", "v3-boilerplate", "fastapi-boilerplate.json"),
        ("lnbits", "v5-lnbits", "lnbits.json"),
        ("fba", "v6-fba", "fastapi-best-architecture.json"),
        ("fullstack", "fullstack-r4", "full-stack-fastapi-template.json"),
        ("realworld", "realworld-r1", "fastapi-realworld.json"),
        ("kibo", "kibo-r3", "kibo-backend.json")]
f = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
ppr = lambda p: f"{f(p['precision'])} / {f(p['precision_strict'])} / {f(p['recall'])}"
print("| Repo | Lần chạy | Khối | Bản cũ: P / Pk / R | Bản 4: P / Pk / R | Bản 4 ngoài: P / Pk / R | Trích dẫn | Token |")
print("|---|---|---:|---|---|---|---:|---:|")
for name, run, orc in RUNS:
    g = json.loads((ROOT / "evaluation/quote-evidence/runs" / run / "graph.json").read_text(encoding="utf-8"))
    g.setdefault("file_lines", {})
    scores = [evaluate.score(g, json.loads((ROOT / "experiments/quote-evidence/oracle" / folder / orc)
                                           .read_text(encoding="utf-8"))) for folder in ("rev3", ".")]
    print(f"| {name} | `{run}` | {len(g['components'])} | {ppr(scores[0]['internal'])} | {ppr(scores[1]['internal'])} "
          f"| {ppr(scores[1]['external'])} | {f(scores[1]['quote_validity'])} | {g['meta'].get('tokens', '-')} |")
