"""Additional synthetic checks after independent scorer reviews. No model or held-out data.
Run from the repository root using scripts/.venv/Scripts/python.exe.
"""
import json
import sys
from pathlib import Path

sys.path[:0] = [str(Path(p).resolve()) for p in ("slice", "slice/tools")]
import fr029_score as scorer
import fr029_accept as acceptance
import fr029_grade_merge as merge


def http_fact(method):
    return {"id": "f-" + method, "kind": "http_call", "confidence": "exact",
            "evidence": [{"path": "a.py", "start_line": 1}],
            "attributes": {"library": {"state": "known", "value": "httpx"},
                           "method": {"state": "known", "value": method},
                           "url": {"state": "known", "value": "https://x"}}}


gold = {"http_calls": [{"where": "a.py:1", "library": "httpx", "method": "GET",
                        "target": {"kind": "literal", "value": "https://x"}}]}
observed = {}
for order in [("POST", "GET"), ("GET", "POST")]:
    result = {"facts": [http_fact(method) for method in order], "components": [], "limitations": []}
    report = scorer.score(result, gold)
    observed["duplicates_" + ",".join(order)] = {
        "tp": report["http_calls"]["tp"], "fp": report["http_calls"]["fp"],
        "method_correct": report["http_calls"]["attributes"]["method"]["correct"],
        "exact": acceptance.exact_wrong(result, report),
    }
result = {"facts": [http_fact("GET")], "components": [], "limitations": []}
report = scorer.score(result, {})
observed["unscored_exact"] = {"http": report["http_calls"], "exact": acceptance.exact_wrong(result, report)}
observed["array_rank_collapsed"] = (
    scorer._type_response("array[array[integer]]", False) == scorer._type_response("array[integer]", False)
)
observed["dynamic_empty_fields_accepted"] = scorer._fields_ok(
    [], {"unknown_ok": True, "fields": [("x", None, "string", True, False)], "alt_types": {}}
)
finding_a = {"fixture": "sample", "kind": "model", "item": "Thing", "evidence": "m.py:10",
             "field": "fields.foo.required"}
finding_b = dict(finding_a, field="fields.bar.nullable")
observed["different_fields_same_consensus_key"] = merge.key(finding_a) == merge.key(finding_b)
print(json.dumps(observed, ensure_ascii=False, indent=2))
