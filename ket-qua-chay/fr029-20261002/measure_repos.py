"""Read four development repositories without importing or executing their code."""
import argparse
import collections
import json
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--engine-root', type=Path, required=True)
p.add_argument('--samples', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
sys.path.insert(0, str(a.engine_root))
from l3slice import extract, snapshot

a.out.mkdir(parents=True, exist_ok=False)
summary = []
for repo in sorted(a.samples.iterdir()):
    if not repo.is_dir():
        continue
    snap, sources = snapshot.take(repo)
    inv = snapshot.inventory(snap)
    fs = extract.extract(snap, sources, inv['units'][0]['id'])
    routes = [f for f in fs['facts'] if f['kind'] == 'route']
    row = {'repo': repo.name, 'snapshot_id': snap['snapshot_id'],
           'facts': dict(collections.Counter(f['kind'] for f in fs['facts'])),
           'limitations': dict(collections.Counter(n['code'] for n in fs['limitations'])),
           'routes': [{'method': f['attributes']['method'], 'path': f['attributes']['path'],
                       'response': f['attributes']['response_model_ids'],
                       'bodies': f['attributes'].get('bodies')} for f in routes]}
    summary.append(row)
    (a.out / (repo.name + '.facts.json')).write_text(json.dumps(fs, ensure_ascii=False, indent=2), encoding='utf-8')
(a.out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps([{k: v for k, v in r.items() if k != 'routes'} for r in summary], ensure_ascii=False, indent=2))
