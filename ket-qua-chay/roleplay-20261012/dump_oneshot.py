"""Write the exact one-shot request (system prompt + user message) a real model would get, for a role-play model.
Usage (from the repo root): python dump_oneshot.py <source dir> <membership.json> <out dir>"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "slice")
from l3slice import snapshot  # noqa: E402
from l3slice.docagent import ProviderError, run_oneshot  # noqa: E402
from l3slice.docfacts import Claims  # noqa: E402
from l3slice.docpipeline import load_components  # noqa: E402
from l3slice.source_tools import SourceTools  # noqa: E402

src, membership, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
snap, sources = snapshot.take(src)
tools = SourceTools(snap, sources)
unit = snapshot.inventory(snap)["units"][0]["id"]
components = load_components(json.loads(membership.read_text(encoding="utf-8")), snap, unit, tools.scope)


class Capture:
    name = model = "capture"
    prices = None

    def chat(self, messages, tools_, tool_choice=None):
        (out / "system.txt").write_text(messages[0]["content"], encoding="utf-8")
        (out / "user.txt").write_text(messages[1]["content"], encoding="utf-8")
        (out / "tool.json").write_text(json.dumps(tools_, ensure_ascii=False, indent=1), encoding="utf-8")
        raise ProviderError("CAPTURED", False)


run_oneshot(tools, Claims(tools), components, Capture())
print("chars:", len((out / "system.txt").read_text(encoding="utf-8")), len((out / "user.txt").read_text(encoding="utf-8")))
