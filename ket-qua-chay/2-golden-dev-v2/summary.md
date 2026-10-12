# Golden v1 — tập development

Gold: `candidate`, human_review_complete = False. Chỉ báo TP/FP/FN, không báo tỷ lệ (D12).

Extractor: `slice-ast-v3`. Case: 38. Không chấm được: không.

| Nhóm | TP | FP | FN |
|---|---:|---:|---:|
| entity | 18 | 0 | 4 |
| entity_columns | 108 | 0 | 0 |
| limitation | 2 | 0 | 0 |
| reference | 84 | 0 | 1 |
| route | 61 | 0 | 0 |

false_exact (tổng): 0

| Nguồn / nhóm | TP | FP | FN |
|---|---:|---:|---:|
| fastapi-docs/route | 7 | 0 | 0 |
| netflix-dispatch/entity | 2 | 0 | 2 |
| netflix-dispatch/entity_columns | 60 | 0 | 0 |
| netflix-dispatch/limitation | 0 | 0 | 0 |
| netflix-dispatch/reference | 5 | 0 | 0 |
| netflix-dispatch/route | 18 | 0 | 0 |
| orders-fixture/entity | 11 | 0 | 2 |
| orders-fixture/entity_columns | 27 | 0 | 0 |
| orders-fixture/limitation | 2 | 0 | 0 |
| orders-fixture/reference | 54 | 0 | 0 |
| orders-fixture/route | 15 | 0 | 0 |
| pycg/reference | 25 | 0 | 1 |
| sqlmodel-docs/entity | 5 | 0 | 0 |
| sqlmodel-docs/entity_columns | 21 | 0 | 0 |
| sqlmodel-docs/route | 21 | 0 | 0 |
