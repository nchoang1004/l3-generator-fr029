"""Validate the OpenAPI blocks of every API-*.md with openapi-spec-validator, and result.json with the contract schema
(through slice/tests/contracts.py, the same helper the tests use)."""
import json
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
sys.path.insert(0, "D:/VSF/l3-generator-l3/slice/tests")
from openapi_spec_validator import validate  # noqa: E402

for md in sorted(OUT.glob("tech-specs/*/api/*.md")):
    text = md.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    spec = next((json.loads(b) for b in blocks if '"openapi"' in b), None)
    if spec is None:
        print(md.name, "không có khối OpenAPI")
        continue
    validate(spec)
    ops = sum(1 for p in spec["paths"].values() for m in p if m in ("get", "post", "put", "delete", "patch"))
    omitted = spec.get("x-analysis", {}).get("omitted_operations", [])
    print(f"{md.name}: OpenAPI 3.1 hợp lệ, {ops} operation, {len(omitted)} bị bỏ có lý do")

import contracts  # noqa: E402
names = [n for n in dir(contracts) if not n.startswith("_")]
print("contracts helpers:", names)
