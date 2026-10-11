"""Read published bytes independently. Never calls renderer check_* or extractor.

This is a contract oracle, not an LLM judge. Each failed check has a location and
expected/actual data; syntax validation alone is never treated as semantic parity.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml
import sqlglot
from sqlglot import exp
from jsonschema import Draft202012Validator
from openapi_spec_validator import OpenAPIV31SpecValidator
from .contracts import validate


def blocks(text, lang):
    return re.findall(r'^```' + re.escape(lang) + r'\s*\n(.*?)^```', text, re.M | re.S)


def rows(text):
    return [[c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
            for line in text.splitlines() if line.startswith('|') and not re.match(r'^\|[ -]*---', line)]


def value(f):
    return f.get('value') if isinstance(f, dict) and f.get('state') == 'known' else None


def references(doc):
    """Resolve only local JSON pointers; never download an external reference."""
    errors = []
    def visit(obj):
        if isinstance(obj, dict):
            ref = obj.get('$ref')
            if ref:
                if not ref.startswith('#/'):
                    errors.append('non-local $ref: ' + ref)
                else:
                    item = doc
                    try:
                        for key in ref[2:].split('/'):
                            item = item[key.replace('~1', '/').replace('~0', '~')]
                    except (KeyError, TypeError):
                        errors.append('dangling $ref: ' + ref)
            for v in obj.values():
                visit(v)
        elif isinstance(obj, list):
            for v in obj:
                visit(v)
    visit(doc)
    return errors


def text_value(f):
    if f.get('state') != 'known':
        return None
    v = f['value']
    if isinstance(v, list):
        return ', '.join(map(str, v)) if v else '(rỗng)'
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    return str(v)


class Audit:
    def __init__(self):
        self.checks = []

    def check(self, condition, code, location, expected, actual):
        self.checks.append(dict(code=code, location=str(location), passed=bool(condition), expected=expected, actual=actual))

    def equal(self, actual, expected, code, location):
        self.check(actual == expected, code, location, expected, actual)

    def errors(self):
        return [x for x in self.checks if not x['passed']]

    def schema(self, obj, number, definition, location):
        try:
            validate(obj, number, definition)
            err = None
        except Exception as exc:
            err = str(exc)[:1500]
        self.equal(err, None, 'contract-schema', location)

    def markdown_field(self, actual, field, location):
        expected = text_value(field)
        if expected is None:
            marker = {'unknown':'unknown', 'redacted':'đã che', 'not_applicable':'không áp dụng'}[field['state']]
            self.check(marker in actual and field['reason'].replace('|', '\\|') in actual,
                       'markdown-state-reason', location, marker + ' + reason', actual)
        else:
            # Decode only presentation escaping; values must not be changed by formatting.
            import html
            actual = html.unescape(actual).replace('\\|', '|').replace('\\`', '`')
            self.equal(actual, expected.replace('\n', ' ').replace('\r', ' '), 'markdown-value', location)


def audit_bundle(output: Path, verified: dict, allow_failed=False):
    a = Audit()
    b = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    d = json.loads((output / 'result.json').read_text(encoding='utf-8'))
    a.schema(b, 8, 'ResultBundle', 'manifest.json')
    a.schema(d, 8, 'ResultData', 'result.json')
    a.equal(d, {k:v for k,v in b.items() if k != 'artifacts'}, 'manifest-result-parity', 'result.json')
    a.equal(d['result'], verified, 'frozen-input', 'result.json/result')
    arts = b['artifacts']
    for key in ('artifact_id', 'path'):
        a.equal(len({x[key] for x in arts}), len(arts), 'unique-artifact-' + key, 'manifest.json')
    expected_files = {'manifest.json'}
    for item in arts:
        rel = item['path']
        target = output / rel
        safe = output.resolve() in target.resolve().parents and not Path(rel).is_absolute()
        a.check(safe, 'path-containment', rel, 'inside output', str(target))
        if not safe:
            continue
        if item['status'] == 'failed':
            a.check(allow_failed, 'artifact-ready', rel, 'ready unless failure injected', item['error'])
            a.check(bool(item['error']) and item['sha256'] is None and item['bytes'] is None,
                    'failed-metadata', rel, 'error; no fake digest', item)
            continue
        expected_files.add(rel)
        a.check(target.is_file(), 'artifact-exists', rel, True, target.is_file())
        if not target.is_file():
            continue
        raw = target.read_bytes()
        a.equal(hashlib.sha256(raw).hexdigest(), item['sha256'], 'artifact-hash', rel)
        a.equal(len(raw), item['bytes'], 'artifact-bytes', rel)
        a.check(not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw, 'utf8-lf', rel, 'UTF-8 no BOM, LF', 'checked')
        text = raw.decode('utf-8')
        if item['kind'] in ('api', 'table', 'event'):
            audit_contract(a, text, rel, item['kind'], verified, b)
    a.equal(sorted(p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()),
            sorted(expected_files), 'no-unregistered-files', output)
    audit_graph(a, output, verified, arts)
    readme = (output / 'README.md').read_text(encoding='utf-8')
    for item in arts:
        if item['kind'] in ('api', 'table', 'event'):
            a.check(item['path'] in readme, 'readme-index', 'README.md', item['path'], 'present' if item['path'] in readme else 'missing')
    for notice in b['render_notices']:
        a.check(notice['code'] in readme, 'notice-visible', 'README.md', notice['code'], 'present' if notice['code'] in readme else 'missing')
    for o in verified['model']['contract_owners']:
        matching = []
        for item in arts:
            if item['kind'] in ('api','table','event') and item['status'] == 'ready':
                t = (output / item['path']).read_text(encoding='utf-8')
                front = yaml.safe_load(t.split('---', 2)[1])
                if o['fact_id'] in front['fact_ids']:
                    matching.append((item['kind'], front['owner_component_id']))
        want = [] if o['component_id'] is None else [(o['contract_kind'], o['component_id'])]
        a.equal(matching, want, 'ownership-placement', o['fact_id'])
        if o['component_id'] is None:
            a.check(any(n['code'] == 'CONTRACT_OWNER_UNRESOLVED' and o['fact_id'] in n['fact_ids'] for n in b['render_notices']),
                    'unknown-owner-notice', o['fact_id'], 'notice, no guessed owner', b['render_notices'])
    return a


def audit_contract(a, text, path, kind, v, b):
    front = yaml.safe_load(text.split('---', 2)[1])
    a.equal(front.get('generated'), True, 'generated-label', path)
    a.equal(front.get('non_normative'), True, 'non-normative-label', path)
    a.equal(front.get('snapshot_id'), v['snapshot_id'], 'snapshot-label', path)
    facts = {f['id']:f for f in v['facts']['facts']}
    for fid in front['fact_ids']:
        f = facts[fid]
        for ev in f['evidence']:
            a.check(ev['id'] in text and f"{ev['path']}:{ev['start_line']}" in text,
                    'evidence-preserved', path, ev['id'] + ' + path:line', 'present' if ev['id'] in text else 'missing')
    if kind == 'api':
        audit_api(a, text, path, [facts[i] for i in front['fact_ids']], facts, b)
    elif kind == 'table':
        audit_tables(a, text, path, [facts[i] for i in front['fact_ids']])
    elif kind == 'event':
        audit_events(a, text, path, [facts[i] for i in front['fact_ids']])


def audit_api(a, text, path, routes, facts, b):
    docs = [json.loads(x) for x in blocks(text, 'json')]
    a.check(len(docs) <= 1, 'one-openapi-block', path, '<=1', len(docs))
    ops = {}
    for doc in docs:
        errs = references(doc)
        a.equal(errs, [], 'local-openapi-refs', path)
        if not errs:
            errors = [str(e)[:500] for e in OpenAPIV31SpecValidator(doc).iter_errors()]
            a.equal(errors, [], 'openapi-3.1-format', path)
        for p, methods in doc['paths'].items():
            for method, op in methods.items():
                for fid in op['x-analysis']['fact_ids']:
                    a.check(fid not in ops, 'one-operation-per-fact', path, 'unique', fid)
                    ops[fid] = (p, method, op, doc)
    for f in routes:
        fid, attrs = f['id'], f['attributes']
        candidates = [r for r in rows(text) if '`' + fid + '`' in r]
        a.equal(len(candidates), 1, 'route-row-cardinality', path + ':' + fid)
        if len(candidates) == 1:
            r = candidates[0]
            for index, field in enumerate(['application_id','method','path','handler','request_model_ids','response_model_ids','status_codes','auth']):
                if field in attrs and not (field == 'path' and value(attrs[field]) is None and 'path_suffix' in attrs):
                    a.markdown_field(r[index], attrs[field], path + ':' + field)
        if fid not in ops:
            a.check(any(n['code'] == 'OPENAPI_OPERATION_OMITTED' and fid in n['fact_ids'] for n in b['render_notices']),
                    'omitted-operation-notice', path, fid, b['render_notices'])
            continue
        p, method, op, doc = ops[fid]
        a.equal(p, value(attrs['path']), 'openapi-path', path)
        a.equal(method.upper(), value(attrs['method']), 'openapi-method', path)
        a.equal(sorted(op['responses']), sorted(map(str, value(attrs['status_codes']) or [])), 'openapi-status', path)
        a.equal(op['x-analysis'].get('application_id'), value(attrs['application_id']), 'openapi-application', path)
        a.check(value(attrs['application_id']) is not None and value(attrs.get('registration_context')) is not None,
                'operation-identity-known', path, 'known app and registration identity, else omitted', attrs)
        if value(attrs['auth']) is None:
            a.check('security' not in op and 'security' not in doc, 'no-invented-auth', path, 'no security declaration', op.get('security'))
        params = value(attrs.get('parameters'))
        if params is not None and all(all(value(x.get(k)) is not None for k in ['name','in','required']) for x in params):
            actual = [(x['name'], x['in'], x['required'], x.get('schema')) for x in op.get('parameters', [])]
            expected = [(value(x['name']), value(x['in']), value(x['required']), value(x.get('type'))) for x in params]
            if all(x[3] is not None for x in expected):
                a.equal(actual, expected, 'parameter-semantics', path)
        # Verify every model referenced by an explicitly associated body, including field required/nullability.
        for body in value(attrs.get('bodies')) or []:
            model = facts.get(body['model_id'])
            if not model or not body.get('media_type'):
                continue
            schemas = doc.get('components', {}).get('schemas', {})
            matches = [s for s in schemas.values() if model['id'] in s.get('x-analysis', {}).get('fact_ids', [])]
            a.equal(len(matches), 1, 'body-model-present', path)
            if not matches:
                continue
            ms = matches[0]
            fields = value(model['attributes']['fields']) or []
            a.equal(sorted(ms.get('properties', {})), sorted(value(x['name']) for x in fields), 'model-fields', path)
            a.equal(sorted(ms.get('required', [])), sorted(value(x['name']) for x in fields if value(x['required']) is True), 'model-required', path)
            for field in fields:
                name, typ = value(field['name']), value(field['type'])
                actual = ms.get('properties', {}).get(name)
                if typ is not None and 'x-model-fact' not in json.dumps(typ):
                    expected = {'anyOf':[typ, {'type':'null'}]} if value(field['nullable']) else typ
                    a.equal(actual, expected, 'model-field-type-nullability', path + ':' + name)
            a.check('x-model-fact' not in json.dumps(ms), 'nested-model-resolved', path, 'local resolved schemas', ms)
        if 'requestBody' in op:
            # API-004 bodies carry no body-required field. Renderer must not assert true without evidence.
            a.check(op['requestBody'].get('required') is not True, 'body-required-not-invented', path,
                    'do not assert required=true without an input contract field', op['requestBody'])


def audit_tables(a, text, path, tables):
    sql = '\n'.join(blocks(text, 'sql'))
    for f in tables:
        attrs = f['attributes']
        # Each table is linked to its fact by an independently parsed SQL comment.
        match = re.search(r'^-- fact: ' + re.escape(f['id']) + r'\n(.*?)(?=^-- (?:fact|omitted):|\Z)', sql, re.M | re.S)
        if not match:
            a.check('-- omitted: ' + f['id'] in sql, 'ddl-omission-explicit', path, f['id'], sql)
            continue
        dialect = value(attrs['dialect'])
        try:
            statements = sqlglot.parse(match[1], read='postgres' if dialect == 'postgresql' else dialect)
        except Exception as exc:
            a.check(False, 'ddl-parse', path, 'parseable DDL', str(exc)); continue
        a.equal(len(statements), 1, 'ddl-single-statement', path)
        stmt = statements[0]
        a.check(isinstance(stmt, exp.Create), 'ddl-create-only', path, 'CREATE TABLE', type(stmt).__name__)
        if not isinstance(stmt, exp.Create):
            continue
        a.equal(stmt.this.this.name, value(attrs['name']), 'ddl-table-name', path)
        columns = list(stmt.find_all(exp.ColumnDef))
        wanted = value(attrs['columns']) or []
        a.equal([x.name for x in columns], [value(x['name']) for x in wanted], 'ddl-column-order', path)
        for actual, expected in zip(columns, wanted):
            dialect_name = 'postgres' if dialect == 'postgresql' else dialect
            try:
                expected_type = sqlglot.parse_one('CREATE TABLE t (x ' + value(expected['type']) + ')', read=dialect_name).find(exp.ColumnDef).args['kind']
                a.equal(actual.args['kind'], expected_type, 'ddl-column-type', path + ':' + actual.name)
            except Exception as exc:
                a.check(False, 'ddl-type-valid', path, 'catalogued type', str(exc))
            notnull = any(isinstance(x.kind, exp.NotNullColumnConstraint) for x in actual.constraints)
            a.equal(notnull, value(expected['nullable']) is False, 'ddl-nullability', path + ':' + actual.name)
        actual_pk = [x.name for pk in stmt.find_all(exp.PrimaryKey) for x in pk.expressions]
        a.equal(actual_pk, [value(x['name']) for x in wanted if value(x['primary_key'])], 'ddl-primary-key', path)
        expected_fk = [(value(c['name']), value(c['foreign_key'])['table'], value(c['foreign_key'])['column'])
                       for c in wanted if value(c['foreign_key']) is not None]
        actual_fk = []
        for fk in stmt.find_all(exp.ForeignKey):
            ref = fk.args['reference'].this
            actual_fk.append((fk.expressions[0].name, ref.this.name, ref.expressions[0].name))
        a.equal(actual_fk, expected_fk, 'ddl-foreign-key', path)
        # Read the human table too: don't let a correct SQL block hide incorrect documentation.
        section = text.split('Fact `' + f['id'] + '`', 1)[1].split('\n## ', 1)[0]
        human_rows = rows(section)[1:]
        a.equal(len(human_rows), len(wanted), 'table-row-count', path)
        for row, col in zip(human_rows, wanted):
            for index, key in enumerate(['name','type','primary_key','foreign_key','nullable']):
                a.markdown_field(row[index], col[key], path + ':' + key)


def audit_events(a, text, path, events):
    schemas = [json.loads(x) for x in blocks(text, 'json')]
    for f in events:
        matches = [s for s in schemas if f['id'] in s.get('x-analysis', {}).get('fact_ids', [])]
        a.equal(len(matches), 1, 'event-schema-count', path)
        if not matches:
            continue
        s = matches[0]
        try:
            Draft202012Validator.check_schema(s)
            err = None
        except Exception as exc:
            err = str(exc)[:500]
        a.equal(err, None, 'event-schema-2020-12', path)
        a.equal(references(s), [], 'event-local-refs', path)
        payload = value(f['attributes']['payload'])
        actual = {k:v for k,v in s.items() if k not in ('$schema', 'x-analysis')}
        a.equal(actual, payload if payload is not None else {}, 'event-payload-preserved', path)
        if payload is None:
            a.equal(s['x-analysis'].get('completeness'), 'partial', 'unknown-payload-partial', path)
        r = [r for r in rows(text) if '`' + f['id'] + '`' in r]
        a.equal(len(r), 1, 'event-row-count', path)
        if r:
            for index, key in enumerate(['topic','broker','namespace','serialization_context'], start=1):
                a.markdown_field(r[0][index], f['attributes'][key], path + ':' + key)


def audit_graph(a, output, v, artifacts):
    model = v['model']
    nodes = sorted(x['id'] for x in model['components'] + model.get('external_systems', []))
    expected_edges = Counter((e['source_component_id'], e['target_component_id'], e['relation_type']) for e in model['edges'])
    mmd = (output / 'architecture.mmd').read_text(encoding='utf-8')
    embedded = blocks((output / 'README.md').read_text(encoding='utf-8'), 'mermaid')
    a.equal([s.strip() for s in embedded], [mmd.strip()], 'readme-mermaid-parity', 'README.md')
    # Renderer defines n0..nN in ordinal model-ID order. Parse actual edges, not its internal plan.
    declared = re.findall(r'^\s*(n\d+)\[', mmd, re.M)
    a.equal(sorted(declared), sorted('n' + str(i) for i in range(len(nodes))), 'mermaid-node-count', 'architecture.mmd')
    mapping = {'n'+str(i): nid for i,nid in enumerate(nodes)}
    edges = re.findall(r'(n\d+)\s*-->\|"?([^|"\n]+)"?\|\s*(n\d+)', mmd)
    actual = Counter((mapping.get(s,s), mapping.get(t,t), rel) for s,rel,t in edges)
    a.equal(actual, expected_edges, 'mermaid-edge-parity', 'architecture.mmd')
    if not any(x['kind'] == 'diagram_image' and x['status'] == 'ready' for x in artifacts):
        return
    root = ET.fromstring((output / 'architecture.svg').read_text(encoding='utf-8'))
    gotnodes = [el.attrib['data-node'] for el in root.iter() if 'data-node' in el.attrib]
    gotedges = Counter(tuple(el.attrib['data-edge'].split('|')) for el in root.iter() if 'data-edge' in el.attrib)
    a.equal(sorted(gotnodes), nodes, 'svg-node-parity', 'architecture.svg')
    a.equal(gotedges, expected_edges, 'svg-edge-parity', 'architecture.svg')
    forbidden = [el.tag for el in root.iter() if el.tag.split('}')[-1] in ['script','foreignObject','image','use','a','iframe']
                 or any(k.lower().startswith('on') or 'href' in k.lower() for k in el.attrib)]
    a.equal(forbidden, [], 'svg-active-content', 'architecture.svg')
