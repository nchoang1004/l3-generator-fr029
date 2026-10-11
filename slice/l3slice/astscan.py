"""Small static readings of Python source that the FR-029 checker relies on (no code is executed).

The checker never takes facts from here: these functions only decide whether a claimed line can hold what the agent
says (a call's URL argument, the module a call goes through) and which lines the agent must account for.
"""
from __future__ import annotations

import ast
import io
import re
import tokenize
from collections import Counter

HTTP_LIBS = {"httpx", "requests", "aiohttp"}
HTTP_VERBS = {"get", "post", "put", "patch", "delete", "head", "options", "request", "stream", "send"}
CLIENT_CLASSES = {"AsyncClient", "Client", "ClientSession", "Session"}
CLIENT_NAME = re.compile(r"client|session|http", re.I)


# Python 3.14 (PEP 758) allows `except A, B:` without parentheses; older parsers need them. Lines stay in place.
PEP758 = re.compile(r"^([ \t]*except\*?[ \t]+)([^():#\r\n]+,[^():#\r\n]+?)([ \t]*:)", re.M)


def parse(source: str):
    try:
        return ast.parse(source)
    except (SyntaxError, ValueError):
        pass
    fixed = PEP758.sub(lambda m: m.group(1) + "(" + m.group(2) + ")" + m.group(3), source)
    try:
        return ast.parse(fixed) if fixed != source else None
    except (SyntaxError, ValueError):
        return None


