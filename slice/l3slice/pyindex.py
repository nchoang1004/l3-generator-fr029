"""Name resolution for Python source, read from the syntax tree only.

Ported from l3gen 0.1 (`src/l3gen/languages/python/resolution.py`, `core/resolution/symbol_table.py`,
`core/resolution/inheritance.py` on branch `feat/language-first-semantic-v2`). Changes:
- module-level code is a caller of its own (`__module__`), which l3gen 0.1 skipped;
- a target found through a guessed variable type is marked inferred;
- imports inside functions and `try` blocks are read as well;
- a name imported through a module that imports it in turn (a package `__init__.py` re-export) points at the
  file that defines it;
- a small value flow (golden D30): module-level variable types, callables returned by a function, and
  functions/instances passed as arguments. Targets found this way are marked inferred.
Nothing from the analysed repository is imported or executed.
"""
from __future__ import annotations

import ast
import builtins
import collections
from dataclasses import dataclass, field
from pathlib import PurePosixPath

FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef)
SOURCE_ROOTS = ("src",)
MAX_DEPTH = 10
MAX_ALIAS = 5
BUILTINS = frozenset(dir(builtins))
EXTERNAL = "thuộc thư viện ngoài, ngoài phạm vi repo"


def dotted(node) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        head = dotted(node.value)
        return f"{head}.{node.attr}" if head else None
    return None


def module_name(path: str, package_dirs: set[str]) -> str:
    """`app/x.py` -> `app.x`; `app/__init__.py` -> `app`; a top `src/` without `__init__.py` is a source root."""
    p = PurePosixPath(path)
    parts = list(p.parts[:-1])
    if parts and parts[0] in SOURCE_ROOTS and parts[0] not in package_dirs:
        parts = parts[1:]
    return ".".join(parts if p.stem == "__init__" else [*parts, p.stem])


@dataclass(frozen=True)
class Definition:
    qname: str
    path: str
    node: ast.AST
    kind: str  # module | class | function | method | assign


@dataclass
class Scope:
    path: str
    module: str
    names: dict[str, str] = field(default_factory=dict)
    wildcard: bool = False
    star_from: list[str] = field(default_factory=list)  # modules of `from m import *`

    def resolve(self, name: str) -> str | None:
        return self.names.get(name)


@dataclass
class ClassRec:
    qname: str
    path: str
    node: ast.ClassDef
    bases: list[str]
    methods: set[str]


@dataclass
class Ref:
    written: str
    target: str | None
    resolved: bool
    inferred: bool = False
    reason: str | None = None
    external: bool = False


def _relative(module: str, is_package: bool, level: int, imported: str | None) -> str:
    if level == 0:
        return imported or ""
    parts = module.split(".") if module else []
    package = parts if is_package else parts[:-1]
    package = package[:len(package) - (level - 1)] if level > 1 else package
    base = ".".join(package)
    return f"{base}.{imported}" if base and imported else (imported or base)


def annotation_name(node) -> str | None:
    """Class named by an annotation; unwraps `X | None`, `Optional[X]`, `Annotated[X, ...]`, string annotations."""
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split("[")[0].strip() or None
    if isinstance(node, ast.Subscript):
        head = (dotted(node.value) or "").split(".")[-1]
        if head in ("Annotated", "Optional"):
            inner = node.slice.elts[0] if isinstance(node.slice, ast.Tuple) else node.slice
            return annotation_name(inner)
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        for side in (node.left, node.right):
            if not (isinstance(side, ast.Constant) and side.value is None):
                return annotation_name(side)
        return None
    return dotted(node)


