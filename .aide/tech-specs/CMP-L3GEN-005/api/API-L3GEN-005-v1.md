---
uid: "01M3B99N5T4F4DCBZDC4WTPZ5M"
key: "API-L3GEN-005-v1"
type: "api-contract"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-005"],"satisfies":["FR-L3GEN-022","FR-L3GEN-027"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-AI-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# API-L3GEN-005-v1 — Hợp đồng dựng mô hình kiến trúc

## 1. Phạm vi và giao diện

Owner CMP-005; caller CMP-001; consumer CMP-007. Nguồn: CMP-L3GEN-005 r2, ADR-2026-003 r2 (phương án A), FR-L3GEN-022 r2, FR-L3GEN-027 r3 ở nhánh `docs/gate-2` commit `5d06f14`. Đây là giao diện hàm nội bộ, không phải HTTP service. CMP-005 chỉ dùng FactSet của CMP-004 và inventory/snapshot đã được cấp; gọi model qua CMP-006. Không đọc thêm source, tạo fact mới hoặc công bố kết luận.

**D-03 đang mở theo yêu cầu người phụ trách ngày 25/09/2026.** Contract này hoàn thiện hình dạng dữ liệu, kiểm membership, binding và lỗi; **chưa chọn thuật toán chia component**. `directory-v1` và phương án kết hợp code/LLM chỉ là ứng viên thử nghiệm. Việc hoàn thành tài liệu, kiểm schema hay dùng fixture không tự duyệt một ứng viên. Xem mục 3.1.

```text
build_architecture(input: BuildArchitectureInput,
                   gateway: ModelGateway,
                   context: RunContext) -> BuildArchitectureResult
```

`RunContext` là capability nội bộ do CMP-001 cấp: run ID, cancellation khi engine timeout/shutdown, snapshot reader chỉ đọc, disclosure record và budget dùng chung. Cancellation ở đây không thêm thao tác user-cancel ngoài scope. Context không được serialize vào prompt. `BuildArchitectureInput` phải tương ứng đúng inventory đã kiểm của run; `units` là projection ổn định, không phải inventory nguồn thứ hai. `file_ids` chứa toàn bộ source file đủ điều kiện chia nhóm, kể cả file không trích được fact. Một đơn vị phải có ít nhất một file; tập đơn vị rỗng được trả mô hình rỗng kèm limitation; lần chạy vẫn `partial` nếu publish được (CMP-007 r2 §4).

Hàm trả `model` khi đã kiểm xong toàn bộ membership và tham chiếu. Lỗi đầu vào bất biến trả `error` và `model:null`; lỗi model trả `partial` với phần code dựng được. FactSet đầu vào không bị sửa hoặc cắt; CMP-001 giữ nó trong kết quả run và CMP-007 nhận lại cùng tập dữ kiện. `full`/`partial` ở đây chỉ là mức hoàn thành bước dựng model, không khẳng định độ đúng hoặc coverage.

## 2. JSON Schema nguồn

