---
uid: "01M3B99N5VD55SQXBXERQEPN2M"
key: API-L3GEN-007-v1
type: api-contract
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-007"],"satisfies":["FR-L3GEN-022","FR-L3GEN-023","FR-L3GEN-024","FR-L3GEN-027"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-SEC-002"]}
verified_at: null
verified_against: []
classification: internal
ai_assisted: true
---

# Contract cửa kiểm bằng chứng

Draft theo CMP-L3GEN-007 r2 ở nhánh `docs/gate-2` commit `5d06f14`, gồm mục "Kiểm nội dung contract trước khi xuất". `verify(snapshot, inventory, facts, architecture_model, rule_catalog) -> VerifiedResult` là giao diện nội bộ. CMP-001 điều phối, CMP-008 chỉ xuất VerifiedResult. Không dùng LLM để quyết pass. Binding D-01 là chi tiết L3 chặt hơn AC-022-02 (FR-022 r2): chỉ loại thêm cạnh, không nhận cạnh mà AC loại. Cần review/kiểm rule thực tế; không coi schema pass là accuracy pass.

## 1. Trình tự kiểm và chính sách loại

1. Kiểm version/schema, cùng snapshot; lỗi envelope/snapshot thì trả lỗi `INPUT_CONTRACT_INVALID`, không xuất model nửa kiểm.
2. Kiểm mọi Fact ID, EvidenceRef, hash và range bằng snapshot; kiểm typed attributes của API-L3GEN-004-v1. Fact hỏng bị loại khỏi tập công bố, giữ decision và limitation.
3. Kiểm membership, unique ID, owner unit, nhãn và lý do; có file không có fact dùng được thì giữ phạm vi file ở inventory/limitation, không bịa code fact để lấp evidence.
4. Kiểm từng cạnh bằng rule có version, cùng facts; không chỉ tin kết quả sơ kiểm của CMP-005. Loại cạnh không qua rule.
5. Dọn tham chiếu sau khi loại: không để cạnh trỏ node bị loại, field/model reference trỏ fact bị loại. Phần bị mất chuyển unknown/partial kèm lý do; không tự thay bằng thực thể khác.
6. Kiểm nội dung contract (CMP-007 r2 §1): từng trường known của fact route/table/event theo rule `CONTRACT-FIELD`; owner trong `model.contract_owners` theo rule `CONTRACT-OWNER`. Trường không qua kiểm chuyển `unknown` kèm lý do; fact vẫn giữ phần còn lại.
7. Lập evidence_index từ dữ kiện còn hợp lệ; decision bị loại có thể chứa ID đầu vào không tồn tại để chẩn đoán, không coi ID đó là evidence công bố.
8. Giao kết quả một lần; CMP-001 xác định trạng thái run theo bảng lifecycle tại API-001. Có claim bị loại hoặc thiếu kiến trúc thì partial. Loại hết mọi kết luận thì trả mô hình rỗng kèm giới hạn, trạng thái `partial` (CMP-007 r2 §4). Mô hình rỗng không bao giờ là completed.

**D-03 vẫn mở.** Verifier nhận partition cùng `partition_version` từ producer, không tự chạy lại hoặc lựa chọn thuật toán chia component. Membership của fixture chỉ kiểm hợp đồng tham chiếu. Không chuyển heuristic grouping thành `exact` vì code thực hiện, và không coi verdict accepted là phê duyệt thuật toán.

## 2. Catalog rule ban đầu — đề xuất để review

