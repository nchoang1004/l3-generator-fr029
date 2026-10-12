"""CMP-004: facts read from the Python syntax tree (API-004).

Covers FastAPI routes (with `include_router`, `mount`, app factories and `if` conditions), Pydantic request/response
models, SQLAlchemy/SQLModel tables, Kafka/FastStream events, httpx/requests calls, environment config, libraries
from manifests, and call references. Name resolution comes from `pyindex` (ported from l3gen 0.1).
Nothing is imported or executed. Values the tree does not show stay `unknown` with a reason; a value taken from a
documented framework default is marked `inferred` and its rule is named in `confidence_reason`.
"""
from __future__ import annotations

import ast
import re
import tomllib

from .common import SCHEMA_VERSION, compact, has_secret, is_known, known, not_applicable, sha, unknown
from .pyindex import FUNCS, Ref, Resolver, annotation_name, depends_target, dotted

EXTRACTOR_VERSION = "slice-ast-v4"
VERBS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
FASTAPI = {"fastapi.FastAPI", "fastapi.applications.FastAPI"}
ROUTER = {"fastapi.APIRouter", "fastapi.routing.APIRouter"}
ENGINE_FACTORIES = {"sqlalchemy.create_engine", "sqlalchemy.engine.create_engine", "sqlmodel.create_engine"}
BASE_FACTORIES = {"sqlalchemy.orm.declarative_base", "sqlalchemy.ext.declarative.declarative_base"}
BASE_CLASSES = {"sqlalchemy.orm.DeclarativeBase", "sqlalchemy.orm.decl_api.DeclarativeBase"}
SQLMODEL = "sqlmodel.SQLModel"
PYDANTIC = {"pydantic.BaseModel", "pydantic.main.BaseModel", SQLMODEL}
SETTINGS = {"pydantic_settings.BaseSettings", "pydantic.BaseSettings"}
COLUMN = {"sqlalchemy.Column", "sqlalchemy.schema.Column", "sqlalchemy.sql.schema.Column"}
MAPPED_COLUMN = {"sqlalchemy.orm.mapped_column"}
COMPOSITE = {"sqlalchemy.orm.composite"}
FIELD = {"sqlmodel.Field"}
NOT_COLUMNS = {"sqlalchemy.orm.relationship", "sqlmodel.Relationship"}
PARAM_SOURCES = {"Query": "query", "Path": "path", "Header": "header", "Cookie": "cookie", "Body": "body",
                 "Form": "body", "File": "body"}
SPECIAL_PARAMS = {"fastapi.Request", "fastapi.Response", "fastapi.BackgroundTasks", "starlette.requests.Request",
                  "fastapi.WebSocket", "sqlalchemy.orm.Session", "sqlmodel.Session"}
HTTP_LIBS = {"httpx", "requests", "aiohttp"}
HTTP_CLIENTS = {"httpx.Client", "httpx.AsyncClient", "requests.Session", "requests.session", "aiohttp.ClientSession"}
UNSUPPORTED_HTTP = {"urllib.request", "http.client", "urllib3", "httpcore", "pycurl", "treq", "niquests",
                    "grequests", "tornado.httpclient"}
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}
KAFKA_PRODUCERS = {"kafka.KafkaProducer", "aiokafka.AIOKafkaProducer", "confluent_kafka.Producer"}
KAFKA_CONSUMERS = {"kafka.KafkaConsumer", "aiokafka.AIOKafkaConsumer", "confluent_kafka.Consumer"}
FASTSTREAM_BROKERS = {"faststream.kafka.KafkaBroker", "faststream.rabbit.RabbitBroker", "faststream.redis.RedisBroker",
                      "faststream.nats.NatsBroker"}
SECRET_NAME = re.compile(r"(secret|password|passwd|token|api_key|apikey|private_key|credential)", re.I)

# Rule `sqlalchemy-type-v1`: SQLAlchemy / Python type -> SQL type token, only once the dialect is proven.
SQL_TYPES = {
    "sqlite": {"Integer": "INTEGER", "BigInteger": "INTEGER", "SmallInteger": "INTEGER", "String": "TEXT",
               "Text": "TEXT", "Unicode": "TEXT", "AutoString": "TEXT", "Float": "REAL", "LargeBinary": "BLOB",
               "int": "INTEGER", "str": "TEXT", "float": "REAL", "bytes": "BLOB"},
    "postgresql": {"Integer": "INTEGER", "BigInteger": "BIGINT", "SmallInteger": "SMALLINT", "String": "TEXT",
                   "Text": "TEXT", "Unicode": "TEXT", "AutoString": "TEXT", "Float": "DOUBLE PRECISION",
                   "Boolean": "BOOLEAN", "Date": "DATE", "DateTime": "TIMESTAMP WITHOUT TIME ZONE",
                   "LargeBinary": "BYTEA", "int": "INTEGER", "str": "TEXT", "float": "DOUBLE PRECISION",
                   "bool": "BOOLEAN", "date": "DATE", "datetime": "TIMESTAMP WITHOUT TIME ZONE", "bytes": "BYTEA"},
}
PARAM_TYPES = {"postgresql": {"String": "VARCHAR", "Unicode": "VARCHAR", "Numeric": "NUMERIC"}}
JSON_TYPES = {"int": "integer", "float": "number", "str": "string", "bool": "boolean", "bytes": "string",
              "datetime": "string", "date": "string", "UUID": "string", "Decimal": "number", "dict": "object",
              "EmailStr": "string"}
JSON_FORMATS = {"datetime": "date-time", "date": "date", "UUID": "uuid", "EmailStr": "email"}  # JSON Schema formats
TEXT_MANIFESTS = re.compile(r"(^|/)(pyproject\.toml|requirements[^/]*\.txt)$")


def _literal(node):
    return node.value if isinstance(node, ast.Constant) else None


def _keyword(call, name: str):
    if not isinstance(call, ast.Call):
        return None
    return next((k.value for k in call.keywords if k.arg == name), None)


def _text(node):
    """(text, is_literal). Non-literal parts are kept as `{expr}`, never guessed."""
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value, True
    if isinstance(node, ast.JoinedStr):
        out, literal = "", True
        for v in node.values:
            if isinstance(v, ast.Constant):
                out += str(v.value)
            else:
                out += "{" + ast.unparse(v.value) + "}"
                literal = False
        return out, literal
    return "{" + ast.unparse(node) + "}", False


class _Builder:
    def __init__(self, snapshot: dict, unit_id: str, sources: dict[str, bytes] | None = None):
        self.snap = snapshot["snapshot_id"]
        self.unit_id = unit_id
        self.files = {f["path"]: f for f in snapshot["files"]}
        self.lines = {p: raw.decode("utf-8", errors="replace").splitlines() for p, raw in (sources or {}).items()}
        self.facts, self.limitations = [], []

    def evidence(self, path: str, start: int, end: int, start_col: int | None = None, end_col: int | None = None) -> dict:
        f = self.files[path]
        return {"id": "ev:" + sha(compact([self.snap, path, start, start_col, end, end_col]).encode()),
                "snapshot_id": self.snap, "file_id": f["file_id"], "path": path, "sha256": f["sha256"],
                "start_line": start, "end_line": end, "start_column": start_col, "end_column": end_col}

    def node_evidence(self, path: str, node: ast.AST) -> dict:
        """Evidence for exactly one syntax node. `ast` columns are UTF-8 byte offsets; API-002 wants code points."""
        def cp(line_no: int, byte_col: int) -> int:
            return len(self.lines[path][line_no - 1].encode("utf-8")[:byte_col].decode("utf-8", errors="replace"))
        return self.evidence(path, node.lineno, node.end_lineno,
                             cp(node.lineno, node.col_offset), cp(node.end_lineno, node.end_col_offset))

    def span(self, path: str, node: ast.AST) -> dict:
        return self.evidence(path, node.lineno, node.end_lineno)

    def fact(self, kind: str, ev: dict, semantic_key: str, attributes: dict, extra_evidence=()) -> dict:
        ident = "fact:" + sha(compact([self.snap, ev["path"], kind, ev["start_line"], ev["start_column"], ev["end_line"],
                                       ev["end_column"], semantic_key]).encode())
        evidence = {ev["id"]: ev}
        for e in extra_evidence:
            evidence.setdefault(e["id"], e)
        fact = {"id": ident, "unit_id": self.unit_id, "kind": kind, "attributes": attributes,
                "evidence": list(evidence.values()), "resolution": "not_applicable", "target_fact_ids": [],
                "confidence": "exact", "completeness": "full"}
        self.facts.append(fact)
        return fact

    def limit(self, code: str, message: str, affected: list[str], stage="extraction"):
        self.limitations.append({"code": code, "message": message, "stage": stage, "affected_ids": affected})


def _finish(fact: dict, inferred=()):
    """Set completeness/confidence from the attributes; partial and inferred always carry a reason."""
    gaps = sorted(k for k, v in fact["attributes"].items() if isinstance(v, dict) and v.get("state") == "unknown")
    if gaps:
        fact["completeness"] = "partial"
        fact["completeness_reason"] = "Trường chưa xác định: " + ", ".join(gaps)
    if inferred:
        fact["confidence"] = "inferred"
        fact["confidence_reason"] = "; ".join(sorted(set(inferred)))


# ---------------------------------------------------------------- tree helpers

def _parents(tree) -> dict:
    out = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            out[child] = node
    return out


def _enclosing(node, parents) -> tuple[ast.AST | None, list[str]]:
    """(innermost enclosing function, conditions of enclosing `if` statements, outermost first)."""
    conds, func, cur = [], None, node
    while cur in parents:
        parent = parents[cur]
        if isinstance(parent, ast.If) and cur in parent.body:
            conds.append(ast.unparse(parent.test))
        elif isinstance(parent, ast.If) and cur in parent.orelse:
            conds.append(f"not ({ast.unparse(parent.test)})")
        if func is None and isinstance(parent, FUNCS):
            func = parent
        cur = parent
    return func, list(reversed(conds))


def _def_paths(tree) -> dict:
    """Every class/function node -> dotted local name (`create_app`, `Cls.method`, `outer.inner`)."""
    out = {}

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, *FUNCS)):
                name = prefix + child.name
                out[child] = name
                visit(child, name + ".")
            else:
                visit(child, prefix)
    visit(tree, "")
    return out


class _File:
    """Per-file helpers computed once."""

    def __init__(self, path, tree, r: Resolver):
        self.path, self.tree, self.scope = path, tree, r.scopes[path]
        self.module = r.module_of[path]
        self.prefix = f"{self.module}." if self.module else ""
        self.parents = _parents(tree)
        self.defs = _def_paths(tree)


# ---------------------------------------------------------------- symbols

def _symbols(b: _Builder, r: Resolver, files: dict) -> dict[str, dict]:
    """One symbol fact per module, class, function, method and nested function (`outer.inner`, golden D20)."""
    out = {}
    for path, f in files.items():
        n_lines = len(b.lines.get(path, []))
        if n_lines:
            ev = b.evidence(path, 1, n_lines)
            q = f"{f.prefix}__module__"
            out[q] = b.fact("symbol", ev, q, {"name": known(q, ev["id"]), "local_name": known("__module__", ev["id"]),
                                              "symbol_kind": known("module", ev["id"]),
                                              "signature": not_applicable("Module không có chữ ký")})
        for node, local in f.defs.items():
            ev = b.span(path, node)
            q = f"{f.prefix}{local}"
            kind = "class" if isinstance(node, ast.ClassDef) else "function"
            sig = known(f"({ast.unparse(node.args)})", ev["id"]) if isinstance(node, FUNCS) else not_applicable("Class")
            out[q] = b.fact("symbol", ev, q, {"name": known(q, ev["id"]), "local_name": known(local, ev["id"]),
                                              "symbol_kind": known(kind, ev["id"]), "signature": sig})
    return out


# ---------------------------------------------------------------- routes

