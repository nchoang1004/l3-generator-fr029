"""Sinh tài liệu L3.md theo mẫu SPEC mục 7.

Nguyên tắc trình bày: người đọc phải luôn phân biệt được đâu là dữ liệu đọc từ
code, đâu là lời do AI viết thêm. Mọi dòng đều kèm vị trí `file:dòng` để tự kiểm
chứng tại source.

Mục "Giới hạn đã biết" luôn xuất hiện, kể cả khi rỗng — để người đọc biết ngay
tài liệu này đáng tin tới đâu, không phải đoán.
"""

from pathlib import Path

from l3gen.ai.enrichment import Descriptions, entity_id, external_id, route_id
from l3gen.ai.reviewer import Review
from l3gen.models.iam import IntermediateArchitectureModel

MINUTES_PER_ITEM = (15, 20)
"""Hệ số quy đổi công sức. Là hằng số cấu hình, KHÔNG do AI sinh ra (SPEC mục 5.3)."""

MAX_PATH_DISPLAY = 60


def write_markdown(
    iam: IntermediateArchitectureModel,
    output_dir: Path,
    descriptions: Descriptions | None = None,
    review: Review | None = None,
) -> Path:
    path = output_dir / "L3.md"
    text = "\n".join(_render(iam, descriptions or Descriptions(), review or Review()))
    path.write_text(text + "\n", encoding="utf-8", errors="backslashreplace")
    return path


def _render(
    iam: IntermediateArchitectureModel, descriptions: Descriptions, review: Review
) -> list[str]:
    lines: list[str] = []
    lines += _header(iam)
    lines += _overview(iam)
    lines += _routes(iam, descriptions)
    lines += _entities(iam, descriptions)
    lines += _external(iam, descriptions)
    lines += _call_graph(iam)
    lines += _diagram_link()
    lines += _graph_summary(iam)
    lines += _review_findings(review)
    lines += _limitations(iam, descriptions, review)
    return lines


def _header(iam: IntermediateArchitectureModel) -> list[str]:
    stamp = iam.metrics.scanned_at.strftime("%d/%m/%Y %H:%M UTC")
    return [
        "# Tài liệu kiến trúc L3",
        "",
        f"> Sinh tự động bởi l3gen {iam.metrics.tool_version} vào {stamp}.",
        ">",
        "> **Route, bảng dữ liệu, lời gọi ra ngoài, quan hệ gọi hàm** đọc trực tiếp từ"
        " cây cú pháp. Mỗi dòng có cột *Vị trí* để tự kiểm chứng tại source.",
        "> **Cột Mô tả** do AI viết thêm cho dễ đọc — không dùng làm căn cứ xác lập"
        " cấu trúc.",
        "> Cột **Bằng chứng / đầy đủ** ghi hai nhãn tách biệt. `exact / partial` nghĩa là"
        " thực thể chắc chắn có thật, nhưng còn thuộc tính chưa biết đủ.",
        "> Dòng nào có `inferred`, `partial`, hoặc tham chiếu chưa nối được thì luôn kèm"
        " lý do. Hãy kiểm tra tại source trước khi dựa vào nó.",
        "",
    ]


