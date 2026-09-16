"""FastAPI/Starlette adapter V2, chỉ đọc Semantic IR và kết quả resolver."""

from __future__ import annotations

from collections import defaultdict

from l3gen.core.semantics.registry import OperationModel, SemanticRegistry
from l3gen.models.framework import (
    FrameworkAnalysis,
    FrameworkObject,
    RegistrationOperation,
)
from l3gen.models.iam import APIRoute, FunctionNode, SourceLocation
from l3gen.models.resolution import AbstractValue, ResolvedCall, ResolutionResult
from l3gen.models.semantic import (
    AssignmentFact,
    CallFact,
    DecoratorFact,
    ExpressionIR,
    ScopeFact,
    SemanticProgram,
)

_ROUTER_TYPES = {
    "fastapi.FastAPI",
    "fastapi.applications.FastAPI",
    "fastapi.APIRouter",
    "fastapi.routing.APIRouter",
    "starlette.applications.Starlette",
}
_MAX_MOUNT_DEPTH = 20


def analyze_fastapi(
    program: SemanticProgram,
    resolution: ResolutionResult,
    registry: SemanticRegistry,
) -> FrameworkAnalysis:
    facts = program.all_facts()
    calls = {fact.id: fact for fact in facts if isinstance(fact, CallFact)}
    resolved = {item.call_fact_id: item for item in resolution.calls}
    values = resolution.values_by_slot
    scopes = {fact.scope_id: fact for fact in facts if isinstance(fact, ScopeFact)}

    objects: dict[str, FrameworkObject] = {}
    for call_id, item in resolved.items():
        source = calls[call_id]
        prefix, prefix_literal = _text(_keyword_or_none(source, "prefix"))
        for value in item.result_values:
            if not _is_router(value) or value.value != f"allocation:{call_id}":
                continue
            objects.setdefault(
                value.value,
                FrameworkObject(
                    object_id=value.value,
                    type_symbol=value.type_symbol or "?",
                    prefix=prefix,
                    prefix_is_literal=prefix_literal,
                    location=source.location,
                ),
            )

    # Gắn các tên biến làm nhãn đọc được; object identity vẫn lấy từ allocation site.
    for fact in facts:
        if not isinstance(fact, AssignmentFact) or fact.target.kind != "name":
            continue
        name = fact.target.name or fact.target.text
        slot = f"binding:{fact.scope_id}:{name}:{fact.id}"
        scope = scopes.get(fact.scope_id)
        label = f"{scope.qualified_name}.{name}" if scope else name
        for value in values.get(slot, []):
            if value.value in objects and label not in objects[value.value].labels:
                objects[value.value].labels.append(label)

    decorator_owner = _decorator_owners(facts)
    operations: list[RegistrationOperation] = []
    dropped: list[str] = []
    for call_id, item in resolved.items():
        call = calls[call_id]
        for target in item.targets:
            model = registry.operations.get(target)
            if model is None:
                continue
            operation = _operation_from_call(
                call, item, model, target, values, decorator_owner.get(call_id)
            )
            if not operation.parent_object_ids:
                dropped.append(
                    f"{call.location.file}:{call.location.line_start} "
                    f"không xác định được object nhận {call.callee.text}"
                )
            operations.append(operation)

    # Starlette Route được khai báo trước, sau đó truyền qua routes=[...].
    templates = {
        value.value: (calls[item.call_fact_id], item)
        for item in resolution.calls for value in item.result_values
        if value.kind == "instance" and value.type_symbol == "starlette.routing.Route"
    }
    for call_id, item in resolved.items():
        app_ids = sorted({value.value for value in item.result_values if _is_router(value)})
        routes_slot = item.keyword_slots.get("routes")
        if not app_ids or routes_slot is None:
            continue
        for container in values.get(routes_slot, []):
            if container.kind != "container":
                continue
            for value in values.get(f"items:{container.value}", []):
                template = templates.get(value.value)
                if template is None:
                    continue
                source, route_call = template
                model = OperationModel(
                    "starlette.routing.Route", "RegisterEndpoint",
                    positional={"path": 0, "endpoint": 1},
                    keywords={"path": "path", "endpoint": "endpoint", "methods": "methods"},
                )
                operation = _operation_from_call(source, route_call, model, model.symbol, values, None)
                operation.id += f":attached:{call_id}"
                operation.parent_object_ids = app_ids
                operation.conditions.extend(calls[call_id].conditions)
                # Starlette tự thêm HEAD khi function endpoint có GET.
                if "GET" in operation.methods and "HEAD" not in operation.methods:
                    operation.methods.append("HEAD")
                operations.append(operation)

    return FrameworkAnalysis(
        registry_version=registry.version,
        objects=sorted(objects.values(), key=lambda item: item.object_id),
        operations=sorted(operations, key=lambda item: item.id),
        dropped_operations=sorted(set(dropped)),
    )


