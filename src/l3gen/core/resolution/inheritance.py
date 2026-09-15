"""Leo cây kế thừa để tìm method nằm ở class cha.

Không phụ thuộc ngôn ngữ nào: chỉ làm việc trên ClassRecord, do tầng ngôn ngữ
dựng sẵn.

Bốn quy tắc dừng (SPEC mục 15.4):
  - Class cha nằm ngoài repo  -> dừng, đây là kết quả ĐÚNG không phải lỗi
  - Sâu quá 10 tầng           -> dừng
  - Kế thừa vòng A(B), B(A)   -> dừng, không lặp vô hạn
  - Đa kế thừa, method có ở nhiều cha -> lấy cha khai báo trước, hạ xuống inferred
"""

from collections.abc import Callable
from dataclasses import dataclass, field

MAX_DEPTH = 10


@dataclass
class ClassRecord:
    """Một class trong repo, đã tách khỏi cú pháp của ngôn ngữ."""

    qualified_name: str
    rel_path: str
    line: int
    base_names: list[str] = field(default_factory=list)
    method_names: set[str] = field(default_factory=set)


@dataclass
class ClimbResult:
    """Kết quả tìm method: hoặc thấy chủ sở hữu, hoặc nêu lý do không thấy."""

    owner: ClassRecord | None = None
    ambiguous: bool = False
    reason: str | None = None
    stopped_at_external_base: bool = False
    """True khi dừng vì class cha nằm ngoài repo. Đây là phân loại ĐÚNG:
    method có tồn tại, chỉ là định nghĩa của nó không nằm trong phạm vi quét."""


def find_method_owner(
    start: ClassRecord,
    method_name: str,
    classes: dict[str, ClassRecord],
    resolve_base: Callable[[ClassRecord, str], str | None],
) -> ClimbResult:
    """Tìm class nào thật sự định nghĩa `method_name`, bắt đầu từ `start`.

    resolve_base đổi tên class cha như viết trong code thành tên đầy đủ, dùng
    bảng tên gọi CỦA FILE chứa class con. Truyền vào từ ngoài vì luật này khác
    nhau giữa các ngôn ngữ.
    """
    if method_name in start.method_names:
        return ClimbResult(owner=start)

    visited = {start.qualified_name}
    level = [start]

    for depth in range(1, MAX_DEPTH + 1):
        parents: list[ClassRecord] = []
        external_bases: list[str] = []

        for child in level:
            for base_name in child.base_names:
                base_qname = resolve_base(child, base_name)
                if base_qname is None or base_qname not in classes:
                    external_bases.append(base_name)
                    continue
                if base_qname in visited:
                    continue
                visited.add(base_qname)
                parents.append(classes[base_qname])

        if not parents:
            if external_bases:
                return ClimbResult(
                    stopped_at_external_base=True,
                    reason=(
                        f"class cha '{external_bases[0]}' nằm ngoài repo, "
                        f"không đọc được định nghĩa của '{method_name}'"
                    ),
                )
            return ClimbResult(reason=f"không tìm thấy '{method_name}' trong cây kế thừa")

        owners = [p for p in parents if method_name in p.method_names]
        if len(owners) == 1:
            return ClimbResult(owner=owners[0])
        if len(owners) > 1:
            names = ", ".join(o.qualified_name for o in owners)
            return ClimbResult(
                owner=owners[0],
                ambiguous=True,
                reason=(
                    f"'{method_name}' có ở nhiều class cha ({names}); "
                    f"lấy cha khai báo trước theo quy tắc đa kế thừa"
                ),
            )

        level = parents

    return ClimbResult(reason=f"cây kế thừa sâu quá {MAX_DEPTH} tầng, đã dừng")
