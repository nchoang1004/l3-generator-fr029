"""Tìm API route của FastAPI và ghép đường dẫn đầy đủ (bước 3a).

Đường dẫn cuối cùng nằm rải ở ba chỗ khác nhau, không chỗ nào có đủ:

    main.py    app.include_router(orders_router, prefix="/api/v1")
    orders.py  router = APIRouter(prefix="/orders")
    orders.py  @router.post("/{order_id}/confirm")

    ->  POST /api/v1/orders/{order_id}/confirm

Cách làm: gom ba loại dữ kiện đó lại, dựng cây gắn router, rồi đi từ mỗi route
ngược lên gốc và nối các mảnh đường dẫn.
"""

import ast
from dataclasses import dataclass, field

from l3gen.languages.python.literals import TextValue, keyword_of, read_text
from l3gen.languages.python.parser import ParsedFile
from l3gen.languages.python.resolution import FUNCTION_NODES, Resolver, dotted_name
from l3gen.models.iam import APIRoute, Reference, SourceLocation

HTTP_METHODS = ("get", "post", "put", "delete", "patch")
ROUTER_FACTORIES = ("APIRouter", "FastAPI")
MAX_ROUTER_DEPTH = 10


@dataclass
class RouterObject:
    """Một biến giữ APIRouter() hoặc FastAPI()."""

    qualified_name: str
    rel_path: str
    prefix: TextValue | None


@dataclass
class Mount:
    """Một lần gắn con vào cha, qua include_router() hoặc mount()."""

    parent: str
    child: str
    prefix: TextValue | None
    condition: str | None = None
    """Điều kiện của khối `if` bao ngoài, nếu có.

    `if settings.ENV == "dev": api.include_router(private)` nghĩa là route bên trong
    `private` chỉ tồn tại ở một số môi trường. Không ghi lại thì tài liệu liệt kê nó
    như route bình thường — lỗi số 3 đo được ở Mốc 7."""


@dataclass
class RouteCandidate:
    """Một hàm có decorator route, chưa ghép prefix của các tầng trên."""

    router: str
    method: str
    path: TextValue
    handler: str
    rel_path: str
    line_start: int
    line_end: int
    calls: list[Reference] = field(default_factory=list)


def _last_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _qualify_expr(node: ast.expr | None, scope, resolver: Resolver) -> str | None:
    written = dotted_name(node) if node is not None else None
    return resolver.qualify(scope, written) if written else None


def collect_routers(
    files: list[ParsedFile], resolver: Resolver, module_of: dict[str, str]
) -> dict[str, RouterObject]:
    """Tìm mọi biến giữ APIRouter() hoặc FastAPI()."""
    routers: dict[str, RouterObject] = {}
    for parsed in files:
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""
        if resolver.tables.for_file(parsed.rel_path) is None:
            continue
        for node in parsed.tree.body:
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
                continue
            if _last_name(node.value.func) not in ROUTER_FACTORIES:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    qname = f"{prefix}{target.id}"
                    routers[qname] = RouterObject(
                        qualified_name=qname,
                        rel_path=parsed.rel_path,
                        prefix=read_text(keyword_of(node.value, "prefix")),
                    )
    return routers


def _read_include_router(node: ast.Call) -> tuple[ast.expr | None, TextValue | None]:
    """parent.include_router(child, prefix="/x") -> (nút con, prefix)."""
    child = node.args[0] if node.args else keyword_of(node, "router")
    return child, read_text(keyword_of(node, "prefix"))


def _read_mount(node: ast.Call) -> tuple[ast.expr | None, TextValue | None] | None:
    """parent.mount("/x", app=child) -> (nút con, prefix).

    Đây là `mount()` của Starlette, khác `include_router()` của FastAPI: đường dẫn
    là tham số vị trí thứ nhất, ứng dụng con là tham số thứ hai hoặc keyword `app`.
    Bỏ qua khi con không phải một cái tên — `mount("/", StaticFiles(...))` gắn thư
    mục tĩnh chứ không gắn router, không có route nào để ghép.
    """
    if not node.args:
        return None
    prefix = read_text(node.args[0])
    if prefix is None:
        return None
    child = node.args[1] if len(node.args) > 1 else keyword_of(node, "app")
    return child, prefix


