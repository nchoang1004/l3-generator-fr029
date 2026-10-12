"""Additional offline checks for publication, CLI and source scope."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path.cwd()
OUT=Path(__file__).parent
sys.path[:0]=[str(ROOT/'slice'),str(ROOT/'slice/tests')]
from test_docagent import FIX, MEMBERSHIP, FINDINGS, script
from l3slice.docagent import ScriptedProvider
from l3slice.docpipeline import run_documents
from l3slice import snapshot

results={}
with tempfile.TemporaryDirectory() as td:
    work=Path(td); source=work/'src';source.mkdir()
    files={'route.py':'from fastapi import FastAPI\napp=FastAPI()\n@app.get("/x")\ndef x(): return 1\n',
           'helper.py':'def helper(): return 2\n','db.py':'def save(db): db.commit()\n'}
    for p,s in files.items():(source/p).write_text(s,encoding='utf-8')
    membership=work/'membership.json'
    membership.write_text(json.dumps({'components':[{'name':'Demo','kind':'normal','files':list(files)}]}),encoding='utf-8')
    findings={'routes':[{'method':'GET','handler':'route.py::x','decorator':'route.py:3-4','application':'route.py:2',
        'path_parts':[{'kind':'decorator','value':'/x','at':'route.py:3'}],'params':[],'request_body':None,'response':None,
        'status':{'codes':[200],'rule':'fastapi.default_status_200'},'dependencies':[],'auth':{'unknown':'Not established'}}],
        'file_roles':[{'file':'route.py','role':'Điểm vào','at':'route.py:2'},
          {'file':'db.py','role':'Truy cập dữ liệu','at':'db.py:1'},
          {'file':'helper.py','role':'Service','at':'helper.py:1','call_path':['route.py:4','helper.py:1','db.py:1']}]}
    steps=[ [('read_file',{'path':p}) for p in files], [('submit_findings',findings)], [('finish',{})] ]
    b=run_documents(source,work/'out',membership,'synthetic',ScriptedProvider(steps))
    results['service_without_actual_calls']={'agent':b['agent'],'rejected':b['rejected_claims'],
        'roles':[{ 'role':f['attributes']['role']['value'],'confidence':f['confidence']} for f in b['facts'] if f['kind']=='file_role']}
    (OUT/'invented-service-README.md').write_text((work/'out/README.md').read_text(encoding='utf-8'),encoding='utf-8')

    scenario=work/'script.json'
    scenario.write_text(json.dumps([[{'name':n,'arguments':a} for n,a in step] for step in script(FINDINGS,bad=False)]),encoding='utf-8')
    env=dict(os.environ, PYTHONPATH=str(ROOT/'slice'),PYTHONIOENCODING='utf-8')
    proc=subprocess.run([sys.executable,'-m','l3slice','document','--source',str(FIX),'--output',str(work/'cli-out'),
        '--membership',str(MEMBERSHIP),'--script',str(scenario),'--json'],capture_output=True,text=True,encoding='utf-8',env=env)
    results['cli_smoke']={'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}

    app=work/'scope';(app/'venv').mkdir(parents=True)
    (app/'main.py').write_text('value = 1\n',encoding='utf-8')
    (app/'venv/business.py').write_text('import main\ndef work(): return main.value\n',encoding='utf-8')
    snap,_=snapshot.take(app)
    results['venv_directory_with_project_import']={'snapshot_files':[f['path'] for f in snap['files']],
        'excluded':snap['excluded'],'note':'No pyvenv.cfg; directory contains project source importing main.'}

(OUT/'integration-probes-observed.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