def _overview(iam: IntermediateArchitectureModel) -> list[str]:
    m = iam.metrics
    stack = iam.detected_stack
    inventory_counts = iam.file_inventory.status_counts

    lines = ["## 1. Tổng quan", "", "### Các nhóm ngôn ngữ đã phát hiện", ""]
    lines += [
        "| Đơn vị | Ngôn ngữ | Framework | Số file | Bằng chứng / đầy đủ | Trạng thái |",
        "|---|---|---|---|---|---|",
    ]
    for service in stack.services:
        status = "Đã phân tích" if service.analyzed else f"**Bỏ qua** — {service.skip_reason}"
        frameworks = ", ".join(service.frameworks) or "—"
        lines.append(
            f"| {service.name or '(thư mục gốc)'} | {service.language or '—'} | {frameworks} "
            f"| {service.file_count} | {service.confidence} / {service.completeness} | {status} |"
        )
    lines += [
        "",
        "*Đây là nhóm kỹ thuật để chọn parser, không phải kết luận rằng mỗi nhóm là một"
        " service. Graph ghi application boundary ở mức `candidate` hoặc `unknown`, kèm bằng chứng.*",
        "",
        "### Kết quả lần chạy này",
        "",
        f"- Đã parse **{m.files_analyzed}/{m.files_found}** source file "
        f"({m.lines_of_code:,} dòng) trong {m.duration_seconds:.2f} giây",
        "- File inventory: "
        + ", ".join(f"**{count} {status}**" for status, count in inventory_counts.items()),
        f"- Đã phân tích **{stack.analyzed_count}/{len(stack.services)}** đơn vị; "
        f"kết quả {'chưa đầy đủ' if m.is_partial else 'đầy đủ'}",
        f"- Phát hiện: **{len(iam.routes)}** route, **{len(iam.entities)}** bảng dữ liệu, "
        f"**{len(iam.external_calls)}** lời gọi ra ngoài, **{len(iam.functions)}** hàm",
    ]

    counts = _label_counts(iam)
    lines += [
        f"- Mức bằng chứng: {counts['exact']} exact, {counts['inferred']} inferred",
        f"- Độ đầy đủ: {counts['full']} full, {counts['partial']} partial",
        f"- Chế độ: {'có' if m.ai_enabled else 'không có'} mô tả do AI viết",
        "",
    ]
    lines += _effort_estimate(iam)
    stats = iam.resolution.metrics
    lines += ["### Resolver + Dataflow", "",
              f"- {stats.resolved_calls} call đã nối; {stats.candidate_calls} có nhiều khả năng; "
              f"{stats.unresolved_calls} chưa nối; {stats.runtime_calls} phụ thuộc runtime.",
              f"- {stats.truncated_calls} call chịu ảnh hưởng của giới hạn phân tích.",
              "- Thời gian từng bước và peak memory của process nằm trong `run.json`.", ""]
    return lines


def _label_counts(iam: IntermediateArchitectureModel) -> dict[str, int]:
    counts = {"exact": 0, "inferred": 0, "full": 0, "partial": 0}
    for item in [*iam.routes, *iam.entities, *iam.external_calls]:
        counts[item.confidence] += 1
        counts[item.completeness] += 1
    return counts


def _effort_estimate(iam: IntermediateArchitectureModel) -> list[str]:
    """Quy đổi công sức. Luôn kèm giả định ngay cạnh con số, dùng khoảng chứ không
    dùng số đơn lẻ, và không quy ra tiền (SPEC mục 5.3)."""
    items = len(iam.routes) + len(iam.entities) + len(iam.external_calls)
    if items == 0:
        return []
    low_hours = items * MINUTES_PER_ITEM[0] / 60
    high_hours = items * MINUTES_PER_ITEM[1] / 60
    if high_hours < 8:
        span = f"~{low_hours:.1f}–{high_hours:.1f} giờ"
    else:
        span = f"~{low_hours / 8:.1f}–{high_hours / 8:.1f} ngày công"
    return [
        f"**Ước tính công sức tương đương nếu viết tay:** {span}",
        "",
        f"*Giả định {MINUTES_PER_ITEM[0]}–{MINUTES_PER_ITEM[1]} phút cho mỗi thành phần"
        f" ({items} thành phần) để đọc code, viết mô tả và vẽ sơ đồ; 8 giờ một ngày công."
        " Đây là ước tính theo hệ số cố định, không phải số đo thực nghiệm.*",
        "",
    ]


def _evidence(item) -> str:
    return f"`{item.confidence} / {item.completeness}`"


def _where(location) -> str:
    return f"[{_short(location.file)}:{location.line_start}]({location.file}#L{location.line_start})"


def _short(text: str, limit: int = MAX_PATH_DISPLAY) -> str:
    return text if len(text) <= limit else "…" + text[-(limit - 1):]


def _cell(text: str | None) -> str:
    return (text or "—").replace("|", "\\|")


def _table_cell(entity) -> str:
    """Tên bảng None nghĩa là không đọc được — nói thẳng, không để ô trống."""
    if entity.table_name is None:
        return "*chưa đọc được*"
    return f"`{entity.table_name}`"


