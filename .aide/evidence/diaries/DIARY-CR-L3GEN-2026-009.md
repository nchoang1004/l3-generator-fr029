---
key: DIARY-CR-L3GEN-2026-009
type: diary
group: evidence
scope: lifecycle
change_set: CHG-L3GEN-2026-002
derived_from: [CR-L3GEN-2026-009]
captured_against:
  artifacts:
    - { key: FR-L3GEN-029, revision: 3 }
    - { key: FR-L3GEN-030, revision: 2 }
    - { key: FR-L3GEN-031, revision: 2 }
    - { key: ADR-2026-006, revision: 1 }
  code_tree: "8accd89 + thay đổi chưa commit trên feature/l3-fr029"
ai_assisted: true
written_late: true
---

# DIARY-CR-L3GEN-2026-009 — Giảm token, sửa bộ kiểm, TAI-LIEU.md, bảng và sự kiện (11–12/10/2026)

Nhật ký do Claude ghi ngày 12/10, khi người dùng yêu cầu viết đủ hồ sơ theo `Quy_tac/`. Không viết song song như EXEC §B.15 yêu cầu. Chi tiết từng task ở `DIARY-TASK-L3GEN-029-10` … `13`, `DIARY-TASK-L3GEN-030-1`, `DIARY-TASK-L3GEN-031-1`.

## Diễn giải

| Tin (giờ VN) | Claude hiểu là |
|---|---|
| 19:38–19:43 "gọi quá nhiều lần nên khá tốn token" | Giảm số request; giữ độ chính xác; đo lại cùng repo, cùng model |
| 20:00 "dùng model cao hơn" | Thử gpt-5 trong trần người dùng duyệt |
| 20:08 "xem những ý kiến này đúng không và test kĩ offline" | Tái hiện từng ý của review Codex bằng phép thử không gọi model |
| 20:38 "dùng cách ấy để test sau này" | Từ nay test bằng agent Claude hoặc Codex đóng vai model; không thay nghiệm thu bằng model thật |
| 20:38 "đầu ra chỉ được ghi rõ trong 1 file" + 20:42 "cách A" | Thêm `TAI-LIEU.md`; giữ file máy đọc của FR-029 |
| 20:42 "cứ để đấy" | Không làm archdia.json; AC-030-05, AC-031-04 hoãn |
| 20:59 "làm đi" + /goal | Làm 5 đợt trong bản nghiên cứu, test kỹ |
| 01:07 "kiểm cho trung thực và công bằng" | Repo held-out, đầu ra đóng băng bằng hash, đề giám khảo viết trước, giám khảo khác model |
| 01:30 "phần csdl … kiểm tra thật kĩ" | Gold + đối chiếu FR-030 + 2 vòng giám khảo độc lập |
| 01:29 + 06:22 "viết đầy đủ … sửa lại ux/ui để demo" | Hồ sơ CR/OQ/Task/CTX/PLAN/DIARY/REVIEW cho 11–12/10; sửa giao diện web theo `taste-skill`; tài liệu hướng dẫn demo |

## Đi chệch

- Không ghi CR trước khi làm (EXEC §B.3). Ghi muộn ngày 12/10: CR-L3GEN-2026-009.
- Không có plan trước khi code cho TASK-L3GEN-029-10, 11, 12, 030-1, 031-1. PLAN của các task này ghi muộn, nói rõ không phải plan trước. TASK-L3GEN-029-13 (giao diện) có plan trước khi code.
- Claude tự chọn đọc tĩnh cho bảng, sự kiện, thư viện, cấu hình, middleware, quan hệ component mà không hỏi lại (OQ-L3GEN-019).
- Thêm đầu ra ngoài spec (`TAI-LIEU.md`, errors/tags/summary/examples) khi chưa có CR sửa FR (OQ-L3GEN-020).
- 5 lần chạy thật với OpenAI (0,442 USD) có duyệt trần tiền, nhưng waiver NFR-SEC-002 ghi phạm vi 07/10 (OQ-L3GEN-021).
- Giám khảo dùng agent Claude Sonnet vì Codex báo 401. Agent đóng vai model và giám khảo cùng họ Claude, có thể thiên vị.

## Đánh đổi

- Test bằng agent đóng vai model: gần như không tốn tiền API, kiểm được bộ kiểm và prompt; không đo được model thật.
- Đọc tĩnh phần không phải API: không tốn token, đo được với gold (32/32 bảng, 341/341 cột); lệch hướng "agent thuần".

## Câu hỏi mở

OQ-L3GEN-019, 020, 021, 022 (mở 12/10/2026).

## Ghi bù 09/10/2026

Tin 09/10 10:37 "có thể bịa tí cho đẹp cũng đc" (CR-L3GEN-2026-008-requests-03). Claude trả lời trong chat là không bịa: hồ sơ ghi muộn, để draft, không lập approval hay số đo chưa có. Hồ sơ 12/10 giữ cùng cách làm.
