---
generated: true
non_normative: true
snapshot_id: "snap:c1495361276c6c8cd263abcb7919dea2d99441c993412393b1b5bc40363054af"
owner_component_id: "cmp_feb33ad0dd6c5afcb686ceacb60106d85eaf3b0b9033c5cb172ef4e7fd3ad589"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:0dabd6cd1f0d8e83556760f03b20af7650bdafe44da4d77a865b33e6f9e07b36", "fact:678a9e546bff3fa2b09ad37a23d4e86203f60f53a7343fea0a0b61055d93b4fb"]
evidence_ids: ["ev:258fe43cbe026a2ccccdf171b8205c955f6d440fef27e08ab9feb2ea25309ea9", "ev:2f6f598cef50b14a0eb34dc35c9bcec5daf789e077337a46d9d7ff26234aeb1e", "ev:43f4bf3eead790210a807e0c43ef3589e95aa90601c3b7af5cfabae7b74058c2", "ev:4f3250b9de024058ffc7ab85d3ac6be45447a0c309485b14609f8cb4d31e727d", "ev:62c7289873fa886af5630b3c78d33b02f298cf75e5c1505b9515b267c76c4787", "ev:78609a72c2112158435261d536b80256a5d67aa1e5587ec2f1a0cc761681d02a", "ev:7c16a52fadaa4bb55b545ca053efab983937f2fe7d9390fadf4f48d4f24d8da6", "ev:7f3f694f9603ba4377dfa3c2031f1356bda3f68ffbf5e5b3e79166d0a7f5f7da", "ev:85026da3798191125fbd40cde79719d038ad2f3604391306a90250df72fde028", "ev:932777da2933566ff3da7bc96d991687b1190d5753e77f4c18a2999cf682466e", "ev:aa2726e045587f8286ec1a4572e2adc5b35d48fff50a606687d4e7a705191016", "ev:bd56a16542743a7c6588e883edd57843170b64834d9b2ecf007b657b1c6c0317", "ev:ca2f3e772c9497936d5e84304ac2b86421d11992d006c8a65e7d4f8fcdfa9508", "ev:d034db1b41d260fa38551a5270eab5c82388dcce0dbdf2104ba615ab914d172a", "ev:ed1860be0d853c23ca6235b1c36fa34263b986aa05447875ca4b052cc4477583", "ev:fa6f094cd4c88ec00a26b5c43c9c2e2349345b7a7de2a5dd3d273f7b1ca99e4a"]
---
# TBL — app

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng notebooks

Dialect: unknown — Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal. Fact `fact:0dabd6cd1f0d8e83556760f03b20af7650bdafe44da4d77a865b33e6f9e07b36`. Confidence inferred, completeness partial.

Evidence: `ev:7c16a52fadaa4bb55b545ca053efab983937f2fe7d9390fadf4f48d4f24d8da6` (app/models/notebooks.py:15-70), `ev:43f4bf3eead790210a807e0c43ef3589e95aa90601c3b7af5cfabae7b74058c2` (app/models/notebooks.py:16), `ev:bd56a16542743a7c6588e883edd57843170b64834d9b2ecf007b657b1c6c0317` (app/models/notebooks.py:18), `ev:fa6f094cd4c88ec00a26b5c43c9c2e2349345b7a7de2a5dd3d273f7b1ca99e4a` (app/models/notebooks.py:18-20), `ev:4f3250b9de024058ffc7ab85d3ac6be45447a0c309485b14609f8cb4d31e727d` (app/models/notebooks.py:21), `ev:85026da3798191125fbd40cde79719d038ad2f3604391306a90250df72fde028` (app/models/notebooks.py:21).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | unknown — Chưa xác định SQL dialect từ source; khai trong code: int | True | không áp dụng — Không khai ForeignKey/foreign_key | False |
| title | unknown — Chưa xác định SQL dialect từ source; khai trong code: String(length=64) | False | không áp dụng — Không khai ForeignKey/foreign_key | False |

## Bảng notes

Dialect: unknown — Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal. Fact `fact:678a9e546bff3fa2b09ad37a23d4e86203f60f53a7343fea0a0b61055d93b4fb`. Confidence inferred, completeness partial.

Evidence: `ev:aa2726e045587f8286ec1a4572e2adc5b35d48fff50a606687d4e7a705191016` (app/models/notes.py:16-83), `ev:78609a72c2112158435261d536b80256a5d67aa1e5587ec2f1a0cc761681d02a` (app/models/notes.py:17), `ev:62c7289873fa886af5630b3c78d33b02f298cf75e5c1505b9515b267c76c4787` (app/models/notes.py:19-21), `ev:932777da2933566ff3da7bc96d991687b1190d5753e77f4c18a2999cf682466e` (app/models/notes.py:19), `ev:2f6f598cef50b14a0eb34dc35c9bcec5daf789e077337a46d9d7ff26234aeb1e` (app/models/notes.py:22), `ev:7f3f694f9603ba4377dfa3c2031f1356bda3f68ffbf5e5b3e79166d0a7f5f7da` (app/models/notes.py:22), `ev:d034db1b41d260fa38551a5270eab5c82388dcce0dbdf2104ba615ab914d172a` (app/models/notes.py:23), `ev:ed1860be0d853c23ca6235b1c36fa34263b986aa05447875ca4b052cc4477583` (app/models/notes.py:23), `ev:258fe43cbe026a2ccccdf171b8205c955f6d440fef27e08ab9feb2ea25309ea9` (app/models/notes.py:25), `ev:ca2f3e772c9497936d5e84304ac2b86421d11992d006c8a65e7d4f8fcdfa9508` (app/models/notes.py:25-27).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | unknown — Chưa xác định SQL dialect từ source; khai trong code: int | True | không áp dụng — Không khai ForeignKey/foreign_key | False |
| title | unknown — Chưa xác định SQL dialect từ source; khai trong code: String(length=64) | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| content | unknown — Chưa xác định SQL dialect từ source; khai trong code: str | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| notebook_id | unknown — Chưa xác định SQL dialect từ source; khai trong code: int | False | {"column": "id", "table": "notebooks"} | False |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- omitted: fact:0dabd6cd1f0d8e83556760f03b20af7650bdafe44da4d77a865b33e6f9e07b36: dialect chưa biết
-- omitted: fact:678a9e546bff3fa2b09ad37a23d4e86203f60f53a7343fea0a0b61055d93b4fb: dialect chưa biết
```