def name_of(node) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def dotted(node) -> str | None:
    """`B.inject` for an attribute chain, the bare name for a Name."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def root_name(node) -> str | None:
    """`requests` for requests.Session().get, `c` for c.get."""
    while isinstance(node, (ast.Attribute, ast.Call, ast.Subscript)):
        node = node.func if isinstance(node, ast.Call) else node.value
    return node.id if isinstance(node, ast.Name) else None


def string_rows(source: str) -> set[int]:
    """Lines that are wholly inside a multi-line string: its middle lines, and its last line when nothing but
    closing punctuation follows the string. A line where code follows the closing quotes stays code."""
    rows = set()
    lines = source.split("\n")
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.STRING and tok.end[0] > tok.start[0]:
                rows |= set(range(tok.start[0] + 1, tok.end[0]))
                after = lines[tok.end[0] - 1][tok.end[1]:] if tok.end[0] - 1 < len(lines) else ""
                if not after.strip(" \t),]};:"):
                    rows.add(tok.end[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return set()
    return rows


_IMPORTS = {}  # id(tree) -> (tree, result): the same trees are asked many times


def imports(tree) -> dict[str, tuple[str, str | None]]:
    """local name -> (module, imported name or None for `import module`). A relative import keeps its dots
    (`from . import requests` -> (".requests", None)), so a project module never reads as an HTTP library."""
    hit = _IMPORTS.get(id(tree))
    if hit is not None and hit[0] is tree:
        return hit[1]
    if len(_IMPORTS) > 20000:
        _IMPORTS.clear()
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out[a.asname or a.name.split(".")[0]] = (a.name, None)
        elif isinstance(n, ast.ImportFrom) and n.module:
            for a in n.names:
                out[a.asname or a.name] = ("." * (n.level or 0) + n.module, a.name)
        elif isinstance(n, ast.ImportFrom):  # from . import items: the module items, found next to the file
            for a in n.names:
                out[a.asname or a.name] = ("." * (n.level or 0) + a.name, None)
    _IMPORTS[id(tree)] = (tree, out)
    return out


class ModuleIndex:
    """Readable files by module name, built once: a/b.py and a/b/__init__.py answer `a.b`, also below a folder
    (src layouts)."""

    def __init__(self, files):
        self.files = set(files)
        self.by_tail = {}
        for f in self.files:
            if not f.endswith(".py"):
                continue
            mod = f[:-3].removesuffix("/__init__").split("/")
            for i in range(len(mod)):
                self.by_tail.setdefault(".".join(mod[i:]), []).append(f)
        self.cache = {}

    def find(self, module: str, current: str) -> str | None:
        module = module.lstrip(".")  # relative: looked up next to the file first, like any name
        key = (module, current.rsplit("/", 1)[0] if "/" in current else "")
        if key not in self.cache:
            hits = self.by_tail.get(module, [])
            folder = key[1]
            near = [h for h in hits if h.startswith(folder)] if folder else []
            exact = [h for h in hits if h[:-3].removesuffix("/__init__").replace("/", ".") == module]
            pick = exact or near or hits
            self.cache[key] = pick[0] if len(pick) == 1 else (sorted(pick, key=len)[0] if exact else None)
        return self.cache[key]


class HttpScan:
    """Which names in one file are HTTP clients or HTTP functions (for the suspect scan and the claim checks)."""

    def __init__(self, source: str, tree, imported_clients: set[str] = frozenset(),
                 imported_makers: set[str] = frozenset(), imported_providers: set[str] = frozenset(),
                 state_clients: set[str] = frozenset(), qualified_clients: dict = None, imported_aliases: dict = None):
        """`qualified_clients`: clients.wire -> library, for `import clients`; `imported_aliases`: Annotated aliases
        of other files that hold a client (Wire = Annotated[httpx.Client, Depends(get_wire)]) -> library."""
        imp = imports(tree)
        self.modules = {local for local, (mod, name) in imp.items() if name is None and mod.split(".")[0] in HTTP_LIBS}
        self.module_of = {local: mod.split(".")[0] for local, (mod, name) in imp.items()
                          if name is None and mod.split(".")[0] in HTTP_LIBS}
        self.functions = {local for local, (mod, name) in imp.items()
                          if name and mod.split(".")[0] in HTTP_LIBS and name.lower() in HTTP_VERBS}
        # what each such name really calls: from requests import post as send_it -> post, requests
        self.function_verb = {local: name.lower() for local, (mod, name) in imp.items() if local in self.functions}
        self.function_lib = {local: mod.split(".")[0] for local, (mod, name) in imp.items() if local in self.functions}
        # a client class only when it comes from an HTTP library: `from httpx import Client as C`, httpx.Client();
        # a bare `Session` may be SQLAlchemy's
        self.makers = {local for local, (mod, name) in imp.items()
                       if name and mod.split(".")[0] in HTTP_LIBS and name in CLIENT_CLASSES} | set(imported_makers)
        self.capable = bool(self.modules or self.functions or self.makers or imported_clients or imported_providers
                            or state_clients or qualified_clients or imported_aliases
                            or re.search(r"\.(?:httpx|requests|aiohttp)\.(?:AsyncClient|Client|ClientSession|Session)\b",
                                         source))  # _host.aiohttp.ClientSession(...)
        self.maker_lib = {local: mod.split(".")[0] for local, (mod, name) in imp.items()
                          if name and mod.split(".")[0] in HTTP_LIBS and name in CLIENT_CLASSES}
        if isinstance(imported_makers, dict):  # InventoryClient of another file -> the library it subclasses
            self.maker_lib.update({k: v for k, v in imported_makers.items() if v})
        for n in ast.walk(tree):  # class Transport(httpx.Client): a client too, of that library
            if isinstance(n, ast.ClassDef) and any(name_of(b) in self.makers or self._library_class(b) for b in n.bases):
                self.makers.add(n.name)
                lib = next((self.maker_lib.get(name_of(b)) or (self.module_of.get(root_name(b)) if self._library_class(b)
                                                                else None) for b in n.bases), None)
                if lib:
                    self.maker_lib[n.name] = lib
        self.source = source
        self.tree = tree
        self.depends_clients = set()  # parameters filled by Depends(helper yielding a client)
        self._functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        # client name -> the library its constructor comes from, when one can be told
        self.client_lib = {k: v for k, v in imported_clients.items() if v} if isinstance(imported_clients, dict) else {}
        self.qualified = dict(qualified_clients or {})  # clients.wire -> library
        self.client_aliases = dict(imported_aliases or {})  # Wire = Annotated[httpx.Client, ...] -> library
        self.bound_attrs = {}  # self.fetch = self._wire.get: attribute -> the client method it holds
        self.containers = {}  # clients = {"a": httpx.Client()}: dict name -> library of its clients
        self.client_attrs = set(state_clients)  # attributes bound to a client (self.client, app.state.wire)
        self.clients = set(self.modules) | set(imported_clients)
        maker_functions = set(imported_providers)  # helpers of other files that hand out a client
        self.maker_function_lib = dict(imported_providers) if isinstance(imported_providers, dict) else {}
        if not self.capable:  # no HTTP library nor imported client: nothing here can make or hold a client
            self.maker_functions, self.assigned_other, self.attr_other = maker_functions, set(), set()
            return
        for _ in range(3):  # helpers returning a client, and names bound to them, until nothing changes
            maker_functions |= {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                and self._returns_client(n, maker_functions)}
            self._aliases(tree, maker_functions)
            for n in ast.walk(tree):  # @property def transport(self): return self._wire
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and any(name_of(d) in ("property", "cached_property") for d in n.decorator_list) \
                        and (self.typed_client(n.returns) or any(
                            isinstance(r, ast.Return) and r.value is not None and (
                                self.makes(r.value, maker_functions) or (isinstance(r.value, ast.Attribute)
                                                                          and r.value.attr in self.client_attrs))
                            for r in ast.walk(n))):
                    self.client_attrs.add(n.name)
            for n in ast.walk(tree):  # self._factory = factory or self._default_client: calling it makes a client
                if isinstance(n, ast.Assign) and (self._names_maker(n.value, maker_functions) or (
                        isinstance(n.value, ast.Call) and name_of(n.value.func) == "partial" and n.value.args
                        and name_of(n.value.args[0]) in maker_functions)):
                    maker_functions |= {name_of(t) for t in n.targets if name_of(t)}
            before = len(self.clients)
            self._bind(tree, maker_functions)
            if len(self.clients) == before:
                break
        self.maker_functions = maker_functions
        for n in ast.walk(tree):  # fetch = wire.get: calling `fetch(...)` is an HTTP call
            if isinstance(n, ast.Assign) and isinstance(n.value, (ast.IfExp, ast.BoolOp)):  # a.post if x else a.put
                sides = n.value.values if isinstance(n.value, ast.BoolOp) else [n.value.body, n.value.orelse]
                side = next((x for x in sides if isinstance(x, ast.Attribute) and x.attr in HTTP_VERBS
                             and (name_of(x.value) in self.clients or root_name(x) in self.modules)), None)
                if side is not None:
                    n = ast.Assign(targets=n.targets, value=side)
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute) and n.value.attr in HTTP_VERBS \
                    and (name_of(n.value.value) in self.clients or root_name(n.value) in self.modules):
                for t in n.targets:
                    if isinstance(t, ast.Attribute):
                        self.bound_attrs[t.attr] = n.value
                    if isinstance(t, ast.Name):
                        self.functions.add(t.id)
                        self.function_verb[t.id] = n.value.attr
                        lib = self.lib_of(n.value.value) or self.module_of.get(root_name(n.value))
                        if lib:
                            self.function_lib[t.id] = lib
        kinds = {}  # (class, attribute) -> kinds of the values `self.attribute` is set to inside that class
        for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
            for n in ast.walk(cls):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target] if isinstance(n, ast.AnnAssign) \
                    and n.value is not None else []
                for t in targets:
                    if isinstance(t, ast.Attribute) and name_of(t.value) == "self":
                        kinds.setdefault((cls.name, t.attr), set()).add(
                            "client" if self.makes(n.value, maker_functions)
                            or (isinstance(n, ast.AnnAssign) and self.typed_client(n.annotation)) else _plain(n.value))
        self.attr_other = {k for k, v in kinds.items() if v == {"other"}}
        self.assigned_other = {t.id for n in ast.walk(tree) if isinstance(n, ast.Assign)
                               and not self.makes(n.value, maker_functions) for t in n.targets if isinstance(t, ast.Name)
                               and t.id not in self.clients}

    def _names_maker(self, expr, maker_functions) -> bool:
        """The value names (does not call) a client maker: get_wire, self._default_client, httpx.AsyncClient, also
        as one side of `a or b` / `a if c else b`."""
        sides = expr.values if isinstance(expr, ast.BoolOp) else [expr.body, expr.orelse] if isinstance(expr, ast.IfExp) \
            else [expr]
        return any(isinstance(x, (ast.Name, ast.Attribute)) and (
            name_of(x) in maker_functions or (isinstance(x, ast.Name) and x.id in self.makers) or self._library_class(x))
            for x in sides)

    def _aliases(self, tree, maker_functions):
        """Wire = Annotated[httpx.Client, Depends(get_wire)] at module level: a parameter typed Wire is a client."""
        for n in tree.body:
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Subscript) and name_of(n.value.value) == "Annotated" \
                    and isinstance(n.value.slice, ast.Tuple):
                provider = next((name_of(e.args[0]) for e in n.value.slice.elts[1:] if isinstance(e, ast.Call)
                                 and name_of(e.func) == "Depends" and e.args and name_of(e.args[0]) in maker_functions), None)
                if provider or self.typed_client(n.value.slice.elts[0]):
                    lib = self.annotation_lib(n.value.slice.elts[0]) or self.maker_function_lib.get(provider)
                    for t in n.targets:
                        if isinstance(t, ast.Name):
                            self.client_aliases[t.id] = lib

    def makes(self, expr, maker_functions=frozenset()) -> bool:
        """The expression creates (or hands out) an HTTP client."""
        if expr is None:
            return False
        if isinstance(expr, ast.Name):
            return expr.id in self.clients
        if isinstance(expr, ast.Subscript):  # clients["primary"]
            return name_of(expr.value) in self.containers
        if isinstance(expr, ast.Attribute):  # wire = self._wire, wire = clients.wire, request.app.state.http
            return ((name_of(expr.value) in ("self", "cls") or name_of(expr.value) == "state")
                    and expr.attr in self.client_attrs) or dotted(expr) in self.qualified
        if isinstance(expr, ast.Await):
            return self.makes(expr.value, maker_functions)
        if isinstance(expr, (ast.BoolOp, ast.IfExp)):  # c = given or httpx.Client(); c = a if x else b
            sides = expr.values if isinstance(expr, ast.BoolOp) else [expr.body, expr.orelse]
            return any(self.makes(x, maker_functions) for x in sides)
        if not isinstance(expr, ast.Call):
            return False
        f = expr.func
        if (isinstance(f, ast.Name) and f.id in self.makers) or self._library_class(f) or name_of(f) in maker_functions:
            return True
        if isinstance(f, ast.Attribute) and f.attr == "session" and root_name(f) in self.modules:
            return True  # requests.session()
        if isinstance(f, ast.Attribute) and f.attr in ("enter_context", "enter_async_context") and expr.args:
            return self.makes(expr.args[0], maker_functions)  # AsyncExitStack hands the client back
        if isinstance(f, ast.Attribute):  # httpx.Client().get(url).json(): a method's result is not the client
            return False
        return any(isinstance(a, ast.Call) and self.makes(a, maker_functions) for a in expr.args)  # closing(httpx.Client())

    def lib_of(self, expr) -> str | None:
        """The HTTP library an expression's client comes from: httpx.Client(), C() with C imported from httpx,
        a name bound to such a client."""
        if expr is None:
            return None
        if isinstance(expr, ast.Name):
            return self.client_lib.get(expr.id) or self.module_of.get(expr.id)
        if isinstance(expr, ast.Subscript) and name_of(expr.value) in self.containers:
            return self.containers[name_of(expr.value)]
        if isinstance(expr, ast.Attribute) and not isinstance(expr.value, ast.Call):  # self.client, clients.wire
            return self.qualified.get(dotted(expr)) or self.client_lib.get(expr.attr)
        for c in ast.walk(expr):
            if isinstance(c, ast.Call):
                f = c.func
                if isinstance(f, ast.Name) and f.id in self.maker_lib:
                    return self.maker_lib[f.id]
                if name_of(f) in getattr(self, "maker_function_lib", {}):  # self._get_client(), get_wire()
                    return self.maker_function_lib[name_of(f)]
                if self._library_class(f) or (isinstance(f, ast.Attribute) and f.attr == "session"):
                    return self.module_of.get(root_name(f))
        return None

    def typed_client(self, ann) -> bool:
        """The annotation names an HTTP client class: imported from an HTTP library (or a subclass of one), or
        reached through the module (httpx.AsyncClient). SQLAlchemy's `Session` is not one."""
        if ann is None:
            return False
        if isinstance(ann, ast.Constant) and isinstance(ann.value, str):
            try:
                return self.typed_client(ast.parse(ann.value, mode="eval").body)
            except SyntaxError:
                return False
        if isinstance(ann, ast.BinOp) and isinstance(ann.op, ast.BitOr):  # httpx.Client | None
            return self.typed_client(ann.left) or self.typed_client(ann.right)
        if isinstance(ann, ast.Subscript):  # Optional[Client], Annotated[Client, ...]; not dict[str, Client]
            elts = ann.slice.elts if isinstance(ann.slice, ast.Tuple) else [ann.slice]
            outer = name_of(ann.value)
            return outer in ("Optional", "Union", "Annotated") and any(
                self.typed_client(e) for e in (elts[:1] if outer == "Annotated" else elts))
        return (isinstance(ann, ast.Name) and (ann.id in self.makers or ann.id in self.client_aliases)) \
            or self._library_class(ann)

    def annotation_lib(self, ann) -> str | None:
        """The HTTP library a client annotation names: httpx.Client -> httpx, C imported from requests -> requests."""
        for n in ast.walk(ann) if ann is not None else []:
            if isinstance(n, ast.Name) and n.id in self.maker_lib:
                return self.maker_lib[n.id]
            if isinstance(n, ast.Name) and self.client_aliases.get(n.id):
                return self.client_aliases[n.id]
            if self._library_class(n):
                return self.module_of.get(root_name(n))
        return None

    def constructor(self, call) -> bool:
        """This very call builds or hands out a client: httpx.Client(), C(), get_wire(), requests.session()."""
        if not isinstance(call, ast.Call):
            return False
        f = call.func
        return (isinstance(f, ast.Name) and (f.id in self.makers or f.id in self.maker_functions)) \
            or (isinstance(f, ast.Attribute) and name_of(f.value) in ("self", "cls") and f.attr in self.maker_functions) \
            or self._library_class(f) \
            or (isinstance(f, ast.Attribute) and f.attr == "session" and root_name(f) in self.modules)

    def _library_class(self, node) -> bool:
        """httpx.Client, requests.Session, aiohttp.ClientSession reached through the module."""
        return isinstance(node, ast.Attribute) and node.attr in CLIENT_CLASSES and (
            root_name(node) in self.modules or name_of(node.value) in HTTP_LIBS)  # _host.aiohttp.ClientSession

    def _returns_client(self, fn, maker_functions) -> bool:
        if self.typed_client(fn.returns):
            return True
        local = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign) and self.makes(n.value, maker_functions):
                local |= {t.id for t in n.targets if isinstance(t, ast.Name)}
            if isinstance(n, (ast.With, ast.AsyncWith)):
                for item in n.items:
                    if isinstance(item.optional_vars, ast.Name) and self.makes(item.context_expr, maker_functions):
                        local.add(item.optional_vars.id)
        sources = {}
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign) and self.makes(n.value, maker_functions):
                sources.update({t.id: n.value for t in n.targets if isinstance(t, ast.Name)})
            if isinstance(n, (ast.With, ast.AsyncWith)):
                sources.update({i.optional_vars.id: i.context_expr for i in n.items if isinstance(i.optional_vars, ast.Name)
                                and self.makes(i.context_expr, maker_functions)})
        for n in ast.walk(fn):
            if isinstance(n, (ast.Return, ast.Yield)) and n.value is not None:
                if self.makes(n.value, maker_functions) or (isinstance(n.value, ast.Name) and n.value.id in local):
                    lib = self.lib_of(sources.get(n.value.id) if isinstance(n.value, ast.Name) else n.value)
                    if lib:  # remember which library the helper's client comes from
                        self.maker_function_lib.setdefault(fn.name, lib)
                    return True
        return False

    def _bind(self, tree, maker_functions):
        def add(t, source=None):
            name = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else None
            if isinstance(t, ast.Attribute):
                self.client_attrs.add(t.attr)
            if name:
                self.clients.add(name)
                lib = self.lib_of(source) if source is not None else None
                if lib:
                    self.client_lib.setdefault(name, lib)

        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and n.value.values and all(
                    self.makes(v, maker_functions) for v in n.value.values):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        self.containers[t.id] = self.lib_of(n.value.values[0])
            if isinstance(n, ast.Assign) and self.makes(n.value, maker_functions):
                for t in n.targets:
                    add(t, n.value)
            elif isinstance(n, ast.AnnAssign) and (self.makes(n.value, maker_functions) or self.typed_client(n.annotation)):
                add(n.target, n.value if self.makes(n.value, maker_functions) else None)
                if self.annotation_lib(n.annotation) and isinstance(n.target, ast.Name):
                    self.client_lib.setdefault(n.target.id, self.annotation_lib(n.annotation))
            elif isinstance(n, (ast.With, ast.AsyncWith)):
                for item in n.items:
                    if item.optional_vars is not None and self.makes(item.context_expr, maker_functions):
                        add(item.optional_vars, item.context_expr)
            elif isinstance(n, ast.arg) and self.typed_client(n.annotation):
                self.clients.add(n.arg)
                lib = self.annotation_lib(n.annotation)
                if lib:
                    self.client_lib.setdefault(n.arg, lib)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):  # wire=Depends(get_wire)
                args = n.args.posonlyargs + n.args.args
                pairs = list(zip(args, [None] * (len(args) - len(n.args.defaults)) + list(n.args.defaults))) + \
                    list(zip(n.args.kwonlyargs, n.args.kw_defaults))
                for arg, default in pairs:
                    exprs = [default] + (arg.annotation.slice.elts[1:] if isinstance(arg.annotation, ast.Subscript)
                                         and isinstance(arg.annotation.slice, ast.Tuple) else [])
                    provider = next((name_of(t) for e in exprs if isinstance(e, ast.Call) and name_of(e.func) == "Depends"
                                     for t in e.args[:1] + [k.value for k in e.keywords if k.arg == "dependency"]
                                     if name_of(t) in maker_functions), None)
                    if provider:
                        self.clients.add(arg.arg)
                        self.depends_clients.add(arg.arg)
                        if self.maker_function_lib.get(provider):
                            self.client_lib.setdefault(arg.arg, self.maker_function_lib[provider])

    def _enclosing(self, line: int):
        inside = [f for f in self._functions if f.lineno <= line <= (f.end_lineno or f.lineno)]
        return max(inside, key=lambda f: f.lineno) if inside else None

    def local_kind(self, call, name: str) -> str | None:
        """"client"/"other" when the function around the call binds `name` itself (c = httpx.Client(), c = {...},
        with ... as c, a parameter typed or filled as a client); None when the function does not say."""
        fn = self._enclosing(call.lineno)
        if fn is None:
            return None
        kinds = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
                kinds.add("client" if self.makes(n.value, self.maker_functions) else _plain(n.value))
            elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == name:
                kinds.add("client" if self.typed_client(n.annotation) or self.makes(n.value, self.maker_functions)
                          else "other")
            elif isinstance(n, (ast.With, ast.AsyncWith)):
                for item in n.items:
                    if isinstance(item.optional_vars, ast.Name) and item.optional_vars.id == name:
                        kinds.add("client" if self.makes(item.context_expr, self.maker_functions)
                                  else _plain(item.context_expr))
        for arg in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs:
            if arg.arg == name:
                if self.typed_client(arg.annotation) or name in self.depends_clients:
                    kinds.add("client")
                elif name_of(arg.annotation.value if isinstance(arg.annotation, ast.Subscript) else arg.annotation) in (
                        "dict", "Dict", "list", "List", "set", "Set", "tuple", "Tuple", "Mapping", "Sequence",
                        "str", "int", "float", "bool", "bytes"):
                    kinds.add("other")  # clients: dict[str, httpx.Client] holds clients, it is not one
        kinds.discard(None)
        return kinds.pop() if len(kinds) == 1 else None

    def other_attr(self, recv, call) -> bool:
        """`self.client` inside a class that only ever sets it to a plain value (self.client = {...})."""
        if not (isinstance(recv, ast.Attribute) and name_of(recv.value) == "self" and call is not None):
            return False
        inside = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)
                  and n.lineno <= call.lineno <= (n.end_lineno or n.lineno)]
        return bool(inside) and (max(inside, key=lambda n: n.lineno).name, recv.attr) in self.attr_other

    def super_client(self, recv, call) -> str | None:
        """`super()` inside a client subclass (class Signed(requests.Session): ... super().request(...)): that
        class's name; None otherwise."""
        if not (isinstance(recv, ast.Call) and name_of(recv.func) == "super" and call is not None):
            return None
        inside = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef) and n.name in self.makers
                  and n.lineno <= call.lineno <= (n.end_lineno or n.lineno)]
        return max(inside, key=lambda n: n.lineno).name if inside else None

    def receiver_lib(self, recv, call) -> str | None:
        """The library of a call's client, read first from the function around the call: two functions may each
        take a `wire` of another library."""
        fn = self._enclosing(call.lineno) if isinstance(recv, ast.Name) else None
        if fn is not None:
            libs = set()
            for arg in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs:
                if arg.arg == recv.id and self.typed_client(arg.annotation):
                    libs.add(self.annotation_lib(arg.annotation))
            for n in ast.walk(fn):
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == recv.id for t in n.targets) \
                        and not isinstance(n.value, ast.Name):
                    libs.add(self.lib_of(n.value))
                elif isinstance(n, (ast.With, ast.AsyncWith)):
                    libs |= {self.lib_of(i.context_expr) for i in n.items
                             if isinstance(i.optional_vars, ast.Name) and i.optional_vars.id == recv.id}
            if len(libs) == 1 and None not in libs:
                return libs.pop()
            if libs:
                return None  # bound here, to something whose library this file does not tell
        cls = self.super_client(recv, call)
        return self.maker_lib.get(cls) if cls else self.lib_of(recv)

    def _binds(self, call, name) -> bool:
        """The function around the call assigns `name` itself (to something this file cannot tell)."""
        fn = self._enclosing(call.lineno)
        if fn is not None and any(a.arg == name for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs):
            return True
        return fn is not None and any(
            (isinstance(n, (ast.Assign, ast.AnnAssign)) and any(isinstance(t, ast.Name) and t.id == name
                                                                 for t in (n.targets if isinstance(n, ast.Assign) else [n.target])))
            or (isinstance(n, (ast.With, ast.AsyncWith)) and any(isinstance(i.optional_vars, ast.Name)
                                                                  and i.optional_vars.id == name for i in n.items))
            for n in ast.walk(fn))

    def claim_client(self, recv, call=None) -> bool:
        """The receiver of a claimed call is a client this file shows: a local bound to one in the same function,
        an attribute bound to one (self.client), an HTTP module, or a client built in place. A `c` that is a
        client in another function, or a local `session`, does not vouch for this call."""
        if isinstance(recv, ast.Name):
            kind = self.local_kind(call, recv.id) if call is not None else None
            if kind:
                return kind == "client"
            if call is not None and self._binds(call, recv.id):  # client = redis.Redis() here, httpx elsewhere
                return False
            return recv.id in self.clients
        if isinstance(recv, ast.Attribute) and not isinstance(recv.value, ast.Call):
            if self.other_attr(recv, call):
                return False
            return recv.attr in self.client_attrs or root_name(recv) in self.modules or dotted(recv) in self.qualified
        if isinstance(recv, ast.Subscript):  # clients["primary"].get(...)
            return name_of(recv.value) in self.containers
        # httpx.Client().get(...), super().request(...) in a client subclass; not httpx.get(...).json().get(...)
        return self.constructor(recv) or self.super_client(recv, call) is not None

    def virtual_calls(self, tree, start: int, end: int) -> list:
        """The HTTP call a line makes without writing it: asyncio.to_thread(c.get, url) and self.fetch(url) with
        self.fetch = self._wire.get, rebuilt as c.get(url) at that place so the usual checks apply."""
        out = []
        for c in ast.walk(tree):
            if not isinstance(c, ast.Call) or not start <= c.lineno <= end:
                continue
            made = []
            for i, a in enumerate(c.args if name_of(c.func) != "partial" else []):  # partial(...) does not call yet
                if isinstance(a, ast.Attribute) and a.attr in HTTP_VERBS and (
                        name_of(a.value) in self.clients or root_name(a) in self.modules
                        or (isinstance(a.value, ast.Attribute) and a.value.attr in self.client_attrs)):
                    made.append(ast.Call(func=a, args=c.args[i + 1:], keywords=c.keywords))
            if isinstance(c.func, ast.Attribute) and c.func.attr in self.bound_attrs:
                made.append(ast.Call(func=self.bound_attrs[c.func.attr], args=c.args, keywords=c.keywords))
            for v in made:
                ast.copy_location(v, c)
                v.end_lineno, v.end_col_offset = c.end_lineno, c.end_col_offset
                out.append(v)
        return out

    def is_client(self, name: str) -> bool:
        """A known client, or an unknown name that reads like one (an untyped `session` parameter)."""
        return name in self.clients or (self.capable and name not in self.assigned_other
                                        and bool(CLIENT_NAME.search(name)))

    def http_lines(self, tree) -> Counter:
        """Line -> number of calls that may be HTTP there: client.verb(...), module.verb(...), an imported verb
        function. A name the enclosing function binds to something else (c = {...}) is not a client there."""
        out = Counter()
        for c in ast.walk(tree):
            if not isinstance(c, ast.Call):
                continue
            f = c.func
            if name_of(f) != "partial" and any(isinstance(a, ast.Attribute) and a.attr in HTTP_VERBS and (
                    name_of(a.value) in self.clients or root_name(a) in self.modules
                    or (isinstance(a.value, ast.Attribute) and a.value.attr in self.client_attrs)) for a in c.args):
                out[c.lineno] += 1  # the HTTP method is passed on, the call happens there
            if isinstance(f, ast.Attribute) and f.attr in HTTP_VERBS:
                base = f.value
                name = root_name(base) if not isinstance(base, (ast.Name, ast.Attribute)) else name_of(base)
                kind = self.local_kind(c, base.id) if isinstance(base, ast.Name) else None
                if kind == "other":
                    continue
                if isinstance(base, ast.Subscript):  # clients["primary"].get(...)
                    ok = name_of(base.value) in self.containers
                elif isinstance(base, ast.Call):  # a client built in place, super() of a client subclass; not .json()
                    ok = self.constructor(base) or self.super_client(base, c) is not None
                elif self.other_attr(base, c):
                    ok = False  # self.client = {...} in this class
                elif isinstance(base, ast.Attribute) and (base.attr in self.client_attrs or dotted(base) in self.qualified):
                    ok = True  # self.client.get(...), request.app.state.wire.get(...), clients.wire.get(...)
                else:
                    ok = kind == "client" or (name and self.is_client(name)) or root_name(base) in self.modules
                if ok:
                    out[f.end_lineno] += 1  # the line showing `.get(`, also when the receiver sits on the line above
            elif isinstance(f, ast.Name) and f.id in self.functions:
                out[c.lineno] += 1
            elif isinstance(f, ast.Attribute) and f.attr in self.bound_attrs:
                out[c.lineno] += 1  # self.fetch(url) with self.fetch = self._wire.get
            elif isinstance(f, ast.Call) and name_of(f.func) == "getattr" and len(f.args) >= 2 \
                    and (not isinstance(f.args[1], ast.Constant) or str(f.args[1].value).lower() in HTTP_VERBS) \
                    and (name_of(f.args[0]) in self.clients or root_name(f.args[0]) in self.modules):
                out[c.lineno] += 1  # getattr(wire, "get")(url), getattr(client, method)(path)
        return out


