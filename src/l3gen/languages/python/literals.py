"""Đọc giá trị chuỗi từ cây cú pháp, giữ nguyên phần không giải được.

Nguyên tắc: gặp biến thì giữ nguyên tên biến trong ngoặc nhọn, KHÔNG đoán giá trị.
`f"{settings.API_PREFIX}/orders"` cho ra `"{settings.API_PREFIX}/orders"` — người
đọc thấy ngay chỗ nào là thật, chỗ nào phụ thuộc lúc chạy.
"""

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class TextValue:
    """Một chuỗi đã đọc từ cây cú pháp."""

    text: str
    is_literal: bool
    """True nếu đọc được trọn vẹn. False nếu còn phần phụ thuộc lúc chạy."""

    @property
    def placeholders(self) -> bool:
        return not self.is_literal


def read_text(node: ast.expr | None) -> TextValue | None:
    """Đọc một biểu thức thành chuỗi. None nếu không phải chuỗi."""
    if node is None:
        return None

    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return TextValue(node.value, True)
        return None

    if isinstance(node, ast.JoinedStr):
        parts, literal = [], True
        for piece in node.values:
            if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                parts.append(piece.value)
            elif isinstance(piece, ast.FormattedValue):
                parts.append("{" + ast.unparse(piece.value) + "}")
                literal = False
            else:
                parts.append("{?}")
                literal = False
        return TextValue("".join(parts), literal)

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = read_text(node.left), read_text(node.right)
        if left and right:
            return TextValue(left.text + right.text, left.is_literal and right.is_literal)

    return TextValue("{" + ast.unparse(node) + "}", False)


def keyword_of(call: ast.Call, name: str) -> ast.expr | None:
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def is_true(node: ast.expr | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is True