def materialize_routes(
    analysis: FrameworkAnalysis,
    functions: list[FunctionNode],
    service: str = "python",
) -> tuple[list[APIRoute], list[str]]:
    objects = {item.object_id: item for item in analysis.objects}
    parents: dict[str, list[RegistrationOperation]] = defaultdict(list)
    endpoints: list[RegistrationOperation] = []
    for operation in analysis.operations:
        if operation.kind in ("AttachRouter", "MountApplication"):
            for child in operation.child_object_ids:
                parents[child].append(operation)
        elif operation.kind == "RegisterEndpoint":
            endpoints.append(operation)

    functions_by_symbol = {item.qualified_name: item for item in functions}
    routes: list[APIRoute] = []
    dropped = list(analysis.dropped_operations)
    for endpoint in endpoints:
        if not endpoint.endpoint_symbols:
            dropped.append(
                f"{endpoint.location.file}:{endpoint.location.line_start} "
                "không xác định được hàm xử lý route"
            )
            continue
        for parent in endpoint.parent_object_ids:
            chains = _prefix_chains(parent, objects, parents)
            if not chains:
                chains = [([], ["không lần được chuỗi mount (vòng lặp hoặc quá sâu)"], True)]
            for pieces, conditions, chain_partial in chains:
                endpoint_piece = (endpoint.path or "", endpoint.path_is_literal)
                path = _join_path([*pieces, endpoint_piece])
                for handler in endpoint.endpoint_symbols:
                    function = functions_by_symbol.get(handler)
                    notes: list[str] = []
                    if not endpoint.methods:
                        dropped.append(f"{endpoint.location.file}:{endpoint.location.line_start}: {endpoint.reason or 'chưa xác định methods'}")
                    if chain_partial or not endpoint.path_is_literal:
                        notes.append("đường dẫn có phần phụ thuộc runtime")
                    all_conditions = [*conditions, *endpoint.conditions]
                    if all_conditions:
                        notes.append("chỉ đăng ký khi " + " và ".join(all_conditions))
                    if endpoint.reason:
                        notes.append(endpoint.reason)
                    if endpoint.status != "resolved":
                        notes.append(endpoint.reason or f"call có trạng thái {endpoint.status}")
                    for method in endpoint.methods:
                        routes.append(
                            APIRoute(
                                service=service,
                                method=method,
                                path=path,
                                handler_function=handler.rsplit(".", 1)[-1],
                                handler_symbol=handler,
                                calls=list(function.calls) if function else [],
                                confidence="exact",
                                completeness="partial" if notes else "full",
                                reason="; ".join(dict.fromkeys(notes)) or None,
                                location=SourceLocation(
                                    file=endpoint.location.file,
                                    line_start=endpoint.location.line_start,
                                    line_end=endpoint.location.line_end,
                                ),
                            )
                        )
    routes.sort(key=lambda item: (item.path, item.method, item.handler_symbol or ""))
    return routes, sorted(set(dropped))


def _operation_from_call(
    call: CallFact,
    resolved: ResolvedCall,
    model: OperationModel,
    target: str,
    values: dict[str, list[AbstractValue]],
    decorator_owner: str | None,
) -> RegistrationOperation:
    parent_ids = _object_ids(resolved.receiver_slot, values)
    child_slot = _operand_slot(resolved, model, "child")
    endpoint_slot = _operand_slot(resolved, model, "endpoint")
    child_ids = _object_ids(child_slot, values)
    endpoints = _symbols(endpoint_slot, values)
    if model.operation == "RegisterDecorator" and decorator_owner:
        endpoints = [decorator_owner]

    path_key = "prefix" if model.operation == "AttachRouter" else "path"
    path_expr = _operand_expression(call, model, path_key)
    path, path_literal = _text(path_expr)
    methods = [model.http_method] if model.http_method else _methods(
        _operand_expression(call, model, "methods")
    )
    kind = "RegisterEndpoint" if model.operation == "RegisterDecorator" else model.operation
    reason = resolved.reason
    if kind == "RegisterEndpoint" and not methods:
        if _operand_expression(call, model, "methods") is None:
            methods = ["GET"]
        else:
            reason = _append_reason(reason, "methods phụ thuộc runtime; chưa tạo route cụ thể")
    if len(parent_ids) > 1 or len(child_ids) > 1 or len(endpoints) > 1:
        reason = _append_reason(reason, "có nhiều object/endpoint có thể đúng")
    if kind in ("AttachRouter", "MountApplication") and not child_ids:
        reason = _append_reason(reason, "không xác định được object con")
    if kind == "RegisterEndpoint" and not endpoints:
        reason = _append_reason(reason, "không xác định được endpoint")
    return RegistrationOperation(
        id=f"framework-op:{call.id}:{target}",
        kind=kind,
        framework_symbol=target,
        parent_object_ids=parent_ids,
        child_object_ids=child_ids,
        endpoint_symbols=endpoints,
        path=path,
        path_is_literal=path_literal,
        methods=[method for method in methods if method],
        conditions=list(call.conditions),
        status="candidates" if reason and resolved.status == "resolved" else resolved.status,
        evidence=list(resolved.evidence),
        reason=reason,
        location=call.location,
    )


