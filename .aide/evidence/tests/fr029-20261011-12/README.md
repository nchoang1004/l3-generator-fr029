# Bằng chứng test đợt 11–12/10/2026 (CR-L3GEN-2026-009)

File này liệt kê kết quả test đã chạy và nơi để bằng chứng gốc.

| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Suite `unittest`, 12/10 trước khi sửa giao diện | 520/521; lỗi duy nhất `test_gateway.Gateway.test_unknown_ids_are_dropped` (có từ trước) | `suite-before-ui.log` |
| Chạy thật oneshot trên Teamhide, 11/10 | gpt-4.1-mini 0/5 route; gpt-5 4–5/5 route; tổng 0,442 USD | `ket-qua-chay/oneshot-20261011*/cost.json` |
| Agent Claude đóng vai model, 12/10 | tdd-docker: route 6/6; Teamhide: completed, route 5/5 | `ket-qua-chay/roleplay-20261012/` |
| Held-out orderflow, 12/10 | Gold route 23/23, model 9/9, HTTP 2/2; giám khảo 202/213 | `ket-qua-chay/heldout-orderflow-20261012/`; REVIEW-HELDOUT-L3GEN-2026-008 |
| Bảng CSDL, 12/10 | Gold 32/32 bảng, 341/341 cột; giám khảo vòng 2 285/287 cột | `ket-qua-chay/db-check-20261012/`; REVIEW-HELDOUT-L3GEN-2026-009, 010 |
| Review code 11/10 | 8 lỗi, đều có test đỏ trước | `../fr029-code-review-20261011/`, `../fr029-review-20261011-*.log`; REVIEW-CODE-L3GEN-2026-013 |

Lệnh chạy suite (từ thư mục gốc repo):

```bash
scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
```