def _walk_with_conditions(body: list[ast.stmt], conditions: tuple[str, ...] = ()):
    """Duyệt thân module, mang theo điều kiện của mọi khối `if` bao ngoài.

    Dùng thay `ast.walk` vì `ast.walk` làm phẳng cây: nó thấy lời gọi nhưng mất
    thông tin lời gọi đó có nằm trong `if` hay không.
    """
    for node in body:
        if isinstance(node, ast.If):
            test = ast.unparse(node.test)
            yield from _walk_with_conditions(node.body, (*conditions, test))
            yield from _walk_with_conditions(node.orelse, (*conditions, f"không ({test})"))
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                yield inner, conditions


def collect_mounts(files: list[ParsedFile], resolver: Resolver) -> list[Mount]:
    """Tìm mọi lần gắn router hoặc ứng dụng con, đã đổi tên biến sang tên đầy đủ."""
    mounts: list[Mount] = []
    for parsed in files:
        scope = resolver.tables.for_file(parsed.rel_path)
        if scope is None:
            continue
        for node, conditions in _walk_with_conditions(parsed.tree.body):
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr == "include_router":
                found = _read_include_router(node)
            elif node.func.attr == "mount":
                found = _read_mount(node)
            else:
                continue
            if found is None:
                continue
            child_node, prefix = found
            parent = _qualify_expr(node.func.value, scope, resolver)
            child = _qualify_expr(child_node, scope, resolver) if child_node else None
            if parent and child:
                mounts.append(
                    Mount(parent, child, prefix, " và ".join(conditions) or None)
                )
    return mounts


def _read_route_decorator(decorator: ast.expr, scope, resolver: Resolver):
    """Decorator kiểu @router.post("/x") -> (router, method, đường dẫn)."""
    if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
        return None
    if decorator.func.attr not in HTTP_METHODS:
        return None

    router_qname = _qualify_expr(decorator.func.value, scope, resolver)
    if router_qname is None:
        return None

    path_node = decorator.args[0] if decorator.args else keyword_of(decorator, "path")
    path = read_text(path_node) or TextValue("", True)
    return router_qname, decorator.func.attr.upper(), path


def collect_route_candidates(
    files: list[ParsedFile], resolver: Resolver, module_of: dict[str, str]
) -> list[RouteCandidate]:
    """Tìm mọi hàm có decorator route."""
    from l3gen.languages.python.common.callgraph import calls_inside

    candidates: list[RouteCandidate] = []
    for parsed in files:
        scope = resolver.tables.for_file(parsed.rel_path)
        if scope is None:
            continue
        for node in parsed.tree.body:
            if not isinstance(node, FUNCTION_NODES):
                continue
            for decorator in node.decorator_list:
                found = _read_route_decorator(decorator, scope, resolver)
                if found is None:
                    continue
                router_qname, method, path = found
                candidates.append(
                    RouteCandidate(
                        router=router_qname,
                        method=method,
                        path=path,
                        handler=node.name,
                        rel_path=parsed.rel_path,
                        line_start=node.lineno,
                        line_end=getattr(node, "end_lineno", node.lineno) or node.lineno,
                        calls=calls_inside(node, scope, resolver),
                    )
                )
    return candidates


@dataclass
class Chain:
    """Một đường đi từ router lên gốc: các mảnh prefix, và điều kiện gặp dọc đường."""

    pieces: list[TextValue | None]
    conditions: list[str] = field(default_factory=list)


