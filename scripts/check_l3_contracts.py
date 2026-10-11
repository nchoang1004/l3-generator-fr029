"""Check embedded draft contracts offline; does not evaluate the analyzer or approve gates."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urldefrag, urljoin

import yaml
from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from openapi_spec_validator import validate as validate_openapi
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / '.aide/tech-specs'
BASE = 'https://l3gen.local/contracts/'


def blocks(text):
    return re.findall(r'^```(json|yaml)\s*\n(.*?)^```\s*$', text, re.M | re.S)


def objects(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from objects(item)


def check_bundle_invariants(bundle):
    """Small example checker only: referential/owner integrity, not binding semantics."""
    verified = bundle['result']
    model, facts = verified['model'], verified['facts']
    snapshot = bundle['snapshot_id']
    if any(x['snapshot_id'] != snapshot for x in (verified, verified['inventory'], model, facts)):
        raise ValueError('cross-snapshot result')
    fact_ids = {x['id'] for x in facts['facts']}
    evidence_by_id = {x['id']: x for x in verified['evidence_index']}
    evidence_ids = set(evidence_by_id)
    nodes = model['components'] + model.get('external_systems', [])
    if len(nodes) > 50:
        raise ValueError('model exceeds 50 nodes')
    node_ids = {x['id'] for x in nodes}
    edge_ids = {x['id'] for x in model['edges']}
    for records in (facts['facts'], verified['evidence_index'], nodes, model['edges']):
        if len({x['id'] for x in records}) != len(records):
            raise ValueError('duplicate identity')
    memberships = [fid for component in model['components'] for fid in component['member_file_ids']]
    if len(set(memberships)) != len(memberships):
        raise ValueError('file assigned to multiple components')
    if len({d['subject_id'] for d in verified['decisions']}) != len(verified['decisions']):
        raise ValueError('multiple final decisions for subject')
    for evidence in verified['evidence_index']:
        if evidence['snapshot_id'] != snapshot:
            raise ValueError('cross-snapshot evidence')
        if evidence['end_line'] < evidence['start_line']:
            raise ValueError('invalid range')
    for fact in facts['facts']:
        if not set(fact['target_fact_ids']) <= fact_ids:
            raise ValueError('dangling fact target')
        for evidence in fact['evidence']:
            if evidence_by_id.get(evidence['id']) != evidence:
                raise ValueError('fact evidence differs from index')
        for attribute in objects(fact['attributes']):
            if 'evidence_ids' in attribute and not set(attribute['evidence_ids']) <= evidence_ids:
                raise ValueError('dangling attribute evidence')
    for node in nodes:
        if not set(node['evidence_ids']) <= evidence_ids:
            raise ValueError('dangling node evidence')
    for edge in model['edges']:
        if not {edge['source_component_id'], edge['target_component_id']} <= node_ids:
            raise ValueError('dangling edge endpoint')
        if not set(edge['fact_ids']) <= fact_ids or not set(edge['evidence_ids']) <= evidence_ids:
            raise ValueError('dangling evidence/fact')
    accepted = {x['subject_id'] for x in verified['decisions'] if x['verdict'] == 'accepted'}
    rejected = {x['subject_id'] for x in verified['decisions'] if x['verdict'] == 'rejected'}
    if not node_ids | edge_ids <= accepted or (node_ids | edge_ids) & rejected:
        raise ValueError('published graph includes unaccepted claim')
    for decision in verified['decisions']:
        if decision['verdict'] == 'accepted':
            if not set(decision['fact_ids']) <= fact_ids or not set(decision['evidence_ids']) <= evidence_ids:
                raise ValueError('accepted decision has dangling reference')
    # API-005 §3.2: one owner entry per route/table/event fact; owner holds the declaration file.
    owners = model['contract_owners']
    contract_facts = {x['id']: x for x in facts['facts'] if x['kind'] in ('route', 'table', 'event')}
    if sorted(o['fact_id'] for o in owners) != sorted(contract_facts):
        raise ValueError('contract facts and owner entries differ')
    components = {c['id']: c for c in model['components']}
    for owner in owners:
        if owner['component_id'] is None:
            continue
        component = components.get(owner['component_id'])
        if component is None:
            raise ValueError('owner component missing')
        declared = contract_facts[owner['fact_id']]['attributes'].get('declaration_evidence_id', {})
        if declared.get('state') != 'known' or owner['evidence_ids'] != [declared['value']]:
            raise ValueError('owner evidence is not the declaration')
        if evidence_by_id[declared['value']]['file_id'] not in component['member_file_ids']:
            raise ValueError('owner component does not contain declaration file')
    slugs = bundle['export_context']['component_slugs']
    if set(slugs) != {c['id'] for c in model['components']}:
        raise ValueError('slug map does not match published components')
    if len({slug.casefold() for slug in slugs.values()}) != len(slugs):
        raise ValueError('duplicate slug')
    artifacts = bundle['artifacts']
    if len({a['artifact_id'] for a in artifacts}) != len(artifacts) or len({a['path'].casefold() for a in artifacts}) != len(artifacts):
        raise ValueError('duplicate artifact identity/path')
    contract_paths = {a['path'] for a in artifacts if a['kind'] in ('api', 'table', 'event')}
    for notice in bundle['render_notices']:
        if not set(notice['fact_ids']) <= fact_ids:
            raise ValueError('notice cites missing fact')
        if notice['artifact_path'] is not None and notice['artifact_path'] not in contract_paths:
            raise ValueError('notice cites missing contract artifact')


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def fixture_walkthrough():
    """Hand-authored data, not an extractor, partitioner, verifier or renderer."""
    text = (SPECS/'examples/contract-walkthrough.md').read_text(encoding='utf-8')
    fragments = re.findall(r'^`([^`]+\.py)`\n\n```python\n(.*?)^```', text, re.M | re.S)
    if len(fragments) != 2:
        raise ValueError('walkthrough must contain exactly two source fragments')
    sources = {path: content.encode('utf-8') for path, content in fragments}
    files = [dict(file_id='file:'+digest(path.encode()), path=path, sha256=digest(content),
                  byte_size=len(content), encoding='utf-8') for path, content in sorted(sources.items())]
    snap = 'snap:'+digest(compact([[f['path'], f['sha256'], f['byte_size']] for f in files]).encode())
    snapshot = dict(schema_version='0.1.0', snapshot_id=snap, files=files, excluded=[])
    unit = 'unit:'+digest((snap+'\n.').encode())
    inventory = dict(schema_version='0.1.0', snapshot_id=snap, support_matrix_version='fixture-only-v1',
                     grouping_policy_version='fixture-membership-v1', outcome='ready',
                     units=[dict(id=unit, root_path='.', language='Python', framework='FastAPI/SQLAlchemy',
                                 support='partial', file_ids=[f['file_id'] for f in files], flat=False)],
                     excluded=[], limitations=[])
    by_path = {f['path']: f for f in files}
    evidence = []
    def ev(path, start, end):
        file = by_path[path]
        value = dict(id='ev:'+digest(compact([snap,path,start,None,end,None]).encode()),
                     snapshot_id=snap,file_id=file['file_id'],path=path,sha256=file['sha256'],
                     start_line=start,end_line=end,start_column=None,end_column=None)
        evidence.append(value)
        return value
    call_ev = ev('api/routes.py', 8, 8)
    target_ev = ev('storage/models.py', 10, 11)
    handler_ev = ev('api/routes.py', 7, 8)
    route_ev = ev('api/routes.py', 4, 8)
    table_ev = ev('storage/models.py', 6, 8)
    def fact(kind, source, semantic_key, attrs):
        ident = 'fact:'+digest(compact([snap,source['path'],kind,source['start_line'],None,source['end_line'],None,semantic_key]).encode())
        return dict(id=ident,unit_id=unit,kind=kind,attributes=attrs,evidence=[source],
                    resolution='not_applicable',target_fact_ids=[],confidence='exact',completeness='full')
    def known(value, source):
        return dict(state='known',value=value,evidence_ids=[source['id']])
    def unknown(reason):
        return dict(state='unknown',reason=reason)
    target = fact('symbol',target_ev,'storage.models.load_items',{
        k:known(v,target_ev) for k,v in dict(name='storage.models.load_items',symbol_kind='function',signature='load_items()').items()})
    handler = fact('symbol',handler_ev,'api.routes.list_items',{
        k:known(v,handler_ev) for k,v in dict(name='api.routes.list_items',symbol_kind='function',signature='list_items()').items()})
    call = fact('reference',call_ev,'api.routes.list_items->storage.models.load_items',{
        k:known(v,call_ev) for k,v in dict(reference_kind='call',source_symbol='api.routes.list_items',target_symbol='storage.models.load_items').items()})
    call.update(resolution='resolved',target_fact_ids=[target['id']])
    route = fact('route',route_ev,'api.routes.app:GET:/items',{
        k:known(v,route_ev) for k,v in dict(method='GET',path='/items',handler='api.routes.list_items',
            registration_context='api.routes.app:GET:/items',request_model_ids=[],status_codes=[200],parameters=[],
            handler_fact_id=handler['id'],application_id='app:api.routes.app',declaration_evidence_id=route_ev['id']).items()})
    route['attributes'].update(response_model_ids=unknown('Fixture does not infer an implicit response model'),
                               auth=unknown('Fixture does not inspect all authentication mechanisms'))
    route.update(completeness='partial',completeness_reason='Response model and authentication not determined in fixture')
    column = {k:known(v,table_ev) for k,v in dict(name='id',type='INTEGER',primary_key=True).items()}
    # Dialect-specific type is not proven by importing the generic SQLAlchemy Integer.
    column['type'] = unknown('No SQL dialect established')
    for key in ('foreign_key','nullable'):
        column[key] = unknown('Not established by this hand-authored fixture')
    table = fact('table',table_ev,'storage.models.Item',dict(name=known('items',table_ev),
        dialect=unknown('No engine or dialect in these files'),columns=known([column],table_ev),
        declaration_evidence_id=known(table_ev['id'],table_ev)))
    table.update(completeness='partial',completeness_reason='SQL dialect and column details are unknown')
    facts = [call,target,handler,route,table]
    fact_set = dict(schema_version='0.1.0',snapshot_id=snap,extractor_version='fixture-manual-v1',facts=facts,
                    limitations=[dict(code='FIXTURE_PARTIAL',message='Hand-authored subset; no extraction was run',
                                      stage='extraction',affected_ids=[route['id'],table['id']])])
    components = []
    for path in ('api/routes.py','storage/models.py'):
        file_id = by_path[path]['file_id']
        cid = 'cmp_'+digest(compact([snap,unit,[file_id]]).encode())
        components.append(dict(id=cid,unit_id=unit,name=path.split('/')[0],member_file_ids=[file_id],grouping_source='code',
            confidence='inferred',inference_reason='Membership preassigned by fixture, not an evaluated partition algorithm',
            completeness='full',evidence_ids=sorted(e['id'] for e in evidence if e['path']==path),label_status='path_fallback'))
    ca, cb = [c['id'] for c in components]
    edge_id = 'edge_'+digest(compact([snap,ca,cb,'calls']).encode())
    edge = dict(id=edge_id,source_component_id=ca,target_component_id=cb,relation_type='calls',
        fact_ids=sorted([call['id'],target['id']]),evidence_ids=sorted([call_ev['id'],target_ev['id']]),
        origin='static',confidence='exact',completeness='full',rule_id='resolved-target',rule_version='1-draft')
    limits = [dict(code='MODEL_NOT_RUN',message='Contract fixture; no provider invoked',stage='model',affected_ids=sorted([ca,cb]))]
    owners = [dict(fact_id=route['id'],contract_kind='api',component_id=ca,rule_id='declaration-file',rule_version='1-draft',evidence_ids=[route_ev['id']]),
              dict(fact_id=table['id'],contract_kind='table',component_id=cb,rule_id='declaration-file',rule_version='1-draft',evidence_ids=[table_ev['id']])]
    model = dict(schema_version='0.1.0',snapshot_id=snap,partition_version='fixture-membership-v1',components=components,
                 external_systems=[],edges=[edge],contract_owners=owners,limitations=limits,rejected_proposals=[])
    decisions = [dict(subject_id=edge_id,verdict='accepted',rule_id='resolved-target',rule_version='1-draft',
                      fact_ids=edge['fact_ids'],evidence_ids=edge['evidence_ids'],reason='Expected fixture verdict; not engine output')]
    for component in components:
        decisions.append(dict(subject_id=component['id'],verdict='accepted',rule_id='MEMBER-SOURCE',rule_version='1',
            fact_ids=sorted(f['id'] for f in facts if f['evidence'][0]['file_id'] in component['member_file_ids']),
            evidence_ids=component['evidence_ids'],reason='Expected fixture membership verdict; semantic quality not evaluated'))
    verified = dict(schema_version='0.1.0',snapshot_id=snap,inventory=inventory,facts=fact_set,model=model,evidence_index=evidence,
                    decisions=decisions,limitations=fact_set['limitations']+limits)
    data = dict(schema_version='0.1.0',run_id='run_contract_example',snapshot_id=snap,result=verified,
        export_context=dict(repository_name='Contract example',system_slug='CONTRACT-EXAMPLE',renderer_version='fixture-json-v1',
                            template_version='fixture-only-v1',component_slugs={ca:'API',cb:'STORAGE'}),render_notices=[])
    result_json = json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    bundle = dict(data,artifacts=[dict(artifact_id='art_0123456789abcdef',kind='json',path='result.json',media_type='application/json',
                                     status='ready',sha256=digest(result_json.encode()),bytes=len(result_json.encode()),error=None)])
    return dict(snapshot=snapshot,inventory=inventory,facts=fact_set,architecture=model,verified=verified,bundle=bundle,
                result_json=result_json), sources


def check_walkthrough(value, sources):
    """Check byte identity/ranges and composition, not interpretation of source."""
    snapshot = value['snapshot']
    files = snapshot['files']
    for f in files:
        raw = sources[f['path']]
        if f['file_id'] != 'file:'+digest(f['path'].encode()) or f['sha256'] != digest(raw) or f['byte_size'] != len(raw):
            raise ValueError('source manifest identity mismatch')
    manifest = [[f['path'],f['sha256'],f['byte_size']] for f in sorted(files,key=lambda f:f['path'])]
    if snapshot['snapshot_id'] != 'snap:'+digest(compact(manifest).encode()):
        raise ValueError('snapshot identity mismatch')
    if any(value[name]['snapshot_id'] != snapshot['snapshot_id'] for name in ('inventory','facts','architecture','verified','bundle')):
        raise ValueError('walkthrough snapshot mismatch')
    by_id = {f['file_id']: f for f in files}
    for ev in value['verified']['evidence_index']:
        file = by_id.get(ev['file_id'])
        if not file or file['path'] != ev['path'] or file['sha256'] != ev['sha256']:
            raise ValueError('evidence file/hash mismatch')
        lines = sources[file['path']].decode('utf-8').splitlines()
        if not 1 <= ev['start_line'] <= ev['end_line'] <= len(lines):
            raise ValueError('evidence outside source')
    result_data = json.loads(value['result_json'])
    if result_data != {k:v for k,v in value['bundle'].items() if k!='artifacts'}:
        raise ValueError('result.json differs from manifest')
    artifact = value['bundle']['artifacts'][0]
    raw = value['result_json'].encode('utf-8')
    if artifact['sha256'] != digest(raw) or artifact['bytes'] != len(raw):
        raise ValueError('artifact byte integrity mismatch')
    check_bundle_invariants(value['bundle'])


def run(report=False):
    paths = sorted(SPECS.glob('*/api/API-*.md'))
    if len(paths) != 8:
        raise ValueError(f'Expected 8 contracts, got {len(paths)}')
    schemas, docs, uids, hashes = {}, {}, set(), {}
    link_count = 0
    for path in paths:
        text = path.read_text(encoding='utf-8')
        front = yaml.safe_load(text.split('---', 2)[1])
        uid = str(front['uid'])
        if not re.fullmatch(r'[0-7][0-9A-HJKMNP-TV-Z]{25}', uid) or uid in uids:
            raise ValueError(f'{path.name}: bad/duplicate ULID')
        uids.add(uid)
        if front['status'] != 'draft' or front['key'] != path.stem:
            raise ValueError(f'{path.name}: wrong draft metadata')
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#')):
                continue
            if not (path.parent / unquote(target.split('#')[0])).exists():
                raise ValueError(f'{path.name}: broken link {target}')
            link_count += 1
        docs[path.stem] = []
        for lang, raw in blocks(text):
            item = json.loads(raw) if lang == 'json' else yaml.safe_load(raw)
            docs[path.stem].append(item)
            if isinstance(item, dict) and '$schema' in item:
                Draft202012Validator.check_schema(item)
                if item['$id'] in schemas:
                    raise ValueError('Duplicate schema ID')
                schemas[item['$id']] = item
    registry = Registry().with_resources((uri, Resource.from_contents(schema)) for uri, schema in schemas.items())
    ref_count = 0
    for uri, schema in schemas.items():
        for obj in objects(schema):
            if '$ref' in obj:
                registry.resolver(uri).lookup(obj['$ref'])
                ref_count += 1

    def validate(value, number, name):
        uri = f'{BASE}API-L3GEN-{number:03}-v1.schema.json'
        Draft202012Validator({'$ref': uri + '#/$defs/' + name}, registry=registry,
                             format_checker=FormatChecker()).validate(value)

    # Flatten JSON Schema references into OAS components for offline OAS validation.
    oas = next(d for d in docs['API-L3GEN-001-v1'] if isinstance(d,dict) and 'openapi' in d)
    oas = copy.deepcopy(oas)
    def rewrite(value, base):
        if isinstance(value, dict):
            out = {}
            for k, v in value.items():
                if k in ('$schema', '$id'):
                    continue
                if k == '$ref':
                    uri, frag = urldefrag(urljoin(base, v))
                    if uri in schemas:
                        if not frag.startswith('/$defs/'):
                            raise ValueError('Unsupported schema pointer ' + frag)
                        parts = frag[len('/$defs/'):].split('/',1)
                        stem = uri.rsplit('/',1)[-1].removesuffix('.schema.json')
                        v = '#/components/schemas/' + stem + '__' + parts[0] + ('/'+parts[1] if len(parts)>1 else '')
                    elif not v.startswith('#/components/'):
                        raise ValueError('Unknown non-local OpenAPI ref: ' + v)
                out[k] = rewrite(v, base)
            return out
        if isinstance(value, list):
            return [rewrite(v,base) for v in value]
        return value
    oas = rewrite(oas, BASE+'web.openapi.json')
    for uri, schema in schemas.items():
        stem = uri.rsplit('/',1)[-1].removesuffix('.schema.json')
        for name, definition in schema['$defs'].items():
            oas['components']['schemas'][stem+'__'+name] = rewrite(definition, uri)
    validate_openapi(oas)
    for obj in objects(oas):
        if '$ref' in obj and obj['$ref'].startswith('#/'):
            target = oas
            for part in obj['$ref'][2:].split('/'):
                target = target[part.replace('~1','/').replace('~0','~')]
    # Test the published examples as well as shared schema composition.
    checked = []
    for key, values in docs.items():
        for value in values:
            if not isinstance(value,dict) or '$schema' in value or 'openapi' in value:
                continue
            number = int(key.split('-')[2])
            definition = None
            if number == 2:
                definition = 'Snapshot' if 'files' in value else 'Range' if 'start_line' in value else 'SnapshotError'
            elif number == 5 and 'components' in value: definition = 'ArchitectureModel'
            elif number == 6 and 'status' in value: definition = 'ModelResponse'
            elif number == 6 and value.get('kind') == 'label_components': definition = 'LabelResult'
            elif number == 6 and value.get('kind') == 'propose_edges': definition = 'EdgeResult'
            if definition:
                validate(value,number,definition)
                checked.append(f'{key}/{definition}')
            elif number == 1:
                name = ('CliResult' if 'exit_code' in value else 'RunView' if 'state' in value else 'EvidenceView' if 'evidence' in value
                        else 'Error' if {'code', 'message', 'action'} <= value.keys() else None)
                if name:
                    Draft202012Validator({'$ref':'#/components/schemas/'+name, 'components':oas['components']}, format_checker=FormatChecker()).validate(value)
                    checked.append(key+'/'+name)
                elif 'repository_token' not in value:
                    raise ValueError('Unclassified example in '+key)
            else:
                raise ValueError('Unclassified example in '+key)
    walkthrough, sources = fixture_walkthrough()
    for stage, number, definition in [('snapshot',2,'Snapshot'),('inventory',3,'Inventory'),('facts',4,'FactSet'),
                                      ('architecture',5,'ArchitectureModel'),('verified',7,'VerifiedResult'),('bundle',8,'ResultBundle')]:
        validate(walkthrough[stage],number,definition)
        checked.append('walkthrough: '+definition)
    validate(json.loads(walkthrough['result_json']),8,'ResultData')
    check_walkthrough(walkthrough,sources)
    checked.append('walkthrough: ResultData, real source hashes/ranges and result.json checksum')
    bundle = walkthrough['bundle']
    node_a,node_b = [c['id'] for c in bundle['result']['model']['components']]
    model_request = dict(schema_version='0.1.0',run_id=bundle['run_id'],request_id='req_fixture',snapshot_id=bundle['snapshot_id'],
        kind='propose_edges',scope_id='scope_fixture',file_ids=[f['file_id'] for f in walkthrough['snapshot']['files']],
        fact_set=walkthrough['facts'],components=walkthrough['architecture']['components'],edges=walkthrough['architecture']['edges'],
        prompt_version='fixture-only-v1',tool_version='fixture-only-v1',max_output_tokens=1000)
    validate(model_request,6,'ModelRequest')
    checked.append('ModelRequest referencing walkthrough facts/model (not sent)')

    negatives = []
    def reject(name, fn):
        try: fn()
        except Exception as exc:
            if not isinstance(exc, (ValueError, ValidationError)):
                raise
            negatives.append(name)
        else: raise ValueError('Negative case unexpectedly passed: '+name)
    bad = copy.deepcopy(bundle); extra = bad['result']['model']['components'][0]
    bad['result']['model']['components'] += [dict(copy.deepcopy(extra), id=f'cmp_extra_{i}', member_file_ids=[f'file_extra_{i}']) for i in range(49)]
    reject('model with 51 nodes', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['artifacts'][0]['status']='failed'
    reject('failed artifact has ready hash',lambda:validate(bad,8,'ResultBundle'))
    badfact=copy.deepcopy(bundle['result']['facts']['facts'][0]); badfact['confidence']='inferred'
    reject('inferred without reason',lambda:validate(badfact,4,'Fact'))
    badfact=copy.deepcopy(bundle['result']['facts']['facts'][0]); badfact['completeness']='partial'
    reject('partial without reason',lambda:validate(badfact,4,'Fact'))
    for name, source in [('Component', bundle['result']['model']['components'][0]), ('Edge', bundle['result']['model']['edges'][0])]:
        bad_object = copy.deepcopy(source); bad_object['completeness'] = 'partial'
        reject(name+' partial without reason', lambda:validate(bad_object,5,name))
    reject('redacted leaks value',lambda:validate({'state':'redacted','reason':'secret','value':'not-a-real-key'},4,'FieldValue'))
    bad = copy.deepcopy(bundle); bad['result']['model']['edges'][0]['target_component_id']='missing'
    reject('dangling endpoint',lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['facts']['snapshot_id']='s2'
    reject('cross-snapshot facts',lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['model']['contract_owners'][0]['component_id'] = node_b
    reject('owner component lacks declaration file', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['model']['contract_owners'].pop()
    reject('contract fact without owner entry', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['model']['contract_owners'][0].update(component_id=None, evidence_ids=[])
    reject('unresolved owner without reason', lambda:validate(bad,8,'ResultBundle'))
    bad = copy.deepcopy(bundle); bad['result']['decisions'][0]['verdict']='rejected'
    reject('rejected edge published', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['facts']['facts'][0]['attributes']['reference_kind']['evidence_ids']=['missing']
    reject('attribute cites missing evidence', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); del bad['result']['model']['partition_version']
    reject('missing partition policy version', lambda:validate(bad,8,'ResultBundle'))
    bad = copy.deepcopy(bundle); del bad['result']['facts']['extractor_version']
    reject('missing extractor version', lambda:validate(bad,8,'ResultBundle'))
    bad = copy.deepcopy(bundle); del bad['result']['inventory']
    reject('missing inventory for scope presentation', lambda:validate(bad,8,'ResultBundle'))
    bad = copy.deepcopy(bundle); bad['result']['model']['components'][1]['member_file_ids'] = bad['result']['model']['components'][0]['member_file_ids']
    reject('file belongs to two components', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['result']['decisions'].append(copy.deepcopy(bad['result']['decisions'][0]))
    reject('duplicate final verdict', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['export_context']['component_slugs'].pop(node_a)
    reject('missing component slug', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['export_context']['component_slugs'][node_b] = bad['export_context']['component_slugs'][node_a]
    reject('duplicate component slug', lambda:check_bundle_invariants(bad))
    bad = copy.deepcopy(bundle); bad['render_notices']=[dict(code='CONTRACT_OWNER_UNRESOLVED',reason='Test',fact_ids=['missing'],field_paths=[],artifact_path=None)]
    reject('notice cites missing fact', lambda:check_bundle_invariants(bad))
    bad['render_notices'][0].update(fact_ids=[bundle['result']['facts']['facts'][0]['id']],artifact_path='missing.md')
    reject('notice cites missing artifact', lambda:check_bundle_invariants(bad))
    bad_walk = copy.deepcopy(walkthrough); bad_walk['snapshot']['files'][0]['sha256']='0'*64
    reject('source hash altered', lambda:check_walkthrough(bad_walk,sources))
    bad_walk = copy.deepcopy(walkthrough); bad_walk['verified']['evidence_index'][0]['end_line']=999
    reject('evidence range outside source', lambda:check_walkthrough(bad_walk,sources))
    bad_walk = copy.deepcopy(walkthrough); bad_walk['bundle']['artifacts'][0]['sha256']='0'*64
    reject('artifact checksum altered', lambda:check_walkthrough(bad_walk,sources))
    bad_walk = copy.deepcopy(walkthrough); bad_walk['result_json']='{}'
    reject('result.json differs from manifest', lambda:check_walkthrough(bad_walk,sources))
    label = copy.deepcopy(next(v for v in docs['API-L3GEN-006-v1'] if v.get('kind')=='label_components'))
    label['component_labels'][0]['member_file_ids']=['invented_file']
    reject('LLM label attempts to change membership', lambda:validate(label,6,'LabelResult'))
    bad_request=copy.deepcopy(model_request); bad_request['kind']='group_flat'
    reject('group_flat without flat units', lambda:validate(bad_request,6,'ModelRequest'))
    denied=dict(status='denied',text='unpermitted source',evidence=None,error_code='OUTSIDE_SCOPE')
    reject('denied read exposes content', lambda:validate(denied,6,'CodeReadResult'))
    for value in docs['API-L3GEN-001-v1']:
        if isinstance(value, dict) and 'repository_token' in value:
            reject('credential field in GitHub input', lambda:Draft202012Validator(
                {'$ref':'#/components/schemas/GitHubRequest','components':oas['components']}).validate(value))
    # The derived report is checked after writing; all other README links must already exist.
    readme = SPECS/'README.md'
    extra_docs=[readme,SPECS/'examples/contract-walkthrough.md',ROOT/'docs/L3-Generator-ke-hoach-trien-khai-L3.md']
    for path in extra_docs:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if target.startswith(('http:', 'https:', '#')):
                continue
            resolved=(path.parent / unquote(target.split('#')[0])).resolve()
            if resolved != ROOT/'.aide/generated/contract-checks/L3-DRAFT-CHECK.md' and not resolved.exists():
                raise ValueError(str(path)+': broken link: '+target)
            link_count += 1
    for path in (*extra_docs, Path(__file__).resolve(), ROOT/'scripts/requirements-l3-check.txt'):
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = [f'8 draft contracts; {len(schemas)} JSON Schemas; OpenAPI {oas["openapi"]}',
               f'{ref_count} schema refs resolved offline; {link_count} local links',
               f'{len(checked)} positive examples; {len(negatives)} negative checks',
               'NOT checked: real analyzer, LLM provider, full binding semantics, gold accuracy, UI, or gates.']
    print('\n'.join(summary))
    if report:
        dest=ROOT/'.aide/generated/contract-checks/L3-DRAFT-CHECK.md'
        dest.parent.mkdir(parents=True,exist_ok=True)
        (dest.parent/'L3-WALKTHROUGH.json').write_text(json.dumps(walkthrough,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        lines=['# Kiểm cấu trúc bộ L3 draft','', '> Derived, non-normative. Không phải approval hoặc benchmark sản phẩm.','',
               'Lệnh: `scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py --report`','',*summary,'',
               '## Kiểm dương','',*[f'- {x}' for x in checked],'','## Kiểm âm','',*[f'- {x}' for x in negatives],'',
               '## Môi trường','',f'Python {sys.version.split()[0]}',
               *[f'- {name}=={importlib.metadata.version(name)}' for name in ('jsonschema','PyYAML','openapi-spec-validator')],'',
               '## Hash nguồn khi kiểm','', '| File | SHA256 |','|---|---|',*[f'| {p} | `{h}` |' for p,h in hashes.items()],'',
               'Ví dụ viết tay: [nguồn và cách đọc](../../tech-specs/examples/contract-walkthrough.md), [payload qua từng bước](L3-WALKTHROUGH.json). Không phải output analyzer hoặc gold độc lập. Hash/bytes được đối soát trên source văn bản và chuỗi result.json thực trong fixture, không chạy parser/renderer sản phẩm.',
               'Các quy tắc typed attributes đầy đủ, grouping, semantic binding, budget, cleanup và rendering phải được hiện thực/kiểm ở task sản phẩm; schema pass không chứng minh chúng đã hoạt động. D-03 vẫn mở; membership fixture không lựa chọn thuật toán.','']
        dest.write_text('\n'.join(lines),encoding='utf-8',newline='\n')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',action='store_true')
    args=parser.parse_args()
    run(args.report)
