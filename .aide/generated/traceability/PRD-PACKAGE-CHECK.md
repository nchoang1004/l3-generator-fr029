# Kiểm cấu trúc hồ sơ BL-r5 — CHG-L3GEN-2026-002

Ngày: 2026-09-23. Kiểm cục bộ cho candidate chưa review; không phải `check-sdlc` chính thức hoặc kiểm thử sản phẩm.

| Kiểm | Kết quả |
|---|---|
| Baseline 20 artifact: hash, revision, key, UID | Pass bằng `scripts/prd_package.py check --change-set CHG-L3GEN-2026-002 --baseline BL-r5.yaml` |
| 9 FR / 36 AC / 5 NFR | Đủ trong candidate |
| AC có Given/When/Then, mã không trùng | Pass: 36/36, không trùng |
| Key mới không trùng key cũ | FR-019 đến 027, NFR `-002` và OPS-001, GOAL-004 đến 007, KPI-006 đến 010, CAP-007 đến 012 |
| Open Question | OQ-007 và OQ-008 closed |
| impact.yaml | Parse YAML được; 20 touches, 0 FR bị OQ chặn. 6 stale là CAP-007 đến 012: L1 nằm ngoài baseline và trỏ vào FR; nghĩa là phải rà lại L1 khi yêu cầu đổi |
| L1 coverage | `scripts/l1_coverage.py` xanh: 9/9 FR có CAP, revision khớp |
| L2 bổ sung lát sinh L3 | Kiểm cục bộ: revision trong `verified_against` khớp; 8 CMP đủ 7 mục; ADR-003 rev 2, CMP rev 2, threat model rev 4 và AVW đồng bộ |
| Link Markdown nội bộ | 0 thiếu file trong phạm vi kiểm nêu dưới đây; không kết luận về tài liệu ngoài phạm vi |
| Scope Gate | Chưa review, chưa ký |

BL-r1 đến BL-r4 giữ lại làm lịch sử. BL-r5 cập nhật FR-027 rev 3, giữ PRD rev 28. L1/L2 lập trước khi ký Scope Gate theo yêu cầu của Khiêm; nếu review đổi FR thì rà lại thiết kế. Architecture Gate chưa qua, chưa lập L3 contract của công cụ.

Phạm vi kiểm link: `.aide/` hiện hành, README và hướng dẫn review; bỏ code fence, anchor thuần và URL ngoài, giải mã URL-encoded path. Check hash không xác nhận nội dung đúng. Script impact không thay kiểm revision hoặc liên kết L2; các kiểm đó thực hiện riêng.

Chưa thực hiện: benchmark sản phẩm, product test, threat-model test, chọn repo dataset, đo token thật. Thử nhanh model trên app mẫu 6 file ghi ở OQ-L3GEN-008. `implementation_target`/`validated_by` lập sau Scope Gate.

**Lịch sử.** Báo cáo cho BL-r14 của CHG-L3GEN-2026-001 nằm trong lịch sử git của file này; BL-r14 chỉ kiểm lại được tại commit `1c283509c3ec1eec5e65de1005f00a8d4e3cbc91`.