def _field_default(r: Resolver, cls: str, field: str, depth=0):
    """(path, literal node) of `field: str = "..."` in `cls` or its repository bases, nearest first."""
    rec = r.classes.get(cls)
    if rec is None or depth > 10:
        return None
    for stmt in rec.node.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == field:
            ok = isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str)
            return (rec.path, stmt.value) if ok else None
    return next((d for b in r.bases_of(rec) for d in [_field_default(r, b, field, depth + 1)] if d), None)


def _settings_default(r: Resolver, f, node):
    """`settings.API_V1_STR` where `settings = Settings()` (or `settings = get_settings()` with a return annotation
    naming the Settings class), module level or local to the function, and `class Settings(BaseSettings)` declares
    `API_V1_STR: str = "/api/v1"` -> (path of the class, the literal node). Refused when a repository subclass of
    that class declares the field with another value. An environment variable can override the value at run time,
    so the result is inferred (settings-default-v1)."""
    if not (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)):
        return None
    name, value, scope = node.value.id, None, f.scope
    func, _ = _enclosing(node, f.parents)
    if func is not None:
        value = next((s.value for s in ast.walk(func) if isinstance(s, ast.Assign) and len(s.targets) == 1
                      and isinstance(s.targets[0], ast.Name) and s.targets[0].id == name), None)
    if value is None:
        q = r.qualify(scope, name)
        if q in r.assigns:
            path, value = r.assigns[q]
            scope = r.scopes[path]
    if not (isinstance(value, ast.Call) and not value.args and not value.keywords):
        return None
    cls = r.qual_node(scope, value.func)
    d = r.defs.get(cls)
    if d is not None and d.kind == "function":  # a factory: the class its return annotation names
        cls = r.resolve_type(r.scopes[d.path], annotation_name(d.node.returns))
    if cls not in r.classes or not r.subclass_of(cls, SETTINGS):
        return None
    found = _field_default(r, cls, node.attr)
    if found is None:
        return None
    for sub in r.classes:
        if sub != cls and r.subclass_of(sub, {cls}):
            other = _field_default(r, sub, node.attr)
            if other is None or other[1].value != found[1].value:
                return None
    return found


class _Routers:
    """FastAPI()/APIRouter() objects, module-level or local to an app factory (golden D21: `file::func.var`)."""

    def __init__(self, b: _Builder, r: Resolver, files: dict):
        self.b, self.r, self.files = b, r, files
        self.objs, self.local, self.mounts = {}, {}, []
        for path, f in files.items():
            for node in ast.walk(f.tree):
                if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                        and isinstance(node.value, ast.Call)):
                    continue
                q = r.qual_node(f.scope, node.value.func)
                if q not in FASTAPI | ROUTER:
                    continue
                func, _ = _enclosing(node, f.parents)
                var = node.targets[0].id
                local = var if func is None else f"{f.defs[func]}.{var}"
                key = f"{path}::{local}"
                prefix = _keyword(node.value, "prefix") if q in ROUTER else None
                self.objs[key] = {"path": path, "local": local, "is_app": q in FASTAPI,
                                  "qname": f"{f.prefix}{var}" if func is None else None,
                                  "prefix": _text(prefix), "prefix_ev": b.node_evidence(path, prefix) if prefix else None,
                                  "ev": b.span(path, node)}
                if func is not None:
                    self.local.setdefault((path, func), {})[var] = key
        for path, f in files.items():
            for node in ast.walk(f.tree):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr in ("include_router", "mount")):
                    continue
                func, conds = _enclosing(node, f.parents)
                if node.func.attr == "include_router":
                    child_node = node.args[0] if node.args else _keyword(node, "router")
                    prefix = _keyword(node, "prefix")
                else:
                    child_node = node.args[1] if len(node.args) > 1 else _keyword(node, "app")
                    prefix = node.args[0] if node.args else _keyword(node, "path")
                for site in self._sites(path, func, [node.func.value, child_node, prefix]):
                    (p_path, p_func, p_node), (c_path, c_func, c_node), (x_path, _, x_node), extra_conds, site_ev = site
                    parent = self.key(p_path, p_func, p_node)
                    child = self.key(c_path, c_func, c_node) if c_node is not None else None
                    if parent and child:
                        evs = [b.span(path, node)] + ([site_ev] if site_ev else [])
                        site_main = evs[-1]
                        text, text_ev, rule = _text(x_node), None, None
                        if x_node is not None and not text[1]:
                            default = _settings_default(r, files[x_path], x_node)
                            if default is not None:  # settings-default-v1: the literal is where the field is declared
                                text, rule = (default[1].value, True), "settings-default-v1"
                                text_ev = b.node_evidence(default[0], default[1])
                                evs.append(b.node_evidence(x_path, x_node))
                        self.mounts.append({"parent": parent, "child": child, "prefix": text, "rule": rule,
                                            "prefix_ev": text_ev or (b.node_evidence(x_path, x_node) if x_node is not None else None),
                                            "conds": extra_conds + conds, "ev": site_main, "evs": evs})

    def _sites(self, path, func, nodes):
        """Where each expression really comes from. Plain case: here. When the expressions are parameters of a
        module-level function, each call site of that function supplies the arguments instead."""
        params = [a.arg for a in [*func.args.posonlyargs, *func.args.args]] if func is not None else []
        if func is None or not any(isinstance(n, ast.Name) and n.id in params for n in nodes if n is not None):
            yield tuple((path, func, n) for n in nodes) + ([], None)
            return
        f = self.files[path]
        target_q = f"{f.prefix}{f.defs[func]}"
        for c_path, cf in self.files.items():
            for call in ast.walk(cf.tree):
                if not isinstance(call, ast.Call) or self.r.qual_node(cf.scope, call.func) != target_q:
                    continue
                c_func, c_conds = _enclosing(call, cf.parents)
                args = dict(zip(params, call.args))
                args.update({k.arg: k.value for k in call.keywords if k.arg})
                resolved = []
                for n in nodes:
                    if isinstance(n, ast.Name) and n.id in params:
                        resolved.append((c_path, c_func, args.get(n.id)))
                    else:
                        resolved.append((path, func, n))
                yield tuple(resolved) + (c_conds, self.b.span(c_path, call))

    def key(self, path, func, node) -> str | None:
        name = dotted(node)
        if name is None:
            return None
        f = self.files[path]
        cur = func
        while cur is not None:
            local = self.local.get((path, cur), {})
            if name in local:
                return local[name]
            cur, _ = _enclosing(cur, f.parents)
        q = self.r.qualify(f.scope, name)
        return next((k for k, o in self.objs.items() if o["qname"] is not None and o["qname"] == q), None)

    def chains(self, key, depth=0, seen=frozenset()):
        """Every path from an application down to `key`: list of (keys app..key, mounts app..key)."""
        if depth > 10 or key in seen:
            return []
        ups = [m for m in self.mounts if m["child"] == key]
        if not ups:
            return [([key], [])] if self.objs[key]["is_app"] else []
        out = []
        for m in ups:
            for keys, mounts in self.chains(m["parent"], depth + 1, seen | {key}):
                out.append((keys + [key], mounts + [m]))
        return out


def _route_decorators(func, f: _File, routers: _Routers):
    """(router key, [methods], path node, decorator call, method evidence node) for each route decorator."""
    out = []
    outer, _ = _enclosing(func, f.parents)
    for dec in func.decorator_list:
        if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)):
            continue
        key = routers.key(f.path, outer, dec.func.value)
        if key is None:
            continue
        attr = dec.func.attr
        path_node = dec.args[0] if dec.args else _keyword(dec, "path")
        if attr in VERBS and path_node is not None:
            out.append((key, [attr.upper()], path_node, dec, dec.func))
        elif attr == "api_route" and path_node is not None:
            methods = _keyword(dec, "methods")
            names = [m.value.upper() for m in getattr(methods, "elts", []) if isinstance(_literal(m), str)]
            out.append((key, names or ["GET"], path_node, dec, methods if methods is not None else dec.func))
    return out


def _schema_of(node, r: Resolver, scope, models: dict):
    """(JSON schema | None, nullable, reason when unknown) for a type annotation."""
    if node is None:
        return None, False, "Không có chú thích kiểu"
    nullable = False
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        sides = [s for s in (node.left, node.right) if not (isinstance(s, ast.Constant) and s.value is None)]
        nullable = len(sides) < 2
        if len(sides) != 1:
            return None, nullable, "Kiểu hợp (union) nhiều nhánh chưa được biểu diễn"
        node = sides[0]
    if isinstance(node, ast.Subscript):
        head = (dotted(node.value) or "").split(".")[-1]
        inner = node.slice.elts[0] if isinstance(node.slice, ast.Tuple) else node.slice
        if head == "Optional":
            schema, _, why = _schema_of(inner, r, scope, models)
            return schema, True, why
        if head == "Annotated":
            return _schema_of(inner, r, scope, models)
        if head in ("tuple", "Tuple") and isinstance(node.slice, ast.Tuple) and not (
                len(node.slice.elts) == 2 and isinstance(node.slice.elts[1], ast.Constant) and node.slice.elts[1].value is Ellipsis):
            return None, nullable, f"Tuple nhiều kiểu {ast.unparse(node)} chưa được biểu diễn"
        if head in ("list", "List", "set", "Set", "tuple", "Tuple", "Sequence"):
            items, item_nullable, why = _schema_of(inner, r, scope, models)
            if items is not None and item_nullable:
                items = {"anyOf": [items, {"type": "null"}]}
            return ({"type": "array", "items": items} if items is not None else None), nullable, why
        if head in ("dict", "Dict"):
            return {"type": "object"}, nullable, None
        return None, nullable, f"Kiểu {ast.unparse(node)} chưa được biểu diễn"
    name = dotted(node)
    if name is None:
        return None, nullable, f"Kiểu {ast.unparse(node)} chưa được biểu diễn"
    q = r.resolve_type(scope, name) or name
    if q in models:
        return {"x-model-fact": models[q]}, nullable, None
    base = name.split(".")[-1]
    if base in JSON_TYPES:
        schema = {"type": JSON_TYPES[base]}
        if base in JSON_FORMATS:
            schema["format"] = JSON_FORMATS[base]
        return schema, nullable, None
    return None, nullable, f"Kiểu {name} chưa được biểu diễn"


def _is_model(q, r: Resolver) -> bool:
    return q is not None and q in r.classes and r.subclass_of(q, PYDANTIC)


class _NestedModels:
    """`models` for `_schema_of`: a repository Pydantic model used inside another one (`notes: list[NoteSchema]`)
    gets its own model fact on first use, so the field points at it instead of staying unknown."""

    def __init__(self, r: Resolver, make):
        self.r, self.make = r, make

    def __contains__(self, q):
        return _is_model(q, self.r)

    def __getitem__(self, q):
        return self.make(q)


def _model_fields(q, r: Resolver, b: _Builder, models: dict, depth=0):
    """Fields of a Pydantic model, inherited repository fields first. Returns (fields, evidence)."""
    rec = r.classes[q]
    scope = r.scopes[rec.path]
    fields, evidence = [], []
    if depth < 10:
        for base in r.bases_of(rec):
            if _is_model(base, r):
                bf, be = _model_fields(base, r, b, models, depth + 1)
                fields += bf
                evidence += be
    for stmt in rec.node.body:
        if not (isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name)):
            continue
        if (dotted(stmt.annotation) or "").split(".")[-1] == "ClassVar" or (
                isinstance(stmt.value, ast.Call) and r.qual_node(scope, stmt.value.func) in NOT_COLUMNS):
            continue
        ev, name_ev = b.span(rec.path, stmt), b.node_evidence(rec.path, stmt.target)
        evidence += [ev, name_ev]
        schema, nullable, why = _schema_of(stmt.annotation, r, scope, models)
        value = stmt.value
        if isinstance(value, ast.Call) and (dotted(value.func) or "").split(".")[-1] == "Field":
            default = value.args[0] if value.args else _keyword(value, "default")
            has_default = (default is not None and not (isinstance(default, ast.Constant) and default.value is Ellipsis)) \
                or _keyword(value, "default_factory") is not None
        else:
            has_default = value is not None and not (isinstance(value, ast.Constant) and value.value is Ellipsis)
        fields = [x for x in fields if x["name"]["value"] != stmt.target.id]
        fields.append({"name": known(stmt.target.id, name_ev["id"]),
                       "type": known(schema, ev["id"]) if schema is not None else unknown(why),
                       "required": known(not has_default, ev["id"]),
                       "nullable": known(nullable, ev["id"])})
    return fields, evidence


