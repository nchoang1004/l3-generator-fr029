"""Rà soát IAM và gắn cờ chỗ nghi ngờ thiếu sót (bước 6b).

Đọc IAM độc lập, KHÔNG đọc mô tả do bước 5 viết. Hai bước AI cố tình không nối
vào nhau: nếu bước rà soát đọc lời do bước mô tả viết, một chỗ AI bịa ở bước
trước có thể lan sang bước sau mà không ai phát hiện.

**Việc phát hiện là tất định, không do AI quyết định.** Đọc kỹ bốn ràng buộc ở
SPEC mục 6b.1 sẽ thấy cả bốn đều là luật đếm được trên IAM: "route có calls
rỗng", "entity không được ai tham chiếu"... Để AI tự quyết định gắn cờ chỗ nào
là mở đường cho nó bịa ra cảnh báo không có bằng chứng. Nên ở đây phần tĩnh phát
hiện, AI chỉ viết lại câu tóm tắt cho dễ đọc.

Hệ quả có ích: cảnh báo vẫn chạy được khi không có AI, chỉ là câu chữ máy móc hơn.
"""

import json
from dataclasses import dataclass, field

from l3gen.ai.client import ask
from l3gen.ai.schemas import FindingSummaryBatch
from l3gen.models.findings import ReviewFinding, ReviewFindings
from l3gen.models.iam import IntermediateArchitectureModel, SourceLocation

MAX_PER_CATEGORY = 15
"""Mỗi loại chỉ nêu tối đa 15 ca. Một danh sách 1000 dòng thì không ai đọc."""

SYSTEM = """Bạn viết lại câu tóm tắt cho các cảnh báo đã được phát hiện sẵn.

Cảnh báo do phần phân tích tĩnh tìm ra, KHÔNG phải do bạn. Việc của bạn chỉ là
diễn đạt cho dễ hiểu.

Quy tắc:
- Một câu, tiếng Việt, tối đa 400 ký tự.
- Giọng cảnh báo, không khẳng định: "có thể thiếu...", "chưa thấy...".
  Tuyệt đối không viết "sẽ lỗi", "chắc chắn sai".
- Chỉ dùng finding_id có trong danh sách.
"""


@dataclass
class Review:
    findings: list[ReviewFinding] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


@dataclass
class _Candidate:
    """Một cảnh báo đã phát hiện, trước khi AI viết lại câu tóm tắt."""

    finding_id: str
    category: str
    fallback_summary: str
    location: SourceLocation
    iam_ref: str
    facts: dict


def _unresolved(iam: IntermediateArchitectureModel) -> list[_Candidate]:
    """Chỉ lấy từ danh sách đã có sẵn trong IAM, không tự tìm thêm ca mới."""
    found = []
    for i, item in enumerate(iam.unresolved_references[:MAX_PER_CATEGORY]):
        found.append(
            _Candidate(
                finding_id=f"unresolved-{i}",
                category="unresolved_reference",
                fallback_summary=f"Tham chiếu chưa xác định được đích: {item.description}",
                location=item.location,
                iam_ref=f"unresolved_references[{i}]",
                facts={"mo_ta": item.description},
            )
        )
    return found


def _empty_handlers(iam: IntermediateArchitectureModel) -> list[_Candidate]:
    """Route có calls rỗng, hoặc mọi lời gọi đều chưa nối được đích."""
    found = []
    for i, route in enumerate(iam.routes):
        resolved = [c for c in route.calls if c.resolved]
        if resolved:
            continue
        if len(found) >= MAX_PER_CATEGORY:
            break
        reason = "không thấy lời gọi nào" if not route.calls else "mọi lời gọi đều chưa nối được đích"
        found.append(
            _Candidate(
                finding_id=f"handler-{i}",
                category="empty_handler_calls",
                fallback_summary=(
                    f"Hàm xử lý '{route.handler_function}' của {route.method} {route.path}: "
                    f"{reason}. Có thể tài liệu chưa phản ánh đủ việc route này làm."
                ),
                location=route.location,
                iam_ref=f"routes[{i}].calls",
                facts={
                    "method": route.method,
                    "duong_dan": route.path,
                    "ham_xu_ly": route.handler_function,
                    "ly_do": reason,
                },
            )
        )
    return found


