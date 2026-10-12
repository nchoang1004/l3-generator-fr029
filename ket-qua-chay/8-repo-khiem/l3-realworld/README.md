# fastapi-realworld-diagram — kết quả phân tích (bản sinh tự động)

- Snapshot: `snap:cc11d7d982bab274bbbbf8ea295de7483f55b060e6658200582a2e4b7dd00e16`
- Schema 0.1.0; renderer slice-render-v2; template slice-template-v1
- Phạm vi: 96 file trong 1 unit; 29 file bị loại khỏi snapshot

## Sơ đồ component

```mermaid
flowchart LR
  n0["Định nghĩa router API"]
  n1["Ngoài sơ đồ: tests"]
  n2["Ngoài sơ đồ: (gốc)"]
  n3["Kết nối cơ sở dữ liệu"]
  n4["Khởi tạo FastAPI ứng dụng"]
  n5["Truy cập dữ liệu repository"]
  n6["Logic nghiệp vụ dịch vụ"]
  n7["Dùng chung"]
  n0 -->|calls| n5
  n1 -->|calls| n5
  n1 -->|calls| n6
  n5 -->|calls| n7
  n4 -->|calls| n7
  n7 -->|calls| n5
  n6 -->|calls| n5
  n7 -->|calls| n6
  n1 -->|calls| n4
  n0 -->|depends_on| n7
  n0 -->|calls| n7
  n0 -->|calls| n6
  n6 -->|calls| n7
  n7 -->|calls| n3
  n1 -->|calls| n7
```

## Mục lục contract

- api: [tech-specs/DINH-NGHIA-ROUTER-API/api/API-FASTAPI-REALWORLD-DIAGRAM-DINH-NGHIA-ROUTER-API-v1.md](tech-specs/DINH-NGHIA-ROUTER-API/api/API-FASTAPI-REALWORLD-DIAGRAM-DINH-NGHIA-ROUTER-API-v1.md) — component `cmp_0b7ea9bdc14e04bf245084a756a7452dcfbcc03f0246020977e6dd1cc705fbb4`

## Mục lục EVT theo topic

- (không có)

## Contract chưa gán được component

- (không có)

## Giới hạn

- `SLICE_SCOPE` (inventory): Lát cắt đầu chỉ nhận route FastAPI và bảng SQLAlchemy Column
- `TABLES_IN_MIGRATIONS_NOT_READ` (extraction): 7 bảng chỉ thấy trong migration Alembic, chưa trích: articles, articles_to_tags, commentaries, favorites, followers_to_followings, tags, users
- `REFERENCE_UNRESOLVED` (extraction): 73 lời gọi chưa nối được đích; giữ là dữ kiện unresolved kèm lý do, không vẽ thành cạnh
- `MODEL_NOT_RUN` (model): Không gọi provider; tên component lấy từ membership

## Giới hạn biểu diễn

- (không có)