def _routes(iam: IntermediateArchitectureModel, descriptions: Descriptions) -> list[str]:
    lines = ["## 2. API Routes", ""]
    if not iam.routes:
        return lines + ["Không phát hiện route nào.", ""]

    has_ai = bool(descriptions.by_id)
    tail = " Mô tả (AI) |" if has_ai else ""
    divider = "---|" if has_ai else ""
    lines += [
        "| Method | Đường dẫn | Hàm xử lý | Gọi tới | Bằng chứng / đầy đủ | Lý do | Vị trí |"
        + tail,
        "|---|---|---|---|---|---|---|" + divider,
    ]
    for index, route in enumerate(iam.routes):
        resolved = [c for c in route.calls if c.resolved]
        calls = ", ".join(f"`{c.name}`" for c in resolved[:3]) or "—"
        if len(resolved) > 3:
            calls += f" (+{len(resolved) - 3})"
        note = _cell(descriptions.get(route_id(index))) + " |" if has_ai else ""
        lines.append(
            f"| {route.method} | `{_short(route.path)}` | `{route.handler_function}` "
            f"| {calls} | {_evidence(route)} | {_cell(route.reason)} | {_where(route.location)} |"
            + note
        )
    return lines + [""]


def _entities(iam: IntermediateArchitectureModel, descriptions: Descriptions) -> list[str]:
    lines = ["## 3. Bảng dữ liệu", ""]
    if not iam.entities:
        return lines + ["Không phát hiện bảng nào.", ""]

    lines += [
        "| Class | Bảng | Cột | Khoá ngoại | Class cha | Bằng chứng / đầy đủ | Lý do | Vị trí |",
        "|---|---|---|---|---|---|---|---|",
    ]
    has_ai = bool(descriptions.by_id)
    if has_ai:
        lines[-2] += " Mô tả (AI) |"
        lines[-1] += "---|"
    for index, entity in enumerate(iam.entities):
        keys = [c.name for c in entity.columns if c.is_primary_key]
        columns = f"{len(entity.columns)}" + (f" (khoá chính: {', '.join(keys)})" if keys else "")
        fks = ", ".join(
            f"`{c.name}` → `{c.foreign_key_ref}`" for c in entity.columns if c.foreign_key_ref
        )
        base = "—"
        if entity.base_class is not None:
            base = f"`{entity.base_class.name}`"
            if entity.base_class.resolved:
                base += f" ({_short(entity.base_class.resolved_module, 30)})"
            else:
                base += " (ngoài repo)"
        lines.append(
            f"| `{entity.class_name}` | {_table_cell(entity)} | {columns} | {fks or '—'} "
            f"| {base} | {_evidence(entity)} | {_cell(entity.reason)} "
            f"| {_where(entity.location)} |"
            + (_cell(descriptions.get(entity_id(index))) + " |" if has_ai else "")
        )
    return lines + [""]


def _external(iam: IntermediateArchitectureModel, descriptions: Descriptions) -> list[str]:
    lines = ["## 4. Phụ thuộc bên ngoài", ""]
    if not iam.external_calls:
        return lines + ["Không phát hiện lời gọi HTTP ra ngoài nào.", ""]

    lines += [
        "| Method | Đích đến | Gọi từ | Bằng chứng / đầy đủ | Lý do | Vị trí |",
        "|---|---|---|---|---|---|",
    ]
    has_ai = bool(descriptions.by_id)
    if has_ai:
        lines[-2] += " Mô tả (AI) |"
        lines[-1] += "---|"
    for index, call in enumerate(iam.external_calls):
        guard = "" if call.inside_try_except else " ⚠"
        lines.append(
            f"| {call.http_method or '—'} | `{_short(call.url_or_host)}`{guard} "
            f"| `{call.caller_function}` | {_evidence(call)} | {_cell(call.reason)} "
            f"| {_where(call.location)} |"
            + (_cell(descriptions.get(external_id(index))) + " |" if has_ai else "")
        )
    lines.append("")
    if any(not c.inside_try_except for c in iam.external_calls):
        lines += ["⚠ = lời gọi không nằm trong khối `try/except`.", ""]
    return lines


