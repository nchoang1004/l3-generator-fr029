# full-stack-fastapi-template-cb740b6 — kết quả phân tích (bản sinh tự động)

- Snapshot: `snap:48597b2fdd287ad86cc29ce72b953974a5e80a8bd80724a4e7127483d7402ac9`
- Schema 0.1.0; renderer slice-render-v2; template slice-template-v1
- Phạm vi: 45 file trong 1 unit; 207 file bị loại khỏi snapshot

## Sơ đồ component

```mermaid
flowchart LR
  n0["Khởi tạo dữ liệu"]
  n1["SMTP email service"]
  n2["Dùng chung"]
  n3["Ngoài sơ đồ: scripts"]
  n4["Mô hình và CRUD"]
  n5["Ngoài sơ đồ: backend"]
  n6["Xác thực người dùng"]
  n7["Cơ sở dữ liệu"]
  n8["Ứng dụng FastAPI"]
  n9["Router API"]
  n7 -->|calls| n4
  n7 -->|depends_on| n4
  n5 -->|depends_on| n4
  n9 -->|calls| n4
  n9 -->|calls| n1
  n5 -->|calls| n6
  n9 -->|calls| n6
  n5 -->|calls| n7
  n4 -->|calls| n6
  n0 -->|calls| n7
  n5 -->|calls| n1
  n5 -->|calls| n4
  n9 -->|depends_on| n4
```

## Mục lục contract

- table: [tech-specs/MO-HINH-VA-CRUD/schema/TBL-FULL-STACK-FASTAPI-TEMPLATE-CB740B6-MO-HINH-VA-CRUD.md](tech-specs/MO-HINH-VA-CRUD/schema/TBL-FULL-STACK-FASTAPI-TEMPLATE-CB740B6-MO-HINH-VA-CRUD.md) — component `cmp_56c9ff88194fbd683a0587f3e7f23bc78f89ccb09fa12ec4e0fda9d3e2d9887e`
- api: [tech-specs/ROUTER-API/api/API-FULL-STACK-FASTAPI-TEMPLATE-CB740B6-ROUTER-API-v1.md](tech-specs/ROUTER-API/api/API-FULL-STACK-FASTAPI-TEMPLATE-CB740B6-ROUTER-API-v1.md) — component `cmp_ece7543ac7f97d7d6f35c953aa9b4ea3dcac3ce97361f2434f9a25db93414bc9`

## Mục lục EVT theo topic

- (không có)

## Contract chưa gán được component

- (không có)

## Giới hạn

- `SLICE_SCOPE` (inventory): Lát cắt đầu chỉ nhận route FastAPI và bảng SQLAlchemy Column
- `PARSE_FAILED` (extraction): backend/app/api/deps.py: SyntaxError
- `REFERENCE_UNRESOLVED` (extraction): 103 lời gọi chưa nối được đích; giữ là dữ kiện unresolved kèm lý do, không vẽ thành cạnh
- `MODEL_NOT_RUN` (model): Không gọi provider; tên component lấy từ membership
- `COMPONENT_WITHOUT_EVIDENCE` (verification): Ngoài sơ đồ: (gốc)

## Giới hạn biểu diễn

- `DDL_BLOCK_OMITTED`: Không bảng nào đủ dữ kiện cho DDL — `fact:bc55ebf0febfb292514d4a8da02096ec1d46d2fbc049f90747e81e9286e6d14f`, `fact:feca1457149e79086f4d45c6a15897d79c9a8713cbb6b42f3b0f022752df83cc`
- `DDL_TABLE_OMITTED`: dialect chưa biết — `fact:bc55ebf0febfb292514d4a8da02096ec1d46d2fbc049f90747e81e9286e6d14f`
- `DDL_TABLE_OMITTED`: dialect chưa biết — `fact:feca1457149e79086f4d45c6a15897d79c9a8713cbb6b42f3b0f022752df83cc`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:0565c24d1a663897d7a52da6d2ee6bae26ffca22a5418e718f96b5935a365a03`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:288e9e25b4053dc25ae2a792e7f66189d8e6a41899631fd3f679f00f3113682c`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:34e7d7bc2be8d6e3b893b4e871cb5717d7e0d1720cba6a5692691fa03104e9fd`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:592222f93121438176f8be03ee2b355be360cc0888cd739064446d7747659852`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:c0cc5671b145a65bceb084fe6fee6bdf45c2fd74c206aaf6d17465c837c260d4`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:ca6a9bfdea5bdbb56bdde5429d116f9a7b451122ce954dd0b2ae270075e67cb8`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:cb4f98fea70376f31f6a1f8d3e816547aa26bea10d0d35227af9b44ec8d49c19`
- `OPENAPI_OPERATION_OMITTED`: Path có tham số nhưng tham số chưa được trích đủ — `fact:d46b020437dbfd11d302c75fe18d59a0f37370dac74f3c855f6006d2fd2ce33b`
