---
uid: "01M30ZP2F2555Q072FXDDZG3W4"
key: "CAP-L3GEN-004"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "approved"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-011"],"governed_by":["ADR-2026-001"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-011","revision":8},{"key":"ADR-2026-001","revision":4},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-004 — Dựng mô hình kiến trúc mức component

## Năng lực này là gì

Gộp `code fact` thành `architecture claim`: nhóm thành viên code thành `component` theo
rule grouping đã công bố, gán `component role`, và tổng hợp nhiều lời gọi code giữa hai
component thành một `dependency` duy nhất kèm danh sách nguồn đóng góp.

Đây là năng lực mà [ADR-2026-001](../adr/ADR-2026-001.md) quyết định ranh giới: phân tích
đủ sâu, trình bày ở mức L3. Nó đứng riêng chính vì quyết định đó cần một chỗ để bám.

## Ranh giới

- Lớp mặc định dừng ở application/component (bất biến miền #7). Không có node cho mỗi
  function trong mô hình kiến trúc.
- Chỉ nâng lên claim khi có evidence membership. Tên thư mục hay tên class riêng lẻ không
  đủ chứng minh một component.
- **Không** tự đọc source — đầu vào là fact từ [CAP-L3GEN-003](CAP-L3GEN-003.md).
- Dữ kiện mức file/class/function vẫn giữ lại, nhưng ở lớp evidence do
  [CAP-L3GEN-005](CAP-L3GEN-005.md) công bố.
- Ngoài phạm vi: call graph đầy đủ mức function làm đầu ra cho người đọc, graph query API
  và graph traversal.

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md) | Xem component và tài liệu L3 của service | M2: component model và L3 ban đầu; M3: nghiệm thu đầy đủ |
