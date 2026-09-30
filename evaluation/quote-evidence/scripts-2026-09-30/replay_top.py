"""Replay the real pass-1 answers of the v7c runs (exposed repos) through the current code. No AI call.
A: current code (reason check on). B: every reason accepted (measures the model's grouping alone).
Pass 2, edge check and naming answer nothing (ambiguous files fall back to the rules)."""
import json
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

CACHE = ROOT / "evaluation/quote-evidence/cache"
RUNS = {"rhoboro": ("rhoboro-async-fastapi-sqlalchemy", "42380a6ca9e59b8430ea2865", "c6c65956460fef4eff67a8ae"),
        "fullstack": ("full-stack-fastapi-template", "ca17cd665b198198194df94a", "3ad0ac03fb45a29712dd7064"),
        "realworld": ("fastapi-realworld", "650259f55744aa1686c98305", "15304cbfb63337114de0de4a"),
        "teamhide": ("teamhide-fastapi-boilerplate", "2bf1f61b959980874a73fa2d", "262ef561b728ed49e4f87388")}
load = lambda h: json.loads(json.loads((CACHE / f"{h}.json").read_text(encoding="utf-8"))["content"])


class Replay:
    def __init__(self, first, second):
        self.answers, self.calls = {"top-1": first, "top-2": second}, []

    def json(self, system, user, schema, *, step, max_tokens):
        self.calls.append(step)
        return json.loads(json.dumps(self.answers.get(step, {})))


f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
real_quote = ai7._quote
print("| Repo | Cách | Khối AI trả (lượt cuối) | Khối giữ | P / Pk / R | File đúng khối | File theo luật | Vấn đề còn |")
print("|---|---|---:|---:|---|---:|---:|---:|")
for name, (orc, h1, h2) in RUNS.items():
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    for mode in ("A", "B"):
        patch = mock.patch.object(ai7, "_quote", real_quote if mode == "A" else
                                  (lambda idx_, text, files: real_quote(idx_, text, files) or
                                   {"file": files[0], "line": 1, "text": "accepted without check"}))
        with patch:
            client = Replay(load(h1), load(h2))
            g = ai7.group(client, idx, facts, an)
            out = ai7.describe(Replay({}, {}), idx, facts, an, g, {})
        out["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
        s = evaluate.score(out, oracle)
        i = s["internal"]
        last = load(h2) if "top-2" in client.calls else load(h1)
        kept = len([k for k in g["blocks"] if k != ai7.SHARED and k in g["block_reasons"]])
        print(f"| {name} | {mode} | {len(last.get('blocks', []))} | {kept} | {f2(i['precision'])} / "
              f"{f2(i['precision_strict'])} / {f2(i['recall'])} | {f2(s['grouping_agreement'])} | {len(g['by_rule'])} + "
              f"{len(g['ambiguous']['no_path'])} không path | {len(g['top']['left'])} |")
