"""For each L3 output: contract schemas (ResultData, ResultBundle, invariants), artifact sha, OpenAPI 3.1 blocks,
evidence re-read from the source tree, and a second CLI run compared byte by byte (only run_id may differ)."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "D:/VSF/l3-generator-l3/slice/tests")
import contracts  # noqa: E402
from openapi_spec_validator import validate  # noqa: E402

SLICE = Path("D:/VSF/l3-generator-l3/slice")
CASES = [  # (output dir, source dir, membership)
    ("7-demo-mentor/l3-rhoboro", "rhoboro-demo", "7-demo-mentor/membership-tu-khiem.json"),
    ("8-repo-khiem/l3-fullstack-goc", "full-stack-fastapi-template-cb740b6", "8-repo-khiem/membership-fullstack-goc.json"),
    ("8-repo-khiem/l3-realworld", "fastapi-realworld-diagram", "8-repo-khiem/membership-realworld.json"),
    ("8-repo-khiem/l3-teamhide", "teamhide_fastapi-boilerplate-df4e6d4", "8-repo-khiem/membership-teamhide.json"),
]
K = Path("D:/VSF/l3-generator-l3/ket-qua-chay")
SR = Path("D:/VSF/l3-generator-quote-evidence/sample-repos")
for out, src, mem in CASES:
    d, s = K / out, SR / src
    r = json.loads((d / "result.json").read_text(encoding="utf-8"))
    m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    contracts.validate(r, 8, "ResultData")
    contracts.validate(m, 8, "ResultBundle")
    contracts.check_bundle_invariants(m)
    bad_art = [a["path"] for a in m["artifacts"] if hashlib.sha256((d / a["path"]).read_bytes()).hexdigest() != a["sha256"]]
    ops = 0
    for md in d.glob("tech-specs/*/api/*.md"):
        for block in re.findall(r"```json\n(.*?)\n```", md.read_text(encoding="utf-8"), re.S):
            if '"openapi"' in block:
                spec = json.loads(block)
                validate(spec)
                ops += sum(1 for p in spec["paths"].values() for k in p if k in ("get", "post", "put", "patch", "delete"))
    evs = [e for f in r["result"]["facts"]["facts"] for e in f["evidence"]]
    bad_ev = sum(1 for e in evs if hashlib.sha256((s / e["path"]).read_bytes()).hexdigest() != e["sha256"]
                 or e["end_line"] > len((s / e["path"]).read_bytes().decode("utf-8").splitlines()))
    with tempfile.TemporaryDirectory() as t:
        subprocess.run([sys.executable, "-m", "l3slice", "analyze", "--source", str(s), "--output", f"{t}/again",
                        "--membership", str(K / mem)], cwd=SLICE, capture_output=True)
        a, b = Path(t) / "again", d
        same = all((a / p.relative_to(b)).read_bytes() == p.read_bytes() for p in b.rglob("*")
                   if p.is_file() and p.name not in ("result.json", "manifest.json"))
        ra = json.loads((a / "result.json").read_text(encoding="utf-8"))
        ra["run_id"] = r["run_id"]
        same = same and ra == r
    print(f"{out:32} schema OK | artifact {len(m['artifacts'])}, sha sai {len(bad_art)} | OpenAPI hợp lệ, {ops} op | "
          f"bằng chứng {len(evs)}, sai {bad_ev} | chạy lại giống: {same}")
