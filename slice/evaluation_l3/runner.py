from __future__ import annotations
import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
import traceback
from pathlib import Path
from unittest.mock import patch

from l3slice import render
from .cases import catalog, corrupt
from .contracts import ROOT, validate
from .oracle import Audit, audit_bundle, blocks


def serial(obj):
    if isinstance(obj, dict):
        return {str(k):serial(v) for k,v in obj.items()}
    if isinstance(obj, (tuple,list)):
        return [serial(x) for x in obj]
    if obj is None or isinstance(obj,(str,int,float,bool)):
        return obj
    return str(obj)


def write_json(path, obj):
    path.write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(path):
    return {p.relative_to(path).as_posix():digest(p) for p in sorted(path.rglob('*')) if p.is_file()}


def broken_svg(*_):
    raise OSError('evaluation injected transient SVG failure')


def unsafe_svg(*_):
    return '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'


def assert_rejected(a, action, codes, location):
    try:
        action()
        a.check(False,'typed-rejection',location,codes,'accepted without error')
    except render.ExportError as exc:
        a.check(exc.code in codes,'typed-rejection',location,codes,exc.code)
    except Exception as exc:
        a.check(False,'typed-rejection',location,codes,type(exc).__name__+': '+str(exc))


def run_case(case, directory):
    directory.mkdir()
    write_json(directory/'case.json',asdict(case))
    v = deepcopy(case.input)
    a = Audit()
    # A malformed positive fixture is an evaluator error, never charged to product.
    try:
        validate(v,7,'VerifiedResult')
    except Exception:
        return dict(status='error',reason='Fixture violates input schema',traceback=traceback.format_exc(),checks=[])
    corrupt(v,case.invalid_mutation)
    write_json(directory/'input.json',v)
    original = deepcopy(v)
    out = directory/'output'
    mode = case.mode
    call = lambda **kw: render.render(v,'run_eval',case.repository_name,out,**kw)
    try:
        if mode == 'reject':
            assert_rejected(a,call,case.expect['codes'],'input.json')
            a.check(not out.exists(),'no-publish-invalid-input',out,False,out.exists())
        elif mode == 'nonempty':
            out.mkdir(); (out/'keep.txt').write_text('existing user file',encoding='utf-8')
            before=file_hashes(out)
            assert_rejected(a,call,['OUTPUT_UNSAFE'],out)
            a.equal(file_hashes(out),before,'existing-output-preserved',out)
        elif mode == 'publish-failure':
            real_write=Path.write_bytes
            def injected(path, data):
                if '.l3slice-' in str(path) and path.name == 'result.json':
                    raise OSError('evaluation injected write failure')
                return real_write(path,data)
            with patch.object(Path,'write_bytes',injected):
                assert_rejected(a,call,['PUBLISH_FAILED'],out)
            a.check(not out.exists(),'no-half-published-output',out,False,out.exists())
            a.equal(list(directory.glob('.*.l3slice-*')),[],'staging-cleanup',directory)
        elif mode.startswith('retry') or mode == 'svg-failure':
            b=call(renderers={'svg':unsafe_svg if mode=='retry-nonretryable' else broken_svg})
            a.checks += audit_bundle(out,original,allow_failed=True).checks
            target=next(x for x in b['artifacts'] if x['kind']=='diagram_image')
            a.equal(target['status'],'failed','fault-injected-target-failed','architecture.svg')
            before=file_hashes(out)
            if mode == 'svg-failure':
                a.equal(target['error']['code'],'RENDER_FAILED','transient-artifact-error','architecture.svg')
            elif mode == 'retry-nonretryable':
                assert_rejected(a,lambda:render.retry_artifact(out,target['artifact_id']),['ARTIFACT_NOT_RETRYABLE'],out)
            elif mode == 'retry-version':
                b['export_context']['renderer_version']='unavailable'
                write_json(out/'manifest.json',b)
                assert_rejected(a,lambda:render.retry_artifact(out,target['artifact_id']),['VERSION_UNAVAILABLE'],out)
            elif mode == 'retry-tamper':
                with (out/'README.md').open('a',encoding='utf-8') as f: f.write('tampered')
                assert_rejected(a,lambda:render.retry_artifact(out,target['artifact_id']),['INVALID_INPUT'],out)
            else:
                if mode == 'retry-crash':
                    try:
                        render.retry_artifact(out,target['artifact_id'],_crash_after_install=True)
                        a.check(False,'crash-injection',out,'simulated crash','no crash')
                    except RuntimeError:
                        a.equal(digest(out/'manifest.json'),before['manifest.json'],'manifest-last-crash-safety','manifest.json')
                        a.equal(json.loads((out/'manifest.json').read_text(encoding='utf-8'))['artifacts'],b['artifacts'],
                                'crash-target-not-ready','manifest.json')
                render.retry_artifact(out,target['artifact_id'])
                a.checks += audit_bundle(out,original).checks
                for path,h in before.items():
                    if path != 'manifest.json':
                        a.equal(digest(out/path),h,'retry-preserves-ready-bytes',path)
                if mode == 'retry-ready':
                    before=file_hashes(out)
                    render.retry_artifact(out,target['artifact_id'])
                    a.equal(file_hashes(out),before,'retry-ready-no-op',out)
        else:
            if mode == 'offline':
                from l3slice import extract, verify, gateway, model, snapshot
                with ExitStack() as stack:
                    for module,fn in [(extract,'extract'),(verify,'verify'),(model,'build'),(snapshot,'take')]:
                        stack.enter_context(patch.object(module,fn,side_effect=AssertionError('upstream called')))
                    stack.enter_context(patch('socket.socket',side_effect=AssertionError('network called')))
                    call()
            else:
                call()
            a.checks += audit_bundle(out,original).checks
            if mode == 'repeat':
                out2=directory/'repeat-output'
                render.render(deepcopy(original),'run_eval',case.repository_name,out2)
                a.equal(file_hashes(out2),file_hashes(out),'deterministic-bytes',out)
            expectations(a,case,out)
        a.equal(v,original,'input-not-mutated','input.json')
    except Exception as exc:
        # Product invocation errors are separated from assertion failures, not disguised as success.
        write_json(directory/'exception.json',dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        return dict(status='error',reason=str(exc),traceback=traceback.format_exc(),checks=a.checks)
    status='fail' if a.errors() else 'pass'
    return dict(status=status,checks=a.checks,failures=a.errors())


def expectations(a,case,out):
    e=case.expect
    b=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    texts={x['path']:(out/x['path']).read_text(encoding='utf-8') for x in b['artifacts'] if x['status']=='ready'}
    for key,kind in [('event_files','event'),('api_files','api')]:
        if key in e:
            a.equal(sum(x['kind']==kind for x in b['artifacts']),e[key],key,'manifest.json')
    if 'api_ops' in e:
        docs=[json.loads(raw) for p,t in texts.items() if '/api/' in p for raw in blocks(t,'json')]
        a.equal(sum(len(ops) for d in docs for ops in d['paths'].values()),e['api_ops'],'expected-operation-count','OpenAPI')
    if 'ddl_tables' in e:
        import re
        count=sum(len(re.findall(r'^CREATE TABLE ',sql,re.M)) for p,t in texts.items() if '/schema/' in p for sql in blocks(t,'sql'))
        a.equal(count,e['ddl_tables'],'expected-ddl-count','SQL')
    if 'text_contains' in e:
        a.check(any(e['text_contains'] in t for p,t in texts.items() if p.endswith('.md')),
                'required-text-visible','Markdown',e['text_contains'],'checked')
    if 'slug_max' in e:
        slugs=list(b['export_context']['component_slugs'].values())
        a.check(all(len(x)<=e['slug_max'] for x in slugs),'slug-length','export_context',e['slug_max'],slugs)
        a.equal(len({x.casefold() for x in slugs}),len(slugs),'unique-slugs','export_context')


NOT_RUN = [
    dict(id='manual-diagram-readability', status='not_run', reason='Human review at 1/10/50 nodes, long labels, arrow visibility and overlapping edges is still required; XML parity is not visual quality.'),
    dict(id='real-verified-result-integration', status='not_run', reason='Synthetic CMP-008 boundary only; no independent real-repository accepted input corpus in this suite.'),
    dict(id='web-download-expiry-concurrency', status='out_of_scope', reason='CMP-001 facade: expiry, download authorization and concurrent writers require separate integration tests.'),
    dict(id='source-truth-LLM-component-quality', status='out_of_scope', reason='Extractor accuracy, LLM reasoning and D-03 partition quality are not renderer metrics.'),
    dict(id='external-user-and-NFR-benchmark', status='not_run', reason='No pilot, OS matrix, large-file performance or acceptance sampling claim; elapsed seconds are diagnostic only.'),
    dict(id='full-crash-matrix', status='not_run', reason='Tests staging write failure and crash after artifact install; not every OS rename/disk-full/process-kill boundary.'),
]


def main(argv=None):
    p=argparse.ArgumentParser(description='Offline isolated CMP-008 contract evaluation (no API key).')
    p.add_argument('--output',type=Path,required=True,help='New directory; refuses to overwrite existing evidence')
    p.add_argument('--case',action='append',default=[],help='Repeat for selected exact case IDs')
    p.add_argument('--list',action='store_true')
    args=p.parse_args(argv)
    cases=catalog()
    if args.list:
        for c in cases: print(f'{c.id}: {c.title}')
        return 0
    if args.case:
        missing=set(args.case)-{c.id for c in cases}
        if missing: p.error('Unknown case IDs: '+', '.join(sorted(missing)))
        cases=[c for c in cases if c.id in args.case]
    out=args.output.resolve()
    if out.exists(): p.error('Output already exists; choose a new path. No files were overwritten.')
    out.mkdir(parents=True)
    provenance_paths = sorted(set(list((ROOT/'slice/l3slice').glob('*.py')) + list((ROOT/'slice/evaluation_l3').rglob('*.py'))
        + list((ROOT/'.aide/tech-specs').glob('*/api/API-*.md'))
        + [ROOT/'slice/tools/evaluate_l3.py',ROOT/'scripts/requirements-l3-check.txt']))
    provenance=dict(started_at=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),
        packages={n:importlib.metadata.version(n) for n in ['jsonschema','referencing','PyYAML','sqlglot','openapi-spec-validator']},
        command=['python','slice/tools/evaluate_l3.py',*(argv or [])],
        files={x.relative_to(ROOT).as_posix():digest(x) for x in provenance_paths if x.is_file()})
    try:
        provenance['git_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        provenance['git_status']=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)
    except Exception as exc: provenance['git_unavailable']=str(exc)
    write_json(out/'provenance.json',provenance)
    results=[]
    for c in cases:
        started=time.perf_counter()
        result=run_case(c,out/c.id)
        result.update(id=c.id,group=c.group,title=c.title,requirement=c.requirement,seconds=round(time.perf_counter()-started,4))
        write_json(out/c.id/'checks.json',result)
        results.append(result)
        print(f'{result["status"].upper():5} {c.id}',flush=True)
    counts={s:sum(r['status']==s for r in results) for s in ['pass','fail','error']}
    report=dict(suite_version='1.0.0',scope='isolated-CMP-008-synthetic-contract-regression',
        acceptance_status='not_evaluated',counts=counts,selected_case_count=len(cases),
        all_catalog_cases_selected=len(cases)==len(catalog()),not_run=NOT_RUN,results=results)
    write_json(out/'report.json',report)
    lines=['# CMP-008 — independent renderer evaluation','',
        f'Cases: {len(cases)}. Pass: {counts["pass"]}; fail: {counts["fail"]}; evaluator/runtime error: {counts["error"]}.',
        '', '**This is a synthetic contract regression result, not a percentage of product quality or acceptance.**',
        'No real-repository precision/recall, LLM quality, component quality or Scope Gate approval is inferred.', '',
        '| Case | Result | Requirement | Findings |','|---|---|---|---|']
    for r in results:
        findings=', '.join(sorted({c['code'] for c in r.get('failures',[])})) or r.get('reason','—')
        lines.append(f'| [{r["id"]}]({r["id"]}/checks.json) | {r["status"]} | {r["requirement"]} | {findings.replace(chr(10)," ").replace("|","/")} |')
    lines+=['','## Not measured / outside this boundary','']+[f'- **{n["id"]}** ({n["status"]}): {n["reason"]}' for n in NOT_RUN]
    lines+=['','## Reproduce','', 'See `provenance.json` for actual source/contract hashes and installed versions. Each case has `input.json`, `case.json`, `checks.json`, and output bytes if published.',
            'Inputs are hand-authored synthetic accepted facts. Their evidence metadata does not claim a real source-ground-truth judgment.',
            'Exit 0 = selected automated cases passed; exit 1 = product assertions failed; exit 2 = at least one evaluator/runtime error. Manual and acceptance gaps remain even with exit 0.','']
    (out/'summary.md').write_text('\n'.join(lines),encoding='utf-8')
    write_json(out/'evidence-hashes.json',file_hashes(out))
    print(json.dumps(counts),flush=True)
    return 2 if counts['error'] else 1 if counts['fail'] else 0
