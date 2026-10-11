"""Load the JSON Schemas embedded in `.aide/tech-specs` so tests validate slice output against the contracts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_l3_contracts as checker  # noqa: E402  (reuse block parser and bundle invariants)

BASE = checker.BASE
OPENAPI_001 = f"{BASE}API-L3GEN-001-v1.openapi.json"


def _registry() -> Registry:
    schemas = {}
    for path in sorted((ROOT / ".aide/tech-specs").glob("*/api/API-*.md")):
        for lang, raw in checker.blocks(path.read_text(encoding="utf-8")):
            if lang == "json":
                item = json.loads(raw)
                if isinstance(item, dict) and "$schema" in item:
                    schemas[item["$id"]] = item
            elif lang == "yaml" and path.name.startswith("API-L3GEN-001"):
                # components.schemas of the facade; relative $refs resolve next to the JSON schemas
                spec = yaml.safe_load(raw)
                schemas[OPENAPI_001] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": OPENAPI_001,
                                        "components": {"schemas": spec["components"]["schemas"]}}
    return Registry().with_resources((uri, Resource.from_contents(s)) for uri, s in schemas.items())


REGISTRY = _registry()


def validate(value, number: int, name: str):
    uri = f"{BASE}API-L3GEN-{number:03}-v1.schema.json#/$defs/{name}"
    Draft202012Validator({"$ref": uri}, registry=REGISTRY, format_checker=FormatChecker()).validate(value)


def validate_http(value, name: str):
    """Schema `components.schemas.<name>` of the API-001 OpenAPI block."""
    Draft202012Validator({"$ref": f"{OPENAPI_001}#/components/schemas/{name}"}, registry=REGISTRY,
                         format_checker=FormatChecker()).validate(value)


check_bundle_invariants = checker.check_bundle_invariants
