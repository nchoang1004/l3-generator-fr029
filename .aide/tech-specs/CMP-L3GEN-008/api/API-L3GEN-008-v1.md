---
uid: "01M3B99N5X6V4AXNWPE3BAHEAQ"
key: "API-L3GEN-008-v1"
type: "api-contract"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-008"],"satisfies":["FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"],"constrained_by":["NFR-L3GEN-ABST-002","NFR-L3GEN-ACC-002","NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# API-L3GEN-008-v1 — Contract nội bộ trình bày và xuất

## 1. Phạm vi và bên gọi

Đây là giao diện trong tiến trình của CMP-L3GEN-008, không mở thêm HTTP service.
CMP-L3GEN-001 điều phối xuất/retry; façade API-L3GEN-001-v1 cung cấp kết quả cho web/CLI.
Nguồn: CMP-L3GEN-008 r2, FR-L3GEN-025 r2, FR-L3GEN-026 r1, FR-L3GEN-027 r3 ở nhánh `docs/gate-2` commit `5d06f14`.

**Revision 5 (02/10/2026, nháp, chờ Architecture Gate BL-r10):** thêm phần của FR-L3GEN-029: mục README "Lời gọi HTTP ra ngoài" (AC-L3GEN-029-06, 029-08) và response `list[Model]` (AC-L3GEN-029-02). `satisfies` đổi sang FR-L3GEN-029 đến 031 vì FR-025 đến 027 đã superseded. Phần còn lại giữ như r4, chưa đối chiếu với CMP-L3GEN-008 r3.
Đầu vào duy nhất về nội dung là `VerifiedResult` của API-L3GEN-007-v1 đã đóng băng. Pipeline nào cấp dữ liệu (kể cả `graph.json` của thí nghiệm v8) phải chuyển về đúng cấu trúc này; trường không có thì ghi `unknown`/limitation, không đổi contract theo pipeline.
Nó chứa `inventory: Inventory`, `facts: FactSet`, `model: ArchitectureModel`, `evidence_index`, `decisions`, `limitations`.
CMP-008 không đọc source, gọi model, suy luận thêm contract, sửa ownership hoặc phục hồi kết luận bị loại.
Đọc bằng chứng đi qua CMP-001 → CMP-007; CMP-008 chỉ chuyển `evidence_id` và `snapshot_id`.
Thuật toán chia component còn **OPEN** ở API-005. CMP-008 giữ nguyên `model.partition_version` như ID policy opaque,
không diễn giải giá trị đó, không chia lại theo thư mục/tên/lời gọi.
Owner của từng contract đọc từ `result.model.contract_owners` do CMP-005 lập và CMP-007 kiểm (ADR-2026-003 r2); CMP-008 không tự gán lại. Đổi tên/slug không đổi owner.

| Thao tác nội bộ | Đầu vào | Đầu ra / điều kiện |
|---|---|---|
| `render` | `run_id`, `VerifiedResult`, tên repository đã chuẩn hóa đầu vào, phiên bản renderer/template, vùng output do CMP-001 cấp | `ResultBundle` hoặc `ExportError`; chỉ nhận schema version hỗ trợ và snapshot trùng khớp |
| `retry_artifact` | `run_id`, `artifact_id`, bundle đã commit và vùng output do CMP-001 cấp | `ResultBundle` mới hoặc `ExportError`; trả cùng bundle khi artifact đã ready, không phân tích lại |
| `read_bundle` | `run_id` đã được façade kiểm quyền và hạn | `ResultBundle` từ một manifest đã commit |

`schema_version` trong contract này là `0.1.0`; revision tài liệu và `v1` của tên file là các trục riêng.
Thay đổi tương thích dữ liệu phải được xem xét theo B.10; draft này không ghi nhận consumer ack hay gate đã đạt.

## 2. Bộ dữ liệu và schema dùng chung

