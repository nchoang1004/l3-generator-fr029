"""Kiểm kê source file trước khi parser hoặc framework adapter chạy.

Inventory là sổ cái bảo toàn độ phủ: mỗi source file được phát hiện có đúng một
record và một trạng thái. Cách xếp folder, manifest hay framework không được làm
file biến mất khỏi sổ cái này.
"""

from collections import Counter
from typing import Literal

from pydantic import BaseModel, model_validator

FileStatus = Literal[
    "discovered",
    "parsed",
    "unsupported_language",
    "parse_error",
    "excluded",
    "oversized",
    "budget_exceeded",
]


class SourceFileRecord(BaseModel):
    path: str
    language: str
    size_bytes: int
    digest: str | None
    status: FileStatus
    reason: str | None = None


class FileInventory(BaseModel):
    files: list[SourceFileRecord]

    @model_validator(mode="after")
    def paths_are_unique(self) -> "FileInventory":
        paths = [item.path for item in self.files]
        if len(paths) != len(set(paths)):
            raise ValueError("mỗi source file phải xuất hiện đúng một lần trong inventory")
        return self

    @property
    def status_counts(self) -> dict[str, int]:
        return dict(sorted(Counter(item.status for item in self.files).items()))
