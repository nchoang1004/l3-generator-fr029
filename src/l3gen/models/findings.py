"""Cảnh báo do bước rà soát sinh ra (SPEC mục 6b.1).

Tách hoàn toàn khỏi IAM. Đây là **cảnh báo cần người xác nhận**, không phải kết
luận. Mỗi cảnh báo bắt buộc trỏ về một vị trí cụ thể trong source.

Chỉ có đúng bốn loại. Không được thêm loại mới — `Literal` chặn ở tầng Pydantic.
"""

from typing import Literal

from pydantic import BaseModel

from l3gen.models.iam import SourceLocation

FindingCategory = Literal[
    "unresolved_reference",
    "empty_handler_calls",
    "orphan_entity",
    "external_call_no_error_handling",
]


class ReviewFinding(BaseModel):
    category: FindingCategory
    summary: str
    """Một câu, giọng cảnh báo ("có thể thiếu..."), không khẳng định chắc chắn."""
    evidence_location: SourceLocation
    related_iam_ref: str
    """Phần tử IAM liên quan, ví dụ "APIRoute[3].handler_function"."""


class ReviewFindings(BaseModel):
    findings: list[ReviewFinding]
