"""Chuyển IAM sang dạng node và cạnh (bước 4c).

Chỉ đọc IAM đã hoàn chỉnh. Không đọc lại source, không dùng AI, không thêm thông
tin nào không có trong IAM (SPEC mục 5.2).

Hai lần chạy trên cùng IAM phải cho ra file giống hệt từng byte. Vì vậy ID được
tạo từ dữ liệu có sẵn, không dùng số tự tăng hay thứ tự duyệt cây.
"""

from l3gen.models.graph import GraphEdge, GraphNode, RepositoryGraph
from l3gen.models.iam import IntermediateArchitectureModel

_TABLE_UNKNOWN = "tên bảng chưa đọc được"


def _module_id(service: str, path: str) -> str:
    return f"module:{service}:{path}"


def _function_id(service: str, path: str, qualified_name: str) -> str:
    return f"function:{service}:{path}:{qualified_name}"


def _route_id(service: str, path: str, method: str, url: str, handler: str) -> str:
    return f"route:{service}:{path}:{method}:{url}:{handler}"


def _entity_id(service: str, path: str, class_name: str) -> str:
    return f"entity:{service}:{path}:{class_name}"


def _external_id(service: str, host: str) -> str:
    return f"external:{service}:{host}"


def _unresolved_id(service: str, path: str, line: int, name: str) -> str:
    return f"unresolved:{service}:{path}:{line}:{name}"


def build_graph(iam: IntermediateArchitectureModel) -> RepositoryGraph:
    nodes: dict[str, GraphNode] = {}
    edges: set[tuple[str, str, str, bool]] = set()

    def add_node(node: GraphNode) -> str:
        nodes.setdefault(node.id, node)
        return node.id

    def add_edge(source: str, target: str, kind: str, resolved: bool) -> None:
        edges.add((source, kind, target, resolved))

    # Node Module cho mọi file có thực thể.
    for function in iam.functions:
        add_node(
            GraphNode(
                id=_module_id(function.service, function.module),
                type="Module",
                label=function.module,
                location=None,
            )
        )

    # Node Function, và cạnh imports từ module chứa nó.
    by_symbol: dict[tuple[str, str], str] = {}
    for function in iam.functions:
        node_id = add_node(
            GraphNode(
                id=_function_id(function.service, function.module, function.qualified_name),
                type="Function",
                label=function.qualified_name,
                location=function.location,
            )
        )
        by_symbol[(function.service, function.qualified_name)] = node_id

    # Cạnh calls: mỗi cạnh ứng đúng một phần tử trong FunctionNode.calls.
    for function in iam.functions:
        source = _function_id(function.service, function.module, function.qualified_name)
        for ref in function.calls:
            target = _reference_target(ref, function.service, function.location, by_symbol, add_node)
            add_edge(source, target, "calls", ref.resolved)

    # Cạnh reads_writes: hàm nào chạm tới bảng nào.
    entity_nodes = {
        (e.service, e.class_name): _entity_id(e.service, e.location.file, e.class_name)
        for e in iam.entities
    }
    for function in iam.functions:
        source = _function_id(function.service, function.module, function.qualified_name)
        for ref in function.entity_refs:
            target = entity_nodes.get((function.service, ref.name))
            if target is not None:
                add_edge(source, target, "reads_writes", ref.resolved)

    # Node Route, cạnh exposes tới hàm xử lý.
    for route in iam.routes:
        route_id = add_node(
            GraphNode(
                id=_route_id(
                    route.service,
                    route.location.file,
                    route.method,
                    route.path,
                    route.handler_function,
                ),
                type="Route",
                label=f"{route.method} {route.path}",
                location=route.location,
            )
        )
        handler = _handler_node(route, by_symbol)
        if handler is not None:
            add_edge(route_id, handler, "exposes", True)
        for ref in route.calls:
            target = _reference_target(ref, route.service, route.location, by_symbol, add_node)
            add_edge(route_id, target, "calls", ref.resolved)

    # Node Entity, cạnh inherits tới class cha.
    for entity in iam.entities:
        entity_id = add_node(
            GraphNode(
                id=_entity_id(entity.service, entity.location.file, entity.class_name),
                type="Entity",
                label=f"{entity.class_name} ({entity.table_name or _TABLE_UNKNOWN})",
                location=entity.location,
            )
        )
        if entity.base_class is not None:
            target = _reference_target(
                entity.base_class, entity.service, entity.location, by_symbol, add_node
            )
            add_edge(entity_id, target, "inherits", entity.base_class.resolved)

    # Node ExternalHost, cạnh calls_external từ hàm gọi.
    for call in iam.external_calls:
        host_id = add_node(
            GraphNode(
                id=_external_id(call.service, call.url_or_host),
                type="ExternalHost",
                label=call.url_or_host,
                location=None,
            )
        )
        caller = by_symbol.get((call.service, call.caller_function))
        if caller is None:
            caller = add_node(
                GraphNode(
                    id=_module_id(call.service, call.location.file),
                    type="Module",
                    label=call.location.file,
                    location=None,
                )
            )
        add_edge(caller, host_id, "calls_external", True)

    return RepositoryGraph(
        nodes=sorted(nodes.values(), key=lambda n: n.id),
        edges=[
            GraphEdge(source_id=s, target_id=t, type=k, resolved=r)
            for s, k, t, r in sorted(edges)
        ],
    )


def _handler_node(route, by_symbol: dict[tuple[str, str], str]) -> str | None:
    """Tìm node của hàm xử lý route, khớp theo tên cuối của tên đầy đủ."""
    for (service, qualified_name), node_id in by_symbol.items():
        if service == route.service and qualified_name.split(".")[-1] == route.handler_function:
            return node_id
    return None


def _reference_target(ref, service: str, location, by_symbol, add_node) -> str:
    """Node đích của một tham chiếu.

    Tham chiếu chưa nối được vẫn có node riêng kiểu Unresolved — không được âm
    thầm loại khỏi graph (SPEC mục 5.2).
    """
    if ref.resolved and ref.resolved_symbol:
        known = by_symbol.get((service, ref.resolved_symbol))
        if known is not None:
            return known
        return add_node(
            GraphNode(
                id=_function_id(service, ref.resolved_module or "?", ref.resolved_symbol),
                type="Function",
                label=ref.resolved_symbol,
                location=None,
            )
        )
    return add_node(
        GraphNode(
            id=_unresolved_id(service, location.file, location.line_start, ref.name),
            type="Unresolved",
            label=ref.name,
            location=location,
        )
    )
