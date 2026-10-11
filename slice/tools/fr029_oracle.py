"""Oracle FR-029: import app FastAPI của một fixture trong venv sandbox, ghi OpenAPI và danh sách route ra JSON.

Chỉ dùng để dựng gold. Không dùng trong sản phẩm, không đưa vào prompt hay input của agent.

Cách chạy (từ gốc repository):

    python slice/tools/fr029_oracle.py --python <venv>/Scripts/python.exe \
        --fixture slice/tests/fixtures/fr029/prefix_chain --target "app.main:create_app()" \
        --env ADMIN_PREFIX=/__ENV_ADMIN_PREFIX__ --out slice/tests/fixtures/fr029/prefix_chain.oracle.json

Script tự gọi lại chính nó bằng python của venv (chế độ --inner), cwd là thư mục fixture.
"""

import argparse
import json
import os
import subprocess
import sys


def outer(args):
    fixture = os.path.abspath(args.fixture)
    env = {k: os.environ[k] for k in ("SYSTEMROOT", "PATH", "TEMP", "TMP") if k in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONIOENCODING"] = "utf-8"
    for item in args.env:
        key, _, value = item.partition("=")
        env[key] = value
    cmd = [args.python, "-B", os.path.abspath(__file__), "--inner", "--fixture", fixture, "--target", args.target]
    proc = subprocess.run(cmd, cwd=fixture, env=env, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(proc.returncode)
    data = json.loads(proc.stdout)
    data["oracle"]["env"] = sorted(args.env)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")
    print(f"wrote {args.out}: {len(data['routes'])} routes, {len(data['models'])} models")


def inner(args):
    sys.dont_write_bytecode = True
    import importlib
    import importlib.metadata as md
    import inspect

    fixture = os.path.abspath(args.fixture)
    sys.path.insert(0, fixture)

    module_name, _, attr = args.target.partition(":")
    call = attr.endswith("()")
    attr = attr[:-2] if call else attr
    module = importlib.import_module(module_name)
    app = getattr(module, attr)
    if call:
        app = app()

    from starlette.routing import Mount, Route, WebSocketRoute
    from fastapi.routing import APIRoute, APIWebSocketRoute

    def rel(path):
        if not path:
            return None
        path = os.path.abspath(path)
        if not path.startswith(fixture + os.sep):
            return None
        return os.path.relpath(path, fixture).replace(os.sep, "/")

    def where(func):
        func = inspect.unwrap(func)
        try:
            file = rel(inspect.getsourcefile(func))
            line = inspect.getsourcelines(func)[1]
        except (TypeError, OSError):
            return None, None
        return file, line

    def type_name(tp):
        if tp is None:
            return None
        if getattr(tp, "__origin__", None) is not None:
            return repr(tp)
        return getattr(tp, "__qualname__", None) or repr(tp)

    def walk(routes, prefix, mounted_openapi):
        out = []
        for r in routes:
            if isinstance(r, Mount):
                sub = r.app
                mount_prefix = prefix + r.path
                if hasattr(sub, "openapi"):
                    mounted_openapi[mount_prefix] = sub.openapi()
                sub_routes = getattr(sub, "routes", None) or []
                out.append({"kind": "Mount", "path": mount_prefix, "app": type(sub).__name__})
                out.extend(walk(sub_routes, mount_prefix, mounted_openapi))
                continue
            file, line = where(r.endpoint) if hasattr(r, "endpoint") else (None, None)
            endpoint = getattr(r, "endpoint", None)
            item = {
                "kind": type(r).__name__,
                "methods": sorted(getattr(r, "methods", None) or []),
                "path": prefix + r.path,
                "mount_prefix": prefix or None,
                "name": getattr(r, "name", None),
                "endpoint_module": getattr(endpoint, "__module__", None),
                "endpoint_qualname": getattr(endpoint, "__qualname__", None),
                "endpoint_file": file,
                "endpoint_first_line": line,  # dòng đầu khối nguồn của hàm, tính cả decorator
            }
            if isinstance(r, APIRoute):
                item["status_code"] = r.status_code
                item["response_model"] = type_name(r.response_model)
                item["response_class"] = type_name(getattr(r.response_class, "value", r.response_class))
                item["include_in_schema"] = r.include_in_schema
            out.append(item)
        return out

    mounted_openapi = {}
    routes = walk(app.routes, "", mounted_openapi)
    openapi = app.openapi()

    import pydantic

    v2 = pydantic.VERSION.startswith("2")
    models = []
    for name, mod in sorted(sys.modules.items()):
        mfile = rel(getattr(mod, "__file__", None))
        if not mfile:
            continue
        for cname, cls in inspect.getmembers(mod, inspect.isclass):
            if cls.__module__ != name or not issubclass(cls, pydantic.BaseModel):
                continue
            fields = []
            if v2:
                for fname, f in cls.model_fields.items():
                    fields.append({
                        "name": fname,
                        "alias": f.alias,
                        "annotation": repr(f.annotation),
                        "required": f.is_required(),
                        "default": repr(f.default) if not f.is_required() else None,
                    })
            else:
                for fname, f in cls.__fields__.items():
                    fields.append({
                        "name": fname,
                        "alias": f.alias,
                        "annotation": repr(f.outer_type_),
                        "required": bool(f.required),
                        "allow_none": bool(f.allow_none),
                        "default": repr(f.default) if not f.required else None,
                    })
            models.append({
                "name": cname,
                "module": name,
                "file": mfile,
                "class_line": inspect.getsourcelines(cls)[1],
                "fields": fields,
            })

    def version(pkg):
        try:
            return md.version(pkg)
        except md.PackageNotFoundError:
            return None

    data = {
        "oracle": {
            "target": args.target,
            "python": sys.version.split()[0],
            "packages": {p: version(p) for p in ("fastapi", "starlette", "pydantic", "pydantic-core", "pydantic-settings")},
        },
        "routes": routes,
        "openapi": openapi,
        "mounted_openapi": mounted_openapi,
        "models": models,
    }
    json.dump(data, sys.stdout, ensure_ascii=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inner", action="store_true")
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--fixture", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--env", action="append", default=[], help="KEY=VALUE cho app cần biến môi trường")
    p.add_argument("--out")
    args = p.parse_args()
    if args.inner:
        inner(args)
    else:
        outer(args)


if __name__ == "__main__":
    main()
