"""Unpack the downloaded GitHub zips into sample-repos/<local_dir> (wrapper folder removed, no execution),
then compare every file of Khiem's v8 snapshot (graph.json "snapshot": path -> sha256) with the unpacked bytes."""
import hashlib
import json
import zipfile
from pathlib import Path

DL = Path(__file__).parent / "dl"
SAMPLE = Path("D:/VSF/l3-generator-quote-evidence/sample-repos")
RUNS = Path("D:/VSF/l3-generator-quote-evidence/evaluation/quote-evidence/runs")
REPOS = {"full-stack-fastapi-template-cb740b6": "fullstack", "fastapi-realworld-diagram": "realworld",
         "teamhide_fastapi-boilerplate-df4e6d4": "teamhide"}
for local, short in REPOS.items():
    dest = SAMPLE / local
    if not dest.exists():
        with zipfile.ZipFile(DL / f"{local}.zip") as z:
            for info in z.infolist():
                rel = info.filename.split("/", 1)[1] if "/" in info.filename else ""
                if not rel or info.is_dir():
                    continue
                if ".." in Path(rel).parts or rel.startswith("/"):
                    raise SystemExit(f"unsafe entry {info.filename}")
                out = dest / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(z.read(info))
    for run in ("v8-draft", "v8-nodraft"):
        snap = json.loads((RUNS / f"{run}-{short}" / "graph.json").read_text(encoding="utf-8"))["snapshot"]
        bad = [p for p, h in snap.items() if not (dest / p).is_file() or hashlib.sha256((dest / p).read_bytes()).hexdigest() != h]
        print(f"{short:9} {run:10}: {len(snap)} file trong snapshot v8, khác {len(bad)} {bad[:3]}")
    print(f"{short:9} tổng file .py: {sum(1 for _ in dest.rglob('*.py'))}")
