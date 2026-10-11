"""Read frozen-at-run contract schemas locally; no product validation helpers or network."""
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]


def load():
    schemas = {}
    by_number = {}
    for p in sorted((ROOT / '.aide/tech-specs').glob('*/api/API-*.md')):
        for raw in re.findall(r'^```json\s*\n(.*?)^```', p.read_text(encoding='utf-8'), re.M | re.S):
            s = json.loads(raw)
            if isinstance(s, dict) and '$schema' in s and '$id' in s:
                schemas[s['$id']] = s
                by_number[int(re.search(r'API-L3GEN-(\d+)', p.name)[1])] = s['$id']
    return Registry().with_resources((uri, Resource.from_contents(s)) for uri, s in schemas.items()), by_number


REGISTRY, IDS = load()


def validate(value, number, definition):
    Draft202012Validator({'$ref': IDS[number] + '#/$defs/' + definition}, registry=REGISTRY,
                         format_checker=FormatChecker()).validate(value)