JSON Schema Draft 2020-12 bên dưới là schema nguồn nhúng trong Markdown.
Các URI `.schema.json` là định danh logic để bộ nạp đăng ký schema, không là yêu cầu tải mạng hay file đã được tạo.
`ResultData` là nội dung `result.json`; `ResultBundle` là nội dung `manifest.json` và body GET result của CMP-001.
Manifest bổ sung danh mục artifact; chính manifest không nằm trong danh mục băm của nó, tránh hash tự tham chiếu.
Các trường dữ liệu trong manifest và `result.json` phải bằng nhau về ngữ nghĩa.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://l3gen.local/contracts/API-L3GEN-008-v1.schema.json",
  "$ref": "#/$defs/ResultBundle",
  "$defs": {
    "IdList": {
      "type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": true
    },
    "ResultDataFields": {
      "type": "object",
      "required": ["run_id", "snapshot_id", "schema_version", "result", "export_context", "render_notices"],
      "properties": {
        "run_id": {"type": "string", "minLength": 1},
        "snapshot_id": {"type": "string", "minLength": 1},
        "schema_version": {"const": "0.1.0"},
        "result": {"$ref": "API-L3GEN-007-v1.schema.json#/$defs/VerifiedResult"},
        "export_context": {"$ref": "#/$defs/ExportContext"},
        "render_notices": {"type": "array", "items": {"$ref": "#/$defs/RenderNotice"}}
      }
    },
    "ResultData": {
      "allOf": [{"$ref": "#/$defs/ResultDataFields"}], "unevaluatedProperties": false
    },
    "ResultBundle": {
      "allOf": [{"$ref": "#/$defs/ResultDataFields"}],
      "type": "object", "required": ["artifacts"], "unevaluatedProperties": false,
      "properties": {
        "artifacts": {"type": "array", "items": {"$ref": "#/$defs/Artifact"}}
      }
    },
    "ExportContext": {
      "type": "object", "additionalProperties": false,
      "required": ["repository_name", "system_slug", "renderer_version", "template_version", "component_slugs"],
      "properties": {
        "repository_name": {"type": "string", "minLength": 1},
        "system_slug": {"type": "string", "pattern": "^[A-Z0-9][A-Z0-9-]*$"},
        "renderer_version": {"type": "string", "minLength": 1},
        "template_version": {"type": "string", "minLength": 1},
        "component_slugs": {
          "type": "object", "propertyNames": {"minLength": 1},
          "additionalProperties": {"type": "string", "pattern": "^[A-Z0-9][A-Z0-9-]*$"}
        },
        "source_link": {
          "type": "object", "additionalProperties": false, "required": ["base_url", "commit"],
          "properties": {
            "base_url": {"type": "string", "pattern": "^https://github\\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"},
            "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"}
          }
        }
      }
    },
    "RenderNotice": {
      "type": "object", "additionalProperties": false,
      "required": ["code", "reason", "fact_ids", "field_paths", "artifact_path"],
      "properties": {
        "code": {"enum": ["CONTRACT_OWNER_UNRESOLVED", "OPENAPI_OPERATION_OMITTED", "OPENAPI_BLOCK_OMITTED", "DDL_TABLE_OMITTED", "DDL_BLOCK_OMITTED", "EVENT_BINDING_UNRESOLVED", "EVENT_PAYLOAD_UNKNOWN"]},
        "reason": {"type": "string", "minLength": 1},
        "fact_ids": {"allOf": [{"$ref": "#/$defs/IdList"}], "minItems": 1},
        "field_paths": {"$ref": "#/$defs/IdList"},
        "artifact_path": {"type": ["string", "null"], "minLength": 1}
      }
    },
    "ExportError": {
      "type": "object", "additionalProperties": false,
      "required": ["code", "reason", "retryable"],
      "properties": {
        "code": {"enum": ["INVALID_INPUT", "SNAPSHOT_MISMATCH", "REFERENCE_INVALID", "PARITY_FAILED", "OUTPUT_UNSAFE", "PUBLISH_FAILED", "VERSION_UNAVAILABLE", "ARTIFACT_NOT_RETRYABLE", "RUN_EXPIRED"]},
        "reason": {"type": "string", "minLength": 1},
        "retryable": {"type": "boolean"}
      }
    },
    "ArtifactError": {
      "type": "object", "additionalProperties": false,
      "required": ["code", "reason", "retryable"],
      "properties": {
        "code": {"enum": ["RENDER_FAILED", "FORMAT_INVALID", "WRITE_FAILED", "VERSION_UNAVAILABLE", "DEPENDENCY_UNAVAILABLE"]},
        "reason": {"type": "string", "minLength": 1},
        "retryable": {"type": "boolean"}
      }
    },
    "Artifact": {
      "type": "object", "additionalProperties": false,
      "required": ["artifact_id", "kind", "path", "media_type", "status", "sha256", "bytes", "error"],
      "properties": {
        "artifact_id": {"type": "string", "pattern": "^art_[A-Za-z0-9_-]{16,80}$"},
        "kind": {"enum": ["readme", "json", "diagram_source", "diagram_image", "api", "table", "event"]},
        "path": {"type": "string", "pattern": "^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*\\.(?:md|json|mmd|svg)$"},
        "media_type": {"enum": ["text/markdown", "application/json", "text/plain", "image/svg+xml"]},
        "status": {"enum": ["pending", "ready", "failed", "retrying"]},
        "sha256": {"type": ["string", "null"], "pattern": "^[a-f0-9]{64}$"},
        "bytes": {"type": ["integer", "null"], "minimum": 0},
        "error": {"anyOf": [{"type": "null"}, {"$ref": "#/$defs/ArtifactError"}]}
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "ready"}}},
          "then": {"properties": {"sha256": {"type": "string"}, "bytes": {"type": "integer"}, "error": {"type": "null"}}}
        },
        {
          "if": {"properties": {"status": {"const": "failed"}}},
          "then": {"properties": {"sha256": {"type": "null"}, "bytes": {"type": "null"}, "error": {"$ref": "#/$defs/ArtifactError"}}}
        },
        {
          "if": {"properties": {"status": {"enum": ["pending", "retrying"]}}},
          "then": {"properties": {"sha256": {"type": "null"}, "bytes": {"type": "null"}, "error": {"type": "null"}}}
        }
      ]
    }
  }
}
```

`ResultData` và `ResultBundle` đều đóng bằng `unevaluatedProperties:false`; `ResultDataFields` chỉ là phần dùng chung,
không là payload xuất. `result.json` không chứa `artifacts`; manifest bổ sung đúng trường này.
`VerifiedResult` tham chiếu tiếp `API-L3GEN-004-v1.schema.json#/$defs/FactSet`, `EvidenceRef`, `Limitation`
và `API-L3GEN-005-v1.schema.json#/$defs/ArchitectureModel`; không định nghĩa bản sao trong CMP-008.
`export_context` giữ đủ cấu hình đặt tên/renderer để retry không phụ thuộc cấu hình hiện tại. `source_link` chỉ có khi source lấy từ GitHub và commit đã được khóa (API-002); khi đó cột evidence có link `blob/<commit>/<path>#L<dòng>`. Source từ ZIP hoặc thư mục local không có link.
`component_slugs` chứa đúng một entry cho mọi component đã công bố, kể cả component không có contract;
không chứa external system, không tự tạo thư mục từ việc có entry.
`render_notices` mô tả giới hạn biểu diễn từ dữ kiện đã kiểm, không sửa `VerifiedResult.limitations` hoặc verdict.
Mỗi notice có ít nhất một fact ID còn hợp lệ; `field_paths` là JSON Pointer từ gốc fact tương ứng, cùng áp dụng cho các fact được liệt kê.
`artifact_path:null` dùng khi chưa xác định được owner; path khác null phải trỏ artifact API/TBL/EVT trong manifest.
Thiếu field không phải `unknown`: consumer giữ các trạng thái known/unknown/not_applicable/redacted của API-004 khi trình bày.

Các kiểm tra ngữ nghĩa bắt buộc ngoài JSON Schema:

- `snapshot_id` ngoài cùng bằng mọi snapshot ID bên trong; không ghép hai lần chạy.
- ID entity, edge, artifact và path là duy nhất trong miền tương ứng; mọi endpoint của cạnh tồn tại trong cùng `result.model`.
- Mọi fact/evidence ID của nội dung được công bố có trong `result.facts`/`result.evidence_index`; ID lạ trong decision rejected chỉ được giữ như chẩn đoán theo API-007, không biến thành link evidence hoặc kết luận.
- `result.model` có tối đa 50 node (component + external system); vượt là `INVALID_INPUT`, không cắt bớt.
- JSON, README, mã sơ đồ, ảnh sơ đồ và web có cùng tập component và cạnh; không có cạnh dangling trong JSON hoặc mã sơ đồ.
- Mỗi fact route/table/event có đúng một mục trong `result.model.contract_owners`.
- Loại artifact, đuôi file và media type khớp nhau; hash/bytes tính trên đúng byte UTF-8 hoặc SVG đã commit.
- Tên slug không trùng sau case-fold; cùng ID luôn dùng cùng slug trong mọi artifact; render notice không tham chiếu fact đã loại.
- Mọi node/cạnh trong model có decision accepted theo API-007; không ép toàn bộ file inventory trở lại model sau khi verification loại kết luận.
- Không xuất nguyên file source, credential hoặc giá trị cấu hình chưa được che; hash không thay thế kiểm tra này.

## 3. Một mô hình, mọi artifact cùng tập component và cạnh

Theo CMP-008 r2 và FR-025 r2 AC-04: mọi output sinh từ **một** mô hình đã kiểm; không artifact nào chứa component hoặc quan hệ mà artifact khác không có. Trần 50 node do CMP-005 giữ (API-005 §3); CMP-008 không ẩn, không thêm node, không gộp cạnh.

- JSON (`result.json`), README, `architecture.mmd`, `architecture.svg` và web cùng dùng toàn bộ `result.model`.
- Function/class/file chỉ nằm ở lớp dữ kiện/bằng chứng; handler và model được nêu trong dòng contract khi có căn cứ.
- Lời gọi unresolved chỉ hiển thị như dữ kiện chưa xác định, không vẽ thành dependency.
- Các góc nhìn API, dữ liệu, tích hợp, dependency dùng ID của cùng `ResultBundle`, không chạy phân tích lại.
- Tài liệu API/TBL/EVT lấy toàn bộ contract fact, không cắt theo số node trên sơ đồ (CMP-008 r2 §2).
- Self-edge không được renderer bổ sung lại; nhiều cạnh khác loại giữa cùng cặp endpoint giữ nguyên ID/loại/chiều đã kiểm.
- Label được escape riêng với token cú pháp: renderer dùng token nội bộ `n0`, `n1`, ... theo thứ tự ID node tăng dần (so sánh ordinal), không chèn ID hoặc tên repository thành cú pháp Mermaid. SVG thể hiện cùng danh sách node/cạnh với mã nguồn.
- Model rỗng cho sơ đồ rỗng và thông báo chưa có kiến trúc đủ bằng chứng, không vẽ node placeholder như component thật.

### 3.1. Kiểm bản xuất

Bước này thuộc CMP-008 r2 §2 ("Kiểm bản xuất") và §3 ("kiểm chéo"). Chạy trước khi publish; đối chiếu bằng ID, không so chuỗi nhãn hoặc số hàng.

| Kiểm | Điều kiện đạt | Không đạt |
|---|---|---|
| Cùng tập node/cạnh | Tập ID node và tập cạnh `(nguồn, đích, loại)` của sơ đồ bằng model; mã Mermaid đúng từng dòng của kế hoạch vẽ; README chứa đúng mã đó | `PARITY_FAILED`, không publish bộ |
| Bảng và khối máy cùng nguồn | Đọc lại fact ID từ chính file đã sinh (dòng bảng, khối máy, danh sách bị bỏ) và so với kế hoạch sinh; mỗi dòng có trong khối máy hoặc được ghi là bị bỏ, không cả hai | Artifact đó `FORMAT_INVALID`, artifact khác giữ nguyên (AC-025-03) |
| Phần thiếu đủ dấu | Mỗi trường `unknown`/`redacted` trong dòng Markdown có lý do; mỗi phần bị bỏ khỏi khối máy có render notice | `FORMAT_INVALID` |
| Định dạng | Mỗi khối OpenAPI validate được với OpenAPI 3.1; mỗi schema EVT là JSON Schema 2020-12 hợp lệ; DDL chỉ dùng token trong catalogue §6.1 | `FORMAT_INVALID` |
| Đủ contract | Mỗi fact route/table/event nằm trong đúng một file contract, hoặc có `CONTRACT_OWNER_UNRESOLVED` | `PARITY_FAILED` |
| Danh sách file | Mọi path trong manifest có file; mọi file contract có trong manifest và README | `PARITY_FAILED` |

### 3.2. Biểu diễn phần thiếu theo từng định dạng

CMP-008 r2 §2 yêu cầu L3 đặc tả phần này. Quy tắc chung (FR-027 r3 "Khi chưa đủ dữ kiện"): xuất phần biết được, ghi `partial`, trường thiếu và lý do; khối máy chỉ chứa phần biểu diễn được đúng định dạng; không tạo giá trị giả.

| Định dạng | Trường chưa biết | Mục chưa biểu diễn được | Không dựng được cả khối |
|---|---|---|---|
| Bảng Markdown (API/TBL/EVT) | Ô ghi `unknown — <lý do>`; `redacted` ghi `đã che — <lý do>`; cột completeness của dòng ghi `partial` | Không áp dụng: bảng luôn giữ mọi dòng | Không áp dụng |
| OpenAPI 3.1 (API) | Ghi ở `x-analysis.unknowns` của operation: field, reason, fact ID. Schema chưa biết là `{}` kèm annotation | Operation bỏ khỏi `paths`, liệt kê ở `x-analysis.omitted_operations` và trong danh sách Markdown "Bỏ khỏi OpenAPI" kèm lý do; notice `OPENAPI_OPERATION_OMITTED` | Không có khối OpenAPI; ghi câu "Chưa có khối OpenAPI: <lý do>"; notice `OPENAPI_BLOCK_OMITTED` |
| DDL (TBL) | Bảng có trường bắt buộc chưa biết thì bỏ cả bảng khỏi DDL (§6) | Comment `-- omitted: <table fact ID>: <lý do>`; notice `DDL_TABLE_OMITTED` | Khối `sql` chỉ có comment; notice `DDL_BLOCK_OMITTED` |
| JSON Schema payload (EVT) | `x-analysis.unknowns`; không đặt `additionalProperties:false` khi chưa chứng minh | Payload chưa biết: schema `{}` kèm `x-analysis.completeness:"partial"`; notice `EVENT_PAYLOAD_UNKNOWN` | Không áp dụng |
| `result.json` | Giữ nguyên FieldValue của API-004 (`unknown`/`redacted`/`not_applicable` kèm reason) | Không áp dụng | Không áp dụng |