def _routes(b: _Builder, r: Resolver, files: dict, symbols: dict):
    routers = _Routers(b, r, files)
    model_facts = {}

    def model_fact(q, kind):
        if (q, kind) not in model_facts:
            rec = r.classes[q]
            ev = b.span(rec.path, rec.node)
            f = b.fact(kind, ev, f"{q}:{kind}", {"name": known(q, ev["id"])})
            model_facts[(q, kind)] = f
            fields, evs = _model_fields(q, r, b, _NestedModels(r, lambda m: model_fact(m, kind)["id"]))
            f["attributes"]["fields"] = known(fields, ev["id"])
            f["evidence"] += [e for e in {e["id"]: e for e in evs}.values() if e["id"] != ev["id"]]
            _finish(f)
        return model_facts[(q, kind)]

    for path, f in files.items():
        for func, local in f.defs.items():
            if not isinstance(func, FUNCS):
                continue
            decs = _route_decorators(func, f, routers)
            handler_q = f"{f.prefix}{local}"
            for key, methods, path_node, dec, method_node in decs:
                chains = routers.chains(key)
                if not chains:
                    # A router that is never attached to an application serves no route (golden orders-wrapper-fake).
                    b.limit("ROUTER_NOT_MOUNTED", f"{path}: {handler_q} khai trên router chưa được gắn vào application nào",
                            [symbols[handler_q]["id"]] if handler_q in symbols else [])
                    continue
                for method in methods:
                    for keys, mounts in chains:
                        _one_route(b, r, f, func, symbols.get(handler_q), handler_q, method, path_node, dec,
                                   method_node, keys, mounts, routers, model_fact)


def _one_route(b, r, f, func, handler, handler_q, method, path_node, dec, method_node, keys, mounts, routers, model_fact):
    path = f.path
    route_ev = b.evidence(path, dec.lineno, func.lineno)
    method_ev, path_ev = b.node_evidence(path, method_node), b.node_evidence(path, path_node)
    root = routers.objs[keys[0]]
    mounted = root["is_app"]
    pieces, path_evs, extra, inferred = [], [path_ev], [method_ev, path_ev], []
    for k, m in zip(keys, [None] + mounts):
        if m is not None:
            extra += m.get("evs", [m["ev"]])
        if m is not None and m["prefix"] is not None:
            pieces.append(m["prefix"])
            if m["prefix_ev"]:
                path_evs.append(m["prefix_ev"])
        o = routers.objs[k]
        extra.append(o["ev"])
        if o["prefix"] is not None:
            pieces.append(o["prefix"])
            if o["prefix_ev"]:
                path_evs.append(o["prefix_ev"])
    own = _text(path_node)
    pieces.append(own)
    extra += path_evs
    chain = "->".join(f"{routers.objs[k]['path']}::{routers.objs[k]['local']}" for k in keys)
    conds = [c for m in mounts for c in m["conds"]]
    attrs = {"method": known(method, method_ev["id"]), "handler": known(handler_q, route_ev["id"]),
             "declaration_evidence_id": known(route_ev["id"], route_ev["id"]),
             "registration_context": known(chain, *[routers.objs[k]["ev"]["id"] for k in keys]),
             "condition": known(" and ".join(conds), *[m["ev"]["id"] for m in mounts]) if conds
             else not_applicable("Không có điều kiện bao quanh lần đăng ký")}
    if handler is not None:
        attrs["handler_fact_id"] = known(handler["id"], route_ev["id"])
    attrs["application_id"] = known(f"app:{root['path']}::{root['local']}", root["ev"]["id"]) if mounted \
        else unknown("Router chưa được gắn vào application nào trong snapshot")
    literal_all = all(p[1] for p in pieces)
    full = _join([p[0] for p in pieces])
    if mounted and literal_all:
        attrs["path"] = known(full, *[e["id"] for e in path_evs])
    else:
        attrs["path"] = unknown("Router chưa được gắn vào application nào" if not mounted else
                                "Prefix phụ thuộc lúc chạy: " + ", ".join(p[0] for p in pieces if not p[1]))
        tail = []
        for p in reversed(pieces):
            if not p[1]:
                break
            tail.insert(0, p[0])
        if tail and (not mounted or not literal_all):
            attrs["path_suffix"] = known(_join(tail), path_ev["id"])
    ruled = [m for m in mounts if m.get("rule")]
    if ruled and is_known(attrs["path"]):
        attrs["prefix_rule"] = known("settings-default-v1", *[m["prefix_ev"]["id"] for m in ruled])
        inferred.append("settings-default-v1: prefix là giá trị mặc định khai trong class Settings; biến môi trường "
                        "có thể ghi đè lúc chạy")
    status = _keyword(dec, "status_code")
    constant = re.fullmatch(r"(?:fastapi|starlette)\.status\.HTTP_(\d{3})_\w+", r.qual_node(f.scope, status) or "")
    if isinstance(_literal(status), int):
        status_ev = b.node_evidence(path, status)
        extra.append(status_ev)
        attrs["status_codes"] = known([_literal(status)], status_ev["id"])
    elif constant:
        status_ev = b.node_evidence(path, status)
        extra.append(status_ev)
        attrs["status_codes"] = known([int(constant.group(1))], status_ev["id"])
        attrs["status_rule"] = known("starlette-status-constant-v1", status_ev["id"])
        inferred.append("starlette-status-constant-v1: status lấy từ tên hằng HTTP_<mã>_… của starlette/fastapi")
    elif status is None:
        attrs["status_codes"] = known([200], route_ev["id"])
        attrs["status_rule"] = known("fastapi-status-default-v1", route_ev["id"])
        inferred.append("fastapi-status-default-v1: decorator không khai status_code, FastAPI trả 200")
    else:
        attrs["status_codes"] = unknown("status_code không phải literal hay hằng HTTP_<mã>; không suy")
    params, request_models, depends, param_evs, param_problem = _parameters(b, r, f, func, full if literal_all else own[0])
    extra += param_evs
    attrs["parameters"] = unknown(param_problem) if param_problem else known(params, route_ev["id"])
    bodies = []
    for q, ev, required in request_models:
        mf = model_fact(q, "request_model")
        bodies.append({"direction": "request", "model_id": mf["id"], "status": None, "media_type": "application/json",
                       "required": required})
        extra.append(ev)
    attrs["request_model_ids"] = known([x["model_id"] for x in bodies], route_ev["id"])
    response_model = _keyword(dec, "response_model")
    resp_node = response_model if response_model is not None else func.returns
    array = isinstance(resp_node, ast.Subscript) and (
        (r.qual_node(f.scope, resp_node.value) or '') in {'typing.List', 'typing.Sequence', 'collections.abc.Sequence'}
        or (isinstance(resp_node.value, ast.Name) and resp_node.value.id in {'list', 'set'}
            and resp_node.value.id not in f.scope.names))
    model_node = resp_node.slice if array else resp_node
    resp_q = r.resolve_type(f.scope, annotation_name(model_node)) if model_node is not None else None
    if _is_model(resp_q, r):
        mf = model_fact(resp_q, "response_model")
        resp_ev = b.node_evidence(path, resp_node)
        code = attrs["status_codes"]["value"][0] if is_known(attrs["status_codes"]) else None
        bodies.append({"direction": "response", "model_id": mf["id"], "status": code, "media_type": "application/json",
                       "required": None})
        if array:
            bodies[-1]["array"] = True
        attrs["response_model_ids"] = known([mf["id"]], resp_ev["id"])
        extra.append(resp_ev)
        if response_model is None:
            inferred.append("fastapi-defaults-v1: kiểu trả về của handler là response model khi không khai response_model")
    elif resp_node is None or (isinstance(resp_node, ast.Constant) and resp_node.value is None):
        attrs["response_model_ids"] = known([], route_ev["id"])  # `-> None`: the route returns no body
    else:
        attrs["response_model_ids"] = unknown("Response model không phải Pydantic model trong repo: " + ast.unparse(resp_node))
    if bodies:
        attrs["bodies"] = known(bodies, route_ev["id"])
        inferred.append("fastapi-defaults-v1: body của Pydantic model dùng media type application/json")
    route_deps = [ast.unparse(depends_target(d) or d) for d in getattr(_keyword(dec, "dependencies"), "elts", [])
                  if _is_depends(d)]
    unread = [p["name"]["value"] for p in params if p["in"]["state"] == "unknown"]
    names = route_deps + depends
    if names or unread:
        attrs["auth"] = unknown("Có dependency " + ", ".join(dict.fromkeys(names)) + "; không kết luận cơ chế xác thực"
                                if names else "Tham số " + ", ".join(unread) + " có kiểu từ file không đọc được; "
                                "không kết luận xác thực")
    else:
        attrs["auth"] = unknown("Không thấy dependency; không kết luận route công khai")
    route = b.fact("route", route_ev, f"{chain}:{method}:{own[0]}", attrs, extra_evidence=extra)
    _finish(route, inferred)
    if mounted and not literal_all:
        b.limit("RUNTIME_DEPENDENT_PREFIX", attrs["path"]["reason"], [route["id"]])


def _join(parts: list[str]) -> str:
    segs = [p.strip("/") for p in parts if p.strip("/")]
    joined = "/" + "/".join(segs) if segs else "/"
    if parts and parts[-1].endswith("/") and joined != "/":
        joined += "/"
    return joined


def _is_depends(node) -> bool:
    return isinstance(node, ast.Call) and (dotted(node.func) or "").split(".")[-1] == "Depends"


def _dependency(r: Resolver, scope, ann, default):
    """The dependency a parameter asks for, or None when it is a plain parameter:
    (provider node or None when unreadable, scope of the provider). Forms: `= Depends(x)`, `= Depends()` (the
    annotated class), `Annotated[T, Depends(x)]`, and an alias `Dep = Annotated[T, Depends(x)]` from another file."""
    if isinstance(ann, ast.Subscript) and (dotted(ann.value) or "").endswith("Annotated") and isinstance(ann.slice, ast.Tuple):
        extra = next((e for e in ann.slice.elts[1:] if _is_depends(e)), None)
        if extra is not None:
            return (depends_target(extra) or ann.slice.elts[0]), scope
    if _is_depends(default):
        return (depends_target(default) or ann), scope
    q = r.qualify(scope, dotted(ann)) if isinstance(ann, (ast.Name, ast.Attribute)) else None
    if q in r.assigns:
        path, value = r.assigns[q]
        if isinstance(value, ast.Subscript) and (dotted(value.value) or "").endswith("Annotated") \
                and isinstance(value.slice, ast.Tuple):
            extra = next((e for e in value.slice.elts[1:] if _is_depends(e)), None)
            if extra is not None:
                return (depends_target(extra) or value.slice.elts[0]), r.scopes[path]
    return None


def _provider_function(r: Resolver, scope, node):
    """(path, function node) of a dependency provider written in the repository: a function, or a class (its
    `__init__`). None for a library provider or a factory call such as `Depends(get_repo(X))`."""
    q = r.qualify(scope, dotted(node)) if isinstance(node, (ast.Name, ast.Attribute)) else None
    d = r.defs.get(q) if q else None
    if d is not None and d.kind == "function":
        return d.path, d.node
    if d is not None and d.kind == "class":
        init = r.methods.get(q, {}).get("__init__")
        return (init.path, init.node) if init is not None else (d.path, None)
    return None


