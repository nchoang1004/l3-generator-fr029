---
generated: true
non_normative: true
snapshot_id: "snap:f4964f64b825d8af3f7a92e49254c5e6c506822efac23974978c5d32c175a886"
owner_component_id: "cmp_12e3f0d56a509f8aa918eb8630467ceb9f3428d97aff1d2174faf6dbe3da840f"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:0f88b4e0b2d4dc8bd03841072811f04c74b6b286d11d4aa931a6e7a8fb6acd93", "fact:dc57572342c6eeae1f72215af26c8fe056b213fbc0f4d535520c0eb4d3500be5"]
evidence_ids: ["ev:042042b19f341417d8e18b0cc3f5f57604aa095d2e1454ffd5fea3810a6db306", "ev:0736d53abd819811958ee4efa86956af7c9dba9daa71ce4300b5ff722d29c8e6", "ev:24b830861d7528a21b466b62544d726eae6e821868c195203bfb834ab8fb7cf1", "ev:27dd5e00d31abc710bd3430ce431a2f75f0cb49f1033863bbd23635db0335fc0", "ev:459cafea4953abce09aaef736f2f927d6395edb87674a0ddd5ea31f2c367aaaa", "ev:479140345e75a9632e6d8e1634c959c91cd46f770bae0d91cf6aab173204bb19", "ev:6a44917c903ed16782407f12f04f81c90cad3e247a19eb10127bed66d232e25a", "ev:795c73ebdacb42cb0a623e2584583faedd63f00d8cdadd4660696c3a801f8421", "ev:806780147ef9b7d54340730467a14c2a02bfc4a206119a720ba01c5cb967bd24", "ev:973b94f83efc63d33752290b9edf0dc02c254f90657f06f64a937cc29d5e737a", "ev:9e72b9f3a265d6f6310bcd63896b181b50752193eecde68de9ff50372be6ef64", "ev:bcbaf36ed98896bf64da167775a856b2d30e6d409162a9ffe5f7e65b39bbe26a", "ev:ec8943465b61c0857843029ecbb5cc9049cc646cc991f7eb42e52c8c5bc5e387", "ev:ff2a9ac01ec0f6211e380b007c1b24386d5d6ad5f2522cfd3fc5b46e936bc091"]
---
# TBL — Lưu trữ

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng items

Dialect: sqlite. Fact `fact:0f88b4e0b2d4dc8bd03841072811f04c74b6b286d11d4aa931a6e7a8fb6acd93`. Confidence inferred, completeness full.

Evidence: `ev:ff2a9ac01ec0f6211e380b007c1b24386d5d6ad5f2522cfd3fc5b46e936bc091` (db/models.py:4), `ev:795c73ebdacb42cb0a623e2584583faedd63f00d8cdadd4660696c3a801f8421` (db/models.py:13-17), `ev:bcbaf36ed98896bf64da167775a856b2d30e6d409162a9ffe5f7e65b39bbe26a` (db/models.py:14), `ev:24b830861d7528a21b466b62544d726eae6e821868c195203bfb834ab8fb7cf1` (db/models.py:15), `ev:806780147ef9b7d54340730467a14c2a02bfc4a206119a720ba01c5cb967bd24` (db/models.py:15), `ev:479140345e75a9632e6d8e1634c959c91cd46f770bae0d91cf6aab173204bb19` (db/models.py:16), `ev:6a44917c903ed16782407f12f04f81c90cad3e247a19eb10127bed66d232e25a` (db/models.py:16), `ev:042042b19f341417d8e18b0cc3f5f57604aa095d2e1454ffd5fea3810a6db306` (db/models.py:17), `ev:459cafea4953abce09aaef736f2f927d6395edb87674a0ddd5ea31f2c367aaaa` (db/models.py:17), `ev:973b94f83efc63d33752290b9edf0dc02c254f90657f06f64a937cc29d5e737a` (db/models.py:24).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | INTEGER | True | không áp dụng — Không khai ForeignKey/foreign_key | False |
| name | TEXT | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| category_id | INTEGER | False | {"column": "id", "table": "categories"} | True |

## Bảng categories

Dialect: sqlite. Fact `fact:dc57572342c6eeae1f72215af26c8fe056b213fbc0f4d535520c0eb4d3500be5`. Confidence inferred, completeness full.

Evidence: `ev:ff2a9ac01ec0f6211e380b007c1b24386d5d6ad5f2522cfd3fc5b46e936bc091` (db/models.py:4), `ev:27dd5e00d31abc710bd3430ce431a2f75f0cb49f1033863bbd23635db0335fc0` (db/models.py:8-10), `ev:9e72b9f3a265d6f6310bcd63896b181b50752193eecde68de9ff50372be6ef64` (db/models.py:9), `ev:0736d53abd819811958ee4efa86956af7c9dba9daa71ce4300b5ff722d29c8e6` (db/models.py:10), `ev:ec8943465b61c0857843029ecbb5cc9049cc646cc991f7eb42e52c8c5bc5e387` (db/models.py:10), `ev:973b94f83efc63d33752290b9edf0dc02c254f90657f06f64a937cc29d5e737a` (db/models.py:24).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | INTEGER | True | không áp dụng — Không khai ForeignKey/foreign_key | False |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- fact: fact:0f88b4e0b2d4dc8bd03841072811f04c74b6b286d11d4aa931a6e7a8fb6acd93
CREATE TABLE "items" (
  "id" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "category_id" INTEGER,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("category_id") REFERENCES "categories" ("id")
);
-- fact: fact:dc57572342c6eeae1f72215af26c8fe056b213fbc0f4d535520c0eb4d3500be5
CREATE TABLE "categories" (
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id")
);
```