def _prefix_chains(
    router_qname: str,
    routers: dict[str, RouterObject],
    parents: dict[str, list[Mount]],
    depth: int = 0,
    seen: frozenset[str] = frozenset(),
) -> list[Chain]:
    """Mọi đường đi từ router này ngược lên gốc, kèm prefix từng chặng."""
    if depth > MAX_ROUTER_DEPTH or router_qname in seen:
        return []

    router = routers.get(router_qname)
    own: list[TextValue | None] = [router.prefix] if router else []

    # Không dừng sớm ở `FastAPI()`. Một app vẫn có thể được gắn vào app khác bằng
    # `app.mount("/api/v1", app=api)` — dừng ở đây thì mọi route mất tiền tố đó mà
    # vẫn bị ghi nhãn "đã đầy đủ". Nếu app thật sự là gốc thì nó không có parent,
    # và nhánh dự phòng bên dưới trả về đúng `own`.
    chains: list[Chain] = []
    for mount in parents.get(router_qname, []):
        upper_chains = _prefix_chains(
            mount.parent, routers, parents, depth + 1, seen | {router_qname}
        )
        for upper in upper_chains:
            conditions = list(upper.conditions)
            if mount.condition:
                conditions.append(mount.condition)
            chains.append(Chain([*upper.pieces, mount.prefix, *own], conditions))

    if not chains and router is not None:
        # Router có thật nhưng chưa thấy ai gắn nó vào đâu. Vẫn xuất route, tính
        # đường dẫn từ chính nó — thà thiếu tiền tố còn hơn giấu cả route đi.
        chains.append(Chain(own))
    return chains


def _join_path(pieces: list[TextValue]) -> str:
    parts = [p.text.strip("/") for p in pieces if p.text.strip("/")]
    joined = "/" + "/".join(parts) if parts else "/"
    if pieces and pieces[-1].text.endswith("/") and joined != "/":
        joined += "/"
    return joined


def _to_route(candidate: RouteCandidate, chain: Chain, service: str) -> APIRoute:
    pieces = [p for p in [*chain.pieces, candidate.path] if p is not None]
    unresolved = [p.text for p in pieces if not p.is_literal]

    # Hai lý do khác nhau khiến route chưa đầy đủ, gộp vào cùng một `reason`:
    # đường dẫn còn phần chỉ biết lúc chạy, và route chỉ được đăng ký có điều kiện.
    notes = []
    if unresolved:
        notes.append("đường dẫn có phần phụ thuộc lúc chạy: " + ", ".join(unresolved))
    if chain.conditions:
        notes.append(
            "chỉ được đăng ký khi " + " và ".join(chain.conditions)
            + " — route này không tồn tại ở mọi môi trường"
        )

    return APIRoute(
        service=service,
        method=candidate.method,
        path=_join_path(pieces),
        handler_function=candidate.handler,
        calls=candidate.calls,
        confidence="exact",
        completeness="partial" if notes else "full",
        reason="; ".join(notes) or None,
        location=SourceLocation(
            file=candidate.rel_path,
            line_start=candidate.line_start,
            line_end=candidate.line_end,
        ),
    )


def build_routes(
    candidates: list[RouteCandidate],
    routers: dict[str, RouterObject],
    mounts: list[Mount],
    service: str,
) -> tuple[list[APIRoute], list[str]]:
    """Ghép prefix của mọi tầng vào từng route.

    Một router gắn vào hai chỗ khác nhau thì sinh ra hai route — đúng như lúc chạy.
    Trả về kèm danh sách route không lần được về gốc.
    """
    parents: dict[str, list[Mount]] = {}
    for mount in mounts:
        parents.setdefault(mount.child, []).append(mount)

    routes: list[APIRoute] = []
    dropped: list[str] = []

    for candidate in candidates:
        chains = _prefix_chains(candidate.router, routers, parents)
        if not chains:
            dropped.append(f"{candidate.method} {candidate.path.text} ({candidate.rel_path})")
            continue
        for chain in chains:
            routes.append(_to_route(candidate, chain, service))

    routes.sort(key=lambda r: (r.path, r.method, r.location.file, r.location.line_start))
    return routes, dropped


def extract_routes(
    files: list[ParsedFile], resolver: Resolver, module_of: dict[str, str], service: str
) -> tuple[list[APIRoute], list[str]]:
    routers = collect_routers(files, resolver, module_of)
    mounts = collect_mounts(files, resolver)
    candidates = collect_route_candidates(files, resolver, module_of)
    return build_routes(candidates, routers, mounts, service)