Ví dụ kiểm cho từng ô có trong test của code lát cắt đầu (`slice/tests/test_slice.py`): API và TBL qua hai fixture `shop_full`, `shop_partial`; EVT qua lớp `EventsFixture` với dữ kiện event soạn tay, vì bộ trích của lát cắt chưa nhận event. Định dạng máy hợp lệ không có nghĩa nội dung đã đầy đủ.

## 4. Cây output, identity và tên an toàn

```text
<output>/
  manifest.json
  result.json
  README.md
  architecture.mmd
  architecture.svg
  tech-specs/<CMP-slug>/
    api/API-<SYS>-<CMP>-v1.md
    schema/TBL-<SYS>-<CMP>.md
    events/EVT-<SYS>-<CMP>-<topic>.md
```

`README.md` có snapshot, phiên bản schema/renderer, sơ đồ, mục lục mọi file contract (gồm mục lục EVT theo topic để tra cả bên gửi lẫn bên nhận), danh sách contract chưa gán được component cùng lý do, coverage và các giới hạn đầu vào (CMP-008 r2, FR-027 r3). README có mục "Lời gọi HTTP ra ngoài": một dòng mỗi fact `http_call`, gồm component chứa dòng gọi, thư viện, method, đích và bằng chứng `file:dòng` kèm nguyên văn. Đích là `url` khi known; không có thì khóa cấu hình `url_config_key`; không có cả hai thì `unknown` kèm lý do (AC-L3GEN-029-08).
Manifest là metadata giao dịch; không thêm thư mục component rỗng. Chỉ sinh loại API/TBL/EVT thực sự có dữ kiện đã kiểm.
Danh mục artifact được lập trước render: đúng một `readme`, `json`, `diagram_source`, `diagram_image`,
thêm một `api`/`table` cho mỗi owner có facts tương ứng và một `event` cho mỗi file EVT theo §6.2.
Không tạo artifact rỗng để thế cho loại contract không tồn tại. README liệt kê tất cả path dự kiến; trạng thái tải thực tế lấy từ manifest,
không nhúng trạng thái ready/failed vào README rồi sửa README khi retry artifact khác.
README/web trình bày unit/path/ngôn ngữ/framework/mức hỗ trợ và excluded từ `result.inventory`, kết hợp limitations từ extraction/verification.
Inventory mô tả phạm vi đã xét, không phải ledger parse thành công; không suy tỷ lệ parse, precision hoặc recall từ số fact, số node hay số file có evidence.
Tên `<SYS>` lấy từ tên repository, `<CMP>` từ tên component; không lấy từ đường dẫn do người dùng yêu cầu tải.
Thuật toán slug: Unicode NFKD, bỏ dấu kết hợp, đổi Đ/đ thành D/d, uppercase invariant;
chuỗi ngoài ASCII A–Z/0–9 đổi thành `-`, gộp dấu `-`, bỏ dấu ở hai đầu; rỗng dùng `SYSTEM`/`COMPONENT`/`TOPIC`.
Tên dành riêng Windows được thêm `X-`; kiểm path đã resolve nằm hoàn toàn trong vùng output, không chấp nhận symlink thoát vùng.
Slug dài hơn 64 ký tự dùng 47 ký tự đầu, `-`, 16 ký tự đầu SHA-256 của tên UTF-8 ban đầu.
Đây là quy tắc làm mịn được đề xuất cho tên rỗng/dài/reserved mà FR-L3GEN-027 chưa quy định.
Nhóm trùng slug sắp theo ID component bất biến, cấp lần lượt tên gốc, `-2`, `-3`; xử lý cả va chạm với tên có sẵn suffix.
Giải quyết bằng cách lấy hậu tố nhỏ nhất chưa dùng trong toàn miền tên, theo thứ tự ID cố định; so tên không phân biệt hoa thường.
Giữ mapping `component_id → slug` của cả lần chạy khi retry; slug không thay ID của model hay key trong bằng chứng.
Topic áp dụng cùng thuật toán. Trùng tên file EVT trong một component thì thêm `-2`, `-3` theo thứ tự nguồn ổn định: (path, dòng, cột) của evidence khai báo sớm nhất, rồi fact ID (FR-027 r3). Topic chưa biết dùng nhãn `UNKNOWN-` + 12 ký tự hex đầu của phần hash trong fact ID, không coi nhãn đó là tên topic thật. `v1` luôn cố định theo FR-L3GEN-027.
Miền uniqueness component là toàn bộ `component_slugs`; miền uniqueness topic là mỗi owner. Sau thêm suffix vẫn kiểm giới hạn đoạn tên,
cắt base trước suffix nếu cần. Cả path phải hợp lệ trên nền tảng output; quá giới hạn path báo `OUTPUT_UNSAFE`, không cắt ngầm lần nữa.

Frontmatter của file sinh cho repository đích phải có `generated: true`, `non_normative: true`,
`snapshot_id`, `owner_component_id`, `schema_version`, `renderer_version`, `template_version`, `fact_ids`, `evidence_ids`.
Không tự gán trạng thái approved, ngày verified, approver hoặc consumer ack cho repository đích.
Mỗi dòng endpoint/cột/event có fact ID, evidence ID, confidence exact/inferred và completeness full/partial. Trường chưa biết giữ trạng thái unknown cùng lý do từ upstream; unknown không phải mức confidence thứ ba.

## 5. API sinh ra: registration context và OpenAPI 3.1

**Owner.** Đọc `result.model.contract_owners` (API-005 §3.2). Mục có `component_id` thì contract vào thư mục của component đó. Mục `component_id:null` thì không tạo file và không tạo thư mục giả; fact giữ trong `result.json`, README liệt kê kèm reason, thêm render notice `CONTRACT_OWNER_UNRESOLVED` với `artifact_path:null`. CMP-008 không sửa limitation upstream.

