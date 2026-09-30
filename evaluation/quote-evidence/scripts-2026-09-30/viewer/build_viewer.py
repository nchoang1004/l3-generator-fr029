"""Dựng trang xem sơ đồ: gom đáp án + các lần chạy v7 vào viewer.html. Không gọi AI.

    python build_viewer.py

Repo lộ: đủ khối, cạnh, trích dẫn. Repo kín: chỉ số tổng (P, Pk, R, token, số khối).
Đầu ra: viewer.html cạnh script (template.html + dữ liệu JSON nhúng).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
Q = ROOT / "experiments/quote-evidence"
RUNS = ROOT / "evaluation/quote-evidence/runs"
OPEN = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy"), ("fullstack", "full-stack-fastapi-template"),
        ("realworld", "fastapi-realworld"), ("teamhide", "teamhide-fastapi-boilerplate")]
CLOSED = [("boilerplate", "fastapi-boilerplate"), ("kibo", "kibo-backend"), ("lnbits", "lnbits"),
          ("fba", "fastapi-best-architecture")]
VERSIONS = [("v7", "Groq, mọi file xếp theo luật"), ("v7b", "Groq, prompt có luật interface"),
            ("v7c", "Groq, chia khối từ trên xuống"), ("v7d", "Groq, a–c đã sửa"),
            ("v7e-gptoss", "OpenRouter gpt-oss-120b, trần 32k"), ("v7e-haiku", "OpenRouter Claude Haiku 4.5, trần 32k")]


def split_quote(text):
    """'path:12 code' -> {file, line, text}."""
    if not text:
        return None
    head, _, code = text.partition(" ")
    f, _, n = head.rpartition(":")
    return {"file": f, "line": int(n) if n.isdigit() else None, "text": code}


def scores(s):
    pick = lambda part: {k: s[part].get(k) for k in ("precision", "precision_strict", "recall")}
    return {"internal": pick("internal"), "external": pick("external"), "grouping": s.get("grouping_agreement")}


def oracle_view(o):
    return {"blocks": [{"key": k, "layer": v[0], "evidence": split_quote(v[1]),
                        "paths": o["components"].get(k, [])} for k, v in o["layers"].items()],
            "shared": o["shared"], "externals": list(o["externals"]),
            "required": [{"s": e[0], "t": e[1], "quote": split_quote(e[2] if len(e) > 2 else None)}
                         for e in o["required"]],
            "acceptable": [{"s": e[0], "t": e[1], "label": e[2] if len(e) > 2 else ""} for e in o["acceptable"]]}


def run_view(d):
    g = json.loads((d / "graph.json").read_text(encoding="utf-8"))
    s = json.loads((d / "score.json").read_text(encoding="utf-8"))
    m = g["meta"]
    return {"tokens": m.get("tokens"), "requests": m.get("requests"), "model": m.get("model"),
            "status": m.get("status"), "issues": m.get("issues", []), "score": scores(s),
            "components": [{k: c[k] for k in ("id", "key", "name", "layer", "shared", "role")} |
                           {"files": c["files"], "role_quote": c.get("role_quote")} for c in g["components"]],
            "edges": [{"s": e["source"], "t": e["target"], "label": e.get("label", ""), "quote": e.get("quote")}
                      for e in g["edges"]],
            "externals": [{"id": x["id"], "name": x["name"], "kind": x["kind"],
                           "edges": [{"s": e["source"], "label": e.get("label", ""), "quote": e.get("quote")}
                                     for e in x["edges"]]} for x in g["externals"]],
            "mapping": {c: v[1] for c, v in s["mapping"].items()},
            "judged": {k: s["all"][k] for k in ("hits", "wrong", "not_counted", "missed")}}


data = {"open": [], "closed": []}
for name, orc in OPEN:
    o = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    runs = {v: {"note": note, **run_view(RUNS / f"{v}-{name}")} for v, note in VERSIONS
            if (RUNS / f"{v}-{name}" / "score.json").exists()}
    data["open"].append({"name": name, "source": o.get("source", ""), "oracle": oracle_view(o), "runs": runs})
for name, _ in CLOSED:
    for v, note in VERSIONS:
        d = RUNS / f"{v}-{name}"
        if (d / "score.json").exists():
            g = json.loads((d / "graph.json").read_text(encoding="utf-8"))
            s = json.loads((d / "score.json").read_text(encoding="utf-8"))
            data["closed"].append({"repo": name, "run": v, "note": note, "model": g["meta"].get("model"),
                                   "tokens": g["meta"].get("tokens"), "blocks": len(g["components"]),
                                   "score": scores(s)})

page = (HERE / "template.html").read_text(encoding="utf-8")
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
(HERE / "viewer.html").write_text(page.replace("/*DATA*/null", blob), encoding="utf-8")
print(f"viewer.html: {len(data['open'])} repo lộ, {len(data['closed'])} lần chạy repo kín, {len(blob) // 1024} KB dữ liệu")
