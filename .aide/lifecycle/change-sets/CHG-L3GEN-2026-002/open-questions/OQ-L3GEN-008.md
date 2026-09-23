---
uid: "01M3632TDD2AVT9ECEZCYQHP43"
key: "OQ-L3GEN-008"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm"
due: "2026-09-23"
change_set: "CHG-L3GEN-2026-002"
---

# OQ-L3GEN-008 — Provider, model và trần mỗi lần chạy

## Câu hỏi

Dùng provider và model nào trong quota miễn phí? Repository lớn tới đâu thì còn chạy nổi trong quota đó?

## Dữ liệu đầu vào

Khiêm cung cấp giới hạn gói miễn phí của Groq ngày 23/09/2026. Bốn cột theo thứ tự: request/phút, request/ngày, token/phút, token/ngày.

| Model | Request/phút | Request/ngày | Token/phút | Token/ngày |
|---|---|---|---|---|
| meta-llama/llama-prompt-guard-2-86m | 30 | 14.400 | 15.000 | 500.000 |
| openai/gpt-oss-120b | 30 | 1.000 | 8.000 | 200.000 |
| openai/gpt-oss-20b | 30 | 1.000 | 8.000 | 200.000 |
| openai/gpt-oss-safeguard-20b | 30 | 1.000 | 8.000 | 200.000 |
| qwen/qwen3.8-27b | 30 | 1.000 | 8.000 | 200.000 |

## Quyết định ngày 23/09/2026

**Người quyết định:** Khiêm giao Agent chọn trong phiên làm việc. Khiêm xác nhận hoặc đổi khi review Scope Gate.

**Chọn `openai/gpt-oss-120b` trên Groq.**

| Lý do | Chi tiết |
|---|---|
| Loại hai model không dùng được | `llama-prompt-guard-2-86m` là model phân loại prompt độc hại; `gpt-oss-safeguard-20b` là model phân loại theo chính sách an toàn. Cả hai không dùng để đề xuất kiến trúc |
| Quota như nhau | Ba model còn lại có cùng giới hạn. Chọn model nhỏ hơn không được thêm quota |
| Chọn model lớn nhất | Cùng quota thì chọn model lớn nhất trong ba. Chất lượng trên bài toán này **chưa đo**; M2 đo theo OBS-L3GEN-001 |

**Trần mỗi lần chạy:** tính theo token của tập dữ kiện, không theo số file, vì model nhận tập dữ kiện chứ không nhận source. Con số ghi tại [NFR-L3GEN-AI-002](../../../../requirements/nfr/NFR-L3GEN-AI-002.md). Quy đổi sang số file hoặc số dòng code chưa đo; M1 đo và công bố.

**Không tự đổi model.** Hết quota thì dừng và báo. Đổi sang model khác là đổi cấu hình, và ghi vào provenance của lần chạy.

- **Blocking:** không còn.
- **Trạng thái:** closed.
- **Còn phải kiểm ở M1:** model có trả JSON đúng schema ổn định không; số token thực tế của tập dữ kiện trên repo mẫu.
