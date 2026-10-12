"""Read-only inventory/integrity checks; not a semantic golden validator."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cases():
    fixture = ROOT / 'slice/tests/fixtures/fr029'
    for p in sorted(fixture.glob('*.gold.json')):
        yield 'fixture/' + p.name.split('.')[0], p, fixture / p.name.split('.')[0]
    yield 'fixture/fr029_e2e', ROOT / 'slice/tests/fixtures/fr029_e2e.gold.json', ROOT / 'slice/tests/fixtures/fr029_e2e'
    dev = Path('D:/VSF/VSF-L3 Generator')
    manifest = json.loads((dev / 'evaluation/golden/v1/manifest.json').read_text(encoding='utf-8'))
    for c in manifest['cases']:
        if c['split'] == 'development' and c['family'] in ('fastapi-docs', 'orders-fixture', 'netflix-dispatch'):
            yield 'dev/' + c['case_id'], dev / c['case'] / 'gold.json', dev / c['source']
    base = Path('D:/VSF/l3-generator-golden-v2')
    for name, revision, source in [
        ('teamhide-fastapi-boilerplate', 3, 'teamhide_fastapi-boilerplate-df4e6d4'),
        ('fastapi_best_architecture', 2, 'fastapi-practices_fastapi_best_architecture-123a44a'),
        ('full-stack-fastapi-template', 2, 'full-stack-fastapi-template-cb740b6'),
        ('igorbenav-FastAPI-boilerplate', 3, 'fastapi-boilerplate'),
    ]:
        yield 'full/' + name, base / f'.aide/evidence/tests/golden-v1/{name}/final-r{revision}.json', base / 'sample-repos' / source
    for name, source in [('tdd-docker', 'testdrivenio_fastapi-tdd-docker-16433b6'), ('agentgpt', 'reworkd_AgentGPT-18b073a'), ('kibo', 'KIBO-Agenda_kibo-backend-89eb3bb')]:
        p = Path(f'D:/VSF/l3-acceptance-gold/{name}/gold.json')
        d = json.loads(p.read_text(encoding='utf-8'))
        yield 'accept/' + name, p, Path('D:/VSF/l3-acceptance-repos') / source / d.get('root', '.')


def walk(x, path='$'):
    if isinstance(x, dict):
        yield path, x
        for k, v in x.items():
            yield from walk(v, path + '.' + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, f'{path}[{i}]')


def inventory():
    rows = []
    for name, gold_path, source in cases():
        d = json.loads(gold_path.read_text(encoding='utf-8'))
        refs, problems = [], []
        checked_sources = {}
        for jp, x in walk(d):
            f, start, end = x.get('file'), x.get('line_from', x.get('line')), x.get('line_to', x.get('line_from', x.get('line')))
            if f and isinstance(start, int):
                refs.append((jp, f, start, end, x.get('quote')))
            for key in ('declared_at', 'where', 'client_at'):
                val = x.get(key)
                if isinstance(val, str) and ':' in val and val.rsplit(':', 1)[1].isdigit():
                    file, line = val.rsplit(':', 1)
                    refs.append((jp + '.' + key, file, int(line), int(line), None))
        skipped = 0
        for jp, file, start, end, quote in refs:
            p = source / file
            if '.env' in p.name:
                skipped += 1
                continue
            if not p.is_file():
                problems.append({'json_path': jp, 'problem': 'missing_file', 'file': file})
                continue
            lines = p.read_text(encoding='utf-8-sig').splitlines()
            checked_sources[file] = digest(p)
            if not (1 <= start <= end <= len(lines)):
                problems.append({'json_path': jp, 'problem': 'invalid_range', 'file': file, 'range': [start, end]})
            elif quote and quote not in '\n'.join(lines[start-1:end]):
                problems.append({'json_path': jp, 'problem': 'quote_not_verbatim_in_range', 'file': file, 'range': [start, end]})
        keys = [(r.get('method'), r.get('path'), r.get('handler')) for r in d.get('routes', [])]
        duplicates = [list(k) for k, count in collections.Counter(keys).items() if count > 1]
        rows.append({'case': name, 'gold': str(gold_path), 'source_root': str(source), 'gold_sha256': digest(gold_path), 'declared_commit': d.get('commit'),
                     'counts': {k: len(v) for k, v in d.items() if isinstance(v, list)}, 'references_checked': len(refs) - skipped,
                     'secret_named_references_skipped': skipped, 'duplicate_route_keys': duplicates, 'structural_problems': problems,
                     'referenced_source_sha256': checked_sources})
    return {'purpose': 'Structural checks only, not semantic correctness; original files unchanged.', 'cases': rows}


if __name__ == '__main__':
    result = inventory()
    (HERE / 'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'cases': len(result['cases']), 'references_checked': sum(r['references_checked'] for r in result['cases']),
                      'problems': [{'case': r['case'], 'problems': r['structural_problems'], 'duplicates': r['duplicate_route_keys']} for r in result['cases'] if r['structural_problems'] or r['duplicate_route_keys']]}, ensure_ascii=False))