def _plain(expr) -> str | None:
    """"other" for a value that cannot be an HTTP client (a literal, a container, a comprehension, an f-string,
    arithmetic); None for a call or a name whose result the file does not show."""
    plain = (ast.Constant, ast.Dict, ast.List, ast.Set, ast.Tuple, ast.ListComp, ast.DictComp, ast.SetComp,
             ast.GeneratorExp, ast.JoinedStr, ast.BinOp, ast.Compare, ast.BoolOp)
    return "other" if isinstance(expr, plain) else None


def client_classes(tree) -> dict:
    """Classes of this module that subclass an HTTP client class (class InventoryClient(httpx.AsyncClient)) -> the
    library of that base."""
    imp = imports(tree)
    modules = {local: mod.split(".")[0] for local, (mod, name) in imp.items()
               if name is None and mod.split(".")[0] in HTTP_LIBS}
    lib_classes = {local: mod.split(".")[0] for local, (mod, name) in imp.items()
                   if name and mod.split(".")[0] in HTTP_LIBS and name in CLIENT_CLASSES}
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            for b in n.bases:
                if isinstance(b, ast.Name) and b.id in lib_classes:
                    out.setdefault(n.name, lib_classes[b.id])
                elif isinstance(b, ast.Attribute) and b.attr in CLIENT_CLASSES and root_name(b) in modules:
                    out.setdefault(n.name, modules[root_name(b)])
    return out


