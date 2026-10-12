"""No-AI run of Khiem's pipeline (run7, every model request answers nothing) on rhoboro-demo. 0 token.
Writes graph.json, diagram.mmd, score.json, steps.json to the output dir."""
import json
import sys
import time
from pathlib import Path

ROOT = Path("D:/VSF/l3-generator-quote-evidence")
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import names  # noqa: E402
import run7  # noqa: E402

# This Windows machine has no scip-python/Pyright: imports fall back to the file the import statement names.
names.occurrences = lambda root, scope: {}


class Nothing:
    calls = []

    def json(self, *a, **k):
        return {}


out = Path(sys.argv[1])
oracle = json.loads((Q / "oracle/rhoboro-async-fastapi-sqlalchemy.json").read_text(encoding="utf-8"))
t = time.perf_counter()
summary = run7.run(ROOT / "sample-repos/rhoboro-demo", out, Nothing(), oracle, True)
summary["wall_s"] = round(time.perf_counter() - t, 2)
print(json.dumps(summary, ensure_ascii=False, indent=2))
