"""Đơn vị phân tích và stack đã nhận diện (SPEC mục 4.4.7).

Một repo có thể chứa nhiều service với stack khác nhau. Mỗi service là một
ServiceUnit. Service dùng stack chưa hỗ trợ thì analyzed = False kèm skip_reason,
chứ không bị bỏ im lặng.
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


class DetectedStack(BaseModel):
    services: list[ServiceUnit]
    analyzed_count: int
    skipped_count: int