`application_id` phân biệt dòng của từng application; `registration_context` phân biệt lần mount. Thiếu một trong các identity cần thiết thì giữ bảng partial và liệt kê phần không đưa vào machine block.
Confidence dòng contract phản ánh cả fact và owner: nếu fact là inferred hoặc component owner là inferred thì dòng là inferred;
completeness là partial nếu một trong hai partial hoặc trường cần hiển thị còn thiếu. Giữ lý do của từng nguồn riêng,
không nâng nhãn bằng cách nói membership đã qua kiểm máy. Giá trị gốc trong VerifiedResult không bị thay đổi.

Một bảng khai báo ở component A nhưng được B sử dụng vẫn thuộc A; B chỉ tham chiếu fact/table ID. Nhiều class mapping cùng tên bảng không tự được gộp: chỉ gộp trong cùng owner khi identity DB/schema/table và định nghĩa không mâu thuẫn được facts chứng minh, giữ mọi fact ID. Event gửi và nhận tạo file ở từng component tương ứng (§6.2); exporter không tự phát minh binding ID trong model.

Một component có route có một Markdown API; bảng gồm application/registration, method, full path,
handler, request model, response model, status code, dependency/auth, fact/evidence và phần chưa biết.
Trước bảng đó (mục "Truy vết") có bảng cho người đọc (mục "Endpoint": method, path, tham số, tên request/response
model, status kèm rule, auth, nhãn, 8 ký tự đầu của fact ID) và mục "Model" liệt kê field của từng model được dùng.
Hai bảng cùng được đọc lại để so với fact (thêm 02/10/2026).
Owner lấy từ `contract_owners`; prefix/mount lấy từ registration context, không lấy riêng tên handler hoặc tên module.
Một router được mount vào hai application giữ hai registration; cùng method/path ở hai application không phải một operation.

Theo FR-027 r3 AC-01, mỗi file API có **một** khối OpenAPI 3.1. Bảng có cột application; mỗi operation ghi `x-analysis.application_id`. Không ghép các application bằng server/path giả.
Trùng method/path trong cùng file (cùng hoặc khác application): bảng giữ mọi dòng và ghi conflict; các operation đó bị omitted khỏi khối OpenAPI với `OPENAPI_OPERATION_OMITTED`. Không chọn handler tùy ý hoặc ghi đè map.
Registration thiếu application/full path/method được ghi unknown, không tự đặt URL để tạo operation.

Khối máy đọc là một khối `json` dùng `openapi: 3.1.0`, `info` và `paths`; validate độc lập.
Theo [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html), một Responses Object cần ít nhất một response;
extension dùng tiền tố `x-`, và Schema Object dựa trên JSON Schema 2020-12.
Chính sách của renderer: trường chưa biết ghi ở `x-analysis.unknowns` với field, reason, fact/evidence ID;
không dùng `type: unknown`, không đặt `nullable` của OpenAPI 3.0, không tự suy `200` hoặc `default` từ việc thiếu status;
`200` chỉ xuất hiện khi fact mang `status_rule` `fastapi-status-default-v1` (API-004), và response ghi tên rule.
Schema chưa biết có thể là `{}` kèm annotation unknown; `{}` không có nghĩa đã chứng minh payload chấp nhận mọi giá trị.
Chỉ khai `type: "null"` khi bằng chứng xác định null thực sự; thiếu thông tin không phải null.
Operation chưa đủ dữ kiện biểu diễn an toàn bị bỏ khỏi `paths` và liệt kê đầy đủ trong `x-analysis.omitted_operations`.
Cách bảo thủ này áp dụng cả khi chưa biết response code; bảng người đọc vẫn giữ dòng unknown và lý do.
Không tạo `security: []` để che việc chưa biết auth; không tạo security scheme, response, parameter hoặc `$ref` thiếu căn cứ.
OpenAPI subset phải có nhãn giới hạn ngay trước khối; kiểm parity tính cả omitted/unknown, không báo đầy đủ giả.
Mỗi operation có `operationId` từ route fact ID đã encode thành token ổn định, `x-analysis.fact_ids` và `evidence_ids`.
`info.title` lấy tên owner; `info.version: generated-v1` là phiên bản tài liệu sinh, không giả là phiên bản API runtime.
Các method biểu diễn là GET/PUT/POST/DELETE/OPTIONS/HEAD/PATCH/TRACE. Method khác, path thiếu parameter bắt buộc,
hoặc conflict method/path trong cùng file làm operation đó omitted. Không đổi chữ hoa/thường của path và không viết lại converter động thành OAS path tùy ý.
Request/response model ID chỉ tham chiếu facts cùng snapshot; tên schema dùng ID đã encode, không dùng class name dễ trùng.
Body response có `array: true` (API-004 r5) thì bảng ghi `list[<model>]` và schema là `{"type":"array","items":{"$ref":…}}`. Chỉ thêm `required`/null union khi FieldValue biết rõ. Không tự dùng `oneOf` cho nhiều model thiếu discriminator/association.
API-004 hiện chưa bảo đảm media type hoặc mapping model→status: vẫn liệt kê model và status trong bảng/`x-analysis`,
chỉ dựng `content` khi upstream có bằng chứng association và media type được adapter hỗ trợ. Có status đã biết vẫn được xuất response
với description trung tính và unknown annotation; không mặc định `application/json`, body, auth scheme hoặc liên kết mọi model tới mọi status.
Không fetch `$ref` qua mạng; mọi `$ref` xuất phải resolve trong cùng khối. Unknown annotation chứa đường dẫn field và reason,
không khôi phục value của redacted; notice `OPENAPI_OPERATION_OMITTED` ghi rõ fact ID và path artifact cho từng operation omitted.

## 6. TBL và EVT sinh ra