def _decorator_owners(facts) -> dict[str, str]:
    calls = [fact for fact in facts if isinstance(fact, CallFact) and fact.context == "decorator"]
    decorators = {
        (fact.location.file, fact.location.line_start, fact.expression.text): fact.owner_symbol
        for fact in facts if isinstance(fact, DecoratorFact)
    }
    found: dict[str, str] = {}
    for call in calls:
        owner = decorators.get((call.location.file, call.location.line_start, call.expression_text))
        if owner:
            found[call.id] = owner
    return found


def _object_ids(slot: str | None, values: dict[str, list[AbstractValue]]) -> list[str]:
    if slot is None:
        return []
    return sorted({value.value for value in values.get(slot, []) if _is_router(value)})


def _symbols(slot: str | None, values: dict[str, list[AbstractValue]]) -> list[str]:
    if slot is None:
        return []
    return sorted(
        {
            value.value
            for value in values.get(slot, [])
            if value.kind == "symbol" and value.symbol_kind in ("function", "method")
        }
    )


def _is_router(value: AbstractValue) -> bool:
    return value.kind == "instance" and value.type_symbol in _ROUTER_TYPES


def _operand_slot(
    resolved: ResolvedCall, model: OperationModel, semantic_name: str
) -> str | None:
    keyword = model.keywords.get(semantic_name)
    if keyword and keyword in resolved.keyword_slots:
        return resolved.keyword_slots[keyword]
    position = model.positional.get(semantic_name)
    if position is not None and position < len(resolved.argument_slots):
        return resolved.argument_slots[position]
    return None


def _operand_expression(
    call: CallFact, model: OperationModel, semantic_name: str
) -> ExpressionIR | None:
    keyword = model.keywords.get(semantic_name)
    if keyword and keyword in call.keywords:
        return call.keywords[keyword]
    position = model.positional.get(semantic_name)
    if position is not None and position < len(call.arguments):
        return call.arguments[position]
    return None


def _keyword_or_none(call: CallFact, name: str) -> ExpressionIR | None:
    return call.keywords.get(name)


def _text(expression: ExpressionIR | None) -> tuple[str | None, bool]:
    if expression is None:
        return None, True
    if expression.kind == "literal" and isinstance(expression.literal, str):
        return expression.literal, True
    if (expression.kind == "formatted_string" or (expression.kind == "binary" and expression.operator == "Add")) and expression.elements:
        pieces = [_text(item) for item in expression.elements]
        if all(text is not None for text, _ in pieces):
            return "".join(text or "" for text, _ in pieces), all(ok for _, ok in pieces)
    return "{" + expression.text + "}", False


def _methods(expression: ExpressionIR | None) -> list[str]:
    if expression is None:
        return []
    candidates = expression.elements if expression.kind in ("list", "tuple") else [expression]
    result: list[str] = []
    for candidate in candidates:
        text, literal = _text(candidate)
        if text and literal and text.upper() in {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT"}:
            result.append(text.upper())
    return result


def _prefix_chains(
    object_id: str,
    objects: dict[str, FrameworkObject],
    parents: dict[str, list[RegistrationOperation]],
    depth: int = 0,
    seen: frozenset[str] = frozenset(),
) -> list[tuple[list[tuple[str, bool]], list[str], bool]]:
    if depth > _MAX_MOUNT_DEPTH or object_id in seen:
        return []
    current = objects.get(object_id)
    own = [(current.prefix, current.prefix_is_literal)] if current and current.prefix else []
    links = parents.get(object_id, [])
    if not links:
        is_application = current and current.type_symbol in {
            "fastapi.FastAPI", "fastapi.applications.FastAPI", "starlette.applications.Starlette"
        }
        notes = [] if is_application else ["chưa thấy router gắn vào application gốc"]
        return [(own, notes, not is_application or any(not literal for _, literal in own))]
    chains: list[tuple[list[tuple[str, bool]], list[str], bool]] = []
    for link in links:
        link_piece = [(link.path, link.path_is_literal)] if link.path else []
        for parent in link.parent_object_ids:
            for upper, conditions, partial in _prefix_chains(
                parent, objects, parents, depth + 1, seen | {object_id}
            ):
                chains.append(
                    (
                        [*upper, *link_piece, *own],
                        [*conditions, *link.conditions],
                        partial or link.status != "resolved" or not link.path_is_literal,
                    )
                )
    return chains


def _join_path(pieces: list[tuple[str, bool]]) -> str:
    texts = [text.strip("/") for text, _ in pieces if text.strip("/")]
    joined = "/" + "/".join(texts) if texts else "/"
    if pieces and pieces[-1][0].endswith("/") and joined != "/":
        joined += "/"
    return joined


def _append_reason(reason: str | None, addition: str) -> str:
    return f"{reason}; {addition}" if reason else addition
