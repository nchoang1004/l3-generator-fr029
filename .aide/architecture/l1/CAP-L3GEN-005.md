---
uid:
key: "CAP-L3GEN-005"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-007","FR-L3GEN-009"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-007","revision":5},{"key":"FR-L3GEN-009","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-005 — Công bố bằng chứng, giới hạn và chất lượng

## Năng lực này là gì

Làm cho kết quả kiểm chứng được. Năng lực này giữ đường truy ngược từ mỗi claim về đúng
`source snapshot` của lần chạy, gắn nhãn chất lượng (`exact`/`inferred`, `full`/`partial`,
`unresolved`/`ambiguous`), và công bố `limitation` cùng `coverage` của run.

Nó tồn tại riêng vì ba bất biến miền sống ở đây: mọi claim phải có evidence (#3);
"không phát hiện thấy" chỉ hợp lệ khi đã xét đủ, thiếu thì phải là limitation (#4); và
confidence, completeness, coverage là ba trục độc lập, không dùng trục này thay trục kia (#5).

## Ranh giới

- **Không** tạo ra claim mới. Nó mô tả chất lượng của cái đã có từ
  [CAP-L3GEN-003](CAP-L3GEN-003.md) và [CAP-L3GEN-004](CAP-L3GEN-004.md).
- Evidence chỉ trỏ vào chính snapshot của run đó, không trỏ sang source hiện tại hay
  snapshot khác (bất biến miền #1).
- `Finding` ở đây là cảnh báo tất định cần xác minh, **không** phải kết luận lỗ hổng bảo
  mật hay lỗi nghiệp vụ.
- Lỗi một file hoặc một adapter không được che mất phần hợp lệ của run (bất biến miền #10).
- **Không** quyết định cách hiển thị — đó là [CAP-L3GEN-006](CAP-L3GEN-006.md).

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md) | Kiểm chứng kết luận bằng nguồn và nhãn | M1 |
| [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md) | Báo lỗi và giới hạn theo từng lần phân tích | M1 |
