"""Gọi mô hình Claude, hỏng thì bỏ qua chứ không làm mất kết quả (SPEC mục 4.3).

Nguyên tắc bao trùm: tầng phân tích tĩnh không phụ thuộc tầng AI. Mạng hỏng, hết
hạn mức, thiếu thư viện — tất cả chỉ làm tài liệu thiếu phần mô tả, không bao giờ
làm mất phần dữ liệu đã đọc từ code.
"""

import os
from dataclasses import dataclass, field
from typing import TypeVar

from pydantic import BaseModel

MODEL = "claude-opus-5"
MAX_TOKENS = 8000
MAX_ATTEMPTS = 3
"""Một lần gọi đầu, thêm tối đa 2 lần thử lại (SPEC mục 4.3)."""

API_KEY_VARS = ("L3GEN_API_KEY", "ANTHROPIC_API_KEY")

T = TypeVar("T", bound=BaseModel)


@dataclass
class AIResult:
    """Kết quả một lượt gọi AI, kèm những gì đã hỏng để ghi vào Giới hạn đã biết."""

    value: BaseModel | None = None
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.value is not None


def read_api_key() -> str | None:
    for name in API_KEY_VARS:
        key = os.environ.get(name)
        if key:
            return key
    return None


def ask(prompt: str, system: str, output_model: type[T]) -> AIResult:
    """Hỏi mô hình, bắt buộc trả về đúng dạng `output_model`.

    Dùng structured output nên mô hình không thể trả về trường nào ngoài schema.
    """
    key = read_api_key()
    if key is None:
        return AIResult(problems=["chưa cấu hình API key"])

    try:
        import anthropic
    except ImportError:
        return AIResult(
            problems=["chưa cài thư viện anthropic; cài bằng: pip install 'l3gen[ai]'"]
        )

    client = anthropic.Anthropic(api_key=key, max_retries=0)
    problems: list[str] = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.messages.parse(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                output_format=output_model,
            )
        except Exception as exc:  # noqa: BLE001 - mọi lỗi AI đều chỉ làm giảm chất lượng
            problems.append(f"lần {attempt}: {type(exc).__name__}: {exc}")
            continue

        if response.stop_reason == "refusal":
            return AIResult(problems=["mô hình từ chối trả lời yêu cầu này"])
        if response.parsed_output is None:
            problems.append(f"lần {attempt}: mô hình không trả về đúng dạng dữ liệu")
            continue
        return AIResult(value=response.parsed_output, problems=problems)

    return AIResult(problems=problems)