TBL gom các bảng thuộc component trong một Markdown, mỗi cột ghi tên, kiểu, PK, FK, nullable và bằng chứng (AC-027-02). Giá trị default không thuộc phạm vi v1.
Chỉ dùng tên bảng/kiểu/dialect đã được trích và kiểm; không suy tên bảng từ class. Dialect lấy từ source; chưa xác định thì ghi chưa biết, không mặc định PostgreSQL (FR-027 r3).
Khối `sql` là DDL dẫn xuất tĩnh cho dialect đã biết, không phải migration và tuyệt đối không được thực thi.
Thiếu tên bảng, kiểu hoặc dialect thì bảng người đọc ghi unknown kèm lý do; phần SQL chỉ có comment ghi điều chưa biết.
Chỉ phát `CREATE TABLE` cho bảng có đủ định nghĩa để không âm thầm bỏ cột/ràng buộc chưa rõ; bảng chưa đủ bị bỏ khỏi DDL có giải thích.
Không phát `UNKNOWN`, kiểu giả, tên bảng giả hoặc giá trị nullable/PK/FK mặc định để làm SQL parse được.
Kiểm identifier quoting theo dialect đã pin; không cài driver, import model ORM hoặc kết nối DB để bổ sung thông tin.
**Đã chốt khi tự review 01/10/2026:** bảng có trường bắt buộc chưa biết thì bỏ cả bảng khỏi DDL, kèm notice. Lý do: một `CREATE TABLE` thiếu cột dễ bị đọc như bảng đầy đủ. FR-027 r3 cho phép cách này ("khối máy chỉ chứa phần biểu diễn được") nhưng chưa chọn rõ; L3 chọn cách này.
Column giữ thứ tự khai báo đã trích, không sắp cột theo tên; bảng sắp theo fact ID. Các giá trị unknown/not_applicable/redacted giữ khác nhau.
DDL của một bảng cần name/dialect/columns biết rõ; mỗi cột có name/type/PK/nullable biết rõ, FK biết rõ hoặc not_applicable có lý do.
Dialect hoặc cú pháp type ngoài bộ renderer hỗ trợ không được chèn thẳng như SQL; bỏ cả bảng đó khỏi DDL,
thêm `DDL_TABLE_OMITTED` với field paths/reason. Identifier phải qua bộ quote dialect. FK tới bảng không thuộc owner được ghi theo identity đã kiểm, không đổi owner để kéo bảng vào file.
Bộ renderer/template đã pin xác định catalogue dialect/type được hỗ trợ; chưa có adapter cho dialect không phải lỗi phân tích upstream.
Trong DDL, comment mang fact/evidence ID giúp đối chiếu; comment bỏ CR/LF và ký tự kết thúc comment từ dữ liệu không tin cậy.

### 6.1. Catalogue DDL ban đầu — `ddl-core-v1`

Catalogue thuộc renderer/template version, không quyết định stack nào được parser hỗ trợ. Chỉ nhận dialect `sqlite` hoặc `postgresql` được facts/rule chứng minh. Không có dialect thì bảng vẫn được mô tả, DDL bị omitted.

| Dialect | Kiểu cột tĩnh được nhận | Phạm vi constraint |
|---|---|---|
| sqlite | INTEGER, REAL, TEXT, BLOB | Cột, PK một cột, NULL/NOT NULL, FK đơn đã biết |
| postgresql | SMALLINT, INTEGER, BIGINT, REAL, DOUBLE PRECISION, BOOLEAN, TEXT, BYTEA, DATE, TIMESTAMP WITHOUT TIME ZONE, TIMESTAMP WITH TIME ZONE; VARCHAR(n), NUMERIC(p,s) với tham số nguyên hợp lệ | Như trên; không SERIAL/IDENTITY/sequence/expression/index/trigger/generated column hoặc named-schema trong v1 |

Kiểu là token từ catalogue, không chèn SQL thô: VARCHAR có n > 0; NUMERIC có 1 ≤ p ≤ 1000 và 0 ≤ s ≤ p. So khớp token canonical do adapter cung cấp; không lấy class Python Integer để tự chọn dialect/type SQL. Identifier được quote bằng double quote và escape quote bên trong, cấm NUL/control; không tách chuỗi chứa dấu chấm thành schema ngầm. Table/schema namespace chưa rõ hoặc được xác định ngoài default search context thì omitted, không đoán.

DDL v1 không phát mệnh đề DEFAULT. PK tối đa một cột, nullable phải false; FK một cột phải có target identity/cột đã kiểm, không tự gộp bảng trùng tên. Bảng có compound key, constraint chưa mô tả được, field thiếu hoặc type chưa hỗ trợ thì giữ bảng mô tả/notice, không xuất DDL thiếu phần như thể đầy đủ.

Định nghĩa còn phụ thuộc khả năng extractor ghi nhận các constraint đã gặp. Nếu adapter không xác định được có constraint ngoài model Column thì đánh table partial với limitation; renderer không chứng nhận DDL tái tạo đầy đủ database. DDL chỉ là subset có nhãn. Trước phát hành renderer phải có ca format/escaping cho từng dialect và so parity với facts; **chưa có kết quả chạy renderer/dialect ở bộ tài liệu này**.

### 6.2. Event contract


Theo FR-027 r3 "Chia tài liệu theo component" và CR-L3GEN-2026-003-decisions-01:

- EVT đặt ở **từng** component có điểm gửi hoặc nhận; owner của mỗi điểm lấy từ `contract_owners`. Mỗi file mô tả vai trò của chính component đó, không có nghĩa component sở hữu độc quyền topic.
- Trong một component, các điểm cùng topic chỉ gom vào một file khi có bằng chứng cùng broker/cấu hình: channel key ở dưới bằng nhau. Khác broker hoặc chưa chứng minh thì mỗi điểm một file.
- Bảng ghi topic, vai trò gửi/nhận của component, broker/config binding, các bên liên quan đã xác minh, schema payload, fact/evidence và unknown kèm lý do.
- Bên kia chỉ được ghi khi CMP-007 đã chấp nhận cạnh event giữa hai component. Không có cạnh đó thì ghi bên kia là `unknown` kèm lý do và đánh dấu `partial` (AC-027-03). Chỉ thấy bên nhận vẫn xuất file. Nhiều bên gửi không phải chọn một bên làm chủ.

