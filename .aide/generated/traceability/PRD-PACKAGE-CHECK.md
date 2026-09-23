# Kiểm cấu trúc hồ sơ BL-r1 — CHG-L3GEN-2026-002

Ngày: 2026-09-23. Kiểm cục bộ cho candidate chưa review; không phải `check-sdlc` chính thức hoặc kiểm thử sản phẩm.

| Kiểm | Kết quả |
|---|---|
| Baseline 19 artifact: hash, revision, key, UID | Pass bằng `scripts/prd_package.py check --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml` |
| 8 FR / 31 AC / 5 NFR | Đủ trong candidate |
| AC có Given/When/Then, mã không trùng | Pass: 31/31, không trùng |
| Key mới không trùng key cũ | FR-019 đến 026, NFR `-002` và OPS-001, GOAL-004 đến 007, KPI-006 đến 010 |
| Open Question | OQ-007 và OQ-008 closed; Change Set View không còn câu hỏi mở |
| impact.yaml | Parse YAML được; 19 touches, 0 stale, 0 FR bị OQ chặn |
| Link Markdown nội bộ | 543 lượt trong README, `docs/`, `.aide/` và file `.md` ở gốc; 0 thiếu file |
| Whitespace | `git diff --check` sạch, trừ ký tự CR có sẵn trong các file CRLF cũ giữ nguyên byte |
| Scope Gate | Chưa review, chưa ký |

Phạm vi kiểm link: bỏ code fence, anchor thuần và URL ngoài. Check hash không xác nhận nội dung đúng. Sinh CSV thành công không thay review nội dung.

`stale: 0` chỉ là kết quả của graph cục bộ. Script bỏ qua artifact deprecated, và không đọc quan hệ `derived_from`/`constrains`. ADR-2026-002 và threat model đã được gắn nhãn lỗi thời bằng tay.

Chưa thực hiện: benchmark sản phẩm, product test, threat-model test, chọn repo/commit cho dataset, đo token thật của tập dữ kiện, kiểm Groq trả JSON đúng schema. `implementation_target`/`validated_by` lập sau Scope Gate, phải xong trước Definition of Ready.

**Lịch sử.** Báo cáo ngày 18/09/2026 cho BL-r14 của CHG-L3GEN-2026-001 (40 artifact, 18 FR / 84 AC / 11 NFR) nằm trong lịch sử git của file này. BL-r14 chỉ kiểm lại được tại commit `1c283509c3ec1eec5e65de1005f00a8d4e3cbc91`, vì các file của nó đã chuyển sang `requirements/_superseded-r23/`.
