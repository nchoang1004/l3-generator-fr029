"""Chuyển IAM sang dạng node và cạnh (bước 4c).

Chỉ đọc IAM đã hoàn chỉnh. Không đọc lại source, không dùng AI, không thêm thông
tin nào không có trong IAM (SPEC mục 5.2).

Hai lần chạy trên cùng IAM phải cho ra file giống hệt từng byte. Vì vậy ID được
tạo từ dữ liệu có sẵn, không dùng số tự tăng hay thứ tự duyệt cây.
"""

from l3gen.models.graph import ApplicationBoundary, GraphEdge, GraphNode, RepositoryGraph
from l3gen.models.iam import IntermediateArchitectureModel
from l3gen.models.semantic import DefinitionFact, ExpressionIR, ImportFact, InheritanceFact

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


def _class_id(service: str, path: str, qualified_name: str) -> str:
    return f"class:{service}:{path}:{qualified_name}"


def _application_id(object_id: str) -> str:
    return f"application:{object_id}"


def _unresolved_id(service: str, path: str, line: int, name: str) -> str:
    return f"unresolved:{service}:{path}:{line}:{name}"


def build_graph(iam: IntermediateArchitectureModel) -> RepositoryGraph:
    nodes: dict[str, GraphNode] = {}
    edges: set[tuple[str, str, str, bool]] = set()
    edge_facts = {}
    edge_locations = {}

    def add_node(node: GraphNode) -> str:
        nodes.setdefault(node.id, node)
        return node.id

    def add_edge(source: str, target: str, kind: str, resolved: bool, fact_id=None, location=None) -> None:
        key = (source, kind, target, resolved)
        edges.add(key)
        if fact_id:
            edge_facts.setdefault(key, set()).add(fact_id)
        location = location or (nodes[source].location if source in nodes else None)
        if location:
            where = _source_location(location)
            edge_locations.setdefault(key, {})[(where.file, where.line_start, where.line_end)] = where

    # Node Module cho mọi file có thực thể.
    for module in iam.semantic_program.modules:
        add_node(
            GraphNode(
                id=_module_id("python", module.file),
                type="Module",
                label=module.file,
                location=None,
            )
        )
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
    for fact in iam.semantic_program.all_facts():
        if not isinstance(fact, DefinitionFact) or fact.symbol_kind != "class":
            continue
        location = _source_location(fact.location)
        node_id = add_node(
            GraphNode(
                id=_class_id("python", fact.location.file, fact.qualified_name),
                type="Class",
                label=fact.qualified_name,
                location=location,
            )
        )
        by_symbol[("python", fact.qualified_name)] = node_id

    # Kế thừa class: resolve bằng import/symbol trong chính module.
    for module in iam.semantic_program.modules:
        imports = {
            fact.local_name: fact.imported_symbol
            for fact in module.facts
            if isinstance(fact, ImportFact)
        }
        local_classes = {
            fact.name: fact.qualified_name
            for fact in module.facts
            if isinstance(fact, DefinitionFact) and fact.symbol_kind == "class"
        }
        for fact in module.facts:
            if not isinstance(fact, InheritanceFact):
                continue
            source = by_symbol.get(("python", fact.class_symbol))
            if source is None:
                continue
            for symbol in iam.resolution.class_bases.get(fact.class_symbol, []):
                target = by_symbol.get(("python", symbol))
                resolved = target is not None
                if target is None:
                    target = add_node(
                        GraphNode(
                            id=_class_id("external", "?", symbol),
                            type="Class",
                            label=symbol,
                            location=None,
                        )
                    )
                add_edge(source, target, "inherits", resolved, fact.id, fact.location)
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
            for target, resolved in _reference_targets(
                ref, function.service, function.location, by_symbol, add_node
            ):
                add_edge(source, target, ref.relation, resolved, ref.call_fact_id, ref.location)

    # Cạnh reads_writes: hàm nào chạm tới bảng nào.
    entity_nodes = {
        (e.service, e.location.file, e.class_name): _entity_id(e.service, e.location.file, e.class_name)
        for e in iam.entities
    }
    for function in iam.functions:
        source = _function_id(function.service, function.module, function.qualified_name)
        for ref in function.entity_refs:
            target = entity_nodes.get((function.service, ref.resolved_module, ref.name))
            if target is not None:
                add_edge(source, target, ref.relation, ref.resolved)
                # Giữ cạnh tổng hợp để output V1 vẫn đọc được; V2 dùng reads/writes.
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
            for target, resolved in _reference_targets(
                ref, route.service, route.location, by_symbol, add_node
            ):
                add_edge(route_id, target, ref.relation, resolved, ref.call_fact_id, ref.location)

    # Object application/router và quan hệ đăng ký/mount do adapter V2 tạo.
    for application in iam.framework_analysis.objects:
        label = application.labels[0] if application.labels else application.type_symbol
        add_node(
            GraphNode(
                id=_application_id(application.object_id),
                type="Application",
                label=label,
                location=_source_location(application.location),
            )
        )
    routes_by_registration = {}
    for route in iam.routes:
        key = (route.location.file, route.location.line_start, route.handler_symbol)
        routes_by_registration.setdefault(key, []).append(route)
    for operation in iam.framework_analysis.operations:
        if operation.kind in ("AttachRouter", "MountApplication"):
            for parent in operation.parent_object_ids:
                for child in operation.child_object_ids:
                    add_edge(
                        _application_id(parent),
                        _application_id(child),
                        "mounts",
                        operation.status == "resolved",
                        operation.id,
                        operation.location,
                    )
        elif operation.kind == "RegisterEndpoint":
            matching_routes = [route for symbol in operation.endpoint_symbols
                               for route in routes_by_registration.get(
                                   (operation.location.file, operation.location.line_start, symbol), [])]
            for parent in operation.parent_object_ids:
                for route in matching_routes:
                    add_edge(
                        _application_id(parent),
                        _route_id(
                            route.service,
                            route.location.file,
                            route.method,
                            route.path,
                            route.handler_function,
                        ),
                        "registers",
                        operation.status == "resolved",
                        operation.id,
                        operation.location,
                    )

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
        add_edge(caller, host_id, "calls_external", call.completeness == "full", location=call.location)

    # Import được lấy trực tiếp từ Common Semantic IR, không quét source lần nữa.
    module_files = {module.module: module.file for module in iam.semantic_program.modules}
    for module in iam.semantic_program.modules:
        source = _module_id("python", module.file)
        for fact in module.facts:
            if not isinstance(fact, ImportFact):
                continue
            imported_module = _known_module(fact.imported_symbol, module_files)
            if imported_module:
                target = _module_id("python", module_files[imported_module])
                resolved = True
            else:
                target = add_node(
                    GraphNode(
                        id=_module_id("external", fact.imported_symbol),
                        type="Module",
                        label=fact.imported_symbol,
                        location=None,
                    )
                )
                resolved = False
            add_edge(source, target, "imports", resolved, fact.id, fact.location)

    boundaries = _application_boundaries(iam)
    # Call ở module/class body cũng thuộc graph, ví dụ app = FastAPI().
    classes = {fact.qualified_name for fact in iam.semantic_program.all_facts()
               if isinstance(fact, DefinitionFact) and fact.symbol_kind == "class"}
    for call in iam.resolution.calls:
        if call.caller_symbol:
            continue
        source = _module_id("python", call.location.file)
        for symbol in call.targets:
            constructs = symbol in classes or any(
                value.kind == "instance" and value.type_symbol == symbol for value in call.result_values
            )
            target = by_symbol.get(("python", symbol))
            if target is None:
                target = add_node(GraphNode(
                    id=(_class_id if constructs else _function_id)("python", "?", symbol),
                    type="Class" if constructs else "Function", label=symbol, location=None,
                ))
            add_edge(source, target, "constructs" if constructs else "calls",
                     call.status == "resolved", call.call_fact_id, call.location)
    return RepositoryGraph(
        nodes=sorted(nodes.values(), key=lambda n: n.id),
        edges=[
            GraphEdge(source_id=s, target_id=t, type=k, resolved=r,
                      fact_ids=sorted(edge_facts.get((s,k,t,r), ())),
                      locations=[value for _, value in sorted(edge_locations.get((s,k,t,r), {}).items())])
            for s, k, t, r in sorted(edges)
        ],
        application_boundaries=boundaries,
    )


