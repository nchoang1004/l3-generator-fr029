# teamhide_fastapi-boilerplate-df4e6d4 — kết quả phân tích (bản sinh tự động)

- Snapshot: `snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f`
- Schema 0.1.0; renderer slice-render-v2; template slice-template-v1
- Phạm vi: 125 file trong 1 unit; 11 file bị loại khỏi snapshot

## Sơ đồ component

```mermaid
flowchart LR
  n0["Quản lý cache"]
  n1["Ngoài sơ đồ: tests"]
  n2["Auth service"]
  n3["Kết nối DB"]
  n4["Worker entrypoint"]
  n5["Ngoài sơ đồ: migrations"]
  n6["CLI khởi chạy"]
  n7["Lưu trữ người dùng"]
  n8["Ngoài sơ đồ: (gốc)"]
  n9["Web entrypoint"]
  n10["Public API router"]
  n11["Xử lý người dùng"]
  n12["Dùng chung"]
  n1 -->|calls| n9
  n1 -->|calls| n2
  n10 -->|calls| n2
  n2 -->|calls| n12
  n1 -->|calls| n11
  n11 -->|calls| n7
  n11 -->|calls| n12
  n9 -->|calls| n3
  n12 -->|calls| n11
  n10 -->|calls| n11
  n1 -->|calls| n12
  n1 -->|calls| n3
  n9 -->|calls| n0
  n1 -->|calls| n0
  n10 -->|calls| n12
  n1 -->|calls| n7
  n11 -->|depends_on| n7
  n1 -->|depends_on| n7
  n7 -->|calls| n3
```

## Mục lục contract

- table: [tech-specs/LUU-TRU-NGUOI-DUNG/schema/TBL-TEAMHIDE-FASTAPI-BOILERPLATE-DF4E6D4-LUU-TRU-NGUOI-DUNG.md](tech-specs/LUU-TRU-NGUOI-DUNG/schema/TBL-TEAMHIDE-FASTAPI-BOILERPLATE-DF4E6D4-LUU-TRU-NGUOI-DUNG.md) — component `cmp_95405d59cd1bf6793aaabbd1b2d696e9fe7a60b0fff12b43107b53c242f65a4a`
- api: [tech-specs/PUBLIC-API-ROUTER/api/API-TEAMHIDE-FASTAPI-BOILERPLATE-DF4E6D4-PUBLIC-API-ROUTER-v1.md](tech-specs/PUBLIC-API-ROUTER/api/API-TEAMHIDE-FASTAPI-BOILERPLATE-DF4E6D4-PUBLIC-API-ROUTER-v1.md) — component `cmp_bfc26ab6cf618b4444fbaa84f29ba0f77c1a5fdff6b9c679cf9218caa28e7516`

## Mục lục EVT theo topic

- (không có)

## Contract chưa gán được component

- (không có)

## Giới hạn

- `SLICE_SCOPE` (inventory): Lát cắt đầu chỉ nhận route FastAPI và bảng SQLAlchemy Column
- `REFERENCE_UNRESOLVED` (extraction): 114 lời gọi chưa nối được đích; giữ là dữ kiện unresolved kèm lý do, không vẽ thành cạnh
- `VALUE_REDACTED` (extraction): Giá trị có dấu hiệu credential đã được che trước khi lưu
- `MODEL_NOT_RUN` (model): Không gọi provider; tên component lấy từ membership

## Giới hạn biểu diễn

- `DDL_BLOCK_OMITTED`: Không bảng nào đủ dữ kiện cho DDL — `fact:8cc7f2347c01991ba09383b9e750166a40ac852dd0ad3530d07a8b3998c2460c`
- `DDL_TABLE_OMITTED`: dialect chưa biết — `fact:8cc7f2347c01991ba09383b9e750166a40ac852dd0ad3530d07a8b3998c2460c`
