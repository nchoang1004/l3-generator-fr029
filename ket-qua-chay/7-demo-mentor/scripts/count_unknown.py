"""How many cells of the reader table (## Endpoint) are still unknown, per repository."""
import glob
import re

for repo in ["7-demo-mentor/l3-rhoboro", "8-repo-khiem/l3-fullstack-goc", "8-repo-khiem/l3-realworld", "8-repo-khiem/l3-teamhide"]:
    rows = []
    for f in glob.glob(f"D:/VSF/l3-generator-l3/ket-qua-chay/{repo}/tech-specs/*/api/*.md"):
        t = open(f, encoding="utf-8").read()
        sec = t.split("## Endpoint", 1)[1].split("## Model", 1)[0]
        rows += [[c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]] for ln in sec.splitlines()
                 if ln.startswith("| ") and "`f:" in ln]
    cols = ["Method", "Path", "Tham số", "Request", "Response", "Status", "Auth"]
    unk = {c: sum(1 for r in rows if r[i].startswith("unknown")) for i, c in enumerate(cols)}
    print(repo.split("/")[-1], "route", len(rows), "| ô unknown:", unk)
