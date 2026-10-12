"""Reproduce checks. Baseline uses the unchanged staged code, not an invented before state."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PY = sys.executable

def run(name, args):
    proc = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, encoding='utf-8', errors='replace',
                          env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
    (OUT / (name + '.log')).write_text(proc.stdout + '\n' + proc.stderr, encoding='utf-8')
    print(name, proc.returncode)
    return {'command': [PY, *args], 'exit_code': proc.returncode}

results = {}
results['tests'] = run('tests', ['-m', 'unittest', 'discover', '-s', 'slice/tests'])
results['contracts'] = run('contracts', ['scripts/check_l3_contracts.py', '--report'])
results['baseline'] = run('baseline', ['scripts/prd_package.py', 'check', '--change-set', 'CHG-L3GEN-2026-002', '--baseline', 'BL-r10.yaml'])
samples = str(ROOT.parent / 'l3-generator-quote-evidence/sample-repos')
with tempfile.TemporaryDirectory() as t:
    engine = Path(t)
    shutil.copytree(ROOT / 'slice/l3slice', engine / 'l3slice', ignore=shutil.ignore_patterns('__pycache__'))
    # Both files had no unstaged edits when this task started. Preserve the exact index bytes.
    for name in ('extract.py', 'render.py'):
        data = subprocess.check_output(['git', 'show', ':slice/l3slice/' + name], cwd=ROOT)
        (engine / 'l3slice' / name).write_bytes(data)
    results['real-before'] = run('real-before', [str(OUT / 'measure_repos.py'), '--engine-root', str(engine),
        '--samples', samples, '--out', str(OUT / 'real-before')])
results['real-after'] = run('real-after', [str(OUT / 'measure_repos.py'), '--engine-root', str(ROOT / 'slice'),
    '--samples', samples, '--out', str(OUT / 'real-after')])
(OUT / 'checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
