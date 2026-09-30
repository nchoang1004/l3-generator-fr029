"""Facts for the v7 pipeline, read from the syntax tree of each file. No AI.

    facts(idx) -> {path: {...}}      idx is pyindex.index(...)

Every call is resolved to the repository file it reaches, through: an imported name; a parameter whose
annotation or Depends(...) names an imported class; a local variable set from such a call; a `self.`
attribute set in any method of the class. A call into a library keeps the library name instead.

Per file:
- calls: [{line, name, last, target, symbol, lib, func, how, session_arg}]
  how = call | decorator | depends | route_dep (inside dependencies=[...]) | routing (argument of
  include_router, add_middleware, mount, Middleware(...)) | arg_ref (a repository name handed to a library)
- funcs: {name: {"routing", "wiring", "abstract": bool, "calls": same-file names, "lines": [[first, last]]}}
- signals: {tier: [line, what]}  first line per tier (entry, api, data, infra); data needs a model or a query
  written here (select(...), session.query, SQL text), not a session call such as get, commit or refresh.
  Signals are hints for the model, except the "sure" ones.
- sure: {tier: [line, what]}      signs that are almost never wrong: FastAPI(, @router.<verb>, include_router,
  create_engine / create_async_engine, __tablename__ / table=True
- io: [[line, lib, kind]]         calls into I/O libraries; kind database, redis, smtp, broker, http, ...
- db_use: [line]                  a query method called on a session, or a session handed to a library
- objects: {name: [line, lib]}    module-level objects built by a library call (FastCRUD(User), aiosql)
- config_refs: [[line, target]]   session=/engine=/bind= given to a library, value from a repository file
- dynamic: [[line, prefix, names]]  import_module(f"a.b.{x}") and the names read with getattr
- strings: [[line, "pkg.mod"]]    "pkg.mod:attr" strings (uvicorn.run("app.server:app"))
- state_set, state_get: {attr: line}  app.state.<attr> written / read
"""
from __future__ import annotations

import ast
import re

SESSION_NAMES = {"session", "db", "conn", "connection", "read_session", "write_session", "db_session",
                 "async_session", "cursor"}
SESSION_TYPE = re.compile(r"Session|Connection")
DB_METHODS = {"execute", "executemany", "exec", "scalar", "scalars", "scalar_one", "stream", "stream_scalars",
              "query", "add", "add_all", "commit", "rollback", "refresh", "delete", "get", "merge", "flush",
              "fetch", "fetchrow", "fetchval", "fetchone", "fetchall", "remove"}
ROUTING = {"include_router", "add_middleware", "mount", "add_api_route", "add_route", "add_websocket_route",
           "add_api_websocket_route", "add_exception_handler", "Middleware"}
HTTP_VERBS = {"get", "post", "put", "patch", "delete", "head", "options", "api_route", "websocket"}
LIFESPAN_NAMES = {"lifespan", "startup", "shutdown", "on_startup", "on_shutdown", "start_app", "stop_app"}
# library -> (kind of external system, calls that open a connection; None = any call)
IO_LIBS = {
    "sqlalchemy": ("database", {"create_engine", "create_async_engine"}),
    "sqlmodel": ("database", {"create_engine"}),
    "asyncpg": ("database", {"create_pool", "connect"}),
    "aiosqlite": ("database", {"connect"}),
    "redis": ("redis", None), "aioredis": ("redis", None),
    "socketio": ("redis", {"AsyncRedisManager", "RedisManager"}),
    "smtplib": ("smtp", {"SMTP", "SMTP_SSL"}), "aiosmtplib": ("smtp", None),
    "fastapi_mail": ("smtp", {"FastMail"}), "emails": ("smtp", {"send"}),
    "celery": ("broker", {"Celery"}), "taskiq_aio_pika": ("broker", None), "taskiq_redis": ("broker", None),
    "aio_pika": ("broker", None), "kombu": ("broker", None),
    "aiomcache": ("memcached", None), "pymemcache": ("memcached", None),
    "httpx": ("http", {"AsyncClient", "Client", "get", "post", "put", "patch", "delete", "request", "stream"}),
    "requests": ("http", None), "aiohttp": ("http", {"ClientSession", "request"}), "grpc": ("http", None),
    "pywebpush": ("http", None),
    "httpx_oauth": ("oauth", None), "authlib": ("oauth", None), "fastapi_sso": ("oauth", None),
    "sentry_sdk": ("monitoring", {"init"}), "opentelemetry": ("monitoring", None),
    "prometheus_client": ("monitoring", None),
}
CLI_LIBS = {"click", "typer", "cappa"}
IMPORTERS = {"import_module", "import_module_cached", "__import__"}


