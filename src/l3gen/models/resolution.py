"""Kết quả Resolver + Dataflow của pipeline V2."""

from typing import Literal

from pydantic import BaseModel, Field

from l3gen.models.semantic import SemanticLocation

ResolutionStatus = Literal["resolved", "candidates", "unresolved", "runtime"]


class EvidenceStep(BaseModel):
    description: str
    location: SemanticLocation | None = None
    fact_id: str | None = None


class AbstractValue(BaseModel):
    kind: Literal["symbol", "instance", "literal", "container", "runtime", "unknown"]
    value: str
    symbol_kind: Literal["class", "function", "module", "method", "external"] | None = None
    # Với instance, ``value`` là danh tính của object (allocation site), còn
    # ``type_symbol`` là kiểu của object. Nhờ vậy hai router cùng kiểu vẫn là
    # hai object riêng biệt trong graph.
    type_symbol: str | None = None
    receiver_object_id: str | None = None
    receiver_type: str | None = None

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.symbol_kind or ''}:{self.type_symbol or ''}:{self.value}:{self.receiver_object_id or ''}"


class ResolvedCall(BaseModel):
    call_fact_id: str
    caller_symbol: str | None
    written_callee: str
    status: ResolutionStatus
    targets: list[str] = Field(default_factory=list)
    receiver_types: list[str] = Field(default_factory=list)
    callee_slot: str | None = None
    receiver_slot: str | None = None
    argument_slots: list[str] = Field(default_factory=list)
    keyword_slots: dict[str, str] = Field(default_factory=dict)
    result_values: list[AbstractValue] = Field(default_factory=list)
    evidence: list[EvidenceStep] = Field(default_factory=list)
    reason: str | None = None
    truncated: bool = False
    location: SemanticLocation


class ResolutionMetrics(BaseModel):
    symbols: int = 0
    constraints: int = 0
    propagated_values: int = 0
    worklist_iterations: int = 0
    resolved_calls: int = 0
    candidate_calls: int = 0
    unresolved_calls: int = 0
    runtime_calls: int = 0
    truncated_calls: int = 0
    duration_seconds: float = 0.0


class ResolutionResult(BaseModel):
    calls: list[ResolvedCall] = Field(default_factory=list)
    values_by_slot: dict[str, list[AbstractValue]] = Field(default_factory=dict)
    metrics: ResolutionMetrics = Field(default_factory=ResolutionMetrics)
    partial: bool = False
    partial_reasons: list[str] = Field(default_factory=list)
    class_bases: dict[str, list[str]] = Field(default_factory=dict)
