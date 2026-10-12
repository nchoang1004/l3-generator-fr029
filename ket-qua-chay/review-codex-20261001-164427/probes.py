"""Independent review probes. Synthetic inputs only; no network or project-source execution."""
import sys, json, tempfile, zipfile, io, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'slice'))
from l3slice import snapshot, extract, model, verify, render, run, gateway
from l3slice.engine import Engine

results = {}
def facts_of(folder):
    snap, sources = snapshot.take(folder)
    inv = snapshot.inventory(snap)
    fs = extract.extract(snap, sources, inv['units'][0]['id'])
    return snap, sources, inv, fs

with tempfile.TemporaryDirectory() as t:
    base=Path(t); src=base/'src'; src.mkdir()
    (src/'main.py').write_text('from fastapi import FastAPI\napp = FastAPI()\n@app.get("/items", status_code=200)\ndef items():\n    return []\n', encoding='utf-8')
    snap,sources,inv,fs=facts_of(src)
    member={'partition_version':'fixture-membership-v1','components':[{'name':'App','files':['main.py']}]}
    arch=model.build(snap,inv['units'][0]['id'],fs,member)
    bad=copy.deepcopy(fs)
    route=next(f for f in bad['facts'] if f['kind']=='route')
    route['attributes']['status_codes']['value']=[20]
    checked=verify.verify(snap,sources,inv,bad,arch)
    value=next(f for f in checked['facts']['facts'] if f['kind']=='route')['attributes']['status_codes']
    bundle=render.render(checked,'run_probe','probe',base/'bad-status')
    results['invalid_status_20_against_source_200']={'verified':value,'published_ready':[a['path'] for a in bundle['artifacts'] if a['status']=='ready']}
    route0=next(f for f in fs['facts'] if f['kind']=='route')
    text,doc,notices,cov=render.render_api(arch['components'][0],[route0],'api.md','Demo',facts={f['id']:f for f in fs['facts']})
    tampered=text.replace('| 200 |','| 404 |')
    results['document_wrong_status_same_ids']={'changed':tampered!=text,'checker_error':render.check_doc('api',tampered,cov)}

    (src/'.venv').mkdir();(src/'.venv/dependency.py').write_text('x=1\n')
    local,_=snapshot.take(src)
    z=base/'source.zip'
    with zipfile.ZipFile(z,'w') as f:
        for p in src.rglob('*'):
            if p.is_file(): f.write(p,p.relative_to(src).as_posix())
    zipped,_=snapshot.take_zip(z)
    results['same_repo_local_zip']={'local_files':[f['path'] for f in local['files']], 'zip_files':[f['path'] for f in zipped['files']], 'same_snapshot':local['snapshot_id']==zipped['snapshot_id']}

    secret_src=base/'secret-source';secret_src.mkdir()
    marker='FAKE_REVIEW_PASSWORD_123'
    (secret_src/'config.py').write_text('from pydantic_settings import BaseSettings\nclass Settings(BaseSettings):\n    DATABASE_URL: str = "postgresql://demo:'+marker+'@localhost/db"\n',encoding='utf-8')
    s,raw,iv,facts=facts_of(secret_src)
    am=model.build(s,iv['units'][0]['id'],facts,{'partition_version':'fixture-membership-v1','components':[{'name':'Config','files':['config.py']}]})
    out=base/'secret-out';render.render(verify.verify(s,raw,iv,facts,am),'run_secret','secret-demo',out)
    results['synthetic_credential_redaction']={'marker_in_result':marker in (out/'result.json').read_text(encoding='utf-8'),'config_values':[f['attributes']['value'] for f in facts['facts'] if f['kind']=='config']}
    results['synthetic_credential_redaction']['marker_survives_egress_mask']=marker in json.dumps(gateway.mask_obj(facts))

    e=Engine(base/'engine')
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w') as f:
        f.writestr('main.py','x = 1\n')
        f.writestr('pyproject.toml','[project]\ndependencies = 1\n')
    rec=e.submit_zip(mem.getvalue())
    try:
        e.step(); raised=None
    except Exception as ex:
        raised=type(ex).__name__+': '+str(ex)
    results['malformed_manifest_worker']={'exception':raised,'state':e.view(rec['run_id'])['state'],'stage':e.view(rec['run_id'])['stage']}

    props=base/'properties';props.mkdir()
    (props/'app.py').write_text('from fastapi import FastAPI\nfrom pydantic import BaseModel\napp=FastAPI()\nclass Item(BaseModel):\n    values: list[int | None]\n@app.post("/items", status_code=201)\ndef create(item: Item) -> Item:\n    return item\n',encoding='utf-8')
    s,raw,iv,facts=facts_of(props)
    results['nullable_array_item']=[f['attributes']['fields'] for f in facts['facts'] if f['kind']=='request_model']
    # Optional body default is lost by the extractor/render boundary.
    p=props/'app.py';p.write_text(p.read_text(encoding='utf-8').replace('item: Item)', 'item: Item = None)'),encoding='utf-8')
    s,raw,iv,facts=facts_of(props)
    ar=model.build(s,iv['units'][0]['id'],facts,{'partition_version':'fixture-membership-v1','components':[{'name':'App','files':['app.py']}]})
    rt=next(f for f in facts['facts'] if f['kind']=='route')
    txt,doc,_,_=render.render_api(ar['components'][0],[rt],'api.md','Demo',facts={f['id']:f for f in facts['facts']})
    results['optional_body']={'source_default':'None','generated_required':doc['paths']['/items']['post']['requestBody']['required']}
    sys.path.insert(0,str(ROOT/'slice/tools'))
    from golden_adapter import to_prediction
    prediction=to_prediction(facts,s,raw,'synthetic-review','test-digest',extract.EXTRACTOR_VERSION)
    projected=next(f for f in prediction['facts'] if f['kind']=='route')
    results['golden_route_labels']={'product_confidence':rt['confidence'],'adapter_confidence':projected['confidence'],'product_completeness':rt['completeness'],'adapter_completeness':projected['completeness']}

Path(__file__).with_name('probes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