def _call_graph(iam: IntermediateArchitectureModel) -> list[str]:
    """Chỉ hiện hàm có liên quan trực tiếp tới route, bảng hoặc lời gọi ra ngoài."""
    lines = ["## 5. Quan hệ gọi hàm (rút gọn)", ""]

    interesting = {r.handler_function for r in iam.routes}
    interesting |= {c.caller_function.split(".")[-1] for c in iam.external_calls}
    shown = [f for f in iam.functions if f.name in interesting and f.calls]

    if not shown:
        return lines + ["Không có hàm nào liên quan trực tiếp tới route hay bảng dữ liệu.", ""]

    for function in sorted(shown, key=lambda f: f.qualified_name)[:40]:
        lines.append(f"- **`{function.qualified_name}`** — {_where(function.location)}")
        for ref in function.calls:
            if ref.resolved:
                lines.append(f"  - `{ref.name}` → `{ref.resolved_module}`")
            else:
                lines.append(f"  - `{ref.name}` → *chưa nối được: {ref.reason}*")
    if len(shown) > 40:
        lines.append(f"- *… và {len(shown) - 40} hàm nữa, xem đầy đủ trong `graph.json`*")
    return lines + [""]


def _diagram_link() -> list[str]:
    return [
        "## 6. Sơ đồ phụ thuộc",
        "",
        "Xem file `diagram.mmd` đi kèm. Sơ đồ rút gọn để đọc được; dữ liệu đầy đủ nằm"
        " trong `graph.json`.",
        "",
    ]


def _graph_summary(iam: IntermediateArchitectureModel) -> list[str]:
    return [
        "## 7. Graph node/cạnh",
        "",
        "Cùng dữ liệu ở trên, trình bày dạng node và cạnh. Xem `graph.json`.",
        "",
    ]


CATEGORY_LABELS = {
    "unresolved_reference": "Tham chiếu chưa nối được đích",
    "empty_handler_calls": "Hàm xử lý route không thấy lời gọi nào",
    "orphan_entity": "Bảng không ai tham chiếu tới",
    "external_call_no_error_handling": "Gọi ra ngoài không có xử lý lỗi",
}


def _review_findings(review: Review) -> list[str]:
    lines = ["## 8. Cảnh báo cần người xác nhận", ""]
    if not review.findings:
        return lines + ["Không có cảnh báo nào trong lần chạy này.", ""]

    lines += [
        "Đây là **cảnh báo**, không phải kết luận. Mỗi dòng trỏ về một vị trí cụ thể"
        " trong source để tự kiểm chứng.",
        "",
        "| Loại | Nội dung | Vị trí |",
        "|---|---|---|",
    ]
    for finding in review.findings:
        label = CATEGORY_LABELS.get(finding.category, finding.category)
        lines.append(
            f"| {label} | {_cell(finding.summary)} | {_where(finding.evidence_location)} |"
        )
    return lines + [""]