def module_clients(tree, source: str, scan=None) -> dict:
    """Names bound to an HTTP client at module level (client = httpx.Client()), importable by other files -> the
    client's library when known."""
    if not any(lib in source for lib in HTTP_LIBS):
        return {}
    scan = scan or HttpScan(source, tree)
    out = {t.id for n in tree.body if isinstance(n, ast.Assign) and scan.makes(n.value, scan.maker_functions)
           for t in n.targets if isinstance(t, ast.Name)}
    out |= {n.target.id for n in tree.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
            and (scan.makes(n.value, scan.maker_functions) or scan.typed_client(n.annotation))}
    return {name: scan.client_lib.get(name) for name in out}


def calls_at(tree, start: int, end: int, verbs=HTTP_VERBS, names=()) -> list:
    """Every call to an HTTP-like verb within [start, end], in reading order; `names` are local names of HTTP
    functions (fetch = wire.get, from httpx import get as fetch)."""
    found = [c for c in ast.walk(tree) if isinstance(c, ast.Call) and start <= c.lineno <= end
             and ((isinstance(c.func, ast.Attribute) and c.func.attr in verbs)
                  or (isinstance(c.func, ast.Name) and (c.func.id.lower() in verbs or c.func.id in names)))]
    return sorted(found, key=lambda c: (c.lineno, c.col_offset, -(c.end_col_offset or 0)))


