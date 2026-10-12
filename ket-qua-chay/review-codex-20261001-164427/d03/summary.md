# D-03 — so sánh ứng viên chia nhóm (tập development)

Gold `candidate`; chỉ báo TP/FP/FN. Case có nhãn kiến trúc: 7.

| Ứng viên | Membership TP | FP | FN | Cạnh TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| A directory-v1 | 14 | 14 | 14 | 0 | 0 | 13 |
| B signals-v0 | 27 | 1 | 1 | 13 | 11 | 0 |
| C v8 | not_run | | | | | |

| Case | Ứng viên | Số nhóm | Membership TP/FP/FN | Cạnh TP/FP/FN |
|---|---|---:|---|---|
| orders-base | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-base | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| orders-prefix | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-prefix | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| orders-two-apps | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-two-apps | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| orders-wrapper-real | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-wrapper-real | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| orders-wrapper-fake | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-wrapper-fake | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| orders-dynamic-prefix | A directory-v1 | 1 | 2/2/2 | 0/0/2 |
| orders-dynamic-prefix | B signals-v0 | 4 | 4/0/0 | 2/1/0 |
| dispatch-case-read | A directory-v1 | 2 | 2/2/2 | 0/0/1 |
| dispatch-case-read | B signals-v0 | 5 | 3/1/1 | 1/5/0 |