def _parameters(b, r, f: _File, func, route_path):
    """FastAPI rules: `{x}` in path -> path; `Query/Header/Cookie/Path(...)` -> that place; Pydantic model -> body;
    other simple types -> query. A dependency is not a parameter, but the parameters of a dependency written in the
    repository are parameters of the route (FastAPI collects them), up to 3 levels.
    Returns (params, models, dependency names, evidence, problem); `problem` makes the whole list unknown."""
    in_path = set(re.findall(r"{(\w+)(?::[^}]*)?}", route_path or ""))
    params, models, evs, opaque, deps = [], [], [], [], []

    def visit(path, fn, scope, depth, seen):
        args = fn.args
        positional = [*args.posonlyargs, *args.args]
        defaults = dict(zip([a.arg for a in positional[len(positional) - len(args.defaults):]], args.defaults))
        defaults.update({a.arg: d for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is not None})
        for a in [*positional, *args.kwonlyargs]:
            if a.arg in ("self", "cls") or a.arg in {p["name"]["value"] for p in params}:
                continue
            default, ann = defaults.get(a.arg), a.annotation
            dep = _dependency(r, scope, ann, default)
            if dep is not None:
                deps.append(ast.unparse(dep[0]) if dep[0] is not None else a.arg)
                found = _provider_function(r, dep[1], dep[0])
                key = found and (found[0], id(found[1]))
                if found and found[1] is not None and depth < 3 and key not in seen:
                    visit(found[0], found[1], r.scopes[found[0]], depth + 1, seen | {key})
                elif not found or found[1] is None:  # library provider, factory call, or class without __init__
                    opaque.append(ast.unparse(dep[0]) if dep[0] is not None else a.arg)
                continue
            if isinstance(ann, ast.Subscript) and (dotted(ann.value) or "").endswith("Annotated") \
                    and isinstance(ann.slice, ast.Tuple) and isinstance(ann.slice.elts[-1], ast.Call):
                default = ann.slice.elts[-1] if default is None else default
            q = r.resolve_type(scope, annotation_name(ann))
            if q in SPECIAL_PARAMS:
                continue
            ev = b.node_evidence(path, a)
            unread = r.unreadable_origin(r.qualify(scope, annotation_name(ann)))
            source = PARAM_SOURCES.get((dotted(default.func) or "").split(".")[-1]) if isinstance(default, ast.Call) else None
            if source is None:
                source = "path" if a.arg in in_path else ("body" if _is_model(q, r) else "query")
            if isinstance(default, ast.Call):
                first = default.args[0] if default.args else _keyword(default, "default")
                has_default = first is not None and not (isinstance(first, ast.Constant) and first.value is Ellipsis)
            else:
                has_default = default is not None
            if source == "body" and not unread:
                if _is_model(q, r):
                    models.append((q, ev, not has_default))  # fastapi-defaults-v1: a body without default is required
                continue
            schema, nullable, why = _schema_of(ann, r, scope, {})
            if schema is not None and nullable:
                schema = {"anyOf": [schema, {"type": "null"}]}
            where = known(source, ev["id"])
            if unread and a.arg not in in_path and not isinstance(default, ast.Call):
                where = unknown(f"Kiểu {annotation_name(ann)} khai ở file không đọc được ({unread}); "
                                "chưa biết là tham số hay dependency")
            params.append({"name": known(a.arg, ev["id"]), "in": where,
                           "required": known(source == "path" or not has_default, ev["id"]),
                           "schema": known(schema, ev["id"]) if schema is not None else unknown(why)})
            evs.append(ev)

    visit(f.path, func, f.scope, 0, frozenset())
    missing = sorted(in_path - {p["name"]["value"] for p in params if is_known(p["in"]) and p["in"]["value"] == "path"})
    problem = None
    if missing:
        problem = (f"Tham số path {', '.join(missing)} không thấy trong handler hay dependency đọc được"
                   + (f" (dependency không đọc được: {', '.join(opaque)})" if opaque else ""))
    return params, models, deps, evs, problem


# ---------------------------------------------------------------- tables