def _handler_node(route, by_symbol: dict[tuple[str, str], str]) -> str | None:
    """Tìm node của hàm xử lý route, khớp theo tên cuối của tên đầy đủ."""
    if route.handler_symbol:
        return by_symbol.get((route.service, route.handler_symbol))
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


def _reference_targets(ref, service: str, location, by_symbol, add_node):
    symbols = ref.candidate_symbols or ([ref.resolved_symbol] if ref.resolved_symbol else [])
    if symbols:
        result = []
        for symbol in symbols:
            known = by_symbol.get((service, symbol))
            if known is None:
                node_type = "Class" if ref.relation == "constructs" else "Function"
                maker = _class_id if node_type == "Class" else _function_id
                known = add_node(
                    GraphNode(
                        id=maker(service, ref.resolved_module or "?", symbol),
                        type=node_type,
                        label=symbol,
                        location=None,
                    )
                )
            result.append((known, ref.status == "resolved" and len(symbols) == 1))
        return result
    return [(_reference_target(ref, service, location, by_symbol, add_node), False)]


def _source_location(location):
    from l3gen.models.iam import SourceLocation

    return SourceLocation(
        file=location.file,
        line_start=location.line_start,
        line_end=location.line_end,
    )


def _known_module(symbol: str, module_files: dict[str, str]) -> str | None:
    parts = symbol.split(".")
    for length in range(len(parts), 0, -1):
        candidate = ".".join(parts[:length])
        if candidate in module_files:
            return candidate
    return None


