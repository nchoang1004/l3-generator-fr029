"""SQLAlchemy/SQLModel adapter V2, đọc IR chung thay vì quét lại Python AST."""

from __future__ import annotations

from collections import defaultdict

from l3gen.models.iam import DBColumn, DBEntity, Reference, SourceLocation
from l3gen.models.resolution import ResolvedCall, ResolutionResult
from l3gen.models.semantic import (
    AssignmentFact,
    CallFact,
    DefinitionFact,
    ExpressionIR,
    ImportFact,
    InheritanceFact,
    ScopeFact,
    SemanticProgram,
)

_DECLARATIVE_FACTORIES = {
    "sqlalchemy.orm.declarative_base",
    "sqlalchemy.ext.declarative.declarative_base",
}
_DECLARATIVE_TYPES = {
    "sqlalchemy.orm.DeclarativeBase",
    "sqlalchemy.orm.DeclarativeBaseNoMeta",
}
_SQLMODEL_TYPES = {"sqlmodel.SQLModel"}
_COLUMN_FACTORIES = {
    "sqlalchemy.Column",
    "sqlalchemy.sql.schema.Column",
    "sqlalchemy.orm.mapped_column",
    "sqlmodel.Field",
}
_RELATIONSHIP_FACTORIES = {"sqlalchemy.orm.relationship", "sqlmodel.Relationship"}
_MAX_BASE_DEPTH = 20


class _Names:
    def __init__(self, facts) -> None:
        scope_names = {
            fact.scope_id: fact.qualified_name
            for fact in facts
            if isinstance(fact, ScopeFact)
        }
        self.parent = {
            fact.scope_id: fact.parent_scope_id
            for fact in facts
            if isinstance(fact, ScopeFact)
        }
        self.imports: dict[tuple[str, str], str] = {}
        self.definitions: dict[tuple[str, str], str] = {}
        for fact in facts:
            if isinstance(fact, ImportFact):
                self.imports[(fact.scope_id, fact.local_name)] = fact.imported_symbol
            elif isinstance(fact, DefinitionFact):
                self.definitions[(fact.scope_id, fact.name)] = fact.qualified_name
            elif (
                isinstance(fact, AssignmentFact)
                and fact.target.kind == "name"
                and fact.scope_id.startswith("module:")
            ):
                name = fact.target.name or fact.target.text
                self.definitions[(fact.scope_id, name)] = f"{scope_names[fact.scope_id]}.{name}"

    def symbol(self, scope_id: str, expression: ExpressionIR) -> str | None:
        if expression.kind == "name":
            scope: str | None = scope_id
            name = expression.name or expression.text
            while scope:
                if (scope, name) in self.definitions:
                    return self.definitions[(scope, name)]
                if (scope, name) in self.imports:
                    return self.imports[(scope, name)]
                scope = self.parent.get(scope)
            return None
        if expression.kind == "attribute" and expression.base is not None:
            base = self.symbol(scope_id, expression.base)
            return f"{base}.{expression.attribute}" if base else None
        return None


def extract_entities_v2(
    program: SemanticProgram,
    resolution: ResolutionResult,
    service: str = "python",
) -> list[DBEntity]:
    facts = program.all_facts()
    definitions = {
        fact.qualified_name: fact
        for fact in facts
        if isinstance(fact, DefinitionFact)
    }
    inheritance = {
        fact.class_symbol: fact for fact in facts if isinstance(fact, InheritanceFact)
    }
    assignments: dict[str, list[AssignmentFact]] = defaultdict(list)
    for fact in facts:
        if isinstance(fact, AssignmentFact) and fact.enclosing_class and fact.scope_id.startswith("class:"):
            assignments[fact.enclosing_class].append(fact)
    calls = {fact.id: fact for fact in facts if isinstance(fact, CallFact)}
    resolved_by_signature: dict[tuple[str, int, str], ResolvedCall] = {}
    for item in resolution.calls:
        source = calls[item.call_fact_id]
        resolved_by_signature[(source.location.file, source.location.line_start, source.expression_text)] = item

    mapped_names = {
        (fact.location.file, fact.local_name) for fact in facts
        if isinstance(fact, ImportFact) and fact.imported_symbol == "sqlalchemy.orm.Mapped"
    }

    def orm_kind(class_symbol: str, depth: int = 0, seen: frozenset[str] = frozenset()):
        if depth > _MAX_BASE_DEPTH or class_symbol in seen:
            return None
        relation = inheritance.get(class_symbol)
        if relation is None:
            return None
        for symbol in resolution.class_bases.get(class_symbol, []):
            if symbol in _SQLMODEL_TYPES:
                return "sqlmodel"
            if symbol in _DECLARATIVE_TYPES:
                return "sqlalchemy"
            if symbol in inheritance:
                found = orm_kind(symbol, depth + 1, seen | {class_symbol})
                if found:
                    return found
        return None

    entities: list[DBEntity] = []
    for symbol, definition in definitions.items():
        if definition.symbol_kind != "class":
            continue
        orm = orm_kind(symbol)
        if orm is None or _is_abstract(assignments.get(symbol, [])):
            continue
        relation = inheritance.get(symbol)
        resolved_bases = resolution.class_bases.get(symbol, [])
        direct_base = resolved_bases[0] if resolved_bases else None
        if orm == "sqlmodel":
            table_kw = relation.keywords.get("table") if relation else None
            if not table_kw or table_kw.kind != "literal" or table_kw.literal is not True:
                continue
        if (
            direct_base in _DECLARATIVE_TYPES
            and not _has_table_or_columns(assignments.get(symbol, []))
        ):
            # `class Base(DeclarativeBase): pass` khai báo base dùng chung,
            # bản thân nó chưa phải một bảng.
            continue
        table_name, confidence, completeness, reason = _table_name(
            definition.name, assignments.get(symbol, []), orm
        )
        entities.append(
            DBEntity(
                service=service,
                class_name=definition.name,
                table_name=table_name,
                columns=_columns(
                    assignments.get(symbol, []), resolved_by_signature, orm, mapped_names
                ),
                base_class=_base_reference(direct_base, definitions),
                confidence=confidence,
                completeness=completeness,
                reason=reason,
                location=_location(definition.location),
            )
        )
    return sorted(entities, key=lambda item: (item.table_name or "", item.class_name))


