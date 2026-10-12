# Kiểm cấu trúc bộ L3 draft

> Derived, non-normative. Không phải approval hoặc benchmark sản phẩm.

Lệnh: `scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py --report`

8 draft contracts; 7 JSON Schemas; OpenAPI 3.1.1
136 schema refs resolved offline; 71 local links
20 positive examples; 31 negative checks
NOT checked: real analyzer, LLM provider, full binding semantics, gold accuracy, UI, or gates.

## Kiểm dương

- API-L3GEN-001-v1/RunView
- API-L3GEN-001-v1/RunView
- API-L3GEN-001-v1/EvidenceView
- API-L3GEN-001-v1/Error
- API-L3GEN-001-v1/Error
- API-L3GEN-001-v1/CliResult
- API-L3GEN-002-v1/Snapshot
- API-L3GEN-002-v1/Range
- API-L3GEN-002-v1/SnapshotError
- API-L3GEN-005-v1/ArchitectureModel
- API-L3GEN-006-v1/LabelResult
- API-L3GEN-006-v1/ModelResponse
- walkthrough: Snapshot
- walkthrough: Inventory
- walkthrough: FactSet
- walkthrough: ArchitectureModel
- walkthrough: VerifiedResult
- walkthrough: ResultBundle
- walkthrough: ResultData, real source hashes/ranges and result.json checksum
- ModelRequest referencing walkthrough facts/model (not sent)

## Kiểm âm

- model with 51 nodes
- failed artifact has ready hash
- inferred without reason
- partial without reason
- Component partial without reason
- Edge partial without reason
- redacted leaks value
- dangling endpoint
- cross-snapshot facts
- owner component lacks declaration file
- contract fact without owner entry
- unresolved owner without reason
- rejected edge published
- attribute cites missing evidence
- missing partition policy version
- missing extractor version
- missing inventory for scope presentation
- file belongs to two components
- duplicate final verdict
- missing component slug
- duplicate component slug
- notice cites missing fact
- notice cites missing artifact
- source hash altered
- evidence range outside source
- artifact checksum altered
- result.json differs from manifest
- LLM label attempts to change membership
- group_flat without flat units
- denied read exposes content
- credential field in GitHub input

## Môi trường

Python 3.11.9
- jsonschema==4.23.0
- PyYAML==6.0.2
- openapi-spec-validator==0.7.2

## Hash nguồn khi kiểm

| File | SHA256 |
|---|---|
| .aide/tech-specs/CMP-L3GEN-001/api/API-L3GEN-001-v1.md | `1904b3de00519c7c547688fba9098b30ccc7674b978fda1277a329b93a59be99` |
| .aide/tech-specs/CMP-L3GEN-002/api/API-L3GEN-002-v1.md | `0b5564db8317b96fc551997f30415f692985209570a6e62ae86405cba2fc600b` |
| .aide/tech-specs/CMP-L3GEN-003/api/API-L3GEN-003-v1.md | `506e957bef26fd5065539cc73ccf5658b4e47f10602954d57dca3771fd901689` |
| .aide/tech-specs/CMP-L3GEN-004/api/API-L3GEN-004-v1.md | `8d1f260f852497afb0ef95892237c9907b34d9c4b3b26869ca28e368f23c0426` |
| .aide/tech-specs/CMP-L3GEN-005/api/API-L3GEN-005-v1.md | `18669782928a62c0598af5d2591efea873d4b0244445527645d96c9ebb62eb44` |
| .aide/tech-specs/CMP-L3GEN-006/api/API-L3GEN-006-v1.md | `2e9b1d02a2220227eea9c76edbe12750d676d444906b5f68acd655046e03179d` |
| .aide/tech-specs/CMP-L3GEN-007/api/API-L3GEN-007-v1.md | `ce65bd88bd69ac5bca11753b707481e77fd542e517ce65150b2cafd332178a71` |
| .aide/tech-specs/CMP-L3GEN-008/api/API-L3GEN-008-v1.md | `4da02bcd03a7b5d46cb43a6507c986cda74881f17c51c8344e775bd949b872a2` |
| .aide/tech-specs/README.md | `2b5207204cf90e1a7742ff7a301de3aefa484195b2dec002f81cf5d0feb90de6` |
| .aide/tech-specs/examples/contract-walkthrough.md | `5f90b9afd6abc07238e08942d98f03087abf5d75c260e605cd4ee4e1efcda340` |
| docs/L3-Generator-ke-hoach-trien-khai-L3.md | `00ccd645b3e11f1cbea2d5420edce4db8a70616a8d55e0c5f06c6fe03d31575f` |
| scripts/check_l3_contracts.py | `d042539ffdae245fcabb0dae4c2983a086217c428ce91183bfe6942bb01d5ff0` |
| scripts/requirements-l3-check.txt | `932ce2799787eda6f8682fbc67e2aef2b2a08f19478b5f94da9aad5052e653ac` |

Ví dụ viết tay: [nguồn và cách đọc](../../tech-specs/examples/contract-walkthrough.md), [payload qua từng bước](L3-WALKTHROUGH.json). Không phải output analyzer hoặc gold độc lập. Hash/bytes được đối soát trên source văn bản và chuỗi result.json thực trong fixture, không chạy parser/renderer sản phẩm.
Các quy tắc typed attributes đầy đủ, grouping, semantic binding, budget, cleanup và rendering phải được hiện thực/kiểm ở task sản phẩm; schema pass không chứng minh chúng đã hoạt động. D-03 vẫn mở; membership fixture không lựa chọn thuật toán.
