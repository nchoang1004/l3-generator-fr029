---
key: TEST-FR029-CHECKER-20261009
type: test-evidence
group: evidence
scope: lifecycle
change_set: CHG-L3GEN-2026-002
derived_from: [CR-L3GEN-2026-008]
captured_at: "2026-10-09T03:18Z"
captured_against:
  code_tree: "79c8235 + thay đổi chưa commit trên feature/l3-fr029 (các file dưới đây chưa được git theo dõi)"
  files:
    - { path: slice/l3slice/docfacts.py, sha256_16: dcc3b0fea3eeda48 }
    - { path: slice/l3slice/astscan.py, sha256_16: 985d5c92b667a6d7 }
    - { path: slice/tools/fr029_checkaudit.py, sha256_16: e009051fc3222ffb }
    - { path: slice/tests/test_checker_counterexamples.py, sha256_16: 4e6a210928d855dd }
ai_assisted: true
---

# Bằng chứng test bộ kiểm FR-029 — 09/10/2026

Thư mục này ghi kết quả test của bộ kiểm FR-029 (`docfacts.py`, `astscan.py`) sau đợt nâng cấp 07–09/10/2026. Bộ kiểm là code tĩnh. Nó kiểm câu trả lời của agent LLM, không tự tạo dữ kiện. Báo cáo: [docs/FR029-bao-cao-kiem-bo-kiem-20261008.md](../../../../docs/FR029-bao-cao-kiem-bo-kiem-20261008.md). Review của giám khảo: [../../reviews/fr029-checker-20261007-09/](../../reviews/fr029-checker-20261007-09/README.md).

## 1. Trạng thái

| Phép thử | Trạng thái | File |
|---|---|---|
| Toàn bộ unit test (`python -m unittest discover -s tests`, chạy trong `slice/`) | **failed**: 426 test, 1 lỗi `test_gateway.Gateway.test_unknown_ids_are_dropped`. Lỗi này có từ trước đợt này, không liên quan bộ kiểm | `unit-tests.log` |
| Gold audit r41 (37 bộ có gold) | **passed**: 0 lỗi ở mọi chỉ số | `gold-audit-r41.summary.json` |
| Bộ kiểm giả "luôn nhận" / "luôn từ chối" | **passed**: phép đo báo lỗi lớn ở mọi chỉ số, tức là phép đo phân biệt được | `gold-audit-r41-sanity-{accept,reject}.summary.json` |
| Dòng có từ 2 lời gọi HTTP, nộp thiếu 1 thì vẫn bị đánh dấu | **not_run** trên gold (gold có 0 dòng như vậy). Chỉ có unit test kiểm | `multi_call_lines: 0` trong summary |
| Held-out 10 repo, gói cuối r32 | **not_run** về chấm lại. Giám khảo mới chấm lại PrintStash và caura (gói r23). Gói r32 lưu để chấm sau | `heldout-r32/` |
| Đo cả sản phẩm (agent LLM + bộ kiểm) sau đợt sửa | **not_run**. Tài khoản OpenAI hết tiền | — |

`passed` của gold audit chỉ đúng với 37 bộ đã đo. Nó không chứng minh bộ kiểm đúng trên mọi repo.

## 2. Gold audit đo gì

Công cụ `slice/tools/fr029_checkaudit.py` đóng vai một agent trả lời đúng gold, rồi trả lời sai có chủ ý, và đếm phản ứng của bộ kiểm.

| Chỉ số trong summary | Nghĩa | r41 |
|---|---|---|
| `routes_false_rejection` / `routes_checked` | Route đúng bị từ chối | 0 / 406 |
| `routes_false_acceptance` / `route_mutations` | Route sai bị nhận | 0 / 1549 |
| `prefix_missing_accepted` / `prefix_mutations` | Thiếu prefix router vẫn nhận | 0 / 131 |
| `registration_false_rejection` / `registration_checked` | Route gold bị coi là chưa đăng ký | 0 / 408 |
| `dependency_false_acceptance` / `dependency_mutations` | Dependency sai bị nhận | 0 / 333 |
| `reminders_wrong`, `dep_params_missed` / `gold_dep_params` | Nhắc tham số sai, sót | 0, 0 / 69 |
| `http_false_acceptance` / `http_mutations` | Lời gọi HTTP sai bị nhận | 0 / 125 |
| `gold_items_not_flagged` / `gold_items_for_suspects` | Route/HTTP gold không bị đánh dấu nghi ngờ | 0 / 441 |
| `suspects_not_gold_item` | Dòng đánh dấu thừa | 4 |

## 3. Repo held-out

Chọn theo thứ tự kết quả `gh search repos fastapi --language=python --sort=updated --stars=">=10"`. Bỏ repo trên 60 MB (theo kích thước GitHub) và repo không phải ứng dụng FastAPI. Clone `--depth 1`.

| Repo | Commit | Thư mục | Ghi chú |
|---|---|---|---|
| Caoyongqi912/case_auto_hub | 561ea0f | `D:/VSF/l3-heldout-repos2/` | |
| primerhq/primer | 0ef7ae5 | `D:/VSF/l3-heldout-repos3/` | |
| caura-ai/caura | 886b8ea | như trên | |
| stevezau/shortlist | 7e3d751 | như trên | |
| ncoevoet/facet | d7beae3 | như trên | |
| spatiumnorth/spatiumddi | cfcc15a | như trên | |
| xiao-villamor/PrintStash | 8d70c55 | như trên | |
| kyleyct/wifi-densepose-elderly | c156cc3 | như trên | Bỏ: không phải FastAPI |
| lindseystead/ai-pdf-autofiller | 4347276 | `D:/VSF/l3-heldout-repos4/` | |
| scalekit-inc/scalekit-sdk-python | 1731d47 | như trên | Bỏ: SDK, FastAPI chỉ ở ví dụ |
| dengyie/xianyu-auto-bot | a2bfe97 | như trên | |
| 3441293738/creatorhub | 037f8b3 | như trên | |

Bốn repo đợt đầu (dispatch, nsidnev, rhoboro, rafsaf) ở `D:/VSF/l3-heldout-repos/`, xem HANDOFF.

## 4. Chạy lại

```bash
cd slice
python -m unittest discover -s tests
python tools/fr029_checkaudit.py --out ../ket-qua-chay/<thư-mục-mới>
python tools/fr029_checkaudit.py --out ../ket-qua-chay/<thư-mục-mới>-sanity-accept --sanity accept
python tools/fr029_checkaudit.py --out ../ket-qua-chay/<thư-mục-mới>-sanity-reject --sanity reject
python tools/fr029_checkaudit.py --out ../ket-qua-chay/<thư-mục-mới> --heldout <đường dẫn repo> ...
```

Kết quả đầy đủ của mọi lần đo (r21–r41, gói held-out r11–r32) ở `ket-qua-chay/fr029-checkaudit-2026100[89]-r*` và `ket-qua-chay/fr029-heldout-2026100[89]-r*`. Mỗi `summary.json` có mục `versions` ghi hash code lúc đo.