Khối dưới là nguồn chuẩn tắc duy nhất. Công cụ trích thành `API-L3GEN-005-v1.schema.json` cùng thư mục để kiểm; không sửa bản trích riêng. Các `$ref` trỏ schema do spec owner tương ứng sinh ra. `schema_version` là phiên bản payload, độc lập revision tài liệu. Chuỗi rỗng không đại diện unknown; field mô tả tùy chọn bị thiếu nghĩa là chưa có annotation, được giải thích bằng `label_status`/limitation.

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-005-v1.schema.json",
  "$ref":"#/$defs/BuildArchitectureInput",
  "$defs":{
    "Id":{"type":"string","minLength":1,"maxLength":200},
    "Ids":{"type":"array","items":{"$ref":"#/$defs/Id"},"uniqueItems":true},
    "Confidence":{"enum":["exact","inferred"]},
    "Completeness":{"enum":["full","partial"]},
    "RelationType":{"enum":["calls","http","publishes","consumes","depends_on"]},
    "Unit":{"type":"object","additionalProperties":false,"required":["unit_id","flat","file_ids"],"properties":{
      "unit_id":{"$ref":"#/$defs/Id"},"flat":{"type":"boolean"},
      "file_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1}
    }},
    "BuildArchitectureInput":{"type":"object","additionalProperties":false,"required":["schema_version","run_id","snapshot_id","fact_set","units","partition_version","rule_set_version"],"properties":{
      "schema_version":{"const":"0.1.0"},"run_id":{"$ref":"#/$defs/Id"},"snapshot_id":{"$ref":"#/$defs/Id"},
      "fact_set":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/FactSet"},
      "units":{"type":"array","items":{"$ref":"#/$defs/Unit"}},
      "partition_version":{"$ref":"#/$defs/Id"},"rule_set_version":{"const":"binding-v1-draft"}
    }},
    "Component":{"type":"object","additionalProperties":false,"required":["id","unit_id","name","member_file_ids","grouping_source","confidence","completeness","evidence_ids","label_status"],"properties":{
      "id":{"$ref":"#/$defs/Id"},"unit_id":{"$ref":"#/$defs/Id"},"name":{"type":"string","minLength":1,"maxLength":200},
      "member_file_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},
      "grouping_source":{"enum":["code","llm","fallback"]},"confidence":{"$ref":"#/$defs/Confidence"},
      "completeness":{"$ref":"#/$defs/Completeness"},"completeness_reason":{"type":"string","minLength":1,"maxLength":1000},"evidence_ids":{"$ref":"#/$defs/Ids"},
      "description":{"type":"string","minLength":1,"maxLength":2000},"role":{"type":"string","minLength":1,"maxLength":200},
      "inference_reason":{"type":"string","minLength":1,"maxLength":1000},"label_status":{"enum":["path_fallback","model_labeled"]},
      "provenance":{"type":"array","minItems":1,"items":{"$ref":"API-L3GEN-006-v1.schema.json#/$defs/Provenance"}}
    },"allOf":[{"if":{"properties":{"grouping_source":{"const":"llm"}}},"then":{"required":["inference_reason","provenance"],"properties":{"confidence":{"const":"inferred"}}}},{"if":{"properties":{"confidence":{"const":"inferred"}}},"then":{"required":["inference_reason"]}},{"if":{"properties":{"completeness":{"const":"partial"}}},"then":{"required":["completeness_reason"]}}]},
    "ExternalSystem":{"type":"object","additionalProperties":false,"required":["id","name","fact_ids","evidence_ids","confidence","completeness"],"properties":{
      "id":{"$ref":"#/$defs/Id"},"name":{"type":"string","minLength":1,"maxLength":200},
      "fact_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},"evidence_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},
      "confidence":{"$ref":"#/$defs/Confidence"},"completeness":{"$ref":"#/$defs/Completeness"},"completeness_reason":{"type":"string","minLength":1,"maxLength":1000},
      "inference_reason":{"type":"string","minLength":1,"maxLength":1000}
    },"allOf":[{"if":{"properties":{"confidence":{"const":"inferred"}}},"then":{"required":["inference_reason"]}},{"if":{"properties":{"completeness":{"const":"partial"}}},"then":{"required":["completeness_reason"]}}]},
    "Edge":{"type":"object","additionalProperties":false,"required":["id","source_component_id","target_component_id","relation_type","fact_ids","evidence_ids","origin","confidence","completeness","rule_id","rule_version"],"properties":{
      "id":{"$ref":"#/$defs/Id"},"source_component_id":{"$ref":"#/$defs/Id"},"target_component_id":{"$ref":"#/$defs/Id"},
      "relation_type":{"$ref":"#/$defs/RelationType"},"fact_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},
      "evidence_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},"origin":{"enum":["static","llm"]},
      "confidence":{"$ref":"#/$defs/Confidence"},"completeness":{"$ref":"#/$defs/Completeness"},"completeness_reason":{"type":"string","minLength":1,"maxLength":1000},
      "rule_id":{"enum":["resolved-target","http-binding","event-binding","config-binding"]},"rule_version":{"const":"1-draft"},
      "label":{"type":"string","minLength":1,"maxLength":200},"inference_reason":{"type":"string","minLength":1,"maxLength":1000},
      "provenance":{"type":"array","minItems":1,"items":{"$ref":"API-L3GEN-006-v1.schema.json#/$defs/Provenance"}}
    },"allOf":[{"if":{"properties":{"origin":{"const":"llm"}}},"then":{"required":["inference_reason","provenance"],"properties":{"confidence":{"const":"inferred"}}}},{"if":{"properties":{"confidence":{"const":"inferred"}}},"then":{"required":["inference_reason"]}},{"if":{"properties":{"completeness":{"const":"partial"}}},"then":{"required":["completeness_reason"]}}]},
    "RejectedProposal":{"type":"object","additionalProperties":false,"required":["proposal_id","kind","reason_code","message","referenced_ids"],"properties":{
      "proposal_id":{"$ref":"#/$defs/Id"},"kind":{"enum":["label_components","propose_edges","group_flat"]},
      "reason_code":{"enum":["UNKNOWN_ID","WRONG_SNAPSHOT","OUTSIDE_SCOPE","MISSING_ENDPOINT_EVIDENCE","UNPROVEN_BINDING","MEMBERSHIP_MISMATCH","IMMUTABLE_FIELD","SCHEMA_INVALID"]},
      "message":{"type":"string","minLength":1,"maxLength":1000},"referenced_ids":{"$ref":"#/$defs/Ids"}
    }},
    "ContractOwner":{"type":"object","additionalProperties":false,"required":["fact_id","contract_kind","component_id","rule_id","rule_version","evidence_ids"],"properties":{
      "fact_id":{"$ref":"#/$defs/Id"},"contract_kind":{"enum":["api","table","event"]},
      "component_id":{"oneOf":[{"$ref":"#/$defs/Id"},{"type":"null"}]},
      "rule_id":{"const":"declaration-file"},"rule_version":{"const":"1-draft"},
      "evidence_ids":{"$ref":"#/$defs/Ids"},"reason":{"type":"string","minLength":1,"maxLength":1000}
    },"allOf":[{"if":{"properties":{"component_id":{"type":"null"}}},"then":{"required":["reason"]},"else":{"properties":{"evidence_ids":{"minItems":1}}}}]},
    "ArchitectureModel":{"type":"object","additionalProperties":false,"required":["schema_version","snapshot_id","partition_version","components","edges","contract_owners","limitations","rejected_proposals"],"properties":{
      "schema_version":{"const":"0.1.0"},"snapshot_id":{"$ref":"#/$defs/Id"},"partition_version":{"$ref":"#/$defs/Id"},
      "components":{"type":"array","items":{"$ref":"#/$defs/Component"}},"external_systems":{"type":"array","items":{"$ref":"#/$defs/ExternalSystem"}},
      "edges":{"type":"array","items":{"$ref":"#/$defs/Edge"}},
      "contract_owners":{"type":"array","items":{"$ref":"#/$defs/ContractOwner"}},
      "limitations":{"type":"array","items":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/Limitation"}},
      "rejected_proposals":{"type":"array","items":{"$ref":"#/$defs/RejectedProposal"}}
    }},
    "BuildError":{"type":"object","additionalProperties":false,"required":["code","message","retryable"],"properties":{
      "code":{"enum":["INVALID_INPUT","SNAPSHOT_MISMATCH","INVENTORY_MISMATCH","PARTITION_POLICY_UNAVAILABLE","CANCELLED","INTERNAL_INVARIANT"]},
      "message":{"type":"string","minLength":1,"maxLength":1000},"retryable":{"const":false}
    }},
    "BuildArchitectureResult":{"type":"object","additionalProperties":false,"required":["status","model","error"],"properties":{
      "status":{"enum":["full","partial","error"]},"model":{"oneOf":[{"$ref":"#/$defs/ArchitectureModel"},{"type":"null"}]},
      "error":{"oneOf":[{"$ref":"#/$defs/BuildError"},{"type":"null"}]}
    },"allOf":[{"if":{"properties":{"status":{"const":"error"}}},"then":{"properties":{"model":{"type":"null"},"error":{"$ref":"#/$defs/BuildError"}}},"else":{"properties":{"model":{"$ref":"#/$defs/ArchitectureModel"},"error":{"type":"null"}}}}]}
  }
}
```

## 3. Membership, định danh và tính lặp lại

| Quy tắc | Hành vi bắt buộc của bản draft |
|---|---|
| Phạm vi | Mỗi file trong hợp `units.file_ids` thuộc đúng một component cùng unit; file nằm ngoài tập này bị từ chối. Không chia theo symbol. File ngoài phạm vi không bị biến thành component. |
| Policy chia nhóm | `partition_version` là định danh bất biến của policy + cấu hình, không phải lựa chọn thuật toán mặc định. Phiên bản output phải bằng input. Engine tra registry cấu hình nội bộ; không nạp mã, path hoặc URL từ ID. Policy chưa chọn/không tồn tại trả `PARTITION_POLICY_UNAVAILABLE`, không âm thầm dùng `directory-v1`. |
| Repo phẳng theo nguồn hiện hành | Nếu policy đã được chọn phân loại unit là flat, dùng một request `group_flat` cho toàn bộ flat units, tách membership theo unit. Chỉ nhận cả proposal nếu partition phủ đúng mỗi file một lần, không nhóm rỗng/nhóm xuyên unit. Code cấp ID; tên nhóm model không tham gia ID. Contract này giữ ranh giới FR-022 hiện hành, không chốt heuristic flat. |
| Fallback phẳng | Một component chưa chia nhóm cho mỗi unit, giữ tất cả file của unit, `grouping_source:fallback`, `label_status:path_fallback`, `completeness:partial`. Không tạo một component cho mỗi file. |
| ID | Component ID = `cmp_` + SHA-256 của UTF-8 JSON array `[snapshot_id,unit_id,sorted(member_file_ids)]` compact. Edge ID = `edge_` + SHA-256 của `[snapshot_id,source_id,target_id,relation_type]`. External ID có prefix `ext_` và hash `[snapshot_id,canonical_target_identity]`. Không dùng tên model hoặc thứ tự request. |
| Tất định | Membership code/fallback và static edges tất định với cùng snapshot, facts, partition/rule version. Sau grouping bằng model, static edges chỉ tất định **với partition đã cố định**; không hứa hai lượt model cho cùng grouping. |
| Nhãn | `label_status:path_fallback` nói rõ tên theo path chưa được model đặt. Model đặt nhãn không đổi membership, ID, quan hệ, fact hay confidence của cạnh có sẵn. Description/role là annotation suy ra, không phải fact mới. |
| Trần 50 node | Mô hình giao đi có tối đa 50 node (component + external system), theo NFR-ABST-002 r2 và CMP-005 r2 §4: "giữ trần; phần dư nằm ở lớp bằng chứng". Cách gom phần dư là một phần của thuật toán chia nhóm (D-03, còn mở); policy nào không giữ được trần thì không được chọn. Model vượt 50 node là `INTERNAL_INVARIANT`, không cắt bớt ngầm. Mọi artifact dùng cùng tập node này (CMP-008 r2); không có projection ẩn node. |

Component không có fact vẫn giữ membership trước verification; `evidence_ids:[]`, `completeness:partial` và limitation chỉ rõ chưa có kết luận source đủ bằng chứng. CMP-007 không được công bố mô tả suy đoán cho component đó. `grouping_source:code` chỉ nói ai thực hiện phép chia, không tự chứng minh component đúng về trách nhiệm. `exact` chỉ dùng khi membership là ánh xạ trực tiếp theo ranh giới được chứng minh; membership suy ra từ heuristic hoặc LLM dùng `inferred` với lý do. Cả hai vẫn cần đánh giá độc lập theo OBS.

### 3.1. Phần cố định để review và phần cố ý chưa chốt

| Phần | Trạng thái của thiết kế này |
|---|---|
| Schema component, membership theo file, cùng snapshot/unit, ID và kiểm tham chiếu | Đã đặc tả trong bản draft, chờ review thông thường; consumer không cần biết thuật toán |
| Thuật toán, source root/flat heuristic, trọng số dependency/tên, mức gộp/tách | **D-03 OPEN — chưa chọn** |
| Mở rộng LLM sửa membership cho repo có thư mục | **Ứng viên nghiên cứu**, chưa được phép bởi FR-022/NFR-AI-002 hiện hành |
| Phép kiểm downstream và renderer | Dùng membership fixture được ghi trước; không chạy hoặc đánh giá thuật toán chia nhóm |

Ba ứng viên để so sánh: (A) thư mục đầu tiên (`directory-v1`, chỉ làm mốc đơn giản); (B) code kết hợp root/thư mục/tên/dependency; (C) code tạo nhóm rồi LLM đề xuất chỉnh phần mơ hồ. Chưa ứng viên nào được mặc định là thắng hoặc được bật production. Không đặt ngưỡng/trọng số giả để lấp quyết định còn mở.

Điều kiện đóng D-03: hai thành viên thống nhất mức trách nhiệm của component và ranh giới file/unit; pin cùng snapshot và gold độc lập; so sánh membership, cạnh, biến động và ngân sách trên repo theo chức năng/theo tầng/phẳng/bọc root/có phần dùng chung; ghi kết quả và phương án được chọn. Chỉnh trên tập dev. Golden v1 hiện chỉ có nhãn kiến trúc ở 7 case dev (20 component, 28 membership, 13 cạnh), dưới cỡ mẫu OBS, và không có nhãn kiến trúc ở held-out. Vì vậy so sánh hiện chỉ báo được TP/FP/FN; muốn đánh giá trên held-out thì phải gán nhãn kiến trúc cho tập đó trước. Nếu chọn C, đồng bộ FR-022, NFR-AI-002, CMP-003/005/006 và task schema trước khi dùng; schema hiện không cấp quyền đó.

Không có policy khả dụng: CMP-005 trả lỗi định kiểu, CMP-001 giữ dữ kiện và công bố thiếu bước kiến trúc theo policy run; không giả là đã chia tốt bằng cách trả fallback âm thầm. Fallback một component/unit chỉ áp dụng cho lỗi tác vụ flat **sau khi** đã chọn policy. Test double có tên `fixture-membership-v1` nhận membership được soạn sẵn, chỉ dùng trong kiểm contract, không đưa vào CLI/web hay registry production.

Mọi component, external system hoặc cạnh có `completeness:partial` phải có `completeness_reason` ngay trên đối tượng; `inference_reason` giải thích confidence và không thay lý do thiếu dữ liệu. Model trước verification giữ partition để kiểm; `VerifiedResult.model` sau CMP-007 chỉ chứa các đối tượng được chấp nhận, phần bị loại nằm trong decision/limitation.

### 3.2. Component sở hữu contract

Theo ADR-2026-003 r2 và CMP-005 r2 §1: CMP-005 xác định component sở hữu từng contract; CMP-007 kiểm; CMP-008 chỉ đọc kết quả, không tự gán lại. `contract_owners` có đúng một mục cho mỗi fact `route`, `table`, `event` trong FactSet đầu vào.

| Loại | Component sở hữu (FR-027 r3) | Nơi lấy file khai báo |
|---|---|---|
| `api` (fact `route`) | Component chứa nơi khai báo route | Evidence `declaration_evidence_id` của route (decorator hoặc lời gọi đăng ký route) |
| `table` | Component chứa khai báo bảng/model ánh xạ | `declaration_evidence_id` của table |
| `event` | Component chứa điểm gửi hoặc nhận đó; mỗi điểm một mục | `declaration_evidence_id` của event (call site publish/consume) |

Rule `declaration-file` / `1-draft`:

1. Lấy `declaration_evidence_id` của fact. Phải là FieldValue known và trỏ evidence có trong `fact.evidence`.
2. Tìm component cùng `unit_id` có `member_file_ids` chứa `file_id` của evidence đó. So bằng ID, không so đường dẫn gần giống hay tên.
3. Đúng một component: ghi `component_id` và `evidence_ids:[declaration_evidence_id]`.
4. Không có `declaration_evidence_id` known, hoặc file không thuộc component nào: `component_id:null`, `evidence_ids:[]`, `reason` nêu nguyên nhân. Fact vẫn giữ trong kết quả `partial` (CMP-005 r2 §1); không đặt vào component gọi nó.

Nơi gọi API hoặc dùng bảng chỉ tham chiếu, không đổi owner. Router được mount ở file khác không đổi owner. Owner theo source không phải bằng chứng về deployment hay quyền sở hữu nghiệp vụ.

## 4. Luật dựng và kiểm cạnh

Mọi fact/evidence ID phải thuộc đúng FactSet và snapshot; mọi file evidence phải có trong snapshot, digest/range hợp lệ theo API-004. Với component, evidence phải nằm trong member file. Với cạnh, `evidence_ids` là hợp evidence của `fact_ids`, không được chèn evidence từ fact không được trích dẫn. Chỉ `attributes` có FieldValue `state:known` và evidence hợp lệ mới được dùng trong binding; unknown/redacted/not_applicable không bằng nhau chỉ vì cùng nhãn trạng thái. Dữ kiện thật ở hai đầu là điều kiện cần, **không tự chứng minh loại, chiều hoặc binding**. Các cờ `resolved`, `exact` và `full` không thay kiểm nội dung thuộc tính/đích.

| `rule_id` / relation | Đủ điều kiện nhận | Trường hợp loại |
|---|---|---|
| `resolved-target` / `calls`, `depends_on` | Có fact lời gọi/import với `resolution:resolved`; target fact ID tồn tại, quan hệ target được extractor hỗ trợ, vị trí source thuộc A và target thuộc B. | Target ID lạ, target ngoài snapshot, unresolved, hai symbol cùng tên nhưng không có binding. |
| `http-binding` / `http` | Fact HTTP client thuộc A; fact route thuộc B; method, normalized path, base URL/service identity và app registration context khớp qua literal/config binding đã trích. Không làm mất prefix/query semantics. | Chỉ cùng suffix `/users`, host động, nhiều app cùng path nhưng thiếu app identity. |
| `event-binding` / `publishes`, `consumes` | Fact producer/consumer cùng broker identity, topic và serialization context đã xác định; chiều `publishes` từ producer tới consumer, `consumes` từ consumer tới producer. | Chỉ trùng topic, broker unknown, chiều đảo, broker không được extractor hỗ trợ. |
| `config-binding` / `depends_on` | Config reference của A có đích xác định và fact đích thuộc B; đường dẫn key và scope config khớp, không chỉ cùng tên biến. | Trùng từ khóa hoặc model khẳng định mà không có reference/binding trong facts. |

Luật chỉ dùng attribute đã được extractor định nghĩa và kiểm được; thiếu attribute/binding thì `UNPROVEN_BINDING`, không điền bằng lời giải thích model. AC-022-02 (FR-022 r2) và CMP-005 r2 chỉ yêu cầu dữ kiện ở hai đầu. `binding-v1-draft` là chi tiết L3 chặt hơn: còn phải chứng minh loại, chiều, đích bằng rule có phiên bản. Rule này chỉ loại thêm cạnh, không nhận cạnh mà AC loại; chờ review. Chưa phải bộ rule đã triển khai/đo nghiệm thu; việc này không chọn hoặc sửa thuật toán chia component ở D-03.

Static edge gộp theo bộ `(source,target,relation_type)`, giữ tất cả fact/evidence; bỏ self-edge khỏi sơ đồ dependency nhưng giữ fact gốc. Static edge có binding trực tiếp được `exact`; grouping LLM làm endpoint attribution suy ra thì cạnh là `inferred` kèm lý do. Model proposal được nhận luôn `origin:llm,confidence:inferred`; nếu trùng static edge, giữ static edge và bổ sung provenance proposal, không hạ/đổi loại hoặc nhân đôi cạnh. `completeness` lấy `partial` nếu còn ngữ cảnh/membership chưa đầy đủ nhưng chứng cứ tối thiểu của chính binding vẫn đủ; thiếu chứng cứ bắt buộc cho binding thì loại cạnh, không dùng nhãn partial để cho qua.

External system là node tùy chọn riêng, không có file membership và dùng chung namespace ID. Hai trường endpoint giữ tên `*_component_id` vì compatibility nhưng có thể tham chiếu external ID. Chỉ tạo external từ target identity **đã resolved bằng code**, có fact/evidence tại cấu hình/lời gọi trong snapshot; không khẳng định source bên ngoài đã được phân tích. Trong revision này LLM proposal chỉ nối component nội bộ: không có fact thật ở hai đầu thì loại. Extension external cần review vì L2 chưa mô tả node type này; producer chưa hỗ trợ có thể bỏ `external_systems` và giữ external references trong FactSet/limitations.

## 5. Lỗi, transaction, concurrency

| Tình huống | Kết quả |
|---|---|
| FactSet khác snapshot, ID trùng hoặc inventory không nhất quán | `error`, không gọi gateway, không trao model dở dang. |
| Policy chưa chọn, ID policy không hỗ trợ hoặc cấu hình khác phiên bản khai báo | `error:PARTITION_POLICY_UNAVAILABLE`, `model:null`; không tự dùng thuật toán khác hoặc gọi LLM. |
| Timeout/quota/key/schema/budget ở gateway | Giữ partition và cạnh tĩnh; `partial`; ghi limitation với mã gateway, tên path và trạng thái chưa đặt nhãn. |
| Grouping thiếu/trùng file | Loại cả grouping proposal, ghi `MEMBERSHIP_MISMATCH`; fallback một component mỗi unit. |
| Label sửa membership/ID | Loại annotation, giữ bản code; ghi `IMMUTABLE_FIELD` nếu payload qua schema mà ý nghĩa vẫn sửa đối tượng. |
| Một edge proposal sai | Loại edge đó, ghi ID/lý do, kiểm proposal khác; edge bị loại không tới CMP-007 như cạnh công bố. |
| Gemini input cộng output reserve >50.000 token | Không cắt FactSet cho vừa. Bỏ riêng tác vụ đó; grouping fallback hoặc chỉ giữ static edges; `partial`. |
| Hủy run hoặc invariant nội bộ cuối bước lỗi (gồm model vượt 50 node) | `error`, không publish model; caller giữ FactSet để xử lý kết quả theo API-001. |
| Fact route/table/event không tìm được owner | Ghi `contract_owners` với `component_id:null` và reason; `partial`; không loại fact. |

Grouping và dựng cạnh chạy một luồng. Label tasks có thể song song; gateway giữ semaphore/budget toàn run. Không gọi lại model thành công để retry bước export. Sau validation, giao model bất biến một lần; provenance của annotation/grouping/edge dùng schema API-006.

## 6. Ví dụ và tiêu chí kiểm

Ví dụ dương dưới kiểm theo `#/$defs/ArchitectureModel`; fixture phải cung cấp fact `f_call`, `f_target`, `f_route`, evidence `e_call`, `e_target`, `e_route` trong snapshot `s1` (`e_route` ở `file_a`): `f_call` ở `file_a`, target `f_target` ở `file_b`, binding resolved. Membership được soạn sẵn theo `fixture-membership-v1`, không phải kết quả chạy thuật toán hoặc lựa chọn D-03. ID ngắn chỉ dùng fixture, kiểm sản phẩm tính ID theo quy tắc hash mục 3.

