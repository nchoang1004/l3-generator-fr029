"""Build an oracle JSON from a hand-written spec (taken from ve-tay/*.md).

    python build_oracle.py spec_<repo>.py      then: oracle_tool.py <repo> <oracle.json> --finalize

For every "file:line" the spec gives, read that line from the repository, check that the snippet copied
from the hand drawing occurs in it ("..." = any text), and write the whole stripped line into the JSON.
Nothing is decided here: blocks, layers and edges all come from the spec.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ORACLE = ROOT / "experiments/quote-evidence/oracle"
sys.path.insert(0, str(ORACLE))
import oracle_tool  # noqa: E402

spec_path = Path(sys.argv[1])
mod = importlib.util.spec_from_file_location("spec", spec_path)
spec = importlib.util.module_from_spec(mod)
mod.loader.exec_module(spec)
S = spec.SPEC
old = json.loads((ORACLE / "rev3" / S["file"]).read_text(encoding="utf-8"))
repo = ROOT / old["local_dir"]
errors = []


def matches(snippet: str, text: str) -> bool:
    pos = 0
    for part in (p.strip() for p in snippet.split("...")):
        if part:
            i = text.find(part, pos)
            if i < 0:
                return False
            pos = i + len(part)
    return True


def ev(ref: str, snippet: str) -> str:
    path, n = ref.rsplit(":", 1)
    f = repo / path
    if not f.is_file():
        errors.append(f"no file: {ref}")
        return ref
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    text = lines[int(n) - 1].strip() if 0 < int(n) <= len(lines) else ""
    if not matches(snippet, text):
        errors.append(f"snippet not on line: {ref}\n    want: {snippet}\n    line: {text}")
    return f"{path}:{n} {text}"


out = {k: old[k] for k in ("repo", "source", "local_dir", "set") if k in old}
out["rev"] = 4
out["written"] = S["written"] + " | " + old.get("written", "")
out["note"] = S["note"]
out["components"] = S["components"]
out["shared"] = S["shared"]
out["layers"] = {k: [layer, ev(ref, snip)] for k, (layer, ref, snip) in S["layers"].items()}
out["externals"] = S["externals"]
out["required"] = [[a, b, ev(ref, snip)] for a, b, ref, snip in S["required"]]
out["acceptable"] = [[a, b, label, ev(ref, snip)] if ref else [a, b, label]
                     for a, b, label, ref, snip in S["acceptable"]]
if errors:
    print("\n".join(errors))
    sys.exit(1)
(ORACLE / S["file"]).write_text(oracle_tool.dump(out), encoding="utf-8")
print(f"wrote {S['file']}: {len(out['components'])} components, {len(out['required'])} required, "
      f"{len(out['acceptable'])} labelled acceptable")
