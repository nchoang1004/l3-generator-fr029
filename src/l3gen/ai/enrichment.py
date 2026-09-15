"""Nhờ AI viết mô tả bằng lời cho từng thành phần (bước 5).

Ba lớp chặn để AI không thể sửa dữ liệu:

1. Schema khoá cứng — chỉ có `target_id` và `text`, không có trường nào để thêm
   route hay bảng dữ liệu.
2. Lọc lại sau khi nhận — `target_id` nào không có trong danh sách gửi đi thì bỏ.
3. Ghi ra file riêng, không nhét vào IAM.json.

Lớp 3 là lớp mạnh nhất: nó biến "AI không được sửa dữ liệu" từ một lời hứa thành
một điều kiểm chứng được bằng `diff`.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from l3gen.ai.client import AIResult, ask
from l3gen.ai.schemas import DescriptionBatch
from l3gen.models.iam import IntermediateArchitectureModel

BATCH_SIZE = 25

SYSTEM = """Bạn viết mô tả ngắn cho các thành phần của một hệ thống phần mềm.

Dữ liệu đưa cho bạn được đọc trực tiếp từ cây cú pháp của source code — nó là sự
thật đã được xác minh. Việc của bạn CHỈ là diễn đạt lại cho người đọc dễ hiểu.

Quy tắc:
- Mỗi mô tả 1-2 câu, tiếng Việt, tối đa 400 ký tự.
- Chỉ nói những gì suy ra được từ dữ liệu đã cho. Không suy đoán về nghiệp vụ,
  không nhắc tới thứ không có trong dữ liệu.
- Không biết thì viết "chưa đủ dữ liệu để mô tả".
- Chỉ dùng target_id có trong danh sách. Không tự tạo mã mới.
"""


@dataclass
class Descriptions:
    """Mô tả do AI viết, cất riêng ngoài IAM."""

    by_id: dict[str, str] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)
    rejected: int = 0
    """Số mô tả bị loại vì trỏ tới mã không tồn tại."""

    def get(self, target_id: str) -> str | None:
        return self.by_id.get(target_id)


def route_id(index: int) -> str:
    return f"route-{index}"


def entity_id(index: int) -> str:
    return f"entity-{index}"


def external_id(index: int) -> str:
    return f"external-{index}"


def _items(iam: IntermediateArchitectureModel) -> list[dict]:
    """Gom mọi thứ cần mô tả thành danh sách phẳng, chỉ giữ dữ liệu cần thiết."""
    items = []
    for i, route in enumerate(iam.routes):
        items.append({
            "target_id": route_id(i),
            "loai": "API route",
            "method": route.method,
            "duong_dan": route.path,
            "ham_xu_ly": route.handler_function,
            "goi_toi": [c.name for c in route.calls if c.resolved][:5],
            "vi_tri": f"{route.location.file}:{route.location.line_start}",
        })
    for i, entity in enumerate(iam.entities):
        items.append({
            "target_id": entity_id(i),
            "loai": "bảng dữ liệu",
            "class": entity.class_name,
            "ten_bang": entity.table_name,
            "cot": [
                {"ten": c.name, "kieu": c.type, "khoa_ngoai": c.foreign_key_ref}
                for c in entity.columns[:12]
            ],
            "vi_tri": f"{entity.location.file}:{entity.location.line_start}",
        })
    for i, call in enumerate(iam.external_calls):
        items.append({
            "target_id": external_id(i),
            "loai": "lời gọi ra ngoài",
            "method": call.http_method,
            "dich": call.url_or_host,
            "goi_tu": call.caller_function,
            "vi_tri": f"{call.location.file}:{call.location.line_start}",
        })
    return items


def enrich(iam: IntermediateArchitectureModel) -> Descriptions:
    """Xin mô tả cho mọi thành phần. Lỗi ở một lô không làm hỏng các lô khác."""
    result = Descriptions()
    items = _items(iam)
    if not items:
        return result

    for start in range(0, len(items), BATCH_SIZE):
        batch = items[start : start + BATCH_SIZE]
        allowed = {item["target_id"] for item in batch}
        prompt = (
            "Viết mô tả cho từng thành phần dưới đây.\n\n"
            + json.dumps(batch, ensure_ascii=False, indent=2)
        )
        answer: AIResult = ask(prompt, SYSTEM, DescriptionBatch)

        if not answer.ok:
            result.problems.extend(answer.problems)
            continue

        for description in answer.value.descriptions:
            if description.target_id not in allowed:
                # AI trả về mã không có trong danh sách gửi đi. Bỏ, không nhận.
                result.rejected += 1
                continue
            result.by_id[description.target_id] = description.text.strip()

    return result


def write_descriptions(descriptions: Descriptions, output_dir: Path) -> Path:
    """Ghi ra file riêng — KHÔNG trộn vào IAM.json."""
    path = output_dir / "descriptions.json"
    path.write_text(
        json.dumps(
            {
                "note": "Do AI viết. Không phải dữ liệu đọc từ code. Không dùng làm căn cứ.",
                "descriptions": descriptions.by_id,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return path