```json
{
  "schema_version":"0.1.0","snapshot_id":"s1","partition_version":"fixture-membership-v1",
  "components":[
    {"id":"cmp_a","unit_id":"u1","name":"api","member_file_ids":["file_a"],"grouping_source":"code","confidence":"exact","completeness":"full","evidence_ids":["e_call"],"label_status":"path_fallback"},
    {"id":"cmp_b","unit_id":"u1","name":"service","member_file_ids":["file_b"],"grouping_source":"code","confidence":"exact","completeness":"full","evidence_ids":["e_target"],"label_status":"path_fallback"}
  ],
  "edges":[{"id":"edge_ab","source_component_id":"cmp_a","target_component_id":"cmp_b","relation_type":"calls","fact_ids":["f_call","f_target"],"evidence_ids":["e_call","e_target"],"origin":"static","confidence":"exact","completeness":"full","rule_id":"resolved-target","rule_version":"1-draft"}],
  "contract_owners":[{"fact_id":"f_route","contract_kind":"api","component_id":"cmp_a","rule_id":"declaration-file","rule_version":"1-draft","evidence_ids":["e_route"]}],
  "limitations":[],"rejected_proposals":[]
}
```

| Ca contract dự kiến | Kết quả mong đợi |
|---|---|
| Đảo thứ tự facts/file input, fixed partition | ID và static graph không đổi; sort ID trước serialize. |
| Policy chưa chọn/không hỗ trợ | `PARTITION_POLICY_UNAVAILABLE`; không có provider request hoặc default partition âm thầm. |
| `f_call` là unresolved, còn `f_target` tồn tại | Không có edge; vẫn giữ cả hai facts. |
| HTTP client A và route B có evidence thật nhưng host khác | `UNPROVEN_BINDING`; schema pass không làm edge được nhận. |
| Proposal tham chiếu evidence snapshot `s2` | `WRONG_SNAPSHOT`; cạnh không xuất hiện trong model. |
| Flat grouping gán `file_a` hai nhóm, bỏ `file_b` | Loại cả proposal; một component chứa `[file_a,file_b]` cho `u1`; partial. |
| Flat grouping hợp lệ, đổi tên nhóm giữa hai lượt | Membership cố định thì ID giữ nguyên; provenance ghi hai kết quả riêng, không hứa nội dung giống nhau. |
| Policy cho 51 node | `INTERNAL_INVARIANT`; không cắt bớt, không publish. Policy đó không đạt điều kiện chọn ở D-03. |
| Route khai báo ở `file_a`, router mount ở `file_b` | Owner là component chứa `file_a`. |
| Table không có `declaration_evidence_id` known | Owner `null` có reason; fact giữ nguyên; `partial`. |
| Provider hỏng sau static build | `partial`, static graph giữ nguyên, limitation có nguyên nhân; không đoán cạnh thay thế. |

Đây là ca thiết kế cho provider giả/invariant checker, không phải evidence đã chạy hoặc benchmark accuracy. Breaking change gồm đổi enum/ngữ nghĩa ID, membership, required field hoặc relation rule; tăng payload major và review CMP-001/006/007/008 trước khi đóng phiên bản.