def _columns(
    assignments: list[AssignmentFact],
    resolved_calls: dict[tuple[str, int, str], ResolvedCall],
    orm: str,
    mapped_names: set[tuple[str, str]],
) -> list[DBColumn]:
    columns: list[DBColumn] = []
    for fact in assignments:
        if fact.target.kind != "name" or (fact.target.name or fact.target.text).startswith("__"):
            continue
        name = fact.target.name or fact.target.text
        resolved = None
        if fact.value.kind == "call":
            resolved = resolved_calls.get(
                (fact.location.file, fact.value.source_line or fact.location.line_start, fact.value.text)
            )
        targets = set(resolved.targets) if resolved else set()
        if targets & _RELATIONSHIP_FACTORIES:
            continue
        mapped = bool(fact.annotation and fact.annotation.base and
                      (fact.location.file, fact.annotation.base.text) in mapped_names)
        if not (targets & _COLUMN_FACTORIES) and not mapped and not (orm == "sqlmodel" and fact.annotation):
            continue
        if fact.annotation and "ClassVar[" in fact.annotation.text:
            continue
        annotation = fact.annotation.text if fact.annotation else "?"
        if mapped and fact.annotation.elements:
            annotation = fact.annotation.elements[0].text
        call = fact.value if fact.value.kind == "call" else None
        column_type = annotation
        if column_type == "?" and call and call.arguments:
            non_fk = [arg for arg in call.arguments if not _is_foreign_key(arg, fact.location.file, resolved_calls)]
            if non_fk:
                column_type = non_fk[0].text
        foreign_key = None
        if call:
            fk = call.keywords.get("foreign_key")
            if fk:
                foreign_key = _literal_text(fk)
            if foreign_key is None:
                for argument in call.arguments:
                    if _is_foreign_key(argument, fact.location.file, resolved_calls) and argument.arguments:
                        foreign_key = _literal_text(argument.arguments[0])
        primary = bool(
            call
            and call.keywords.get("primary_key")
            and call.keywords["primary_key"].kind == "literal"
            and call.keywords["primary_key"].literal is True
        )
        columns.append(
            DBColumn(
                name=name,
                type=column_type,
                is_primary_key=primary,
                foreign_key_ref=foreign_key,
            )
        )
    return columns


def _is_foreign_key(expression, file, calls) -> bool:
    resolved = calls.get((file, expression.source_line, expression.text))
    return bool(resolved and set(resolved.targets) & {
        "sqlalchemy.ForeignKey", "sqlalchemy.sql.schema.ForeignKey"
    })


def _table_name(class_name: str, assignments: list[AssignmentFact], orm: str):
    for fact in assignments:
        if fact.target.kind != "name" or (fact.target.name or fact.target.text) != "__tablename__":
            continue
        literal = _literal_text(fact.value)
        if literal is not None:
            return literal, "exact", "full", None
        return fact.value.text, "exact", "partial", "__tablename__ phụ thuộc runtime"
    if orm == "sqlmodel":
        return class_name.lower(), "inferred", "full", "SQLModel dùng tên class viết thường"
    return None, "exact", "partial", "tên bảng do lớp cơ sở quyết định lúc runtime"


def _is_abstract(assignments: list[AssignmentFact]) -> bool:
    return any(
        fact.target.kind == "name"
        and (fact.target.name or fact.target.text) == "__abstract__"
        and fact.value.kind == "literal"
        and fact.value.literal is True
        for fact in assignments
    )


def _has_table_or_columns(assignments: list[AssignmentFact]) -> bool:
    return any(
        fact.target.kind == "name"
        and (
            (fact.target.name or fact.target.text) == "__tablename__"
            or not (fact.target.name or fact.target.text).startswith("__")
        )
        for fact in assignments
    )


def _base_reference(
    base: str | None, definitions: dict[str, DefinitionFact]
) -> Reference | None:
    if base is None:
        return None
    definition = definitions.get(base)
    return Reference(
        name=base.rsplit(".", 1)[-1],
        resolved_module=definition.location.file if definition else None,
        resolved=definition is not None,
        resolved_symbol=base if definition else None,
        confidence="exact" if definition else None,
        completeness="full" if definition else "partial",
        reason=None if definition else f"{base} thuộc thư viện ngoài",
        status="resolved" if definition else "unresolved",
    )


def _callee_ends(expression: ExpressionIR, name: str) -> bool:
    return bool(
        expression.kind == "call"
        and expression.callee
        and expression.callee.text.rsplit(".", 1)[-1] == name
    )


def _literal_text(expression: ExpressionIR) -> str | None:
    return expression.literal if expression.kind == "literal" and isinstance(expression.literal, str) else None


def _module_name(scope_id: str, facts) -> str:
    scope = next(
        (fact for fact in facts if isinstance(fact, ScopeFact) and fact.scope_id == scope_id),
        None,
    )
    return scope.qualified_name if scope else scope_id.removeprefix("module:")


def _location(location) -> SourceLocation:
    return SourceLocation(file=location.file, line_start=location.line_start, line_end=location.line_end)
