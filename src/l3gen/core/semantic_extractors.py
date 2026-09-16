"""Tạo các model kiến trúc chung từ Common Semantic IR và resolver V2."""

from __future__ import annotations

from l3gen.core.semantics.registry import SemanticRegistry
from l3gen.models.iam import (
    DBEntity,
    FunctionNode,
    Reference,
    SourceLocation,
    UnresolvedReference,
)
from l3gen.models.resolution import ResolvedCall, ResolutionResult
from l3gen.models.semantic import DefinitionFact, SemanticProgram


def extract_functions_v2(
    program: SemanticProgram,
    resolution: ResolutionResult,
    registry: SemanticRegistry,
    service: str = "python",
) -> tuple[list[FunctionNode], list[UnresolvedReference]]:
    definitions = {
        fact.qualified_name: fact
        for fact in program.all_facts()
        if isinstance(fact, DefinitionFact)
    }
    functions = {
        symbol: FunctionNode(
            service=service,
            qualified_name=symbol,
            name=fact.name,
            class_name=_owner_class(symbol, definitions),
            module=fact.location.file,
            calls=[],
            location=_location(fact.location),
        )
        for symbol, fact in definitions.items()
        if fact.symbol_kind in ("function", "async_function")
    }
    unresolved: list[UnresolvedReference] = []

    for call in resolution.calls:
        function = functions.get(call.caller_symbol or "")
        if function is None:
            continue
        reference = _reference(call, definitions, registry)
        function.calls.append(reference)
        if call.status in ("unresolved", "runtime"):
            unresolved.append(
                UnresolvedReference(
                    description=(
                        f"{function.qualified_name} gọi '{call.written_callee}': "
                        f"{call.reason or call.status}"
                    ),
                    location=_location(call.location),
                )
            )

    result = sorted(functions.values(), key=lambda item: (item.module, item.qualified_name))
    for function in result:
        function.calls.sort(key=lambda item: (item.name, item.resolved_symbol or ""))
    return result, unresolved


def attach_entity_references(
    functions: list[FunctionNode],
    entities: list[DBEntity],
    program: SemanticProgram,
    resolution: ResolutionResult,
) -> None:
    """Nối class bảng xuất hiện trong argument vào function chứa call đó."""
    definitions = [
        fact
        for fact in program.all_facts()
        if isinstance(fact, DefinitionFact) and fact.symbol_kind == "class"
    ]
    by_class_location = {(fact.name, fact.location.file): fact.qualified_name for fact in definitions}
    entity_symbols = {
        by_class_location[(entity.class_name, entity.location.file)]: entity
        for entity in entities if (entity.class_name, entity.location.file) in by_class_location
    }
    by_function = {item.qualified_name: item for item in functions}
    for call in resolution.calls:
        function = by_function.get(call.caller_symbol or "")
        if function is None:
            continue
        slots = [*call.argument_slots, *call.keyword_slots.values()]
        referenced = {
            value.value if value.kind == "symbol" else value.type_symbol
            for slot in slots
            for value in resolution.values_by_slot.get(slot, [])
            if (
                (value.kind == "symbol" and value.value in entity_symbols)
                or (value.kind == "instance" and value.type_symbol in entity_symbols)
            )
        }
        existing = {ref.resolved_symbol for ref in function.entity_refs}
        for symbol in sorted(referenced - existing):
            entity = entity_symbols[symbol]
            # Chỉ tách read/write khi biết API của session. Tên ngắn `get`
            # hoặc `delete` ở object chưa rõ không chứng minh thao tác database.
            targets = set(call.targets)
            if targets & {f"sqlalchemy.orm.Session.{verb}" for verb in ("add", "delete", "merge")}:
                relation = "writes"
            elif targets & {f"sqlalchemy.orm.Session.{verb}" for verb in ("query", "get")}:
                relation = "reads"
            else:
                relation = "reads_writes"
            function.entity_refs.append(
                Reference(
                    name=entity.class_name,
                    resolved_module=entity.location.file,
                    resolved=True,
                    resolved_symbol=symbol,
                    confidence="exact",
                    completeness="full",
                    reason=None,
                    status="resolved",
                    relation=relation,
                )
            )


def _reference(
    call: ResolvedCall,
    definitions: dict[str, DefinitionFact],
    registry: SemanticRegistry,
) -> Reference:
    single = call.targets[0] if len(call.targets) == 1 else None
    definition = definitions.get(single or "")
    relation = "constructs" if call.targets and all(
        _is_class(target, definitions, registry) for target in call.targets
    ) else "calls"
    return Reference(
        name=call.written_callee,
        resolved_module=definition.location.file if definition else None,
        resolved=call.status == "resolved",
        resolved_symbol=single,
        confidence="exact" if call.status == "resolved" else None,
        completeness="full" if call.status == "resolved" else "partial",
        reason=call.reason,
        status=call.status,
        candidate_symbols=list(call.targets),
        evidence=list(call.evidence),
        call_fact_id=call.call_fact_id,
        location=_location(call.location),
        relation=relation,
    )


def _is_class(
    symbol: str,
    definitions: dict[str, DefinitionFact],
    registry: SemanticRegistry,
) -> bool:
    definition = definitions.get(symbol)
    if definition:
        return definition.symbol_kind == "class"
    model = registry.callables.get(symbol)
    return bool(model and model.kind == "class")


def _owner_class(symbol: str, definitions: dict[str, DefinitionFact]) -> str | None:
    parent = symbol.rsplit(".", 1)[0]
    definition = definitions.get(parent)
    return definition.name if definition and definition.symbol_kind == "class" else None


def _location(location) -> SourceLocation:
    return SourceLocation(
        file=location.file,
        line_start=location.line_start,
        line_end=location.line_end,
    )