def _static_symbol(
    expression: ExpressionIR,
    imports: dict[str, str],
    local_classes: dict[str, str],
) -> str | None:
    if expression.kind == "name":
        name = expression.name or expression.text
        return local_classes.get(name) or imports.get(name)
    if expression.kind == "attribute" and expression.base is not None:
        base = _static_symbol(expression.base, imports, local_classes)
        return f"{base}.{expression.attribute}" if base else None
    return None


def _application_boundaries(iam: IntermediateArchitectureModel) -> list[ApplicationBoundary]:
    child_ids = {
        child
        for operation in iam.framework_analysis.operations
        if operation.kind in ("AttachRouter", "MountApplication")
        for child in operation.child_object_ids
    }
    application_types = {"fastapi.FastAPI", "starlette.applications.Starlette"}
    roots = [
        item
        for item in iam.framework_analysis.objects
        if item.type_symbol in application_types and item.object_id not in child_ids
    ]
    if not roots:
        return [
            ApplicationBoundary(
                id="application-boundary:unknown",
                status="unknown",
                reason=(
                    "chưa có đủ bằng chứng về application gốc; folder và nhóm ngôn ngữ "
                    "không được tự coi là service"
                ),
            )
        ]
    return [
        ApplicationBoundary(
            id=f"application-boundary:{item.object_id}",
            status="candidate",
            application_node_id=_application_id(item.object_id),
            entrypoint_file=item.location.file,
            evidence=[
                f"{item.location.file}:{item.location.line_start} tạo {item.type_symbol}",
                "object này không được mount làm con của application khác",
            ],
            reason=(
                "đây là application gốc theo quan hệ framework; chưa khẳng định là "
                "service triển khai độc lập nếu thiếu Docker/Kubernetes/process config"
            ),
        )
        for item in roots
    ]
