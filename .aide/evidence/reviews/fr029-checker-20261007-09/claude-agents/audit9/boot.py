import sys, os, types, tempfile
A = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(A, "tmp"), exist_ok=True)
tempfile.tempdir = os.path.join(A, "tmp")
sys.dont_write_bytecode = True
m = types.ModuleType("openapi_spec_validator"); m.validate = lambda *a, **k: None
sys.modules.setdefault("openapi_spec_validator", m)
S = "d:/VSF/l3-generator-l3/slice"
os.chdir(S)
sys.path[:0] = [S, S + "/tests"]
from test_checker_counterexamples import claims_of, route, part, http, reminders  # noqa

import json, subprocess, itertools
_n = itertools.count()
PY = sys.executable


def truth(files, module="main", attr="app", extra=""):
    """Write files to a fresh dir, import module, print OpenAPI paths + params (FastAPI's real behaviour)."""
    d = os.path.join(A, "tmp", f"truth{os.getpid()}_{next(_n)}")
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
    code = (f"import sys,json;sys.path.insert(0,{d!r});import {module} as m;s=getattr(m,{attr!r}).openapi();"
            "print(json.dumps({p:{k:[(x['in'],x['name']) for x in v.get('parameters',[])] for k,v in ops.items()} "
            "for p,ops in s['paths'].items()}))" + extra)
    r = subprocess.run([PY, "-B", "-c", code], capture_output=True, text=True, cwd=d)
    return (r.stdout.strip() or r.stderr.strip()[-600:])
