"""Print what one L3 output says: routes (method, path, status, request/response model, params, source line),
tables (columns), counts, limitations, and an independent evidence check against the source tree."""
import collections
import hashlib
import json
import sys
from pathlib import Path

out, src = Path(sys.argv[1]), Path(sys.argv[2])
r = json.loads((out / "result.json").read_text(encoding="utf-8"))["result"]
F = r["facts"]["facts"]
by = {f["id"]: f for f in F}


def v(fv):
    if not isinstance(fv, dict) or "state" not in fv:
        return fv
    return fv["value"] if fv["state"] == "known" else fv["state"].upper()


def names(ids_fv):
    return [v(by[i]["attributes"]["name"]).rsplit(".", 1)[-1] for i in ids_fv["value"]] if ids_fv["state"] == "known" else v(ids_fv)


print("COUNTS", dict(collections.Counter(f["kind"] for f in F)))
print("ROUTES")
for f in sorted((f for f in F if f["kind"] == "route"), key=lambda f: (str(v(f["attributes"]["path"])), str(v(f["attributes"]["method"])))):
    a = f["attributes"]
    decl = next(e for e in f["evidence"] if e["id"] == a["declaration_evidence_id"]["value"])
    path = v(a["path"]) if a["path"]["state"] == "known" else f"?{v(a.get('path_suffix'))}"
    ps = [f"{v(p['name'])}:{v(p['in'])}" for p in a["parameters"]["value"]] if a["parameters"]["state"] == "known" else v(a["parameters"])
    print(f"  {v(a['method']):6} {path:45} st={v(a['status_codes'])} req={names(a['request_model_ids'])} "
          f"res={names(a['response_model_ids'])} p={ps} @ {decl['path']}:{decl['start_line']}")
print("TABLES")
for f in (f for f in F if f["kind"] == "table"):
    a = f["attributes"]
    cols = [f"{v(c['name'])}{'*' if v(c.get('primary_key')) is True else ''}{'->' + str(v(c['foreign_key'])['table']) if isinstance(v(c.get('foreign_key')), dict) else ''}"
            for c in a["columns"]["value"]] if a["columns"]["state"] == "known" else v(a["columns"])
    print(f"  {v(a['name'])} @ {f['evidence'][0]['path']}: {cols}")
refs = [f for f in F if f["kind"] == "reference"]
print("REFS", len(refs), dict(collections.Counter(f["resolution"] for f in refs)))
print("LIMITS", dict(collections.Counter(l["code"] for l in r["limitations"])))
bad = sum(1 for f in F for e in f["evidence"]
          if hashlib.sha256((src / e["path"]).read_bytes()).hexdigest() != e["sha256"]
          or e["end_line"] > len((src / e["path"]).read_bytes().decode("utf-8").splitlines()))
print("EVIDENCE", sum(len(f["evidence"]) for f in F), "bad", bad)
