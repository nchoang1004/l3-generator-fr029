# Kiểm bộ kiểm FR-029 bằng giám khảo độc lập — 07–09/10/2026

Loại: đánh giá tư vấn (adversarial review của code bộ kiểm và công cụ đo), chưa là Gate approval hoặc finding ID chính thức.

Thư mục này lưu nguyên văn đề bài gửi giám khảo và câu trả lời của họ. Bản gốc nằm ở scratchpad của phiên Claude (thư mục tạm, có thể mất), nên được chép vào đây. Báo cáo tổng hợp: [docs/FR029-bao-cao-kiem-bo-kiem-20261008.md](../../../../docs/FR029-bao-cao-kiem-bo-kiem-20261008.md).

- Giám khảo chính: Codex `gpt-6-astra`, `model_reasoning_effort=high`, chế độ `-s read-only`.
- Khi Codex hết lượt: agent Claude (`general-purpose`), cùng đề bài.
- Giám khảo được dặn không đọc `docs/`, `HANDOFF`, `.aide/evidence/reviews/`. Đề bài chấm held-out còn cấm đọc `slice/` (code bộ kiểm).
- Giờ ghi theo UTC, là lúc file kết quả được ghi.

## 1. Kiểm công bằng (tìm phản ví dụ, kiểm cách đo)

Mỗi vòng xác nhận các phản ví dụ của vòng trước rồi tìm phản ví dụ mới. Đề bài: `codex/codex_fairnessN.md`. Kết quả: `codex/codex_fairnessN_out.md` (vòng 1 không có số: `codex_fairness.md`).

| Vòng | Giám khảo | Lúc | Kết quả đo được tham chiếu | Ca vòng trước đã xử lý | Phản ví dụ mới |
|---|---|---|---|---|---|
| 1 | Codex | 07/10 21:07 | `ket-qua-chay/fr029-checkaudit-20261008-r*` (bản đầu) | — | 25 |
| 2 | Codex | 07/10 21:42 | r11 | xem file | 10 |
| 3 | Codex | 07/10 21:57 | r13 | xem file | 7 |
| 4 | Codex | 07/10 23:48 | r16-real | xem file | 8 |
| 5 | Codex | 08/10 00:03 | r20-real | 25 mục cũ | 7 |
| 6 | Codex | 08/10 09:05 | r26 | 7/7 | 8 |
| 7 | agent Claude | 08/10 (dừng vì giới hạn phiên) | r30 | — | 9 (script `claude-agents/audit7/new7.py`, chạy lại bởi phiên chính) |
| 7 | Codex | 08/10 14:59 | r30 | 8/8 | 8 |
| 8 | Codex | 08/10 15:27 | r33 | 7/8 | 7 |
| 9 | agent Claude | 08/10 (dừng vì giới hạn phiên) | r35 | — | 8 (ghi chú `claude-agents/audit9/notes.md`) |
| 9 | Codex | 08/10 20:30 | r35 | 8/8 | 7 |
| 10 | Codex | 08/10 20:47 | r38 | 6/7 | 6 |

Phản ví dụ được viết thành test trong `slice/tests/test_checker_counterexamples.py`: vòng 1 ở các lớp `Dependencies`, `Routes`, `HttpClaims`, `SuspectRecall`; vòng 2–10 ở `RoundTwo` … `RoundTen`, `RoundSevenCodex`, `RoundNineCodex`, `RoundThreeLeftovers`; phát hiện từ held-out ở `HeldOutFindings`. Từ vòng 4, test chạy đỏ trước khi sửa. Ngoại lệ: 3 test của vòng 1–3 viết cùng lúc với bản sửa, và 2 test trong `HeldOutFindings` (`album_id` là path, factory gọi trong alias) qua ngay từ đầu vì bộ kiểm vốn đã đúng.

## 2. Chấm repo chưa dùng (held-out)

Bộ kiểm xuất "gói" (tham số dependency nó nhắc, dòng nghi ngờ, decorator bị từ chối). Giám khảo đọc source của repo và chấm từng mục. Đề bài: `codex/codex_heldoutX.md`.

| Đợt | Giám khảo | Lúc | Repo | Gói được chấm | Kết quả |
|---|---|---|---|---|---|
| 1 | Codex | 07/10 21:05 | dispatch, nsidnev, rhoboro, rafsaf | bản đầu | `codex/codex_heldout_out.md` |
| 2 | Codex | 07/10 21:40 | như trên | `fr029-heldout-20261008-r6` | `codex/codex_heldout2_out.md` |
| 3 | Codex | 07/10 23:57 | case_auto_hub | r9 | `codex/codex_heldout3_out.md` |
| 4a–c | Codex | 08/10 08:40–08:42 | primer, caura, shortlist | r13 | `codex/codex_heldout4{a,b,c}_out.md` |
| 5a–c | agent Claude | 08/10 09:26–09:32 | facet, spatiumddi, PrintStash | r18 | `claude-agents/judge-{facet,spatiumddi,printstash}.md` (trích từ bản ghi phiên vì Codex hết lượt; đề bài `codex/codex_heldout5{a,b,c}.md`) |
| 6b–c | Codex | 08/10 15:26 | caura, PrintStash (chấm lại sau sửa) | r23 | `codex/codex_heldout6{b,c}_out.md` |
| 7a–c | Codex | 08/10 20:56–21:00 | ai-pdf-autofiller, xianyu-auto-bot, creatorhub | `fr029-heldout-20261009-r30` | `codex/codex_heldout7{a,b,c}_out.md` |

## 3. Chỗ lệch quy trình cần biết khi đọc

- Đề bài vòng 6–10 có đoạn "ghi chú của tác giả" về các mục chưa sửa. Đề bài chấm held-out từ đợt 5 có thêm quy ước phạm vi (FR-028, chỉ tính lời gọi trực tiếp) và gợi ý về cách gói trình bày. EXEC §B.17 cấm đưa lý lẽ của tác giả cho reviewer. Ghi ở `DIARY-CR-L3GEN-2026-008`.
- Hai agent Claude vòng 7 và 9 bị dừng giữa chừng. Phát hiện của họ được phiên chính chạy lại và kiểm bằng test trước khi tính.
- Gói chấm và code thay đổi trong lúc một số vòng Codex đang chạy (Codex tự ghi chú ở vòng 9). Mỗi file kết quả có ghi hash code mà giám khảo đã đọc.

## 4. Bản ghi review đúng khuôn (thêm 09/10/2026)

Từ các file trong thư mục này đã sinh bản ghi review theo khuôn `REVIEW-*.yaml` của dự án (finding ghi ngay trong file, như `REVIEW-ARCH-L3GEN-2026-001`). Finding đánh số `FIND-L3GEN-001` tới `165`, có `severity`, `route`, `disposition` (EXEC §D.3) và `resolution.status` lấy từ phán quyết của vòng sau.

| File | Nội dung |
|---|---|
| `../REVIEW-CODE-L3GEN-2026-001.yaml` … `010.yaml` | 10 vòng Codex, sinh bằng script từ JSON Codex trả về |
| `../REVIEW-CODE-L3GEN-2026-011.yaml`, `012.yaml` | 2 vòng agent Claude bị dừng giữa chừng |
| `../REVIEW-HELDOUT-L3GEN-2026-001.yaml` … `007.yaml` | 7 đợt chấm repo chưa dùng |

Các ca phiên chính tự tìm khi sửa ghi riêng ở mục `self_found_while_fixing`, không tính là phát hiện của giám khảo.
