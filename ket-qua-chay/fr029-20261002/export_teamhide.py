"""Re-export the user's snapshot with its existing membership, never invent a new partition."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'slice'))
from l3slice import snapshot, extract, model, verify, render

out = Path(__file__).resolve().parent
previous = json.loads(Path('D:/FPT3/result.json').read_text(encoding='utf-8'))['result']
source = ROOT.parent / 'l3-generator-quote-evidence/sample-repos/teamhide_fastapi-boilerplate-df4e6d4'
snap, sources = snapshot.take(source)
assert snap['snapshot_id'] == previous['snapshot_id'], 'Do not reuse membership across a changed snapshot'
paths = {f['file_id']: f['path'] for f in snap['files']}
membership = {'partition_version': 'fixture-membership-v1', 'components': [
    {'name': c['name'], 'files': [paths[i] for i in c['member_file_ids']]} for c in previous['model']['components']]}
(out / 'teamhide-existing.membership.json').write_text(json.dumps(membership, ensure_ascii=False, indent=2), encoding='utf-8')
inv = snapshot.inventory(snap)
fs = extract.extract(snap, sources, inv['units'][0]['id'])
arch = model.build(snap, inv['units'][0]['id'], fs, membership)
verified = verify.verify(snap, sources, inv, fs, arch)
bundle = render.render(verified, 'run_fr029_validation', 'teamhide', out / 'teamhide-export')
print(json.dumps([{'path': x['path'], 'status': x['status'], 'error': x.get('error')} for x in bundle['artifacts']], ensure_ascii=False, indent=2))
