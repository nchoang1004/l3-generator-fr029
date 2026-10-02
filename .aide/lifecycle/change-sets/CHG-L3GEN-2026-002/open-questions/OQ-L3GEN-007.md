---
uid: "01M3632TDCAVXX8ND5BB6F53M0"
key: "OQ-L3GEN-007"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm và Hoàng"
due: "2026-09-22"
change_set: "CHG-L3GEN-2026-002"
---

# OQ-L3GEN-007 — Ngưỡng độ đúng khi dùng mô hình ngôn ngữ

## Câu hỏi

BL-r14 đặt precision 90% cho bộ luật tĩnh, vốn cho cùng kết quả mỗi lần chạy. Khi mô hình ngôn ngữ đề xuất component và quan hệ, sai số có dạng khác. Ngưỡng precision và recall, và ngưỡng cho nhãn mức chắc chắn, là bao nhiêu?

## Quyết định ngày 22/09/2026

**Người quyết định:** Khiêm và Hoàng.

- Precision và recall từ 80% trở lên cho mọi nhóm: route, entity/table, HTTP, config, event, thư viện, thành viên component, cạnh dependency.
- Nhãn khớp đáp án từ 80% trở lên.
- Tỷ lệ gán `exact` cho kết luận sai ở mức 5% trở xuống; đây là chỉ số chặn.

## Sửa đổi ngày 02/10/2026 (revision 2)

**Người quyết định:** Khiêm (CR-L3GEN-2026-004 và phiên rà Scope Gate).

| Phần | Trước | Sau | Lý do |
|---|---|---|---|
| Thành viên component, cạnh dependency | P, R ≥ 80% | Bỏ. Sơ đồ chấm bằng mũi tên giữa component: P ≥ 0,8, R ≥ 0,6, báo kèm Pk | Theo tiêu chí nhóm dùng khi phát triển; chấm theo khối, không chấm từng file |
| Nhãn khớp đáp án | ≥ 80% | Bỏ | KPI-L3GEN-009 chỉ đo `exact` sai, máy chấm theo đáp án KPI-L3GEN-008 (đề xuất của Hoàng) |
| `exact` sai | ≤ 5%, mọi kết luận | ≤ 5%, dữ kiện L3 | Mũi tên sơ đồ đều `exact`; tính trên mũi tên thì mâu thuẫn với P ≥ 0,8 |
| Dữ kiện L3 | 80% cho route, entity/table, HTTP, config, event, thư viện | Giữ 80%, thêm request/response model | Loại có trong FR-L3GEN-029 |
| Phạm vi chấm | Không nói | Từng repo kín nhỏ và vừa; repo lớn chỉ báo số | Mục tiêu repo nhỏ và vừa (30/09/2026) |

Ngưỡng ghi tại [NFR-L3GEN-ACC-002](../../../../requirements/nfr/NFR-L3GEN-ACC-002.md). OQ này không đặt số ở chỗ khác.

- **Blocking:** không còn.
- **Trạng thái:** closed.