def _tool_limitations(iam: IntermediateArchitectureModel) -> list[str]:
    """Ba lỗi đo được ở Mốc 7, xem EVALUATION.md mục 5.

    Đây là giới hạn của bản thân công cụ, không phải của repo đang phân tích, nên
    luôn in ra. Người đọc cần biết chỗ nào trong tài liệu này không đáng tin trước
    khi dùng nó, chứ không phải sau khi tự phát hiện.
    """
    unknown = [entity for entity in iam.entities if entity.table_name is None]
    lines = ["### Chỗ trong tài liệu này chưa đầy đủ", ""]
    for reason in iam.resolution.partial_reasons[:10]:
        lines.append(f"- Giới hạn resolver: {reason}")
    notes = [note for module in iam.semantic_program.modules for note in module.analysis_notes]
    if notes:
        lines += [f"- {len(notes)} cấu trúc chưa được mô hình hóa đầy đủ; xem `semantic_program.modules[].analysis_notes` trong IAM.json."]
    if iam.framework_analysis.dropped_operations:
        lines += [f"- {len(iam.framework_analysis.dropped_operations)} thao tác framework chưa dựng được đầy đủ; xem IAM.json."]
    lines.append("")

    if unknown:
        lines += [
            f"**{len(unknown)} bảng dưới đây không đọc được tên bảng.** Các lớp này"
            " không khai `__tablename__`; lớp cơ sở của repo tự sinh tên lúc chạy, mỗi"
            " repo một quy tắc riêng. Cột *Bảng* ở mục 3 ghi *chưa đọc được* thay vì"
            " đoán. Muốn biết tên thật thì đọc lớp cơ sở, hoặc xem schema của cơ sở"
            " dữ liệu.",
            "",
        ]
        for entity in unknown[:10]:
            lines.append(f"- `{entity.class_name}` — {_where(entity.location)}")
        if len(unknown) > 10:
            lines.append(f"- *… và {len(unknown) - 10} lớp nữa, xem `IAM.json`*")
        lines.append("")

    conditional = [r for r in iam.routes if r.reason and "chỉ đăng ký khi" in r.reason]
    if conditional:
        lines += [
            f"**{len(conditional)} route chỉ tồn tại ở một số môi trường.** Chúng được"
            " đăng ký bên trong một khối `if`, nên không có mặt ở mọi lần triển khai."
            " Điều kiện cụ thể ghi ở cột *Lý do* của mục 2.",
            "",
        ]
        for route in conditional[:10]:
            lines.append(f"- `{route.method} {route.path}` — {_where(route.location)}")
        if len(conditional) > 10:
            lines.append(f"- *… và {len(conditional) - 10} route nữa*")
        lines.append("")

    if not unknown and not conditional:
        lines += ["Không có giới hạn nào thuộc loại này trong lần chạy này.", ""]
    return lines


def _limitations(
    iam: IntermediateArchitectureModel, descriptions: Descriptions, review: Review
) -> list[str]:
    """Luôn xuất hiện, kể cả khi rỗng."""
    lines = ["## 9. Giới hạn đã biết", ""]
    lines += _tool_limitations(iam)
    empty = True

    problems = [*descriptions.problems, *review.problems]
    if problems:
        empty = False
        lines += [
            "### Phần AI không chạy được",
            "",
            "Phần dữ liệu đọc từ code vẫn đầy đủ; chỉ thiếu lời văn do AI viết.",
            "",
        ]
        for problem in problems[:5]:
            lines.append(f"- {problem}")
        lines.append("")

    if descriptions.rejected:
        empty = False
        lines += [
            f"- AI trả về {descriptions.rejected} mô tả trỏ tới mã không tồn tại."
            " Đã loại bỏ, không đưa vào tài liệu.",
            "",
        ]

    skipped = [s for s in iam.detected_stack.services if not s.analyzed]
    if skipped:
        empty = False
        lines += ["### Đơn vị bị bỏ qua", ""]
        for service in skipped:
            lines.append(
                f"- **{service.name or '(thư mục gốc)'}** "
                f"({service.language or 'chưa rõ'}, {service.file_count} file): "
                f"{service.skip_reason}. Phần hệ thống này không có trong tài liệu."
            )
        lines.append("")

    if iam.parse_errors:
        empty = False
        lines += ["### File bỏ qua vì lỗi cú pháp", ""]
        for error in iam.parse_errors:
            lines.append(f"- `{error.file}`: {error.error_message}")
        lines.append("")

    if iam.unresolved_references:
        empty = False
        lines += [
            "### Tham chiếu chưa nối được đích",
            "",
            f"Có {len(iam.unresolved_references)} tham chiếu không xác định được đích trong"
            " repo. Đây là giới hạn đã biết của phân tích tĩnh, không phải lỗi: phần lớn do"
            " biến không khai báo kiểu, hoặc tên hàm chỉ có lúc chạy.",
            "",
        ]
        for item in iam.unresolved_references[:20]:
            lines.append(f"- {item.description} — {_where(item.location)}")
        if len(iam.unresolved_references) > 20:
            lines.append(
                f"- *… và {len(iam.unresolved_references) - 20} trường hợp nữa,"
                " xem đầy đủ trong `IAM.json`*"
            )
        lines.append("")

    if empty:
        lines += ["Không có giới hạn nào được ghi nhận trong lần chạy này.", ""]
    return lines
