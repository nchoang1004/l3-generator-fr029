"""Replay role-play answers through the real one-shot pipeline (no paid model). Run from the repo root:
python replay.py <source> <membership> <case dir> <name> [answer files in order: answer.json repair1.json ...]
Writes <case dir>/out*/ (the documents) and <case dir>/refused.json (what the checker refused and the open problems,
as the model would get them in the next request)."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "slice")
from l3slice.docagent import Budget, ScriptedProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

src, membership, case, name = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
answers = [json.loads((case / a).read_text(encoding="utf-8")) for a in sys.argv[5:]]
out = case / f"out{len(answers)}"
shutil.rmtree(out, ignore_errors=True)
ck = case / f"checkpoint{len(answers)}.json"
ck.unlink(missing_ok=True)
seen = []


def reply(i):
    def give(messages):
        seen.append(messages[-1])
        return [("submit_findings", answers[i])]
    return give


provider = ScriptedProvider([reply(i) for i in range(len(answers))])
bundle = run_documents(src, out, membership, name, provider, mode="oneshot", checkpoint=ck,
                       budget=Budget(max_repair_rounds=len(answers) - 1))
saved = json.loads(ck.read_text(encoding="utf-8"))
last_tool = [m for m in saved["messages"] if m["role"] == "tool"][-1]
note = saved["messages"][-1] if saved["messages"][-1]["role"] == "user" else None
(case / "refused.json").write_text(json.dumps({"submit_findings_result": json.loads(last_tool["content"]),
                                               "next_message": json.loads(note["content"]) if note else None},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
a = bundle["agent"]
print("status:", a["status"], a["reason"])
for r in a["requests"]:
    print("  request", r["round"], "accepted", r["accepted"], "refused", r["refused"], "open", r["open_problems"])
kinds = {}
for f in bundle["facts"]:
    kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
print("facts:", kinds)
print("artifacts:", [(x["path"], x["status"]) for x in bundle["artifacts"]])