Payload đã biết dùng JSON Schema Draft 2020-12; chỉ khai property/type/required/constraint có bằng chứng.
Schema partial gắn `x-analysis` với `completeness: partial`, danh sách phần chưa biết và reason; không đặt `additionalProperties: false` khi chưa chứng minh đóng.
Payload hoàn toàn chưa biết dùng schema `{}` kèm annotation unknown và cảnh báo “không phải schema đầy đủ”; không dùng `{ "type": "null" }` thay thế.
API-004 chưa định nghĩa `binding_id`; exporter không đòi trường không có. Channel key là SHA-256 của JSON array canonical
`[broker, namespace, serialization_context, topic]` khi cả bốn FieldValue known và identity được CMP-007 chấp nhận;
đây chỉ là key đặt artifact, không tạo event/channel entity hay quan hệ mới trong model.
Thiếu bất kỳ phần nào, dùng key theo event fact ID và giữ riêng từng fact; thêm notice `EVENT_BINDING_UNRESOLVED`,
không gộp hai unknown/redacted. File EVT hiện producer hoặc consumer của fact có action đã biết; phía đối diện chỉ có ID component
khi có cạnh event accepted và fact ở cả hai đầu. Không biết action thì giữ dòng unknown, không tự suy từ tên hàm.
Các fact cùng channel có payload mâu thuẫn không bị gộp schema bằng union; giữ các schema theo fact ID và nêu conflict trong bảng.
Schema EVT có `$schema` Draft 2020-12, `x-analysis` ghi fact/evidence IDs và scope; không resolve remote `$ref` hoặc tự sinh payload ví dụ.
Các file ở nhiều component có thể trỏ cùng channel key và cạnh accepted; không tạo một owner mới chỉ để thuận tiện đặt thư mục.

## 7. Commit output, lỗi một phần và retry

CMP-001 chỉ chạy một thao tác ghi cho mỗi run tại một thời điểm; các run có vùng riêng, web chỉ đọc bản đã commit. Vì vậy CMP-008 không cần khóa riêng (CMP-008 r2 §7).
Ghi artifact vào thư mục tạm cùng filesystem; validate schema/định dạng, tham chiếu và parity trước khi publish.
Lần xuất đầu ghi `result.json`, manifest và các file hợp lệ xong mới đổi tên thư mục tạm thành output chưa tồn tại.
Không dùng rename để ghi đè output có nội dung chưa được CMP-001 xử lý. `manifest.json` luôn là ResultBundle, không là con trỏ.
Reader pin một manifest cho mỗi request và chỉ phục vụ artifact `ready` có bytes/hash đúng manifest.
Manifest ghi artifact failed với code/reason/retryable; giữ file ready, không để bộ output thiếu file trông như completed.
RunView của CMP-001 quyết định trạng thái run và `analysis_outcome`; không nhân bản lifecycle/expiry trong ResultBundle.

Retry một artifact failed dùng staging riêng: kiểm bundle/cấu hình và hash mọi artifact ready → render/validate target → kiểm hạn lần nữa
→ install target bằng rename/replace nguyên tử → replace `manifest.json` bằng bản hoàn chỉnh mới. Các file ready, `result.json`
và các field ngoài `artifacts` của manifest giữ nguyên byte/giá trị. Reader giữ manifest cũ thấy target failed nên không được tải nó;
reader lấy manifest mới chỉ thấy file đã hoàn tất. Crash giữa install target và manifest không tạo artifact ready giả: byte chưa được
manifest công nhận bị bỏ qua và dọn/ghi lại ở lần retry tiếp. Crash sau commit thấy hash/status mới nhất quán.
Nếu replace manifest thất bại, giữ manifest cũ; target chưa được công nhận không được coi là completed.
Quy tắc này dựa vào việc CMP-001 chỉ cho một thao tác ghi mỗi run, kể cả hai request retry khác artifact. Không thêm idempotency key HTTP ngoài API-001.

Retry chỉ áp dụng artifact failed có `retryable: true`; `failed → retrying → ready|failed`.
`pending → ready|failed` thuộc lần render đầu. Retry trùng đang chạy được CMP-001 gộp; retry ready không viết lại.
Giữ nguyên snapshot, VerifiedResult, slug map, phiên bản renderer/template và byte của mọi artifact ready.
Không gọi model, không lấy source mới, không gia hạn retention; mất phiên bản renderer trả `VERSION_UNAVAILABLE` không tự nâng phiên bản.
`render_notices` được lập từ plan biểu diễn trước lần render đầu và đóng băng cùng `result.json`; lỗi render/I/O chỉ cập nhật artifact.error.
SVG phụ thuộc `architecture.mmd` ready; khi dependency failed, SVG failed với `DEPENDENCY_UNAVAILABLE` và path dự kiến vẫn giữ.
Retry SVG chỉ được nhận khi dependency ready; sửa nguồn sơ đồ không tự retry SVG, không tự viết lại artifact ready.
Retry sau khởi động lại chỉ khả dụng nếu bundle, phiên bản renderer/template và material CMP-001 yêu cầu vẫn được giữ hợp lệ;
contract không hứa lưu source snapshot trong output để làm retry bền vững. Thiếu material trả `ARTIFACT_NOT_RETRYABLE`.
Serialization ổn định: UTF-8 không BOM, LF, thứ tự key/array/row theo ID đã pin, không chèn timestamp hiện tại hoặc random vào nội dung.
Ngoại lệ thứ tự mang nghĩa như column/parameter giữ thứ tự upstream; ID sets mới sinh được sắp ordinal. Không reorder nội dung VerifiedResult
trong lúc retry; hash byte `result.json` đã commit là điểm đối chiếu ngữ cảnh cũ.
Artifact ID là token opaque do registry của run cấp, ổn định qua retry; không phải đường dẫn hoặc ID hiển thị của model.
Hash nội dung không phụ thuộc mốc retry; manifest trạng thái là metadata được phép đổi.

Lỗi schema/snapshot/dangling edge/evidence/parity là lỗi cả bộ: không publish bundle mới và báo CMP-001.
Lỗi renderer/định dạng của một artifact chỉ làm artifact đó failed; JSON nền tảng hoặc manifest không hợp lệ thì không publish bộ.
`pending`/`retrying` mô tả tiến trình trên RunView; manifest đã commit chỉ có ready/failed. Sau lỗi publish lần đầu không có bundle để
retry artifact; CMP-001 giữ error trên RunView. Retry không đổi trạng thái cuối, analysis_outcome, finished_at hoặc expires_at của run.