def call_at(tree, start: int, end: int, verbs=HTTP_VERBS, prefer: str | None = None):
    """The call to an HTTP-like verb within [start, end]: the first whose verb is `prefer` (two calls can share a
    line), else the first one."""
    found = [c for c in ast.walk(tree) if isinstance(c, ast.Call) and start <= c.lineno <= end
             and ((isinstance(c.func, ast.Attribute) and c.func.attr in verbs)
                  or (isinstance(c.func, ast.Name) and c.func.id.lower() in verbs))]
    found.sort(key=lambda c: (c.lineno, c.col_offset))
    preferred = [c for c in found if prefer and call_verb(c) == prefer]
    return (preferred or found or [None])[0]


def call_verb(call, aliases=None) -> str:
    """The HTTP verb a call uses; `aliases` maps local function names to the verb they stand for."""
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return (aliases or {}).get(call.func.id, call.func.id.lower())


def returned_names(expr) -> set[str]:
    """Function names a factory may return: `return f`, `return a if flag else b`."""
    if isinstance(expr, ast.Name):
        return {expr.id}
    if isinstance(expr, ast.IfExp):
        return returned_names(expr.body) | returned_names(expr.orelse)
    return set()


SCALARS = {"str", "int", "float", "bool", "date", "datetime", "time", "UUID", "Decimal"}


