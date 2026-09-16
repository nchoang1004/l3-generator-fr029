"""Kết quả chuẩn hóa hành vi framework sau khi call đã được resolve."""

from typing import Literal

from pydantic import BaseModel, Field

from l3gen.models.resolution import EvidenceStep, ResolutionStatus
from l3gen.models.semantic import SemanticLocation


class FrameworkObject(BaseModel):
    object_id: str
    type_symbol: str
    labels: list[str] = Field(default_factory=list)
    prefix: str | None = None
    prefix_is_literal: bool = True
    location: SemanticLocation


class RegistrationOperation(BaseModel):
    id: str
    kind: Literal["AttachRouter", "MountApplication", "RegisterEndpoint"]
    framework_symbol: str
    parent_object_ids: list[str] = Field(default_factory=list)
    child_object_ids: list[str] = Field(default_factory=list)
    endpoint_symbols: list[str] = Field(default_factory=list)
    path: str | None = None
    path_is_literal: bool = True
    methods: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    status: ResolutionStatus
    evidence: list[EvidenceStep] = Field(default_factory=list)
    reason: str | None = None
    location: SemanticLocation


class FrameworkAnalysis(BaseModel):
    registry_version: str
    objects: list[FrameworkObject] = Field(default_factory=list)
    operations: list[RegistrationOperation] = Field(default_factory=list)
    dropped_operations: list[str] = Field(default_factory=list)