class Resolver:
    """Repository-wide definitions + per-file name tables. One table per file: the same short name may mean
    different things in two files, and merging the tables would silently point edges at the wrong file."""

    def __init__(self, trees: dict[str, ast.Module], unreadable: tuple[str, ...] = ()):
        """`unreadable`: paths of .py files that did not parse; names from them are known to exist but unknown."""
        self.trees = trees
        package_dirs = {PurePosixPath(p).parent.as_posix() for p in [*trees, *unreadable]
                        if PurePosixPath(p).name == "__init__.py"}
        self.module_of = {p: module_name(p, package_dirs) for p in trees}
        self.path_of_module = {m: p for p, m in self.module_of.items()}
        self.unreadable = {module_name(p, package_dirs) for p in unreadable}
        self.aliases = self._import_aliases(package_dirs)
        self.defs: dict[str, Definition] = {}
        self.methods: dict[str, dict[str, Definition]] = {}
        self.known_modules: set[str] = set()
        self.classes: dict[str, ClassRec] = {}
        self.returns: dict[str, ast.AST | None] = {}
        self.assigns: dict[str, tuple[str, ast.AST]] = {}
        self.scopes: dict[str, Scope] = {}
        for path, tree in trees.items():
            self._index(path, tree)
        for path, tree in trees.items():
            self.scopes[path] = self._scope(path, tree)
        followed = {p: {k: self._reexported(q) for k, q in s.names.items()} for p, s in self.scopes.items()}
        for path, names in followed.items():
            self.scopes[path].names = names
        self.external_origin = self._external_origin()
        self.dynamic_origin = {q for q, (p, v) in self.assigns.items() if isinstance(v, ast.Call)
                               and self.qualify(self.scopes[p], dotted(v.func)) in DYNAMIC_IMPORTS}
        self.returned = {}
        self.returned = self._returned()
        self.param_bindings = self._param_bindings()

    def _import_aliases(self, package_dirs: set[str]) -> dict[str, str]:
        """`app` -> `backend.app` when `backend/app` is a top package under a folder that is not one (the code runs
        from `backend/`). Kept only when the short name is unique and is not already a module of the repository."""
        tops = [d for d in package_dirs if "/" in d and d.rsplit("/", 1)[0] not in package_dirs]
        short = collections.Counter(d.rsplit("/", 1)[1] for d in tops)
        own = {m.split(".")[0] for m in self.module_of.values()}
        out = {}
        for d in tops:
            name, full = d.rsplit("/", 1)[1], d.replace("/", ".")
            if short[name] == 1 and name not in own and d.split("/")[0] not in SOURCE_ROOTS:
                out[name] = full
        return out

    def _canon(self, name: str) -> str:
        head, dot, rest = name.partition(".")
        return f"{self.aliases[head]}{dot}{rest}" if head in self.aliases else name

    def unreadable_origin(self, qname: str | None) -> str | None:
        """The module a name comes from when that module's file did not parse."""
        return next((m for m in self.unreadable if qname and (qname == m or qname.startswith(m + "."))), None)

    # ---- tables ----
    def _index(self, path: str, tree: ast.Module):
        module = self.module_of[path]
        if module:
            parts = module.split(".")
            self.known_modules.update(".".join(parts[:i]) for i in range(1, len(parts) + 1))
        prefix = f"{module}." if module else ""
        self.defs[f"{prefix}__module__"] = Definition(f"{prefix}__module__", path, tree, "module")
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                q = f"{prefix}{node.name}"
                self.defs[q] = Definition(q, path, node, "class")
                methods = {c.name for c in node.body if isinstance(c, FUNCS)}
                self.classes[q] = ClassRec(q, path, node, [d for d in (dotted(b) for b in node.bases) if d], methods)
                for c in node.body:
                    if isinstance(c, FUNCS):
                        d = Definition(f"{q}.{c.name}", path, c, "method")
                        self.defs[d.qname] = d
                        self.methods.setdefault(q, {})[c.name] = d
                        self.returns[d.qname] = c.returns
            elif isinstance(node, FUNCS):
                q = f"{prefix}{node.name}"
                self.defs[q] = Definition(q, path, node, "function")
                self.returns[q] = node.returns
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for t in targets:
                    if isinstance(t, ast.Name):
                        q = f"{prefix}{t.id}"
                        self.defs.setdefault(q, Definition(q, path, node, "assign"))
                        if node.value is not None:
                            self.assigns[q] = (path, node.value)

    def _scope(self, path: str, tree: ast.Module) -> Scope:
        module = self.module_of[path]
        prefix = f"{module}." if module else ""
        s = Scope(path, module)
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, *FUNCS)):
                s.names[node.name] = f"{prefix}{node.name}"
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                for t in (node.targets if isinstance(node, ast.Assign) else [node.target]):
                    if isinstance(t, ast.Name):
                        s.names[t.id] = f"{prefix}{t.id}"
        is_package = path.endswith("__init__.py")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    s.names[a.asname or a.name.split(".")[0]] = self._canon(a.name if a.asname else a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                base = _relative(module, is_package, node.level, node.module)
                base = self._canon(base) if node.level == 0 else base
                for a in node.names:
                    if a.name == "*":
                        s.wildcard = True
                        s.star_from.append(base)
                        continue
                    s.names[a.asname or a.name] = f"{base}.{a.name}" if base else a.name
        return s

    def _reexported(self, q: str, depth: int = 0) -> str:
        """Where an imported name is defined: `models.Note` is `models.notes.Note` when `models/__init__.py` imports
        it from `.notes`. Follows a chain of such imports; a name the repository defines or a module stays as is."""
        if depth >= MAX_DEPTH or q in self.defs or q in self.path_of_module:
            return q
        parts = q.split(".")
        for i in range(len(parts) - 1, 0, -1):
            module = ".".join(parts[:i])
            if module in self.path_of_module:
                scope = self.scopes[self.path_of_module[module]]
                target = scope.names.get(parts[i])
                if target is None and not parts[i].startswith("_"):  # `from .x import *` brings public names only
                    for star in scope.star_from:
                        found = self._reexported(".".join([star, *parts[i:]]), depth + 1)
                        if found in self.defs or found in self.path_of_module:
                            return found
                if target is None or target == ".".join(parts[:i + 1]):
                    return q
                return self._reexported(".".join([target, *parts[i + 1:]]), depth + 1)
        return q

    # ---- value flow ----
    def _value(self, scope: Scope, node, local_callables=None, local_instances=None):
        """What an expression evaluates to: ('callable', qname) | ('instance', class qname) | None."""
        if isinstance(node, (ast.Name, ast.Attribute)):
            name = dotted(node)
            if local_callables and name in local_callables:
                return "callable", local_callables[name]
            if local_instances and name in local_instances:
                return "instance", local_instances[name]
            q = self.qualify(scope, name)
            for _ in range(MAX_ALIAS):  # `b = param_func` at module level: follow the alias
                if q in self.assigns and isinstance(self.assigns[q][1], (ast.Name, ast.Attribute)):
                    alias_path, alias_value = self.assigns[q]
                    q = self.qualify(self.scopes[alias_path], dotted(alias_value))
                else:
                    break
            if q and q in self.defs and self.defs[q].kind in ("function", "method", "class"):
                return "callable", q
        elif isinstance(node, ast.Call):
            q = self.qualify(scope, dotted(node.func))
            if q in self.classes:
                return "instance", q
            if q in self.returned:
                return self.returned[q]
        return None

    def _returned(self) -> dict[str, tuple[str, str]]:
        """Function -> what its `return` statements give back, when all of them agree."""
        out = {}
        for q, d in self.defs.items():
            if d.kind not in ("function", "method"):
                continue
            values = set()
            for node in _own_nodes(d.node):
                if isinstance(node, ast.Return) and node.value is not None:
                    v = self._value(self.scopes[d.path], node.value)
                    values.add(v)
            if len(values) == 1 and None not in values:
                out[q] = values.pop()
        return out

    def _param_bindings(self) -> dict[str, dict[str, set]]:
        """Function -> parameter -> values passed at call sites in the repository."""
        out = {}
        for path, tree in self.trees.items():
            scope = self.scopes[path]
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                target = self.qualify(scope, dotted(node.func))
                if target in self.classes and "__init__" in self.methods.get(target, {}):
                    target = f"{target}.__init__"  # constructor arguments go to __init__
                d = self.defs.get(target or "")
                if d is None or d.kind not in ("function", "method"):
                    continue
                params = [a.arg for a in [*d.node.args.posonlyargs, *d.node.args.args]]
                if d.kind == "method" and params[:1] in (["self"], ["cls"]):
                    params = params[1:]
                pairs = list(zip(params, node.args)) + [(k.arg, k.value) for k in node.keywords if k.arg]
                for name, arg in pairs:
                    v = self._value(scope, arg)
                    if v is not None:
                        out.setdefault(target, {}).setdefault(name, set()).add(v)
        return out

    def flow(self, qname: str | None, body: list, scope: Scope, instances: dict) -> tuple[dict, dict]:
        """(instances, callables) known inside a function or module body, adding the value flow to `instances`."""
        instances = dict(instances)
        callables = {}
        for name, values in self.param_bindings.get(qname or "", {}).items():
            if len(values) == 1:
                kind, q = next(iter(values))
                (instances if kind == "instance" else callables).setdefault(name, q)
        for stmt in body:
            for node in [stmt, *_own_nodes(stmt)]:
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    if self._dynamic(scope, node.value, instances):
                        instances[node.targets[0].id] = DYNAMIC
                        continue
                    v = self._value(scope, node.value, callables, instances)
                    if v is not None:
                        (instances if v[0] == "instance" else callables).setdefault(node.targets[0].id, v[1])
        return instances, callables

    def _dynamic(self, scope: Scope, value, instances: dict) -> bool:
        """`importlib.import_module(...)`, or `getattr(x, ...)` / `x.attr` on such a value: known only at run time."""
        if isinstance(value, ast.Call):
            q = self.qualify(scope, dotted(value.func))
            if q in DYNAMIC_IMPORTS:
                return True
            if dotted(value.func) == "getattr" and value.args:
                return isinstance(value.args[0], ast.Name) and instances.get(value.args[0].id) == DYNAMIC
        return isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name) \
            and instances.get(value.value.id) == DYNAMIC

    def _external_origin(self) -> set[str]:
        out = set()
        for q, (path, value) in self.assigns.items():
            if isinstance(value, ast.Call):
                callee = self.qualify(self.scopes[path], dotted(value.func))
                if callee and not self.internal(callee):
                    out.add(q)
        return out

    # ---- queries ----
    def dynamic_names(self, scope: Scope) -> set[str]:
        """Local names (in this file) assigned from a dynamic import."""
        return {name for name, q in scope.names.items() if q in self.dynamic_origin}

    def internal(self, qname: str) -> bool:
        return qname in self.defs or qname in self.known_modules or qname.split(".")[0] in self.known_modules

    def qualify(self, scope: Scope, written: str | None) -> str | None:
        if not written:
            return None
        direct = scope.resolve(written)
        if direct:
            return direct
        head, _, rest = written.partition(".")
        head_q = scope.resolve(head)
        return f"{head_q}.{rest}" if head_q and rest else None

    def qual_node(self, scope: Scope, node) -> str | None:
        return self.qualify(scope, dotted(node))

    def resolve_type(self, scope: Scope, written: str | None, depth: int = 0) -> str | None:
        """Like qualify, but follows type aliases (`SessionDep = Annotated[Session, Depends(get_db)]`)."""
        q = self.qualify(scope, written)
        if q is None or depth >= MAX_ALIAS or q not in self.assigns:
            return q
        path, value = self.assigns[q]
        inner = value.id if isinstance(value, ast.Name) else (
            annotation_name(value) if isinstance(value, ast.Subscript) else None)
        return (self.resolve_type(self.scopes[path], inner, depth + 1) or q) if inner else q

    def bases_of(self, rec: ClassRec) -> list[str]:
        return [self.qualify(self.scopes[rec.path], b) or b for b in rec.bases]

    def subclass_of(self, qname: str, roots: set[str], depth: int = 0) -> bool:
        """True when the class inherits (through repository classes) from one of `roots`."""
        rec = self.classes.get(qname)
        if rec is None or depth > MAX_DEPTH:
            return False
        for b in self.bases_of(rec):
            if b in roots or self.subclass_of(b, roots, depth + 1):
                return True
        return False

    def find_method(self, class_q: str, method: str):
        """(owner ClassRec | None, ambiguous, reason, stopped_at_external_base). Breadth-first up the bases."""
        start = self.classes.get(class_q)
        if start is None:
            return None, False, f"không tìm thấy class '{class_q}' trong repo", False
        if method in start.methods:
            return start, False, None, False
        visited, level = {class_q}, [start]
        for _ in range(MAX_DEPTH):
            parents, external = [], []
            for child in level:
                for b in self.bases_of(child):
                    if b not in self.classes:
                        external.append(b)
                    elif b not in visited:
                        visited.add(b)
                        parents.append(self.classes[b])
            if not parents:
                if external:
                    return None, False, f"class cha '{external[0]}' nằm ngoài repo", True
                return None, False, f"không tìm thấy '{method}' trong cây kế thừa", False
            owners = [p for p in parents if method in p.methods]
            if owners:
                ambiguous = len(owners) > 1
                return owners[0], ambiguous, ("method có ở nhiều class cha; lấy cha khai báo trước" if ambiguous else None), False
            level = parents
        return None, False, f"cây kế thừa sâu quá {MAX_DEPTH} tầng", False

    # ---- variable types (4 forms, as in l3gen 0.1) ----
    def var_types(self, func, scope: Scope) -> dict[str, str]:
        types: dict[str, str] = {}
        args = func.args
        everything = [*args.posonlyargs, *args.args, *args.kwonlyargs]
        for a in everything:
            q = self.resolve_type(scope, annotation_name(a.annotation))
            if q:
                types[a.arg] = q
        positional = [*args.posonlyargs, *args.args]
        pairs = list(zip(positional[len(positional) - len(args.defaults):], args.defaults)) + \
            list(zip(args.kwonlyargs, args.kw_defaults))
        for a, default in pairs:
            if a.arg not in types and default is not None:
                q = self._depends_type(default, scope)
                if q:
                    types[a.arg] = q
        for node in ast.walk(func):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                q = self.resolve_type(scope, annotation_name(node.annotation))
                if q:
                    types.setdefault(node.target.id, q)
            elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                q = self.qualify(scope, dotted(node.value.func))
                if q and (q in self.classes or not self.internal(q)):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            types.setdefault(t.id, q)
        return types

    def _depends_type(self, default, scope: Scope) -> str | None:
        provider = depends_target(default)
        q = self.qualify(scope, dotted(provider)) if provider is not None else None
        if not q or q not in self.defs:
            return None
        return self.resolve_type(scope, annotation_name(self.returns.get(q)))

    def self_attrs(self, cls: ast.ClassDef, scope: Scope) -> dict[str, str]:
        out = {}
        init_q = f"{scope.module}.{cls.name}.__init__" if scope.module else f"{cls.name}.__init__"
        passed = {p: next(iter(v))[1] for p, v in self.param_bindings.get(init_q, {}).items()
                  if len(v) == 1 and next(iter(v))[0] == "instance"}
        for m in cls.body:
            if isinstance(m, FUNCS) and m.name == "__init__":
                for node in ast.walk(m):
                    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.value, ast.Name)                             and isinstance(node.targets[0], ast.Attribute) and isinstance(node.targets[0].value, ast.Name)                             and node.targets[0].value.id == "self" and node.value.id in passed:
                        out[node.targets[0].attr] = passed[node.value.id]
                for node in ast.walk(m):
                    target, value = (node.targets[0], node.value) if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                        else ((node.target, node.value) if isinstance(node, ast.AnnAssign) else (None, None))
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self" \
                            and isinstance(value, ast.Call):
                        q = self.qualify(scope, dotted(value.func))
                        if q:
                            out[target.attr] = q
        return out

    # ---- calls ----
    def resolve_call(self, call: ast.Call, scope: Scope, var_types: dict, self_attrs: dict,
                     self_class: str | None, callables: dict | None = None) -> Ref | None:
        written = dotted(call.func)
        if written is None:
            if isinstance(call.func, ast.Call) and dotted(call.func.func) == "getattr":
                return Ref(ast.unparse(call.func), None, False, reason="Tên thuộc tính chỉ biết lúc chạy (getattr)")
            if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Call):
                inner = call.func.value
                text = ast.unparse(call.func)
                if isinstance(inner.func, ast.Name) and var_types.get(inner.func.id) == DYNAMIC:
                    return Ref(text, None, False, reason="Class lấy từ module nạp động lúc chạy")
                v = self._value(scope, inner, callables, var_types)
                if v is not None and v[0] == "instance":
                    return self._method(text, v[1], call.func.attr, True)
            return None
        if var_types.get(written.partition(".")[0]) == DYNAMIC:
            return Ref(written, None, False, reason="Giá trị lấy từ module nạp động lúc chạy")
        head, _, tail = written.partition(".")
        if not tail:
            if callables and written in callables:
                return Ref(written, callables[written], True, inferred=True,
                           reason="Đích theo luồng giá trị: biến/tham số giữ hàm này")
            if written in BUILTINS and scope.resolve(written) is None:
                return None
            return self._plain(written, scope)
        if head in self.dynamic_names(scope):
            return Ref(written, None, False, reason="Module được nạp động lúc chạy (importlib.import_module)")
        receiver = var_types.get(head)
        inferred = receiver is not None and head != "self"
        if receiver is None and head == "self":
            attr = tail.partition(".")[0]
            receiver = self_attrs.get(attr) if "." in tail else self_class
            inferred = "." in tail
        if receiver:
            return self._method(written, receiver, tail.rpartition(".")[2], inferred)
        return self._via_scope(written, head, tail, scope)

    def _plain(self, written: str, scope: Scope) -> Ref:
        q = self.qualify(scope, written)
        if q is None:
            why = "file dùng 'import *'" if scope.wildcard else f"không tìm thấy khai báo của '{written}' trong repo"
            return Ref(written, None, False, reason=why)
        if q in self.defs and self.defs[q].kind != "assign":
            return Ref(written, q, True)
        if not self.internal(q):
            return Ref(written, None, False, reason=f"'{q}' {EXTERNAL}", external=True)
        return Ref(written, None, False, reason=f"không tìm thấy khai báo gọi được của '{q}' trong repo")

    def _method(self, written: str, class_q: str, method: str, inferred: bool) -> Ref:
        if class_q not in self.classes:
            ext = class_q in self.external_origin or not self.internal(class_q)
            return Ref(written, None, False, reason=f"'{class_q}' {EXTERNAL}" if ext else f"không tìm thấy class '{class_q}'",
                       external=ext)
        owner, ambiguous, reason, ext = self.find_method(class_q, method)
        if owner is None:
            return Ref(written, None, False, reason=reason, external=ext)
        return Ref(written, f"{owner.qname}.{method}", True, inferred=inferred or ambiguous,
                   reason=reason or ("Kiểu của biến được suy ra từ phép gán/chú thích/Depends" if inferred else None))

    def _via_scope(self, written: str, head: str, tail: str, scope: Scope) -> Ref:
        head_q = scope.resolve(head)
        if head_q is None:
            return Ref(written, None, False, reason="file dùng 'import *'" if scope.wildcard
                       else f"không biết '{head}' là gì trong file này")
        if head_q in self.external_origin or not self.internal(head_q):
            return Ref(written, None, False, reason=f"'{head_q}' {EXTERNAL}", external=True)
        if head_q in self.classes:
            return self._method(written, head_q, tail.rpartition(".")[2], False)
        full = f"{head_q}.{tail}"
        if full in self.defs and self.defs[full].kind != "assign":
            return Ref(written, full, True)
        if full in self.classes:
            return Ref(written, full, True)
        return Ref(written, None, False, reason=f"không tìm thấy khai báo của '{full}' trong repo")


DYNAMIC_IMPORTS = {"importlib.import_module", "__import__"}
DYNAMIC = "<dynamic>"


def _own_nodes(node):
    """Nodes inside `node`, not descending into nested function or class definitions."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        n = stack.pop()
        if isinstance(n, (*FUNCS, ast.ClassDef, ast.Lambda)):
            continue
        yield n
        stack.extend(ast.iter_child_nodes(n))


def depends_target(default):
    """`Depends(get_db)` -> node `get_db`; anything else -> None."""
    if isinstance(default, ast.Call) and (dotted(default.func) or "").split(".")[-1] == "Depends" and default.args:
        return default.args[0]
    return None