| Lỗi | Phạm vi / retry |
|---|---|
| `INVALID_INPUT`, `SNAPSHOT_MISMATCH`, `REFERENCE_INVALID`, `PARITY_FAILED`, `OUTPUT_UNSAFE` | ExportError cả bộ, retryable false; không commit hoặc tự sửa dữ kiện |
| `PUBLISH_FAILED` | ExportError, retryable false trên API artifact; manifest cũ giữ nguyên nếu có. CMP-001 báo lỗi commit; không tuyên bố target ready |
| `VERSION_UNAVAILABLE`, `ARTIFACT_NOT_RETRYABLE`, `RUN_EXPIRED` | ExportError, retryable false; cần khôi phục material hợp lệ hoặc chạy lại theo façade, không đổi version/hạn |
| `RENDER_FAILED`, `WRITE_FAILED` | ArtifactError, retryable true khi lỗi vận hành tạm thời; nếu lỗi tất định đã biết thì false và reason chỉ cách khắc phục |
| `FORMAT_INVALID` | ArtifactError, retryable false với cùng input/version; không coi pass schema là pass parity |
| `DEPENDENCY_UNAVAILABLE` | ArtifactError, retryable true có điều kiện dependency ready; trước đó CMP-001 trả artifact_not_retryable |

Kiểm thiếu ownership/machine fields là notice partial, không là ArtifactError: tài liệu vẫn ready nếu mô tả đúng phần đã biết và unknown.
Renderer phải chuyển mọi giới hạn biểu diễn tới README và web qua render_notices; tải được file không có nghĩa đầy đủ contract.
Trên web, CMP-001 từ chối tải, render/retry hoặc mở bằng chứng khi quá 24 giờ từ trạng thái cuối ban đầu.
Sau khởi động lại phải dọn dữ liệu hết hạn trước phục vụ; CLI output do người dùng quản lý theo SEC-002.
Download chỉ nhận run ID + artifact ID, tra manifest đã commit, kiểm hạn và vùng chứa; không nhận arbitrary path từ client.
Escape Markdown/HTML/Mermaid và làm sạch SVG, vô hiệu hóa script/link tải ngoài; text từ repository là dữ liệu không được thực thi.

## 8. Ca kiểm cần có trước khi triển khai

| Ca | Kết quả kiểm được | Nguồn |
|---|---|---|
| Completed và partial có cùng input version | Cây FR-027, schema/snapshot đúng; partial công bố phần có thật và giới hạn | AC-025-01/02, AC-027-01/02/03 |
| Model 51 node | `INVALID_INPUT`, không publish; không cắt bớt | ABST-002 r2, API-005 §3 |
| JSON, README, Mermaid lệch một cạnh | `PARITY_FAILED`, không publish | AC-025-04, CMP-008 r2 §4 |
| Bảng Markdown có route mà khối OpenAPI không có, không có notice | Artifact API `FORMAT_INVALID` | CMP-008 r2 §4 |
| Mỗi ô của bảng §3.2 | Đúng dấu phần thiếu, đúng notice | CMP-008 r2 §2 |
| Owner `null` | Không có file; README và JSON liệt kê; notice `CONTRACT_OWNER_UNRESOLVED` | CMP-005 r2 §1 |
| Chỉ thấy bên nhận `order-created` | File EVT ở component nhận; bên gửi `unknown`, `partial` | AC-027-03 |
| Cạnh thiếu đích hoặc evidence khác snapshot | Cả generation bị từ chối trước publish | AC-025-02, ACC-002 |
| Hai app cùng GET `/items` trong một component | Bảng giữ hai dòng; cả hai operation omitted khỏi OpenAPI có notice | AC-027-01, §5 |
| Không biết status/type SQL/payload/broker | Unknown có lý do; không bịa 200, DDL, null hoặc event edge | AC-027-01/02/03 |
| Tên trùng, reserved, dấu tiếng Việt, traversal | Mapping ổn định theo ID, mọi path nằm trong vùng output | FR-027, SEC-002 |
| Renderer một artifact lỗi; retry; crash ở từng bước commit | Artifact ready giữ nguyên hash; reader chỉ thấy generation hoàn chỉnh | AC-025-03, CMP-008 §5–7 |
| Hết hạn khi máy tắt, khởi động lại hoặc đang retry | Không phục vụ output/source; retry không kéo dài thời hạn | SEC-002 |

Đây là ca kiểm được đề xuất, chưa là test ID, kết quả chạy hoặc bằng chứng nghiệm thu.

## 9. Nguồn và điểm cần chốt

Nguồn ở nhánh `docs/gate-2` commit `5d06f14`:

- [CMP-L3GEN-008](../../../architecture/l2/CMP-L3GEN-008.md) r2: trách nhiệm, ba bộ sinh, kiểm bản xuất, dữ liệu thiếu, failure mode.
- [CMP-L3GEN-005](../../../architecture/l2/CMP-L3GEN-005.md) r2 và [ADR-2026-003](../../../architecture/adr/ADR-2026-003.md) r2: CMP-005 gán owner.
- [FR-L3GEN-025](../../../requirements/_superseded-r28/fr/FR-L3GEN-025.md) r2, [FR-L3GEN-026](../../../requirements/_superseded-r28/fr/FR-L3GEN-026.md) r1, [FR-L3GEN-027](../../../requirements/_superseded-r28/fr/FR-L3GEN-027.md) r3 (đã superseded): output, web, API/TBL/EVT.
- [FR-L3GEN-029](../../../requirements/fr/FR-L3GEN-029.md) r3: README "Lời gọi HTTP ra ngoài", response `list[Model]` (r5).
- [ABST-002](../../../requirements/nfr/NFR-L3GEN-ABST-002.md) r2, [ACC-002](../../../requirements/nfr/NFR-L3GEN-ACC-002.md) r2, [OPS-001](../../../requirements/nfr/NFR-L3GEN-OPS-001.md) r1, [SEC-002](../../../requirements/nfr/NFR-L3GEN-SEC-002.md) r3.
- [Execution guide](../../../../docs/agentic-sdlc-execution-guide.md), A.1 và B.10.

Chi tiết L3 chưa có trong nguồn: catalogue DDL, thuật toán slug, cách retry/commit manifest, nhãn file topic chưa biết. Đã chốt khi tự review: bỏ cả bảng khỏi DDL khi thiếu trường (§6). D-03 vẫn mở, renderer không chia lại component.