| Rule / version | Điều kiện chấp nhận | Không đủ thì |
|---|---|---|
| MEMBER-SOURCE / 1 | File thành viên có trong snapshot/unit; component có fact/evidence nguồn tương ứng; không sót/trùng assignment trong phạm vi file phân tích | Loại grouping không hợp lệ và ghi limitation; verifier không tự chia lại hoặc fallback. Fallback chỉ do CMP-005 tạo trước verification, theo policy đã được chọn. |
| resolved-target / 1-draft | Fact reference resolved, source ở A, target_fact_ids có fact ở B; loại/chiều hợp lệ | REFERENCE_UNRESOLVED hoặc ENDPOINT_MISMATCH |
| http-binding / 1-draft | Fact HTTP có URL/method biết được; có binding cấu hình chứng minh host/base URL trỏ unit của B và route B khớp context/path/method | BINDING_MISSING/AMBIGUOUS; không suy chỉ từ path giống nhau |
| event-binding / 1-draft | Topic và broker/context biết được, action phù hợp, provenance chứng minh producer/consumer cùng channel | BROKER_UNKNOWN/TOPIC_MISMATCH; chỉ giữ fact ở hai bên, không nối |
| config-binding / 1-draft | Fact config reference ở A có target resolved thuộc B, cùng key/scope có bằng chứng | CONFIG_BINDING_MISSING |
| CONTRACT-FIELD / 1-draft | Với mỗi FieldValue known của fact route/table/event: (a) mọi `evidence_ids` có trong `fact.evidence`, cùng snapshot; (b) trường literal (`method` so không phân biệt hoa thường, `path` khi lấy thẳng từ một literal, từng giá trị của `status_codes`, `name` của table và column, `topic`) phải xuất hiện nguyên văn trong text của ít nhất một evidence range, đọc qua CMP-002 sau khi kiểm hash. Evidence của trường literal là range hẹp có cột, đúng node cú pháp chứa giá trị, để chữ trong comment hay ở chỗ khác không được tính. Trường ghép từ nhiều nguồn (full path = prefix + path) phải có evidence cho từng phần | Trường đó chuyển `unknown`, reason `VALUE_NOT_IN_EVIDENCE` hoặc `EVIDENCE_MISSING`; fact chuyển `partial` có lý do. Không loại cả fact chỉ vì một trường (CMP-004 r2 §Failure mode) |
| CONTRACT-OWNER / 1-draft | Mỗi fact route/table/event có đúng một mục `contract_owners`; mục có `component_id` thì component đó được accepted, cùng unit, và chứa file của evidence trong `evidence_ids`; evidence đó là `declaration_evidence_id` của fact | Đặt `component_id:null` với reason `OWNER_UNPROVEN`; fact giữ nguyên. Không chọn component khác thay thế |
| LABEL-DIRECT / 1 | exact chỉ khi đọc trực tiếp từ fact đủ; cạnh model hoặc grouping model suy ra phải inferred có lý do | Chuẩn hóa nhãn kèm decision; không dùng sửa nhãn để cứu cạnh thiếu evidence |

Mã `VALUE_NOT_IN_EVIDENCE`, `EVIDENCE_MISSING`, `OWNER_UNPROVEN` đứng đầu chuỗi `reason` của FieldValue hoặc ContractOwner; đây là quy ước chuỗi, không phải enum của schema. Catalog này là tập hỗ trợ ban đầu, không bao phủ mọi động học framework. relation_type không có rule tương ứng bị `RULE_UNSUPPORTED`. Không cho model thêm rule vào catalog. Với HTTP đích nằm ngoài repo có thể là external node nếu URL/service identity xác định được; không giả có component nội bộ nhận. Event edge phải theo đúng cặp loại/chiều ở CMP-005: `publishes` producer→consumer, `consumes` consumer→producer; cùng topic không đủ xác định cặp endpoint.

`VerifiedResult.model` chỉ giữ node/cạnh đã accepted; mỗi đối tượng còn lại có decision accepted tương ứng, không có decision rejected cho cùng đối tượng. Kiểm partition đầy đủ thực hiện trên model đầu vào trước khi lọc; sau lọc không yêu cầu component được công bố bao phủ file thiếu evidence. Phạm vi file thiếu evidence được ghi trong limitation với `affected_ids`, đối chiếu inventory nguồn. Không đưa component không có fact/evidence vào sơ đồ chỉ để giữ số lượng. Fact và FieldValue còn lại phải tham chiếu evidence trong index; decision rejected chỉ là chẩn đoán. Nếu bỏ node/cạnh/fact làm mất một phần kết quả, limitation và completeness của đối tượng chịu ảnh hưởng phải phản ánh việc đó.

Accepted nghĩa là vượt rule tĩnh và kiểm tính nhất quán; không tuyên bố kiến trúc runtime đúng 100%. Độ đúng ý nghĩa vẫn phải đo bằng gold độc lập theo OBS. Cách chia chức năng có thể hợp lệ về membership nhưng chưa hợp lý về trách nhiệm; nhãn inferred và review/gold xử lý phần đó.