def scalar(ann, enums=frozenset()) -> bool:
    """A scalar annotation (str, int | None, Optional[UUID], 'str', Literal['a', 'b'], an Enum of the snapshot):
    FastAPI reads it from the query string."""
    if isinstance(ann, ast.Constant) and isinstance(ann.value, str):
        try:
            return scalar(ast.parse(ann.value, mode="eval").body, enums)
        except SyntaxError:
            return False
    if isinstance(ann, ast.BinOp) and isinstance(ann.op, ast.BitOr):
        sides = [x for x in (ann.left, ann.right) if not (isinstance(x, ast.Constant) and x.value is None)]
        return bool(sides) and all(scalar(x, enums) for x in sides)  # int | None, int | str
    if isinstance(ann, ast.Subscript) and name_of(ann.value) == "Literal":
        return True
    if isinstance(ann, ast.Subscript) and name_of(ann.value) == "Union":  # Union[int, str], Union[str, None]
        members = ann.slice.elts if isinstance(ann.slice, ast.Tuple) else [ann.slice]
        members = [x for x in members if not (isinstance(x, ast.Constant) and x.value is None) and name_of(x) != "None"]
        return bool(members) and all(scalar(x, enums) for x in members)
    if isinstance(ann, ast.Subscript) and name_of(ann.value) in ("Optional", "Annotated"):
        inner = ann.slice.elts[0] if isinstance(ann.slice, ast.Tuple) else ann.slice
        return scalar(inner, enums)
    return name_of(ann) in SCALARS or name_of(ann) in enums
