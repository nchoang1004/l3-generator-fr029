"""Common Semantic IR: dữ kiện ngôn ngữ trung tính trước khi hiểu framework."""

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import BaseModel, Field


class SemanticLocation(BaseModel):
    file: str
    line_start: int
    column_start: int
    line_end: int
    column_end: int


class ExpressionIR(BaseModel):
    """Biểu thức bảo toàn cấu trúc, tuyệt đối không gán ý nghĩa framework."""

    kind: Literal[
        "name",
        "attribute",
        "call",
        "literal",
        "list",
        "tuple",
        "dict",
        "subscript",
        "binary",
        "conditional",
        "formatted_string",
        "unknown",
    ]
    text: str
    name: str | None = None
    base: "ExpressionIR | None" = None
    attribute: str | None = None
    callee: "ExpressionIR | None" = None
    arguments: list["ExpressionIR"] = Field(default_factory=list)
    keywords: dict[str, "ExpressionIR"] = Field(default_factory=dict)
    elements: list["ExpressionIR"] = Field(default_factory=list)
    literal: str | int | float | bool | None = None
    operator: str | None = None
    source_line: int | None = None
    source_column: int | None = None


class SemanticFact(BaseModel):
    id: str
    kind: str
    language: str = "python"
    scope_id: str
    location: SemanticLocation
    frontend_version: str
    completeness: Literal["full", "partial"] = "full"
    reason: str | None = None


class ScopeFact(SemanticFact):
    kind: Literal["scope"] = "scope"
    scope_kind: Literal["module", "class", "function"]
    name: str
    qualified_name: str
    parent_scope_id: str | None


class ImportFact(SemanticFact):
    kind: Literal["import"] = "import"
    local_name: str
    imported_symbol: str
    is_wildcard: bool = False


class DefinitionFact(SemanticFact):
    kind: Literal["definition"] = "definition"
    name: str
    qualified_name: str
    symbol_kind: Literal["class", "function", "async_function"]
    conditions: list[str] = Field(default_factory=list)
    return_annotation: ExpressionIR | None = None


class ParameterFact(SemanticFact):
    kind: Literal["parameter"] = "parameter"
    function_symbol: str
    name: str
    position: int
    parameter_kind: Literal["positional", "keyword_only", "vararg", "kwarg"]
    annotation: ExpressionIR | None = None
    default: ExpressionIR | None = None


class AssignmentFact(SemanticFact):
    kind: Literal["assignment"] = "assignment"
    target: ExpressionIR
    value: ExpressionIR
    annotation: ExpressionIR | None = None
    has_value: bool = True
    conditions: list[str] = Field(default_factory=list)
    enclosing_function: str | None = None
    enclosing_class: str | None = None


class CallFact(SemanticFact):
    kind: Literal["call"] = "call"
    expression_text: str
    callee: ExpressionIR
    arguments: list[ExpressionIR] = Field(default_factory=list)
    keywords: dict[str, ExpressionIR] = Field(default_factory=dict)
    conditions: list[str] = Field(default_factory=list)
    enclosing_function: str | None = None
    enclosing_class: str | None = None
    inside_try_except: bool = False
    context: Literal["body", "decorator", "default", "class_base"] = "body"


class ReturnFact(SemanticFact):
    kind: Literal["return"] = "return"
    function_symbol: str
    value: ExpressionIR | None
    conditions: list[str] = Field(default_factory=list)


class InheritanceFact(SemanticFact):
    kind: Literal["inheritance"] = "inheritance"
    class_symbol: str
    bases: list[ExpressionIR]
    keywords: dict[str, ExpressionIR] = Field(default_factory=dict)


class DecoratorFact(SemanticFact):
    kind: Literal["decorator"] = "decorator"
    owner_symbol: str
    expression: ExpressionIR


Fact: TypeAlias = (
    ScopeFact
    | ImportFact
    | DefinitionFact
    | ParameterFact
    | AssignmentFact
    | CallFact
    | ReturnFact
    | InheritanceFact
    | DecoratorFact
)


class SemanticModule(BaseModel):
    module: str
    file: str
    facts: list[Fact]
    analysis_notes: list[str] = Field(default_factory=list)


class SemanticProgram(BaseModel):
    frontend_version: str
    modules: list[SemanticModule]

    def all_facts(self) -> list[Fact]:
        return [fact for module in self.modules for fact in module.facts]