def _last(node: ast.AST) -> str:
    while isinstance(node, (ast.Call, ast.Subscript)):
        node = node.func if isinstance(node, ast.Call) else node.value
    if isinstance(node, ast.Attribute):
        return node.attr
    return node.id if isinstance(node, ast.Name) else ""


def _root(node: ast.AST) -> ast.AST:
    while isinstance(node, (ast.Attribute, ast.Call, ast.Subscript, ast.Await)):
        node = {ast.Attribute: lambda n: n.value, ast.Call: lambda n: n.func,
                ast.Subscript: lambda n: n.value, ast.Await: lambda n: n.value}[type(node)](node)
    return node


def _direct(nodes: list) -> list:
    """All nodes under `nodes`, without entering nested functions or classes."""
    out, stack = [], list(nodes)
    while stack:
        node = stack.pop()
        out.append(node)
        stack.extend(c for c in ast.iter_child_nodes(node)
                     if not isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    return out


def _const_parts(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.JoinedStr):
        return [v.value for v in node.values if isinstance(v, ast.Constant)]
    if isinstance(node, ast.BinOp):
        return _const_parts(node.left) + _const_parts(node.right)
    return []


SQL = re.compile(r"\s*(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|ALTER|DROP)\b", re.I)


def _sql(node: ast.AST) -> bool:
    """SQL text in a call argument, also inside text("...") or an f-string."""
    return any(SQL.match(part) for sub in ast.walk(node) for part in _const_parts(sub)[:1])


class _File:
    def __init__(self, path: str, entry: dict, tree: ast.Module):
        self.path, self.tree = path, tree
        self.out = {"calls": [], "funcs": {}, "signals": {}, "sure": {}, "io": [], "db_use": [], "objects": {},
                    "config_refs": [], "dynamic": [], "strings": [], "state_set": {}, "state_get": {}}
        self.env = {r["local"]: {"target": r["target"], "symbol": r["symbol"], "lib": r["external"]}
                    for r in entry["imports"]}
        self.libs = {r["external"] for r in entry["imports"] if r["external"]}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.env[node.name] = {"target": path, "symbol": node.name}
        self.classes = {}

    # --- resolution -------------------------------------------------------------------------------
    def resolve(self, node: ast.AST, env: dict, cls: dict | None) -> dict | None:
        if isinstance(node, ast.Await):
            return self.resolve(node.value, env, cls)
        if isinstance(node, ast.Call):
            return self.resolve(node.func, env, cls)
        if isinstance(node, ast.Subscript):
            return self.resolve(node.value, env, cls)
        if isinstance(node, ast.Name):
            got = env.get(node.id)
            return got if got else ({"session": True} if node.id in SESSION_NAMES else None)
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "self" and cls is not None:
                if node.attr in cls["attrs"]:
                    return cls["attrs"][node.attr]
                if node.attr in SESSION_NAMES:
                    return {"session": True}
                if node.attr in cls["methods"]:
                    return {"target": self.path, "symbol": node.attr}
                return {"lib": cls["base_lib"]} if cls["base_lib"] else None
            inner = self.resolve(node.value, env, cls)
            return {k: v for k, v in inner.items() if k != "session"} if inner else None
        return None

    def is_session(self, node: ast.AST, env: dict, cls: dict | None) -> bool:
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
            got = cls["attrs"].get(node.attr) if cls else None
            return node.attr in SESSION_NAMES or bool(got and got.get("session"))
        if isinstance(node, ast.Name):
            return node.id in SESSION_NAMES or bool(env.get(node.id, {}).get("session"))
        return False

    def annotation(self, ann: ast.AST | None, env: dict) -> dict | None:
        """The first repository type named in an annotation; Annotated[X, Depends(Y)] gives X."""
        if ann is None:
            return None
        found = None
        for sub in ast.walk(ann):
            if isinstance(sub, ast.Name):
                if SESSION_TYPE.search(sub.id):
                    got = env.get(sub.id) or {}
                    return {**got, "session": True}
                got = env.get(sub.id)
                if got and got.get("target") and found is None:
                    found = got
        return found

    # --- scopes -----------------------------------------------------------------------------------
    def run(self) -> dict:
        module_nodes = [n for n in self.tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        self.bind_locals(_direct(module_nodes), self.env, None, module=True)
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                self.prepare_class(node)
        self.scope("<module>", _direct(module_nodes), self.env, None)
        for node in self.tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.function(node, node.name, self.env, None)
            elif isinstance(node, ast.ClassDef):
                self.klass(node)
        return self.out

    def prepare_class(self, node: ast.ClassDef) -> None:
        cls = {"attrs": {}, "methods": set(), "base_lib": None}
        for base in node.bases:
            got = self.resolve(base, self.env, None)
            if got and got.get("lib"):
                cls["base_lib"] = got["lib"]
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                cls["methods"].add(item.name)
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                env = dict(self.env)
                self.bind_params(item, env)
                for sub in ast.walk(item):
                    if isinstance(sub, (ast.Assign, ast.AnnAssign)):
                        targets = sub.targets if isinstance(sub, ast.Assign) else [sub.target]
                        for t in targets:
                            if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "self" \
                                    and sub.value is not None:
                                got = self.resolve(sub.value, env, None)
                                if got:
                                    cls["attrs"][t.attr] = got
        self.classes[node.name] = cls

    def klass(self, node: ast.ClassDef) -> None:
        cls = self.classes[node.name]
        body = [n for n in node.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        self.scope(node.name, _direct(body + node.decorator_list + node.bases), self.env, cls)
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.function(item, item.name, self.env, cls)
        self.class_signals(node)

    def bind_params(self, node, env: dict) -> None:
        args = node.args
        params = args.posonlyargs + args.args + args.kwonlyargs
        defaults = [None] * (len(args.posonlyargs + args.args) - len(args.defaults)) + list(args.defaults) \
            + list(args.kw_defaults)
        for arg, default in zip(params, defaults):
            got = self.annotation(arg.annotation, env)
            if isinstance(default, ast.Call) and _last(default.func) == "Depends" and default.args:
                got = got or self.resolve(default.args[0], env, None)
            if got:
                env[arg.arg] = got
            elif arg.arg in SESSION_NAMES:
                env[arg.arg] = {"session": True}

    def bind_locals(self, nodes: list, env: dict, cls: dict | None, module: bool = False) -> None:
        for node in nodes:
            if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                got = self.resolve(node.value, env, cls)
                for t in targets:
                    if isinstance(t, ast.Name) and got:
                        env[t.id] = {**got, "session": got.get("session") or t.id in SESSION_NAMES}
                        if module and got.get("lib") and isinstance(node.value, (ast.Call, ast.Await)):
                            self.out["objects"][t.id] = [node.lineno, got["lib"]]
                    if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Attribute) and t.value.attr == "state":
                        self.out["state_set"].setdefault(t.attr, node.lineno)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    if isinstance(item.optional_vars, ast.Name):
                        got = self.resolve(item.context_expr, env, cls) or {}
                        name = item.optional_vars.id
                        opens = re.search(r"session|Session|connect|begin|acquire", _last(item.context_expr))
                        env[name] = {**got, "session": bool(got.get("session") or opens or name in SESSION_NAMES)}

    def function(self, node, qual: str, parent_env: dict, cls: dict | None) -> None:
        env = dict(parent_env)
        self.bind_params(node, env)
        body = _direct(node.body)
        self.bind_locals(body, env, cls)
        rec = self.out["funcs"].setdefault(node.name, {"routing": False, "wiring": False, "calls": set(),
                                                       "lines": [], "abstract": False})
        rec["lines"].append([node.lineno, node.end_lineno])
        decorators = [_last(d) for d in node.decorator_list]
        stubs = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
        if "abstractmethod" in decorators or all(isinstance(s, (ast.Pass, ast.Raise)) for s in stubs):
            rec["abstract"] = True
        if node.name in LIFESPAN_NAMES or any(d.endswith("contextmanager") for d in decorators):
            rec["wiring"] = True
        defaults = [d for d in node.args.defaults + node.args.kw_defaults if d is not None]
        self.scope(qual, body + _direct(node.decorator_list + defaults), env, cls)
        self.function_signals(node, body)
        for sub in body:
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.function(sub, f"{qual}.{sub.name}", env, cls)
                if rec["wiring"]:
                    self.out["funcs"][sub.name]["wiring"] = True

    # --- calls ------------------------------------------------------------------------------------
    def scope(self, qual: str, nodes: list, env: dict, cls: dict | None) -> None:
        func = self.out["funcs"].get(qual.split(".")[-1]) if qual != "<module>" else None
        for node in nodes:
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute) and node.value.attr == "state" \
                    and isinstance(node.ctx, ast.Load):
                self.out["state_get"].setdefault(node.attr, node.lineno)
            if isinstance(node, ast.If) and qual == "<module>" and "__main__" in ast.unparse(node.test):
                self.signal("entry", node.lineno, "__main__")
            if not isinstance(node, ast.Call):
                continue
            self.call(node, qual, env, cls, func)

    def record(self, line: int, name: str, last: str, got: dict | None, qual: str, how: str, session_arg=False):
        got = got or {}
        if not (got.get("target") or got.get("lib")):
            return
        self.out["calls"].append({"line": line, "name": name[:90], "last": last, "target": got.get("target"),
                                  "symbol": got.get("symbol"), "lib": got.get("lib"), "func": qual, "how": how,
                                  "session_arg": session_arg})

    def call(self, node: ast.Call, qual: str, env: dict, cls: dict | None, func: dict | None) -> None:
        last = _last(node.func)
        got = self.resolve(node.func, env, cls)
        values = list(node.args) + [k.value for k in node.keywords]
        session_arg = any(self.is_session(v, env, cls) for v in values)
        text = ast.unparse(node.func)
        self.record(node.lineno, text, last, got, qual, "call", session_arg)
        if func is not None and got and got.get("target") == self.path and got.get("symbol"):
            func["calls"].add(got["symbol"])
        lib = (got or {}).get("lib")
        # database use; a query written here (SQL text, session.query) is a data sign, other session calls are not
        on_session = isinstance(node.func, ast.Attribute) and self.is_session(node.func.value, env, cls)
        if on_session and (last == "query" or (node.args and _sql(node.args[0]))):
            self.signal("data", node.lineno, "query(" if last == "query" else "SQL")
        if on_session and last in DB_METHODS:
            self.out["db_use"].append(node.lineno)
        elif lib and session_arg:
            self.out["db_use"].append(node.lineno)
        if lib:
            for kw in node.keywords:
                if kw.arg in {"session", "engine", "bind", "session_maker", "sessionmaker"}:
                    ref = self.resolve(kw.value, env, cls)
                    if ref and ref.get("target"):
                        self.out["config_refs"].append([getattr(kw, "lineno", node.lineno), ref["target"]])
        # signals and I/O
        self.call_signals(node, last, lib, text)
        # routing, Depends, dependencies=[...], names handed to a library
        if last in ROUTING:
            if func is not None:
                func["routing"] = True
            for v in values:
                self.record(node.lineno, ast.unparse(v), _last(v), self.resolve(v, env, cls), qual, "routing")
        if last == "Depends" and node.args:
            self.record(node.lineno, ast.unparse(node.args[0]), _last(node.args[0]),
                        self.resolve(node.args[0], env, cls), qual, "depends")
        for kw in node.keywords:
            if kw.arg == "dependencies":
                for el in getattr(kw.value, "elts", []):
                    inner = el.args[0] if isinstance(el, ast.Call) and _last(el.func) == "Depends" and el.args else el
                    self.record(el.lineno, ast.unparse(inner), _last(inner), self.resolve(inner, env, cls), qual,
                                "route_dep")
        if lib and last not in ROUTING | HTTP_VERBS and last != "Depends":
            for v in values:
                if isinstance(v, (ast.Name, ast.Attribute)):
                    ref = self.resolve(v, env, cls)
                    if ref and ref.get("target") and ref["target"] != self.path:
                        self.record(node.lineno, ast.unparse(v), _last(v), ref, qual, "arg_ref")
        # names given as strings
        if last in IMPORTERS and node.args and not isinstance(node.args[0], ast.Constant):
            parts = _const_parts(node.args[0])
            if not parts and isinstance(node.args[0], ast.Name):     # module_path = f"..." assigned just above
                parts = self.string_of(node.args[0].id)
            names = self.getattr_names()
            if parts:
                self.out["dynamic"].append([node.lineno, parts, names])
        for v in values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str) and re.fullmatch(r"[\w.]+:\w+", v.value):
                self.out["strings"].append([node.lineno, v.value.split(":")[0]])
            if last in IMPORTERS and isinstance(v, ast.Constant) and isinstance(v.value, str):
                self.out["strings"].append([node.lineno, v.value])

    def string_of(self, name: str) -> list[str]:
        for sub in ast.walk(self.tree):
            if isinstance(sub, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in sub.targets):
                parts = _const_parts(sub.value)
                if parts:
                    return parts
        return []

    def getattr_names(self) -> list[str]:
        names = []
        for sub in ast.walk(self.tree):
            if isinstance(sub, ast.Call) and _last(sub.func) == "getattr" and len(sub.args) > 1 \
                    and isinstance(sub.args[1], ast.Constant) and isinstance(sub.args[1].value, str):
                names.append(sub.args[1].value)
        return sorted(set(names))

    # --- tier signals -----------------------------------------------------------------------------
    def signal(self, tier: str, line: int, what: str, sure: bool = False) -> None:
        for key in ("signals", "sure") if sure else ("signals",):
            old = self.out[key].get(tier)
            if old is None or line < old[0]:
                self.out[key][tier] = [line, what]

    def call_signals(self, node: ast.Call, last: str, lib: str | None, text: str) -> None:
        if last == "FastAPI" and lib == "fastapi":
            self.signal("entry", node.lineno, "FastAPI(", sure=True)
        elif last == "run" and lib == "uvicorn":
            self.signal("entry", node.lineno, "uvicorn.run(")
        elif last == "add_job":
            self.signal("entry", node.lineno, "add_job(")
        elif last in {"APIRouter", "include_router", "add_api_route"} or (lib == "sqladmin" and last == "Admin") \
                or (lib == "socketio" and last in {"AsyncServer", "Server"}):
            self.signal("api", node.lineno, last, sure=last == "include_router")
        elif last in {"select", "insert", "update", "delete"} and lib in {"sqlalchemy", "sqlmodel"}:
            self.signal("data", node.lineno, last)
        if lib in IO_LIBS:
            kind, opens = IO_LIBS[lib]
            if opens is None or last in opens:
                self.out["io"].append([node.lineno, lib, kind])
                if kind != "monitoring":
                    self.signal("infra", node.lineno, f"{lib}.{last}",
                                sure=kind == "database" and last in {"create_engine", "create_async_engine"})

    def function_signals(self, node, body: list) -> None:
        for dec in node.decorator_list:
            last = _last(dec)
            root = _root(dec)
            root_lib = self.env.get(root.id, {}).get("lib") if isinstance(root, ast.Name) else None
            if last in HTTP_VERBS and isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                self.signal("api", dec.lineno, f"@{ast.unparse(dec.func)}", sure=True)
            elif last in {"event", "on"} and (root_lib == "socketio" or "sio" in ast.unparse(dec)):
                self.signal("api", dec.lineno, f"@{last}")
            elif last in {"command", "group", "callback"} and (root_lib in CLI_LIBS or self.libs & CLI_LIBS):
                self.signal("entry", dec.lineno, f"@{last}")
        if isinstance(node, ast.AsyncFunctionDef):
            for sub in body:
                if isinstance(sub, ast.While) and not (isinstance(sub.test, ast.Constant) and not sub.test.value):
                    waits = [c for c in ast.walk(sub) if isinstance(c, ast.Await) and isinstance(c.value, ast.Call)
                             and _last(c.value.func) in {"sleep", "wait_for", "wait"}]
                    if waits:
                        self.signal("entry", sub.lineno, "vòng nền")

    def class_signals(self, node: ast.ClassDef) -> None:
        for item in node.body:
            if isinstance(item, (ast.Assign, ast.AnnAssign)):
                targets = item.targets if isinstance(item, ast.Assign) else [item.target]
                if any(isinstance(t, ast.Name) and t.id == "__tablename__" for t in targets):
                    self.signal("data", node.lineno, "__tablename__", sure=True)
        if any(k.arg == "table" for k in node.keywords):
            self.signal("data", node.lineno, "table=True", sure=True)
        base_names = [_last(b) for b in node.bases]
        if any(b.endswith("Middleware") for b in base_names):
            self.signal("entry", node.lineno, "middleware")
        if any(b == "ModelView" for b in base_names):
            self.signal("api", node.lineno, "ModelView")
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [a.arg for a in item.args.args]
                if (item.name == "__call__" and params[1:4] == ["scope", "receive", "send"]) or \
                        (item.name == "dispatch" and "call_next" in params):
                    self.signal("entry", node.lineno, "middleware")


def facts(idx: dict) -> dict:
    out = {}
    for path, entry in idx.items():
        if entry.get("error") or entry.get("empty"):
            continue
        tree = ast.parse("\n".join(entry["lines"]), filename=path)
        out[path] = _File(path, entry, tree).run()
    for f in out.values():
        for name, rec in f["funcs"].items():
            rec["calls"] = sorted(rec["calls"])
    return out
