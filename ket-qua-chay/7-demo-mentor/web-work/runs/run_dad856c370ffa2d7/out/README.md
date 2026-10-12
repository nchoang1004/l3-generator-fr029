# repository — kết quả phân tích (bản sinh tự động)

- Snapshot: `snap:c1495361276c6c8cd263abcb7919dea2d99441c993412393b1b5bc40363054af`
- Schema 0.1.0; renderer slice-render-v2; template slice-template-v1
- Phạm vi: 32 file trong 1 unit; 13 file bị loại khỏi snapshot

## Sơ đồ component

```mermaid
flowchart LR
  n0["(root)"]
  n1["migrations"]
  n2["app"]
```

## Mục lục contract

- api: [tech-specs/APP/api/API-REPOSITORY-APP-v1.md](tech-specs/APP/api/API-REPOSITORY-APP-v1.md) — component `cmp_feb33ad0dd6c5afcb686ceacb60106d85eaf3b0b9033c5cb172ef4e7fd3ad589`
- table: [tech-specs/APP/schema/TBL-REPOSITORY-APP.md](tech-specs/APP/schema/TBL-REPOSITORY-APP.md) — component `cmp_feb33ad0dd6c5afcb686ceacb60106d85eaf3b0b9033c5cb172ef4e7fd3ad589`

## Mục lục EVT theo topic

- (không có)

## Contract chưa gán được component

- (không có)

## Giới hạn

- `SLICE_SCOPE` (inventory): Lát cắt đầu chỉ nhận route FastAPI và bảng SQLAlchemy Column
- `REFERENCE_UNRESOLVED` (extraction): 47 lời gọi chưa nối được đích; giữ là dữ kiện unresolved kèm lý do, không vẽ thành cạnh
- `MODEL_NOT_RUN` (model): Không gọi provider; tên component lấy từ membership

## Giới hạn biểu diễn

- `DDL_BLOCK_OMITTED`: Không bảng nào đủ dữ kiện cho DDL — `fact:0dabd6cd1f0d8e83556760f03b20af7650bdafe44da4d77a865b33e6f9e07b36`, `fact:678a9e546bff3fa2b09ad37a23d4e86203f60f53a7343fea0a0b61055d93b4fb`
- `DDL_TABLE_OMITTED`: dialect chưa biết — `fact:0dabd6cd1f0d8e83556760f03b20af7650bdafe44da4d77a865b33e6f9e07b36`
- `DDL_TABLE_OMITTED`: dialect chưa biết — `fact:678a9e546bff3fa2b09ad37a23d4e86203f60f53a7343fea0a0b61055d93b4fb`
