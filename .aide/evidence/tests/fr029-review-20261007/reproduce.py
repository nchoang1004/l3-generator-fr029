"""Read-only FR-029 review probes. Run from the project root; no model or held-out data.

These probes describe observed behavior, not approved acceptance expectations.
Temporary fixture outputs are cleaned by the existing test helpers.
"""
import copy
import json
import re
import sys
from pathlib import Path

root = Path.cwd()
sys.path[:0] = [str(root / p) for p in ("slice", "slice/tests", "slice/tools")]
from test_docagent import FINDINGS, FIX, READ, READABLE, run, script, tools_for
from l3slice import snapshot
from l3slice.docagent import ScriptedProvider
from l3slice.docfacts import Claims, build_facts
from l3slice.source_tools import SourceTools
from openapi_spec_validator import validate
import fr029_accept
import fr029_score

observed = {}
tools = tools_for({"a.py": 'import httpx\nhttpx.get(' + " " * 460 + '"https://hidden.example/x")\n'})
read = tools.read_file("a.py")
tools.model_answered()
claims = Claims(tools)
errors = claims.add_http({"at": "a.py:2", "library": "httpx", "method": "GET",
                         "target": {"kind": "literal", "value": "https://hidden.example/x"}})
observed["cut_evidence"] = {
    "value_visible_to_model": "https://hidden.example/x" in read["text"],
    "cut_lines": read.get("cut_lines"), "claim_errors": errors,
    "coverage_complete": tools.coverage()["complete"],
}

snap, sources = snapshot.take(FIX)
tools = SourceTools(snap, sources)
for path in READABLE:
    tools.read_file(path)
tools.model_answered()
claims = Claims(tools)
route = copy.deepcopy(READ)
route["path_parts"][0], route["path_parts"][1] = route["path_parts"][1], route["path_parts"][0]
errors = claims.add_route(route)
fact = build_facts(claims, snap, "review-unit")[0]
observed["reversed_prefix"] = {"errors": errors, "path": fact["attributes"]["path"]["value"]}

claims = Claims(tools)
model = copy.deepcopy(FINDINGS["models"][1])
model["fields"][1]["required"] = True
model["fields"][1]["type"] = "boolean"
errors = claims.add_model(model)
fact = build_facts(claims, snap, "review-unit")[0]
observed["wrong_model_attributes"] = {"errors": errors, "confidence": fact["confidence"]}

findings = copy.deepcopy(FINDINGS)
findings["routes"][1]["params"].append(copy.deepcopy(findings["routes"][1]["params"][0]))
tmp, output, bundle = run(ScriptedProvider(script(findings, bad=False)))
try:
    text = next(output.rglob("API-*.md")).read_text(encoding="utf-8")
    spec = json.loads(re.search(r"```json\s*\n(.*?)```", text, re.S).group(1))
    try:
        validate(spec)
        outcome = "valid"
    except Exception as exc:
        outcome = type(exc).__name__ + ": " + str(exc).splitlines()[0]
    observed["duplicate_openapi_parameter"] = {
        "agent_status": bundle["agent"]["status"],
        "api_status": next(a["status"] for a in bundle["artifacts"] if a["kind"] == "api"),
        "validation": outcome,
    }
finally:
    tmp.cleanup()

result = {"facts": [{"id": "f1", "kind": "http_call", "confidence": "exact",
                     "evidence": [{"path": "a.py", "start_line": 3}],
                     "attributes": {"library": {"state": "known", "value": "httpx"},
                                    "method": {"state": "known", "value": "POST"},
                                    "url": {"state": "known", "value": "https://x"}}}],
          "components": [], "limitations": []}
gold = {"http_calls": [{"where": "a.py:2", "alt_where": ["a.py:3"], "library": "httpx",
                         "method": "GET", "target": {"kind": "literal", "value": "https://x"}}]}
scored = fr029_score.score(result, gold)
observed["exact_score_alias"] = {
    "method_wrong_count": len(scored["http_calls"]["attributes"]["method"]["wrong"]),
    "exact": fr029_accept.exact_wrong(result, scored),
}
print(json.dumps(observed, ensure_ascii=False, indent=2))
