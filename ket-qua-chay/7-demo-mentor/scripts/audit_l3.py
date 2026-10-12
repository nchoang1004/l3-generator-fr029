"""Field-by-field audit of an L3 result.json against a hand-made answer for rhoboro, plus an independent evidence check.
Prints a table; no change to anything."""
import hashlib
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
SRC = Path("D:/VSF/l3-generator-quote-evidence/sample-repos/rhoboro-demo")
r = json.loads((OUT / "result.json").read_text(encoding="utf-8"))["result"]
facts = r["facts"]["facts"]
by_id = {f["id"]: f for f in facts}


def val(fv):
    if not isinstance(fv, dict) or "state" not in fv:
        return fv
    return fv["value"] if fv["state"] == "known" else f"{fv['state']}({fv.get('reason', '')[:60]})"


def model_name(fid):
    f = by_id.get(fid)
    return val(f["attributes"].get("name")) if f else fid


# ---- hand answer (read from source by a person)
ROUTES = {
    ("POST", "/api/notebooks"): ("CreateNotebookRequest", "CreateNotebookResponse", None, []),
    ("GET", "/api/notebooks"): (None, "ReadAllNotebookResponse", None, []),
    ("GET", "/api/notebooks/{notebook_id}"): (None, "ReadNotebookResponse", None, ["notebook_id:int"]),
    ("PUT", "/api/notebooks/{notebook_id}"): ("UpdateNotebookRequest", "UpdateNotebookResponse", None, ["notebook_id:int"]),
    ("DELETE", "/api/notebooks/{notebook_id}"): (None, None, 204, ["notebook_id:int"]),
    ("POST", "/api/notes"): ("CreateNoteRequest", "CreateNoteResponse", None, []),
    ("GET", "/api/notes"): (None, "ReadAllNoteResponse", None, []),
    ("GET", "/api/notes/{note_id}"): (None, "ReadNoteResponse", None, ["note_id:int"]),
    ("PUT", "/api/notes/{note_id}"): ("UpdateNoteRequest", "UpdateNoteResponse", None, ["note_id:int"]),
    ("DELETE", "/api/notes/{note_id}"): (None, None, 204, ["note_id:int"]),
    ("GET", "/"): (None, None, None, []),
}
print("== ROUTES")
seen = set()
for f in facts:
    if f["kind"] != "route":
        continue
    a = f["attributes"]
    k = (val(a["method"]), val(a["path"]))
    seen.add(k)
    exp = ROUTES.get(k)
    req = [model_name(i) for i in (a["request_model_ids"]["value"] if a["request_model_ids"]["state"] == "known" else [])]
    res = [model_name(i) for i in (a["response_model_ids"]["value"] if a["response_model_ids"]["state"] == "known" else [])]
    params = a["parameters"]["value"] if a["parameters"]["state"] == "known" else val(a["parameters"])
    ps = [f"{val(p['name'])}:{val(p.get('schema'))}" for p in params] if isinstance(params, list) else params
    st = val(a["status_codes"])
    print(f"{'OK ' if exp else 'EXTRA'} {k[0]:6} {k[1]:30} req={req or '-'} res={res or val(a['response_model_ids'])[:40]} status={st if not isinstance(st, str) else st[:20]} params={ps} | expected={exp}")
for k in ROUTES:
    if k not in seen:
        print("MISSING", k)

print("\n== MODELS")
for f in facts:
    if f["kind"] in ("request_model", "response_model"):
        a = f["attributes"]
        fields = [(val(x.get("name")), val(x.get("schema")), val(x.get("required"))) for x in a["fields"]["value"]] if a.get("fields", {}).get("state") == "known" else val(a.get("fields"))
        print(f["kind"], val(a.get("name")), fields)

print("\n== TABLES")
for f in facts:
    if f["kind"] == "table":
        a = f["attributes"]
        print(val(a["name"]), "dialect=", val(a.get("dialect")))
        for c in a["columns"]["value"]:
            print("   ", {k: val(v) for k, v in c.items()})

print("\n== CONFIG / LIBRARY")
for f in facts:
    if f["kind"] in ("config", "library"):
        a = f["attributes"]
        print(f["kind"], val(a.get("key") or a.get("name")), val(a.get("source_kind") or a.get("version")))

# ---- independent evidence check: every evidence id, read the file again, hash and range
bad, n = [], 0
for f in facts:
    for ev in f["evidence"]:
        n += 1
        p = SRC / ev["path"]
        raw = p.read_bytes()
        lines = raw.decode("utf-8").splitlines()
        if hashlib.sha256(raw).hexdigest() != ev["sha256"] or not 1 <= ev["start_line"] <= ev["end_line"] <= len(lines):
            bad.append(ev["id"])
print(f"\n== EVIDENCE: {n} checked, {len(bad)} bad")

# ---- literal check: method/path pieces/status really appear in the cited lines
miss = []
for f in facts:
    if f["kind"] != "route":
        continue
    a = f["attributes"]
    evs = {e["id"]: e for e in f["evidence"]}
    text = " ".join("\n".join((SRC / evs[i]["path"]).read_text(encoding="utf-8").splitlines()[evs[i]["start_line"] - 1:evs[i]["end_line"]])
                    for i in a["path"]["evidence_ids"])
    for seg in [s for s in val(a["path"]).split("/") if s]:
        if seg not in text:
            miss.append((val(a["path"]), seg))
print(f"== PATH SEGMENTS NOT IN CITED LINES: {miss}")