## 3. Schema VerifiedResult

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-007-v1.schema.json",
  "$ref":"#/$defs/VerifiedResult",
  "$defs":{
    "VerificationError":{
      "type":"object","additionalProperties":false,"required":["code","message","retryable"],
      "properties":{"code":{"enum":["INPUT_CONTRACT_INVALID","SNAPSHOT_MISMATCH","SNAPSHOT_UNAVAILABLE","RULE_CATALOG_UNAVAILABLE","INTERNAL_INVARIANT"]},"message":{"type":"string","minLength":1},"retryable":{"const":false}}
    },
    "Decision":{
      "type":"object","additionalProperties":false,
      "required":["subject_id","verdict","rule_id","rule_version","fact_ids","evidence_ids","reason"],
      "properties":{
        "subject_id":{"type":"string","minLength":1},"verdict":{"enum":["accepted","rejected"]},
        "rule_id":{"type":"string","minLength":1},"rule_version":{"type":"string","minLength":1},
        "fact_ids":{"type":"array","uniqueItems":true,"items":{"type":"string"}},
        "evidence_ids":{"type":"array","uniqueItems":true,"items":{"type":"string"}},
        "reason":{"type":"string","minLength":1}
      }
    },
    "VerifiedResult":{
      "type":"object","additionalProperties":false,
      "required":["schema_version","snapshot_id","inventory","facts","model","evidence_index","decisions","limitations"],
      "properties":{
        "schema_version":{"const":"0.1.0"},"snapshot_id":{"type":"string","minLength":1},
        "inventory":{"$ref":"API-L3GEN-003-v1.schema.json#/$defs/Inventory"},
        "facts":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/FactSet"},
        "model":{"$ref":"API-L3GEN-005-v1.schema.json#/$defs/ArchitectureModel"},
        "evidence_index":{"type":"array","items":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/EvidenceRef"}},
        "decisions":{"type":"array","items":{"$ref":"#/$defs/Decision"}},
        "limitations":{"type":"array","items":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/Limitation"}}
      }
    }
  }
}
```

Rule catalog version thực tế phải lưu trong decision từng claim; cùng snapshot/model/facts/catalog version cho cùng verdict. `evidence_index` không chứa nội dung raw source. Content khi người dùng mở được đọc qua CMP-002 sau khi kiểm hash/expiry rồi che bí mật. Không tin evidence ID của client ngoài run. Nếu fact/model chưa đủ công bố thì decision và limitation phản ánh đúng, không đánh mọi claim accepted mặc định.

`inventory` giữ nguyên kết quả kiểm kê API-003 đã kiểm cùng snapshot, gồm unit/path/mức hỗ trợ và excluded, để đáp ứng AC-020-01/03 khi xuất hoặc xem lại kết quả. Verifier kiểm file/unit của facts và membership có trong inventory; không xóa unit/file khỏi inventory khi loại một claim. Lỗi parse, thiếu evidence và phần bị loại nằm trong limitations có affected_ids, không suy rằng mọi file trong inventory đã parse thành công. Giữ support/grouping policy version; không tự nhận diện lại root/framework ở đây.

Lỗi terminal được ném dưới dạng exception nội bộ mang payload `VerificationError`; không trộn object lỗi vào `VerifiedResult`. Mất snapshot hoặc catalog chưa đăng ký dừng verification, CMP-001 không publish kết quả chưa kiểm. Claim riêng lẻ không đạt thì dùng decision rejected/limitation thay vì exception toàn run. Catalog có sẵn nhưng không hỗ trợ rule riêng lẻ thì loại claim với `RULE_UNSUPPORTED`. Không tự fallback catalog/version khác.

Khi trả thành công, `model.partition_version` giữ nguyên từ đầu vào, FactSet công bố giữ `extractor_version`. Làm sạch cross-reference tới điểm ổn định: fact đã mất target không còn resolved; field mất tham chiếu chuyển unknown; node/cạnh mất evidence hoặc endpoint bị loại. Duyệt ID theo thứ tự ổn định để quyết định không lệ thuộc thứ tự input. Không gọi provider hoặc ghi source; timeout/cancel của engine hủy toàn lần verify chưa publish. Lưu tối đa một verdict tổng kết trên mỗi subject trong `decisions`; các lỗi bổ sung nằm trong reason/limitation, không giữ hai verdict mâu thuẫn.

## 4. Lỗi và ca kiểm

| Ca | Kết quả mong đợi |
|---|---|
| A gọi ship.example; B có API payment | Không nhận cạnh A→B chỉ vì evidence cả hai có thật |
| Cùng topic, chưa rõ broker | Không nhận cạnh producer/consumer |
| Hai fact reference rõ target, model đề xuất đảo chiều | ENDPOINT_MISMATCH |
| File có thật nhưng hash thuộc snapshot khác | SNAPSHOT_MISMATCH; không phục vụ source mới |
| Node bị loại nhưng cạnh còn tham chiếu | Loại cạnh/ghi limitation, không output mồ côi |
| Model gắn exact cho kết luận suy ra có evidence đủ | Chuyển inferred + lý do, không giấu provenance |
| Mọi claim bị loại | Mô hình rỗng kèm giới hạn; run `partial` nếu publish được |
| Table `name` known là `items` nhưng evidence range không chứa `items` | Trường `name` chuyển unknown, reason `VALUE_NOT_IN_EVIDENCE`; table partial |
| Owner trỏ component không chứa file khai báo | `component_id:null`, reason `OWNER_UNPROVEN`; CMP-008 báo `CONTRACT_OWNER_UNRESOLVED` |

AC-022-02, AC-023-01 đến 04, AC-024-04, AC-027-01 đến 03. Kiểm shape và `$ref` của schema là kiểm tài liệu; các ca ngữ nghĩa này là điều kiện phải hiện thực và test sau, chưa có evidence chạy analyzer.
