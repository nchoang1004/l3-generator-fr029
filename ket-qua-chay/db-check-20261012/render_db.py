"""Sinh đầu ra thật (TBL, TAI-LIEU.md) cho các repo có bảng, không gọi model (phần bảng đọc tĩnh).
Membership: mỗi thư mục cấp 1 là một component; file ở gốc vào 'Gốc'. Chạy từ gốc repo: python render_db.py <out>"""
import json
import shutil
import sys
from pathlib import Path

sys.path[:0] = ["slice", "slice/tools"]
import fr029_checkaudit as A  # noqa: E402
from l3slice import snapshot  # noqa: E402
from l3slice.docagent import ScriptedProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

out = Path(sys.argv[1])
cases = [(c["name"], c["src"]) for c in A.v1_cases()[:4]] + [
    ("tdd-docker", Path("D:/VSF/l3-acceptance-repos/testdrivenio_fastapi-tdd-docker-16433b6/project")),
    ("orderflow", Path("D:/VSF/l3-heldout-repos2/AlexGoster_orderflow-services"))]
for name, src in cases:
    snap, _ = snapshot.take(src)
    groups = {}
    for f in snap["files"]:
        top = f["path"].split("/")[0] if "/" in f["path"] else "Gốc"
        groups.setdefault(top, []).append(f["path"])
    membership = {"components": [{"name": k, "files": v} for k, v in sorted(groups.items())]}
    d = out / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    (d / "membership.json").write_text(json.dumps(membership, ensure_ascii=False), encoding="utf-8")
    b = run_documents(src, d / "out", d / "membership.json", name, ScriptedProvider([]))
    tbl = [a for a in b["artifacts"] if "/schema/" in a["path"]]
    print(name, "tables:", sum(1 for f in b["facts"] if f["kind"] == "table"),
          "TBL files:", [(a["path"], a["status"], (a.get("error") or {}).get("reason")) for a in tbl],
          "limits:", [x["code"] for x in b["limitations"] if x["stage"] == "static"])
