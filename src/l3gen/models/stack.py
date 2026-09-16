"""Nhóm ngôn ngữ và stack đã nhận diện.

Tên ``ServiceUnit`` được giữ tạm để tương thích output V1. Trong V2, mỗi record ở
đây là một nhóm phân tích theo ngôn ngữ, không phải kết luận kiến trúc rằng folder
đó là service. Application/service boundary chỉ được dựng sau graph.
"""

from typing import Literal

from pydantic import BaseModel

Confidence = Literal["exact", "inferred"]
Completeness = Literal["full", "partial"]


class ServiceUnit(BaseModel):
    name: str
    root_path: str
    manifest_file: str | None
    language: str
    frameworks: list[str]
    orm: str | None
    confidence: Confidence
    completeness: Completeness
    detection_reason: str
    file_count: int
    analyzed: bool
    skip_reason: str | None
    unit_kind: Literal["language"] = "language"
    application_boundary: Literal["unknown"] = "unknown"


class DetectedStack(BaseModel):
    services: list[ServiceUnit]
    analyzed_count: int
    skipped_count: int