def _orphan_entities(iam: IntermediateArchitectureModel) -> list[_Candidate]:
    """Bảng không có hàm hay route nào tham chiếu tới, trong phạm vi đã quét."""
    referenced: set[str] = set()
    for function in iam.functions:
        referenced.update(ref.name for ref in function.entity_refs)
    for route in iam.routes:
        referenced.update(ref.name for ref in route.calls if ref.resolved)

    found = []
    for i, entity in enumerate(iam.entities):
        if entity.class_name in referenced or len(found) >= MAX_PER_CATEGORY:
            continue
        found.append(
            _Candidate(
                finding_id=f"orphan-{i}",
                category="orphan_entity",
                fallback_summary=(
                    f"Class {entity.class_name} khai báo một bảng dữ liệu nhưng chưa thấy "
                    f"hàm nào tham chiếu tới, trong phạm vi đã quét. Có thể là bảng không "
                    f"còn dùng, hoặc chỉ được dùng ở phần nằm ngoài phạm vi quét."
                ),
                location=entity.location,
                iam_ref=f"entities[{i}]",
                facts={"class": entity.class_name, "ten_bang": entity.table_name},
            )
        )
    return found


def _unprotected_calls(iam: IntermediateArchitectureModel) -> list[_Candidate]:
    """Lời gọi ra ngoài không nằm trong try/except."""
    found = []
    for i, call in enumerate(iam.external_calls):
        if call.inside_try_except or len(found) >= MAX_PER_CATEGORY:
            continue
        found.append(
            _Candidate(
                finding_id=f"external-{i}",
                category="external_call_no_error_handling",
                fallback_summary=(
                    f"Lời gọi ra {call.url_or_host} trong '{call.caller_function}' không nằm "
                    f"trong khối try/except. Có thể thiếu xử lý lỗi khi dịch vụ ngoài hỏng."
                ),
                location=call.location,
                iam_ref=f"external_calls[{i}]",
                facts={
                    "dich": call.url_or_host,
                    "goi_tu": call.caller_function,
                    "method": call.http_method,
                },
            )
        )
    return found


def detect(iam: IntermediateArchitectureModel) -> list[_Candidate]:
    """Phát hiện tất định. Không dùng AI, không đọc lại source."""
    return [
        *_empty_handlers(iam),
        *_orphan_entities(iam),
        *_unprotected_calls(iam),
        *_unresolved(iam),
    ]


def review(iam: IntermediateArchitectureModel, use_ai: bool) -> Review:
    candidates = detect(iam)
    result = Review()
    if not candidates:
        return result

    summaries: dict[str, str] = {}
    if use_ai:
        allowed = {c.finding_id for c in candidates}
        payload = [
            {"finding_id": c.finding_id, "loai": c.category, **c.facts} for c in candidates
        ]
        answer = ask(
            "Viết lại câu tóm tắt cho từng cảnh báo dưới đây.\n\n"
            + json.dumps(payload, ensure_ascii=False, indent=2),
            SYSTEM,
            FindingSummaryBatch,
        )
        if answer.ok:
            summaries = {
                s.finding_id: s.summary.strip()
                for s in answer.value.summaries
                if s.finding_id in allowed
            }
        else:
            result.problems.extend(answer.problems)

    result.findings = [
        ReviewFinding(
            category=c.category,
            summary=summaries.get(c.finding_id, c.fallback_summary),
            evidence_location=c.location,
            related_iam_ref=c.iam_ref,
        )
        for c in candidates
    ]
    return result


def as_model(review_result: Review) -> ReviewFindings:
    return ReviewFindings(findings=review_result.findings)