def _sql_bindings(b: _Builder, r: Resolver, files: dict) -> dict:
    """Declarative base -> [(dialect, evidence)] proven by `<Base>.metadata.create_all(<engine>)`."""
    engines, bases = {}, set()
    for path, f in files.items():
        for node in f.tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                    and isinstance(node.value, ast.Call):
                func = r.qual_node(f.scope, node.value.func)
                url = _literal(node.value.args[0]) if node.value.args else None
                if func in ENGINE_FACTORIES and isinstance(url, str) and ":" in url:
                    engines[f.prefix + node.targets[0].id] = (url.split(":", 1)[0].split("+", 1)[0], b.span(path, node))
                elif func in BASE_FACTORIES:
                    bases.add(f.prefix + node.targets[0].id)
    bases |= {q for q in r.classes if r.subclass_of(q, BASE_CLASSES) and not any(
        isinstance(s, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__tablename__" for t in s.targets)
        for s in r.classes[q].node.body) and set(r.bases_of(r.classes[q])) & BASE_CLASSES}
    bindings = {}
    for path, f in files.items():
        for node in ast.walk(f.tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "create_all"
                    and isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "metadata"):
                continue
            base = r.qual_node(f.scope, node.func.value.value)
            arg = node.args[0] if node.args else _keyword(node, "bind")
            engine = r.qual_node(f.scope, arg) if arg is not None else None
            if (base in bases or base == SQLMODEL) and engine in engines:
                dialect, engine_ev = engines[engine]
                bindings.setdefault(base, []).append((dialect, [b.span(path, node), engine_ev]))
    return {"bases": bases, "bindings": bindings}


def _table_classes(r: Resolver, sql: dict):
    """(qname, orm, base) for classes that map to a table."""
    for q, rec in r.classes.items():
        if q in sql["bases"]:
            continue
        if any(isinstance(s, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__abstract__" for t in s.targets)
               and _literal(s.value) is True for s in rec.node.body):
            continue
        if any(k.arg == "table" and _literal(k.value) is True for k in rec.node.keywords) and r.subclass_of(q, {SQLMODEL}):
            yield q, "sqlmodel", SQLMODEL
            continue
        base = next((x for x in sql["bases"] if r.subclass_of(q, {x})), None)
        if base is not None:
            yield q, "sqlalchemy", base


def _tables(b: _Builder, r: Resolver, files: dict) -> set[str]:
    sql = _sql_bindings(b, r, files)
    found_tables, named = set(), {}
    for q, orm, base in _table_classes(r, sql):
        rec = r.classes[q]
        path, node, scope = rec.path, rec.node, r.scopes[rec.path]
        decl_ev = b.span(path, node)
        evidence, inferred = [], []
        name_stmt = next((s for s in node.body if isinstance(s, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__tablename__" for t in s.targets)), None)
        attrs = {"declaration_evidence_id": known(decl_ev["id"], decl_ev["id"]),
                 "class_name": known(node.name, decl_ev["id"])}
        if name_stmt is not None and isinstance(_literal(name_stmt.value), str):
            name_ev = b.node_evidence(path, name_stmt.value)
            evidence.append(name_ev)
            attrs["name"] = known(name_stmt.value.value, name_ev["id"])
        elif name_stmt is not None:
            attrs["name"] = unknown("__tablename__ không phải literal")
        elif orm == "sqlmodel":
            name_ev = b.evidence(path, node.lineno, node.lineno)
            evidence.append(name_ev)
            attrs["name"] = known(node.name.lower(), name_ev["id"])
            attrs["name_rule"] = known("sqlmodel-default-tablename-v1", name_ev["id"])
            inferred.append("sqlmodel-default-tablename-v1: không khai __tablename__, SQLModel dùng tên class viết thường")
        else:
            attrs["name"] = unknown("Không có __tablename__ literal; tên bảng do code tính lúc import, không tự suy")
        table_args = next((s.value for s in node.body if isinstance(s, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__table_args__" for t in s.targets)), None)
        if _table_constraints(table_args):  # multi-column unique / index / check written in __table_args__
            attrs["table_constraints"] = known(_table_constraints(table_args), decl_ev["id"])
        bound = sql["bindings"].get(base, [])
        if len({d for d, _ in bound}) == 1:
            dialect = bound[0][0]
            proof = {e["id"]: e for _, evs in bound for e in evs}
            attrs["dialect"] = known(dialect, *proof)
            evidence += list(proof.values())
        else:
            dialect = None
            attrs["dialect"] = unknown("Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal"
                                       if not bound else "Base được nối với nhiều dialect khác nhau")
        columns = []
        for owner in _column_owners(q, r, sql):
            o = r.classes[owner]
            for stmt in o.node.body:
                for part in _composite_parts(stmt, r.scopes[o.path], r) or [stmt]:
                    col = _column(part, o.path, r.scopes[o.path], r, b, dialect, orm, inferred)
                    if col is not None:
                        columns = [c for c in columns if c["name"]["value"] != col[0]["name"]["value"]] + [col[0]]
                        evidence += col[1]
        attrs["columns"] = known(columns, decl_ev["id"])
        fact = b.fact("table", decl_ev, q, attrs, extra_evidence=evidence)
        gaps = sorted({k for k, v in attrs.items() if v["state"] == "unknown"} |
                      {f"columns.{c['name']['value']}.{k}" for c in columns for k, v in c.items() if v["state"] == "unknown"})
        if gaps:
            fact["completeness"], fact["completeness_reason"] = "partial", "Trường chưa xác định: " + ", ".join(gaps)
        if inferred:
            fact["confidence"], fact["confidence_reason"] = "inferred", "; ".join(sorted(set(inferred)))
        found_tables.add(q)
        named.setdefault(attrs["name"].get("value"), []).append((q, fact))
    for name, group in named.items():  # class TaskExtended(Task): same __tablename__ (extend_existing): one table,
        for q, fact in group:          # described by the subclass, which already holds the base's columns
            if name and any(o != q and r.subclass_of(o, {q}) for o, _ in group):
                b.facts.remove(fact)
                found_tables.discard(q)
    return found_tables


def _named_column(arg, func, args, keywords, name_node):
    """`x = Column(...)` built from a column call that carries its name as first argument, located like the call."""
    fake = ast.Assign(targets=[ast.Name(id=name_node.value, ctx=ast.Store())],
                      value=ast.Call(func=func, args=args, keywords=keywords))
    ast.copy_location(fake, arg)
    fake.end_lineno, fake.end_col_offset = arg.end_lineno, arg.end_col_offset
    ast.copy_location(fake.targets[0], name_node)
    fake.targets[0].end_lineno, fake.targets[0].end_col_offset = name_node.end_lineno, name_node.end_col_offset
    return fake


def _composite_parts(stmt, scope, r: Resolver) -> list:
    """`location: Mapped[Location] = composite(mapped_column("lat"), mapped_column("lng"))` -> columns lat, lng."""
    value = stmt.value if isinstance(stmt, (ast.Assign, ast.AnnAssign)) else None
    if not (isinstance(value, ast.Call) and r.qual_node(scope, value.func) in COMPOSITE):
        return []
    return [_named_column(a, a.func, a.args[1:], a.keywords, a.args[0]) for a in value.args
            if isinstance(a, ast.Call) and r.qual_node(scope, a.func) in COLUMN | MAPPED_COLUMN
            and a.args and isinstance(_literal(a.args[0]), str)]


def _column_owners(q, r: Resolver, sql: dict, depth=0) -> list[str]:
    """The class and its repository bases (mixins, SQLModel base models), base first so subclasses override."""
    out = []
    if depth < 10:
        for base in r.bases_of(r.classes[q]):
            if base in r.classes and base not in sql["bases"]:
                out += [x for x in _column_owners(base, r, sql, depth + 1) if x not in out]
    return out + [q]


def _table_variables(b: _Builder, r: Resolver, files: dict, sql: dict, symbols: dict):
    """`assoc = Table("name", Base.metadata, Column(...), ...)` at module level (golden D16: entity kind variable)."""
    for path, f in files.items():
        for node in f.tree.body:
            if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Call)
                    and r.qual_node(f.scope, node.value.func) in {"sqlalchemy.Table", "sqlalchemy.schema.Table"}):
                continue
            var = node.targets[0].id
            q = f"{f.prefix}{var}"
            ev = b.span(path, node)
            symbols[q] = b.fact("symbol", ev, q, {"name": known(q, ev["id"]), "local_name": known(var, ev["id"]),
                                                  "symbol_kind": known("variable", ev["id"]),
                                                  "signature": not_applicable("Biến")})
            call = node.value
            attrs = {"declaration_evidence_id": known(ev["id"], ev["id"]),
                     "variable_name": known(var, ev["id"])}  # declared as `var = Table(...)`, not by a class
            evidence, inferred = [], []
            if call.args and isinstance(_literal(call.args[0]), str):
                name_ev = b.node_evidence(path, call.args[0])
                evidence.append(name_ev)
                attrs["name"] = known(call.args[0].value, name_ev["id"])
            else:
                attrs["name"] = unknown("Tên bảng không phải literal")
            meta = call.args[1] if len(call.args) > 1 else None
            base = r.qual_node(f.scope, meta.value) if isinstance(meta, ast.Attribute) and meta.attr == "metadata" else None
            bound = sql["bindings"].get(base, [])
            dialect = bound[0][0] if len({x for x, _ in bound}) == 1 else None
            if dialect:
                proof = {e["id"]: e for _, evs in bound for e in evs}
                attrs["dialect"] = known(dialect, *proof)
                evidence += list(proof.values())
            else:
                attrs["dialect"] = unknown("Metadata của bảng chưa được nối với một engine có URL literal")
            columns = []
            for arg in call.args[2:]:
                if isinstance(arg, ast.Call) and r.qual_node(f.scope, arg.func) in COLUMN and arg.args \
                        and isinstance(_literal(arg.args[0]), str):
                    fake = ast.Assign(targets=[ast.Name(id=arg.args[0].value, ctx=ast.Store())],
                                      value=ast.Call(func=arg.func, args=arg.args[1:], keywords=arg.keywords))
                    ast.copy_location(fake, arg)
                    fake.end_lineno, fake.end_col_offset = arg.end_lineno, arg.end_col_offset
                    ast.copy_location(fake.targets[0], arg.args[0])
                    fake.targets[0].end_lineno, fake.targets[0].end_col_offset = arg.args[0].end_lineno, arg.args[0].end_col_offset
                    col = _column(fake, path, f.scope, r, b, dialect, "sqlalchemy", inferred)
                    if col is not None:
                        columns.append(col[0])
                        evidence += col[1]
            attrs["columns"] = known(columns, ev["id"])
            fact = b.fact("table", ev, q, attrs, extra_evidence=evidence)
            _finish(fact, inferred)


def _migration_tables(b: _Builder, r: Resolver, files: dict):
    """Tables created only by Alembic `op.create_table("name", ...)` are not facts: a later migration may alter or
    drop them, and replaying migrations is not in this slice. They are reported, not left out silently (KPI-010)."""
    found = []
    for path, f in files.items():
        for node in ast.walk(f.tree):
            if isinstance(node, ast.Call) and r.qual_node(f.scope, node.func) == "alembic.op.create_table" \
                    and node.args and isinstance(_literal(node.args[0]), str):
                found.append((node.args[0].value, path))
    read = {f["attributes"]["name"]["value"] for f in b.facts if f["kind"] == "table" and is_known(f["attributes"]["name"])}
    found = [(n, p) for n, p in found if n not in read]
    if found:
        names = sorted({n for n, _ in found})
        b.limit("TABLES_IN_MIGRATIONS_NOT_READ", f"{len(names)} bảng chỉ thấy trong migration Alembic, chưa trích: "
                + ", ".join(names), sorted({b.files[p]["file_id"] for _, p in found}))


def _column(stmt, path, scope, r: Resolver, b: _Builder, dialect, orm, inferred):
    """One column from `x = Column(...)`, `x: Mapped[T] = mapped_column(...)`, an SQLModel field, or a mixin method
    `@declared_attr def x(cls): return Column(...)`."""
    if isinstance(stmt, FUNCS) and any((dotted(d) or "").split(".")[-1] == "declared_attr" for d in stmt.decorator_list):
        ret = next((s.value for s in stmt.body if isinstance(s, ast.Return)), None)
        if not (isinstance(ret, ast.Call) and r.qual_node(scope, ret.func) in COLUMN):
            return None
        fake = ast.Assign(targets=[ast.Name(id=stmt.name, ctx=ast.Store())], value=ret)
        ast.copy_location(fake, stmt)
        fake.end_lineno, fake.end_col_offset = stmt.end_lineno, stmt.end_col_offset
        ast.copy_location(fake.targets[0], stmt)
        fake.targets[0].end_lineno, fake.targets[0].end_col_offset = stmt.lineno, len(
            b.lines[path][stmt.lineno - 1].encode("utf-8"))
        stmt = fake
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name) \
            and isinstance(stmt.value, ast.Call) and r.qual_node(scope, stmt.value.func) in COLUMN | MAPPED_COLUMN:
        target, call, ann = stmt.targets[0], stmt.value, None
    elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
        target, ann = stmt.target, stmt.annotation
        call = stmt.value if isinstance(stmt.value, ast.Call) else None
        func = r.qual_node(scope, call.func) if call is not None else None
        if func in NOT_COLUMNS or (dotted(ann) or "").split(".")[-1] == "ClassVar":
            return None
        head = ((dotted(ann.value) if isinstance(ann, ast.Subscript) else "") or "").split(".")[-1]
        if head in ("Optional",) and orm == "sqlalchemy":
            return None
        if orm == "sqlalchemy" and head != "Mapped":
            return None
        if func is not None and func not in MAPPED_COLUMN | FIELD | COLUMN:
            return None
        if orm == "sqlmodel" and "Relationship" in ast.unparse(stmt.value or ast.Constant(None)):
            return None
    else:
        return None
    if target.id.startswith("__"):
        return None
    ev, name_ev = b.span(path, stmt), b.node_evidence(path, target)
    first_rule, guessed = len(inferred), []  # rules this column adds and the fields they decide (AC-030-01)
    col = {"name": known(target.id, name_ev["id"])}
    type_node = None
    if call is not None and r.qual_node(scope, call.func) in COLUMN | MAPPED_COLUMN:
        type_node = next((a for a in call.args if not isinstance(a, ast.Constant)
                          and (dotted(a.func if isinstance(a, ast.Call) else a) or "").split(".")[-1] != "ForeignKey"), None)
    if type_node is None and call is not None and _keyword(call, "sa_type") is not None:
        type_node = _keyword(call, "sa_type")  # SQLModel Field(sa_type=DateTime(timezone=True)) wins over the annotation
    inner, optional = ann, False
    if isinstance(inner, ast.Subscript) and (dotted(inner.value) or "").split(".")[-1] == "Mapped":
        inner = inner.slice
    if isinstance(inner, ast.Subscript) and (dotted(inner.value) or "").split(".")[-1] == "Optional":
        inner, optional = inner.slice, True
    if isinstance(inner, ast.BinOp) and isinstance(inner.op, ast.BitOr):
        sides = [s for s in (inner.left, inner.right) if not (isinstance(s, ast.Constant) and s.value is None)]
        optional = len(sides) == 1
        inner = sides[0] if len(sides) == 1 else inner
    alias_calls, alias_ev = _annotated_columns(r, scope, inner)  # id: Mapped[id_key], id_key = Annotated[int, mapped_column(...)]
    if alias_calls:
        alias_ev = b.span(*alias_ev)
        inner = r.assigns[r.qual_node(scope, inner)][1].slice.elts[0]
        if type_node is None:
            types = {ast.unparse(a) for c in alias_calls for a in c.args[:1] if not isinstance(a, ast.Constant)}
            type_node = next(a for c in alias_calls for a in c.args[:1]) if len(types) == 1 else None
    if type_node is not None:
        type_name = (dotted(type_node.func if isinstance(type_node, ast.Call) else type_node) or "").split(".")[-1]
    else:
        type_name = (dotted(inner) or "").split(".")[-1]
    type_args = [_literal(a) for a in type_node.args] if isinstance(type_node, ast.Call) else []
    declared = ast.unparse(type_node) if type_node is not None else (ast.unparse(inner) if inner is not None else None)
    max_length = _literal(_keyword(call, "max_length")) if call is not None else None
    if declared and type_node is None and isinstance(max_length, int):  # SQLModel Field(max_length=255)
        declared += f", max_length={max_length}"
    if dialect is None:
        col["type"] = unknown("Chưa xác định SQL dialect từ source" + (f"; khai trong code: {declared}" if declared else ""))
    elif type_args and type_name in PARAM_TYPES.get(dialect, {}) and all(isinstance(x, int) for x in type_args):
        col["type"] = known(f"{PARAM_TYPES[dialect][type_name]}({','.join(map(str, type_args))})", ev["id"])
        inferred.append("sqlalchemy-type-v1: kiểu SQL ánh xạ từ kiểu SQLAlchemy theo dialect")
        guessed.append("type")
    elif isinstance(type_node, ast.Call) and (type_node.args or type_node.keywords):
        col["type"] = unknown(f"Kiểu {type_name}(...) có tham số; bảng ánh xạ sqlalchemy-type-v1 chưa giữ tham số cho {dialect}")
    elif type_name in SQL_TYPES.get(dialect, {}):
        col["type"] = known(SQL_TYPES[dialect][type_name], ev["id"])
        inferred.append("sqlalchemy-type-v1: kiểu SQL ánh xạ từ kiểu SQLAlchemy theo dialect")
        guessed.append("type")
    else:
        col["type"] = unknown(f"Kiểu {type_name!r} chưa có trong bảng ánh xạ sqlalchemy-type-v1")
    pk = _literal(_keyword(call, "primary_key"))
    alias_pk = {_literal(_keyword(c, "primary_key")) for c in alias_calls}
    if not isinstance(pk, bool) and alias_calls and len(alias_pk) == 1 and isinstance(next(iter(alias_pk)), bool):
        col["primary_key"] = known(next(iter(alias_pk)), alias_ev["id"])  # read from the alias, every branch agrees
    elif not isinstance(pk, bool) and alias_calls and len(alias_pk) > 1:
        col["primary_key"] = unknown("Khóa chính khác nhau giữa các nhánh điều kiện của alias Annotated")
    else:
        col["primary_key"] = known(pk if isinstance(pk, bool) else False, ev["id"])
        if not isinstance(pk, bool):
            inferred.append("sqlalchemy-defaults-v1: không khai primary_key thì là False")
            guessed.append("primary_key")
    nullable = _literal(_keyword(call, "nullable"))
    alias_null = {_literal(_keyword(c, "nullable")) for c in alias_calls}
    if not isinstance(nullable, bool) and len(alias_null) == 1 and isinstance(next(iter(alias_null)), bool):
        nullable = next(iter(alias_null))
    if isinstance(nullable, bool):
        col["nullable"] = known(nullable, ev["id"])
    elif col["primary_key"]["state"] != "known":
        col["nullable"] = unknown("Phụ thuộc khóa chính, mà khóa chính chưa xác định")
    else:
        col["nullable"] = known((not col["primary_key"]["value"]) and (optional if ann is not None else True), ev["id"])
        inferred.append("sqlalchemy-defaults-v1: nullable mặc định là not primary_key; với Mapped/SQLModel theo Optional")
        guessed.append("nullable")
    fk = next((a for a in getattr(call, "args", []) if isinstance(a, ast.Call)
               and (dotted(a.func) or "").split(".")[-1] == "ForeignKey"), None)
    fk_target = _literal(fk.args[0]) if fk is not None and fk.args else None
    if fk is None and _keyword(call, "foreign_key") is not None:
        fk, fk_target = _keyword(call, "foreign_key"), _literal(_keyword(call, "foreign_key"))
    if fk is None:
        col["foreign_key"] = not_applicable("Không khai ForeignKey/foreign_key")
    elif isinstance(fk_target, str) and fk_target.count(".") == 1:
        t, c = fk_target.split(".")
        # ForeignKey('t.c', ondelete=...) or SQLModel Field(foreign_key='t.c', ondelete=...)
        on_delete = _literal(_keyword(fk if isinstance(fk, ast.Call) else call, "ondelete"))
        col["foreign_key"] = known({"table": t, "column": c, **({"ondelete": on_delete} if isinstance(on_delete, str)
                                                                 else {})}, ev["id"])
    else:
        col["foreign_key"] = unknown("Đích khóa ngoại không phải literal bảng.cột")
    flags = [k for k in ("unique", "index") if _literal(_keyword(call, k)) is True  # written as True only, here
             or (alias_calls and all(_literal(_keyword(c, k)) is True for c in alias_calls))]  # or in every alias branch
    if flags:
        col["constraints"] = known(flags, ev["id"])
    rules = sorted({x.split(":")[0] for x in inferred[first_rule:]})
    if rules:
        col["inferred_by"] = known(rules, ev["id"])
    if guessed:  # which values came from a documented default, not from the code
        col["inferred_fields"] = known(guessed, ev["id"])
    return col, [ev, name_ev] + ([alias_ev] if alias_calls else [])


def _table_constraints(node) -> list[str]:
    """UniqueConstraint / Index / CheckConstraint of a __table_args__ tuple, as short text."""
    out = []
    for x in (node.elts if isinstance(node, (ast.Tuple, ast.List)) else []):
        if not isinstance(x, ast.Call):
            continue
        kind, name = (dotted(x.func) or "").split(".")[-1], _literal(_keyword(x, "name"))
        args = [_literal(a) for a in x.args]
        if kind == "UniqueConstraint":
            out.append(f"unique({', '.join(a for a in args if isinstance(a, str))})" + (f" {name}" if isinstance(name, str) else ""))
        elif kind == "Index" and args and isinstance(args[0], str):
            unique = "unique " if _literal(_keyword(x, "unique")) is True else ""
            out.append(f"{unique}index({', '.join(a for a in args[1:] if isinstance(a, str))}) {args[0]}")
        elif kind == "CheckConstraint" and x.args:
            out.append(f"check({ast.unparse(x.args[0])})" + (f" {name}" if isinstance(name, str) else ""))
    return out


def _annotated_columns(r: Resolver, scope, node) -> tuple[list, tuple | None]:
    """mapped_column(...) calls inside a type alias `X = Annotated[T, mapped_column(...)]` (also `a if cond else b`),
    with (path, alias value node) for the evidence; ([], None) when `node` is not such an alias."""
    q = r.qual_node(scope, node) if isinstance(node, (ast.Name, ast.Attribute)) else None
    path, value = r.assigns.get(q, (None, None)) if q else (None, None)
    if not (isinstance(value, ast.Subscript) and (dotted(value.value) or "").split(".")[-1] == "Annotated"
            and isinstance(value.slice, ast.Tuple)):
        return [], None
    calls = []
    for extra in value.slice.elts[1:]:
        for x in ([extra.body, extra.orelse] if isinstance(extra, ast.IfExp) else [extra]):
            if isinstance(x, ast.Call) and r.qual_node(r.scopes[path], x.func) in MAPPED_COLUMN:
                calls.append(x)
    return calls, ((path, value) if calls else None)


# ---------------------------------------------------------------- events, http, config, libraries

def _clients(r: Resolver, f: _File, kinds: set[str]):
    """Names assigned from a client constructor in this file: {written name: (qualified ctor, call)}."""
    out = {}
    for node in ast.walk(f.tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.value, ast.Call):
            q, name = r.qual_node(f.scope, node.value.func), dotted(node.targets[0])
            if q in kinds and name:
                out[name] = (q, node.value)
    return out


def _kafka_broker(call):
    servers = _keyword(call, "bootstrap_servers")
    if servers is None and call.args and isinstance(call.args[0], ast.Dict):
        d = call.args[0]
        servers = next((v for k, v in zip(d.keys, d.values) if _literal(k) == "bootstrap.servers"), None)
    if servers is None and call.args and isinstance(_literal(call.args[0]), str) and "://" in call.args[0].value:
        servers = call.args[0]
    value = _literal(servers)
    return ("known", f"kafka:{value}") if isinstance(value, str) else ("unknown", "Địa chỉ broker không phải literal")


def _serialization(call):
    for kw in ("value_serializer", "value_deserializer"):
        node = _keyword(call, kw)
        if node is not None:
            return ("known", "json") if "json" in ast.unparse(node) else ("unknown", f"{kw} không đọc được định dạng")
    return "unknown", "Không khai báo serializer"


def _event(b, path, node, action, topic_node, broker, serialization):
    ev = b.node_evidence(path, node)
    attrs = {"action": known(action, ev["id"]), "declaration_evidence_id": known(ev["id"], ev["id"]),
             "namespace": not_applicable("Kafka không có namespace riêng; channel xác định bằng broker + topic"),
             "payload": unknown("Payload không có schema đọc được")}
    extra = []
    if topic_node is not None and isinstance(_literal(topic_node), str):
        topic_ev = b.node_evidence(path, topic_node)
        attrs["topic"] = known(topic_node.value, topic_ev["id"])
        extra.append(topic_ev)
    else:
        attrs["topic"] = unknown("Topic không phải literal")
    for key, (state, value) in (("broker", broker), ("serialization_context", serialization)):
        attrs[key] = known(value, ev["id"]) if state == "known" else unknown(value)
    fact = b.fact("event", ev, f"{path}:{node.lineno}:{node.col_offset}:{action}:{ast.unparse(topic_node) if topic_node else ''}",
                  attrs, extra_evidence=extra)
    _finish(fact)


def _events(b: _Builder, r: Resolver, files: dict):
    for path, f in files.items():
        producers, consumers = _clients(r, f, KAFKA_PRODUCERS), _clients(r, f, KAFKA_CONSUMERS)
        brokers = _clients(r, f, FASTSTREAM_BROKERS)
        for node in ast.walk(f.tree):
            if isinstance(node, ast.Call):
                ctor = r.qual_node(f.scope, node.func)
                if ctor in {"kafka.KafkaConsumer", "aiokafka.AIOKafkaConsumer"}:
                    for t in [a for a in node.args if isinstance(_literal(a), str)]:
                        _event(b, path, node, "consume", t, _kafka_broker(node), _serialization(node))
                if not isinstance(node.func, ast.Attribute):
                    continue
                owner, attr = dotted(node.func.value), node.func.attr
                if owner in producers and attr in ("send", "send_and_wait", "produce"):
                    _, c = producers[owner]
                    _event(b, path, node, "publish", node.args[0] if node.args else _keyword(node, "topic"),
                           _kafka_broker(c), _serialization(c))
                elif owner in consumers and attr == "subscribe":
                    _, c = consumers[owner]
                    topics = node.args[0] if node.args else _keyword(node, "topics")
                    for t in getattr(topics, "elts", [topics] if topics is not None else []):
                        _event(b, path, node, "consume", t, _kafka_broker(c), _serialization(c))
                elif owner in brokers and attr == "publish":
                    _, c = brokers[owner]
                    _event(b, path, node, "publish", node.args[1] if len(node.args) > 1 else _keyword(node, "topic"),
                           _kafka_broker(c), ("unknown", "FastStream chọn serializer lúc chạy"))
            elif isinstance(node, FUNCS):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.args \
                            and dotted(dec.func.value) in brokers and dec.func.attr in ("subscriber", "publisher"):
                        _, c = brokers[dotted(dec.func.value)]
                        _event(b, path, dec, "consume" if dec.func.attr == "subscriber" else "publish", dec.args[0],
                               _kafka_broker(c), ("unknown", "FastStream chọn serializer lúc chạy"))


CELERY_APPS = {"celery.Celery"}
SHARED_TASKS = {"celery.shared_task"}
BACKGROUND_TASKS = {"fastapi.BackgroundTasks", "fastapi.background.BackgroundTasks", "starlette.background.BackgroundTasks"}


def _task_event(b, path, node, action, topic, broker, namespace, serialization, inferred=()):
    """A Celery or BackgroundTasks point. Both ends of one channel carry the same broker, namespace and serialization
    values (the same Celery app; the same process for BackgroundTasks), so FR-031 can pair them."""
    ev = b.node_evidence(path, node)
    attrs = {"action": known(action, ev["id"]), "declaration_evidence_id": known(ev["id"], ev["id"]),
             "topic": known(topic, ev["id"]) if topic else unknown("Tên tác vụ không đọc được từ source"),
             "payload": unknown("Đối số tác vụ không có schema đọc được")}
    for key, (state, value) in (("broker", broker), ("namespace", namespace), ("serialization_context", serialization)):
        attrs[key] = known(value, ev["id"]) if state == "known" else unknown(value)
    fact = b.fact("event", ev, f"{path}:{node.lineno}:{node.col_offset}:{action}:{topic or ''}", attrs)
    _finish(fact, inferred)


def _task_events(b: _Builder, r: Resolver, files: dict):
    """FR-031 Phạm vi đọc: Celery (.delay, .apply_async, send_task -> @app.task, @shared_task) and FastAPI
    BackgroundTasks (add_task(f) -> f)."""
    apps = {q for q, (p, v) in r.assigns.items() if isinstance(v, ast.Call) and r.qual_node(r.scopes[p], v.func) in CELERY_APPS}
    tasks = {}  # task function qname -> (task name, app qname or None, inferred reasons)
    for path, f in files.items():
        for node in f.tree.body:
            if not isinstance(node, FUNCS):
                continue
            for dec in node.decorator_list:
                target = dec.func if isinstance(dec, ast.Call) else dec
                app = r.qual_node(f.scope, target.value) if isinstance(target, ast.Attribute) and target.attr == "task" else None
                if app not in apps and r.qual_node(f.scope, target) not in SHARED_TASKS:
                    continue
                named = _literal(_keyword(dec, "name")) if isinstance(dec, ast.Call) else None
                default = f"{f.prefix}{node.name}"
                why = () if isinstance(named, str) else (f"Celery đặt tên tác vụ mặc định <module>.<hàm> = {default} "
                                                          "khi không khai name=",)
                tasks[default] = (named if isinstance(named, str) else default, app if app in apps else None, why)
                _celery_point(b, path, dec, "consume", *tasks[default])
    for path, f in files.items():
        parents = None
        for node in ast.walk(f.tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            owner = r.qual_node(f.scope, node.func.value)
            if node.func.attr in ("delay", "apply_async") and owner in tasks:
                _celery_point(b, path, node, "publish", *tasks[owner])
            elif node.func.attr == "send_task" and owner in apps:
                name = _literal(node.args[0]) if node.args else _literal(_keyword(node, "name"))
                _celery_point(b, path, node, "publish", name if isinstance(name, str) else None, owner, ())
            elif node.func.attr == "add_task" and node.args and isinstance(node.func.value, ast.Name):
                parents = parents or _parents(f.tree)
                func, _ = _enclosing(node, parents)
                args = func.args.posonlyargs + func.args.args + func.args.kwonlyargs if func else []
                if not any(a.arg == node.func.value.id and a.annotation is not None
                           and r.qual_node(f.scope, a.annotation) in BACKGROUND_TASKS for a in args):
                    continue
                target = _background_target(r, f, node.args[0], parents)
                same = (("known", "fastapi.BackgroundTasks"), ("known", "cùng tiến trình với app"),
                        ("known", "không tuần tự hóa (gọi trong tiến trình)"))
                _task_event(b, path, node, "publish", target.qname if target else None, *same)
                if target is not None and target.qname not in tasks:
                    tasks[target.qname] = None  # the receiver is written once, at its definition
                    _task_event(b, target.path, target.node, "consume", target.qname, *same)


def _celery_point(b, path, node, action, name, app, why):
    if app is None:
        unknown_app = ("unknown", "shared_task: app Celery chọn lúc chạy")
        _task_event(b, path, node, action, name, unknown_app, unknown_app, unknown_app, why)
    else:
        _task_event(b, path, node, action, name, ("known", f"celery:{app}"), ("known", app),
                    ("known", f"theo cấu hình của app {app}"), why)


def _background_target(r: Resolver, f, arg, parents):
    """Definition of the function handed to add_task: a name, or self.method inside a class."""
    if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name) and arg.value.id == "self":
        cur = arg
        while cur in parents and not isinstance(cur, ast.ClassDef):
            cur = parents[cur]
        return r.defs.get(f"{f.prefix}{cur.name}.{arg.attr}") if isinstance(cur, ast.ClassDef) else None
    q = r.qual_node(f.scope, arg)
    d = r.defs.get(q) if q else None
    return d if d is not None and d.kind in ("function", "method") else None


def _is_test_file(path):
    parts = path.replace('\\', '/').split('/')
    return bool(set(parts[:-1]) & {'test', 'tests'}) or parts[-1] == 'conftest.py' or \
        parts[-1].startswith('test_') or parts[-1].endswith('_test.py')


def _scoped_nodes(root):
    """Visit a lexical scope without mixing assignments from sibling/nested functions."""
    for child in ast.iter_child_nodes(root):
        yield child
        if not isinstance(child, (*FUNCS, ast.ClassDef, ast.Lambda)):
            yield from _scoped_nodes(child)


def _binding_value(f, node, name):
    """Find the latest preceding assignment visible to this expression; do not guess by variable name."""
    if not name:
        return None, False
    func, _ = _enclosing(node, f.parents)
    scope = func or f.tree
    nodes = list(_scoped_nodes(scope))
    args = list(func.args.posonlyargs) + list(func.args.args) + list(func.args.kwonlyargs) if func else []
    if func:
        args += [a for a in (func.args.vararg, func.args.kwarg) if a]
    # A local write shadows a module binding even when the write occurs later.
    writes = [n for n in nodes if isinstance(n, (ast.Assign, ast.AnnAssign, ast.NamedExpr, ast.AugAssign))
              and any(dotted(t) == name for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))]
    ancestors = set()
    cur = node
    while cur in f.parents:
        cur = f.parents[cur]
        ancestors.add(cur)
    with_values = []
    for n in ancestors:
        if isinstance(n, (ast.With, ast.AsyncWith)):
            with_values += [(n.lineno, i.context_expr) for i in n.items if dotted(i.optional_vars) == name]
    candidates = []
    for n in writes:
        if (n.lineno, n.col_offset) >= (node.lineno, node.col_offset):
            continue
        # Branch-only writes cannot prove a binding outside that branch.
        parent = f.parents.get(n)
        if not isinstance(n, ast.AugAssign) and (parent is scope or parent in ancestors):
            candidates.append(((n.lineno, n.col_offset), n.value))
        else:
            candidates.append(((n.lineno, n.col_offset), None))
    candidates += [((line, -1), value) for line, value in with_values]
    if candidates:
        return max(candidates, key=lambda x: x[0])[1], False
    arg = next((a for a in args if a.arg == name), None)
    if arg:
        return arg.annotation, True
    if writes:
        return None, False
    if name.startswith('self.') and func:
        cls = f.parents.get(func)
        if isinstance(cls, ast.ClassDef):
            values = [n.value for method in cls.body if isinstance(method, FUNCS)
                      for n in _scoped_nodes(method) if isinstance(n, (ast.Assign, ast.AnnAssign))
                      and any(dotted(t) == name for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))]
            if values and len({ast.dump(v) for v in values if v is not None}) == 1:
                return values[0], False
    module_values = [n.value for n in f.tree.body if isinstance(n, (ast.Assign, ast.AnnAssign))
                     and any(dotted(t) == name for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))]
    return (module_values[-1], False) if module_values else (None, False)


def _http_config_key(r, f, node):
    if isinstance(node, ast.Call) and r.qual_node(f.scope, node.func) in {'os.getenv', 'os.environ.get'}:
        return _literal(node.args[0]) if node.args else None
    if isinstance(node, ast.Subscript) and r.qual_node(f.scope, node.value) == 'os.environ':
        return _literal(node.slice)
    if isinstance(node, ast.Attribute):
        value, annotated = _binding_value(f, node, dotted(node.value))
        cls = r.qual_node(f.scope, value if annotated else value.func) if annotated or isinstance(value, ast.Call) else None
        if cls in r.classes and r.subclass_of(cls, SETTINGS):
            return node.attr
    return None


def _http_call_text(b, path, node, evidence_id):
    # Source excerpts must not publish values from credential arguments or headers.
    for part in ast.walk(node):
        if isinstance(part, ast.keyword) and part.arg and (SECRET_NAME.search(part.arg) or part.arg in {'auth', 'headers'}):
            return {'state': 'redacted', 'reason': 'Lời gọi chứa đối số credential/header; không xuất nguyên văn'}
        if isinstance(part, ast.Dict) and any(isinstance(_literal(k), str) and
                (SECRET_NAME.search(_literal(k)) or _literal(k).lower() == 'authorization') for k in part.keys):
            return {'state': 'redacted', 'reason': 'Lời gọi chứa trường nhạy cảm; không xuất nguyên văn'}
    return known(ast.get_source_segment('\n'.join(b.lines[path]), node) or ast.unparse(node), evidence_id)


def _unsupported_routes_http(b, files):
    route_methods = {'add_api_route', 'add_api_websocket_route', 'add_route', 'add_websocket_route'}
    for path, f in files.items():
        for node in ast.walk(f.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in route_methods:
                b.limit('ROUTE_NOT_DECORATOR', f'{path}:{node.lineno}: {ast.unparse(node.func)}(…) '
                        'khai route không qua decorator; chưa đọc ở đợt này', [b.files[path]['file_id']])
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                [node.module or '', *((node.module or '') + '.' + a.name for a in node.names)] \
                if isinstance(node, ast.ImportFrom) else []
            for lib in sorted(UNSUPPORTED_HTTP):
                if any(n == lib or n.startswith(lib + '.') for n in names):
                    b.limit('HTTP_LIBRARY_UNSUPPORTED', f'{path}:{node.lineno}: {lib} chưa được hỗ trợ',
                            [b.files[path]['file_id']])


def _http_and_config(b: _Builder, r: Resolver, files: dict):
    for path, f in files.items():
        for node in ast.walk(f.tree):
            if isinstance(node, ast.Call):
                q = r.qual_node(f.scope, node.func) or ""
                lib, _, method = q.rpartition(".")
                if lib in HTTP_LIBS and isinstance(node.func, ast.Attribute):
                    binding, annotated = _binding_value(f, node, dotted(node.func.value))
                    if annotated or binding is not None:
                        lib = ''  # An argument/local variable shadows the imported module.
                if isinstance(node.func, ast.Attribute) and lib not in HTTP_LIBS:
                    value, annotated = _binding_value(f, node, dotted(node.func.value))
                    ctor = r.qual_node(f.scope, value if annotated else value.func) \
                        if annotated or isinstance(value, ast.Call) else None
                    if ctor in HTTP_CLIENTS:
                        lib, method = ctor.split('.')[0], node.func.attr
                if not _is_test_file(path) and lib in HTTP_LIBS and method in HTTP_METHODS | {'request'}:
                    ev = b.node_evidence(path, node)
                    verb = _literal(node.args[0] if node.args else _keyword(node, 'method')) if method == 'request' else method
                    pos = 1 if method == 'request' else 0
                    url_node = node.args[pos] if len(node.args) > pos else _keyword(node, 'url')
                    url = _text(url_node)
                    attrs = {"method": known(verb.upper(), ev["id"]) if isinstance(verb, str) else unknown('Method phụ thuộc lúc chạy'),
                             "url": known(re.sub(r"\?.*$", "", url[0]), ev["id"]) if url and url[1]
                             else unknown("URL ghép từ giá trị lúc chạy: " + (url[0] if url else "không có")),
                             "library": known(lib, ev['id']),
                             "call_text": _http_call_text(b, path, node, ev['id']),
                             "target_unit_id": unknown("Chưa nối URL với unit trong snapshot")}
                    config_key = _http_config_key(r, f, url_node)
                    if isinstance(config_key, str):
                        attrs['url_config_key'] = known(config_key, ev['id'])
                    _finish(b.fact("http_call", ev, f"{path}:{node.lineno}:{node.col_offset}", attrs))
                elif q in ("os.getenv", "os.environ.get") and node.args and isinstance(_literal(node.args[0]), str):
                    _config(b, path, node, node.args[0].value, "env")
            elif isinstance(node, ast.Subscript) and r.qual_node(f.scope, node.value) == "os.environ" \
                    and isinstance(_literal(node.slice), str):
                _config(b, path, node, node.slice.value, "env")
    for q, rec in r.classes.items():
        if r.subclass_of(q, SETTINGS):
            for stmt in rec.node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    _config(b, rec.path, stmt, stmt.target.id, "settings", default=stmt.value)


def _config(b, path, node, key, source, default=None):
    ev = b.node_evidence(path, node)
    if SECRET_NAME.search(key):
        value = {"state": "redacted", "reason": "Tên khóa có dấu hiệu bí mật"}
    elif default is not None and isinstance(_literal(default), (str, int, float, bool)):
        value = known(_literal(default), ev["id"])
    else:
        value = unknown("Giá trị đọc lúc chạy")
    fact = b.fact("config", ev, f"{path}:{node.lineno}:{node.col_offset}:{key}",
                  {"key": known(key, ev["id"]), "source_kind": known(source, ev["id"]), "value": value})
    _finish(fact, ["golden D22: giá trị mặc định của class cấu hình có thể bị biến môi trường ghi đè"]
            if source == "settings" and is_known(value) else [])


IMPORT_NAMES = {"psycopg2-binary": "psycopg2", "psycopg-binary": "psycopg", "python-jose": "jose", "pyjwt": "jwt",
                "pyyaml": "yaml", "beautifulsoup4": "bs4", "pillow": "PIL", "python-multipart": "multipart",
                "python-dotenv": "dotenv", "scikit-learn": "sklearn", "opencv-python": "cv2"}
QUEUE_LIBS = {"kombu", "pika", "aio_pika", "dramatiq", "rq", "arq", "taskiq", "nats"}  # no event facts yet


def _imports(files: dict) -> dict[str, tuple[str, ast.AST]]:
    """First absolute import of each top-level module: {module: (path, node)}, in path order."""
    out = {}
    for path, f in sorted(files.items()):
        for node in ast.walk(f.tree):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module else []
            for name in names:
                out.setdefault(name.split(".")[0], (path, node))
    return out


def _unsupported_queues(b: _Builder, files: dict):
    """A queue/task library the extractor has no event rule for is reported, not left out silently (KPI-010)."""
    seen = [(m, path, node) for m, (path, node) in sorted(_imports(files).items()) if m in QUEUE_LIBS]
    if seen:
        b.limit("QUEUE_LIBRARY_UNSUPPORTED", "Dùng thư viện hàng đợi/sự kiện chưa hỗ trợ, chưa trích bên gửi/nhận: "
                + ", ".join(f"{m} ({p}:{n.lineno})" for m, p, n in seen),
                sorted({b.files[p]["file_id"] for _, p, _ in seen}))
    pubsub = []  # Redis used as a message bus (publish / pubsub), e.g. a hand-written event bus: not read yet
    for path, f in sorted(files.items()):
        if "redis" not in _imports({path: f}):
            continue
        pubsub += [(path, n.lineno) for n in ast.walk(f.tree) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Attribute) and n.func.attr in ("publish", "pubsub")]
    if pubsub:
        b.limit("QUEUE_LIBRARY_UNSUPPORTED", "Dùng Redis pub/sub làm kênh sự kiện; chưa trích bên gửi/nhận, tài liệu "
                "không liệt kê các sự kiện này: " + ", ".join(f"{p}:{line}" for p, line in sorted(set(pubsub))),
                sorted({b.files[p]["file_id"] for p, _ in pubsub}))


def _libraries(b: _Builder, texts: dict[str, str], files: dict):
    imported = _imports(files)
    declared = set()
    for path, text in texts.items():
        if path.endswith("pyproject.toml"):
            try:
                data = tomllib.loads(text)
            except tomllib.TOMLDecodeError:
                b.limit("MANIFEST_INVALID", f"{path}: TOML không hợp lệ", [b.files[path]["file_id"]])
                continue
            project, tool = data.get("project", {}), data.get("tool", {})
            deps = project.get("dependencies", []) if isinstance(project, dict) else None
            poetry = tool.get("poetry", {}) if isinstance(tool, dict) else None
            poetry_deps = poetry.get("dependencies", {}) if isinstance(poetry, dict) else None
            if not (isinstance(deps, list) and all(isinstance(d, str) for d in deps) and isinstance(poetry_deps, dict)):
                b.limit("MANIFEST_INVALID", f"{path}: dependencies sai cấu trúc", [b.files[path]["file_id"]])
                continue
            entries = list(deps)
            entries += [f"{k}{v if isinstance(v, str) else ''}" for k, v in poetry_deps.items() if k != "python"]
        else:
            entries = [ln.split("#")[0].strip() for ln in text.splitlines()]
            entries = [e for e in entries if e and not e.startswith("-")]
        lines = text.splitlines()
        after = 0  # entries come in file order: each takes the next line that names it, so a package declared
        for entry in entries:  # twice (one line per python version) keeps both lines
            m = re.match(r"^([A-Za-z0-9_.\-]+)(\[[^\]]*\])?\s*(.*)$", entry)
            if not m:
                continue
            line_no = next((i + 1 for i, ln in enumerate(lines) if i >= after and m.group(1) in ln), None) or \
                next((i + 1 for i, ln in enumerate(lines) if m.group(1) in ln), 1)
            after = line_no
            ev = b.evidence(path, line_no, line_no)
            dist = m.group(1).lower()
            module = IMPORT_NAMES.get(dist, dist.replace("-", "_").replace(".", "_"))
            if module not in imported and dist.startswith("python-"):  # python-slugify -> slugify
                module = dist[len("python-"):].replace("-", "_")
            if module not in imported and "-" in dist and dist.split("-")[0] in imported:  # tortoise-orm -> tortoise
                module = dist.split("-")[0]
            extra = []
            if module in imported:
                site = b.node_evidence(*imported[module])
                extra.append(site)
                used = known(True, site["id"])
            else:
                used = unknown(f"Không thấy import {module} trong code đã đọc; có thể dùng gián tiếp (driver, plugin, CLI)")
            attrs = {"name": known(dist, ev["id"]), "manifest": known(path, ev["id"]),
                     "version": known(m.group(3).strip(), ev["id"]) if m.group(3).strip()
                     else unknown("Không ghi ràng buộc phiên bản"),
                     "used": used}
            key = f"{path}:{dist}" if f"{path}:{dist}" not in declared else f"{path}:{dist}:{line_no}"
            declared.add(key)  # a second declaration (another python version) is its own fact
            _finish(b.fact("library", ev, key, attrs, extra_evidence=extra))


# ---------------------------------------------------------------- references

def _references(b: _Builder, r: Resolver, files: dict, symbols: dict, tables: set[str]):
    """Calls (`calls`), `Depends(x)` (`depends`) and table classes named without a call (`reads`).
    One fact per (source, target, relation) (golden D30); calls into libraries are not facts (golden D17)."""
    seen = set()

    def emit(src_q, path, node, relation, ref):
        target = ref.target if ref.resolved else None
        text = ast.unparse(node.func if isinstance(node, ast.Call) else node)
        key = (src_q, target or "?" + text, relation)
        if key in seen or src_q not in symbols:
            return
        seen.add(key)
        ev = b.node_evidence(path, node)
        attrs = {"reference_kind": known(relation, ev["id"]), "source_symbol": known(src_q, ev["id"]),
                 "target_symbol": known(target, ev["id"]) if target else unknown(ref.reason or "Không nối được đích"),
                 "call_text": known(text, ev["id"])}
        fact = b.fact("reference", ev, f"{src_q}->{key[1]}:{relation}", attrs, extra_evidence=[symbols[src_q]["evidence"][0]])
        if target and target in symbols:
            fact["resolution"], fact["target_fact_ids"] = "resolved", [symbols[target]["id"]]
        else:
            fact["resolution"], fact["resolution_reason"] = "unresolved", ref.reason or "Không nối được đích"
            fact["completeness"], fact["completeness_reason"] = "partial", "Đích chưa xác định"
        if ref.inferred:
            fact["confidence"], fact["confidence_reason"] = "inferred", ref.reason or "Đích suy ra từ kiểu biến"

    def depends_of(src_q, path, scope, node):
        provider = depends_target(node)
        if provider is not None:
            ref = r.resolve_call(ast.Call(func=provider, args=[], keywords=[]), scope, {}, {}, None)
            if ref is not None and ref.resolved:
                emit(src_q, path, node, "depends", ref)
            return True
        return False

    def walk(src_q, path, statements, scope, var_types, self_attrs, self_class, callables=None):
        """Calls evaluated when this code runs. Bodies of nested defs belong to the nested symbol (golden D20)."""
        call_funcs = set()
        stack = list(statements)
        while stack:
            node = stack.pop(0)
            if isinstance(node, ast.Lambda):
                continue
            if isinstance(node, (*FUNCS, ast.ClassDef)):
                # decorators and default values run here; the body does not
                for d in node.decorator_list:
                    target = d.func if isinstance(d, ast.Call) else d
                    ref = r.resolve_call(ast.Call(func=target, args=[], keywords=[]), scope, var_types, self_attrs, self_class,
                                         callables)
                    if ref is not None and ref.resolved:
                        emit(src_q, path, d, "calls", ref)
                    if isinstance(d, ast.Call):
                        stack.extend([*d.args, *[k.value for k in d.keywords]])
                if isinstance(node, ast.ClassDef):
                    stack.extend([s for s in node.body if not isinstance(s, (*FUNCS, ast.ClassDef))])
                    stack.extend(node.bases)
                else:
                    stack.extend([d for d in [*node.args.defaults, *node.args.kw_defaults]
                                  if d is not None and depends_target(d) is None])
                continue
            if isinstance(node, ast.Call):
                call_funcs.add(id(node.func))
                if r.qual_node(scope, node.func) not in NOT_COLUMNS:
                    ref = r.resolve_call(node, scope, var_types, self_attrs, self_class, callables)
                    if ref is not None and not ref.external:
                        emit(src_q, path, node, "calls", ref)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and id(node) not in call_funcs:
                q = scope.resolve(node.id)
                if q in tables:
                    emit(src_q, path, node, "reads", Ref(node.id, q, True))
            stack.extend(ast.iter_child_nodes(node))

    def alias_depends(src_q, path, scope, ann):
        """`x: CurrentCase` where `CurrentCase = Annotated[Case, Depends(get_current_case)]` elsewhere."""
        q = r.qualify(scope, dotted(ann)) if isinstance(ann, (ast.Name, ast.Attribute)) else None
        if q not in r.assigns:
            return
        alias_path, value = r.assigns[q]
        if isinstance(value, ast.Subscript) and (dotted(value.value) or "").endswith("Annotated") \
                and isinstance(value.slice, ast.Tuple):
            for extra in value.slice.elts[1:]:
                provider = depends_target(extra)
                if provider is not None:
                    ref = r.resolve_call(ast.Call(func=provider, args=[], keywords=[]), r.scopes[alias_path], {}, {}, None)
                    if ref is not None and ref.resolved:
                        emit(src_q, path, ann, "depends", ref)

    for path, f in files.items():
        mod_types, mod_callables = r.flow(None, list(f.tree.body), f.scope, {})
        walk(f"{f.prefix}__module__", path, list(f.tree.body), f.scope, mod_types, {}, None, mod_callables)
        for func, local in f.defs.items():
            if not isinstance(func, FUNCS):
                continue
            q = f"{f.prefix}{local}"
            owner = local.rsplit(".", 1)[0] if "." in local else None
            cls_q = f"{f.prefix}{owner}" if owner and f"{f.prefix}{owner}" in r.classes else None
            self_attrs = r.self_attrs(r.classes[cls_q].node, f.scope) if cls_q else {}
            var_types, callables = r.flow(q, list(func.body), f.scope, r.var_types(func, f.scope))
            walk(q, path, list(func.body), f.scope, var_types, self_attrs, cls_q, callables)
            for d in [*func.args.defaults, *[x for x in func.args.kw_defaults if x is not None]]:
                depends_of(q, path, f.scope, d)
            for a in [*func.args.posonlyargs, *func.args.args, *func.args.kwonlyargs]:
                ann = a.annotation
                alias_depends(q, path, f.scope, ann)
                if isinstance(ann, ast.Subscript) and (dotted(ann.value) or "").endswith("Annotated") \
                        and isinstance(ann.slice, ast.Tuple):
                    for extra in ann.slice.elts[1:]:
                        depends_of(q, path, f.scope, extra)


# ---------------------------------------------------------------- entry point

def _scrub(container) -> bool:
    """Turn every known FieldValue whose value looks like a credential (URL password, token...) into `redacted`
    (API-004 §2), whatever its key name. Returns True when something was redacted."""
    changed = False
    items = container.items() if isinstance(container, dict) else enumerate(container)
    for key, fv in list(items):
        if isinstance(fv, dict) and fv.get("state") == "known":
            if isinstance(fv["value"], (dict, list)):
                changed |= _scrub(fv["value"])
            if has_secret(fv["value"]):
                container[key] = {"state": "redacted", "reason": "Giá trị có dấu hiệu credential"}
                changed = True
        elif isinstance(fv, (dict, list)):
            changed |= _scrub(fv)
    return changed


def extract(snapshot: dict, sources: dict[str, bytes], unit_id: str) -> dict:
    b = _Builder(snapshot, unit_id, sources)
    trees, texts, unreadable = {}, {}, []
    for path, raw in sorted(sources.items()):
        if TEXT_MANIFESTS.search(path):
            texts[path] = raw.decode("utf-8", errors="replace")
        elif path.endswith(".py"):
            try:
                trees[path] = ast.parse(raw.decode("utf-8"), filename=path)
            except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
                b.limit("PARSE_FAILED", f"{path}: {type(exc).__name__}", [b.files[path]["file_id"]])
                unreadable.append(path)
    r = Resolver(trees, tuple(unreadable))
    files = {p: _File(p, t, r) for p, t in trees.items()}
    symbols = _symbols(b, r, files)
    production_files = {p: f for p, f in files.items() if not _is_test_file(p)}
    _routes(b, r, production_files, symbols)
    _unsupported_routes_http(b, production_files)
    tables = _tables(b, r, files)
    _table_variables(b, r, files, _sql_bindings(b, r, files), symbols)
    _migration_tables(b, r, files)
    _events(b, r, files)
    _task_events(b, r, files)
    _http_and_config(b, r, files)
    _libraries(b, texts, files)
    _unsupported_queues(b, files)
    _references(b, r, files, symbols, tables)
    unresolved = sorted(f["id"] for f in b.facts if f["kind"] == "reference" and f["resolution"] == "unresolved")
    if unresolved:  # KPI-010: a relation with an unknown target is reported, not only kept on its fact
        b.limit("REFERENCE_UNRESOLVED", f"{len(unresolved)} lời gọi chưa nối được đích; giữ là dữ kiện unresolved "
                "kèm lý do, không vẽ thành cạnh", unresolved)
    redacted = [f["id"] for f in b.facts if _scrub(f["attributes"])]
    if redacted:
        b.limit("VALUE_REDACTED", "Giá trị có dấu hiệu credential đã được che trước khi lưu", sorted(redacted))
    ids = [f["id"] for f in b.facts]
    if len(ids) != len(set(ids)):
        raise ValueError("IDENTITY_COLLISION: " + ", ".join(sorted({i for i in ids if ids.count(i) > 1})[:3]))
    b.facts.sort(key=lambda f: f["id"])
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": b.snap, "extractor_version": EXTRACTOR_VERSION,
            "facts": b.facts, "limitations": b.limitations}
