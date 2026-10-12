"""Offline review probes. Synthetic source/claims only; does not edit product or golden."""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / p) for p in ('slice', 'slice/tests', 'slice/tools')]
from test_docagent import FINDINGS, FIX, READ, READABLE, run, script, tools_for
from l3slice import snapshot
from l3slice.docagent import ScriptedProvider
from l3slice.docfacts import Claims
from l3slice.source_tools import SourceTools
from openapi_spec_validator import validate

observed = {}
t = tools_for({'a.py': 'import httpx\nhttpx.get(' + ' ' * 460 + '"https://hidden.example/x")\n'})
read = t.read_file('a.py')
t.model_answered()
c = Claims(t)
observed['cut_evidence'] = {'value_delivered': 'https://hidden.example/x' in read['text'],
    'errors': c.add_http({'at': 'a.py:2', 'library': 'httpx', 'method': 'GET',
        'target': {'kind': 'literal', 'value': 'https://hidden.example/x'}}),
    'coverage_complete': t.coverage()['complete']}

snap, sources = snapshot.take(FIX)
t = SourceTools(snap, sources)
for p in READABLE:
    t.read_file(p)
t.model_answered()
c = Claims(t)
route = copy.deepcopy(READ)
route['path_parts'][0], route['path_parts'][1] = route['path_parts'][1], route['path_parts'][0]
observed['reversed_prefix'] = {'errors': c.add_route(route)}

def pipeline_probe(name, findings):
    tmp, output, bundle = run(ScriptedProvider(script(findings, bad=False)))
    try:
        text = next(output.rglob('API-*.md')).read_text(encoding='utf-8')
        doc = json.loads(re.search(r'```json\s*\n(.*?)```', text, re.S).group(1))
        try:
            validate(doc)
            validity = 'valid'
        except Exception as exc:
            validity = type(exc).__name__ + ': ' + str(exc).splitlines()[0]
        observed[name] = {'agent': bundle['agent'],
            'api_status': next(a['status'] for a in bundle['artifacts'] if a['kind'] == 'api'),
            'validation': validity, 'rejected_count': len(bundle['rejected_claims'])}
        out = Path(__file__).parent / name
        out.mkdir(exist_ok=True)
        (out/'API.md').write_text(text, encoding='utf-8')
        (out/'openapi.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
        (out/'result.json').write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding='utf-8')
        return bundle, doc
    finally:
        tmp.cleanup()

f = copy.deepcopy(FINDINGS)
f['models'][1]['fields'][1].update(type='boolean', required=True, nullable=False)
b, doc = pipeline_probe('wrong_model_attributes', f)
observed['wrong_model_attributes']['model_confidence'] = next(x['confidence'] for x in b['facts']
    if x['kind'] == 'model' and x['attributes']['name']['value'] == 'ItemIn')
observed['wrong_model_attributes']['rendered_itemin_schema'] = next(x for x in doc['components']['schemas'].values()
    if 'price' in x.get('properties', {}))

f = copy.deepcopy(FINDINGS)
f['routes'][1]['params'].append(copy.deepcopy(f['routes'][1]['params'][0]))
pipeline_probe('duplicate_parameter', f)

f = copy.deepcopy(FINDINGS)
f['routes'][1]['auth'] = {'value': 'OAuth2 bearer token required', 'at': 'app/api/items.py:16'}
b, _ = pipeline_probe('invented_auth', f)
observed['invented_auth']['published_auth'] = [x['attributes'].get('auth') for x in b['facts'] if x['kind']=='route']

t = tools_for({'route.py': 'from fastapi import FastAPI\napp=FastAPI()\n@app.get("/x")\ndef x(): return 1\n',
    'helper.py': 'def helper(): return 2\n', 'db.py': 'def save(db): db.commit()\n'})
for p in t.readable:
    t.read_file(p)
t.model_answered()
c = Claims(t)
observed['invented_service_chain'] = {'errors': c.add_role({'file': 'helper.py', 'role': 'Service',
    'at': 'helper.py:1', 'call_path': ['route.py:4', 'helper.py:1', 'db.py:1']}),
    'note': 'No call exists between the three functions.'}

t = tools_for({'a.py': 'from fastapi import FastAPI, Body\napp=FastAPI()\n@app.post("/x")\ndef x(payload: dict = Body(...)): return payload\n'})
t.read_file('a.py'); t.model_answered(); c=Claims(t); errors=[]
c.body({'models': [], 'param': 'payload', 'media_type': 'application/json', 'required': True,
        'embedded': False, 'at': 'a.py:4', 'type': 'object'}, errors)
observed['plain_json_body'] = {'errors': errors}

print(json.dumps(observed, ensure_ascii=False, indent=2))
