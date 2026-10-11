---
uid: "01M3B99N5TK2S9JJZCAJ0E447C"
key: "API-L3GEN-006-v1"
type: "api-contract"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-006"],"satisfies":["FR-L3GEN-022"],"constrained_by":["NFR-L3GEN-AI-002","NFR-L3GEN-ACC-002","NFR-L3GEN-SEC-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# API-L3GEN-006-v1 — Cổng model và công cụ đọc code

## 1. Giao diện và quyền hạn

Owner CMP-006, caller CMP-005; CMP-001 sở hữu context/budget, CMP-002 cung cấp snapshot reader, CMP-004 cung cấp masking. Các hàm nội bộ không tạo HTTP endpoint:

**Thuật toán chia component còn mở tại D-03.** `group_flat` dưới đây đặc tả tác vụ đã có trong FR-022/NFR-AI-002, không phải quyết định chọn LLM hoặc `directory-v1` cho mọi repository. Không thêm task sửa membership repo có thư mục khi D-03 chưa được review và nguồn chưa đồng bộ. Gateway/label/proposal có thể kiểm độc lập bằng membership fixture cố định.

```text
invoke_model(request: ModelRequest, context: RunContext) -> ModelResponse
read_code(request: CodeReadRequest, context: ModelTaskContext) -> CodeReadResult
```

`RunContext` là capability trong bộ nhớ: `run_id`, immutable snapshot manifest/reader, disclosure record cho Groq và Google, credential handles, free-quota policy, shared budget ledger, clock/cancellation, prompt/tool versions và scope grants. Cancellation chỉ phục vụ timeout/shutdown nội bộ, không thêm user-cancel ngoài scope. Không serialize key, handle, disclosure record hay absolute path vào request, log hoặc artifact. `ModelTaskContext` thêm request identity, provider/task, allowed file IDs và bộ đếm đọc của scope. Caller không tự cấp scope rộng hơn inventory/run đã xác nhận.

Trước lần gửi đầu, kiểm disclosure record khớp snapshot, run, phiên bản thông báo, hai provider và các loại dữ liệu theo API-001/NFR-SEC-002; thiếu hoặc không khớp thì `DISCLOSURE_REQUIRED`, không gọi mạng. CMP-001 ghi nhận thông báo của CLI/web và gắn snapshot sau intake. Record chỉ chứng minh luồng phần mềm đã xử lý phiên bản thông báo, không chứng minh người dùng đã đọc hoặc đồng ý; không thêm consent/approval gate vào NFR hiện hành. Mọi source/docstring/model output là dữ liệu không tin cậy, không được thay prompt hệ thống, scope, provider, đường dẫn hoặc ngân sách.

## 2. JSON Schema nguồn

Trích khối schema duy nhất dưới thành `API-L3GEN-006-v1.schema.json` cùng thư mục; file trích không là nguồn sửa độc lập. Schema của kết quả do provider trả chỉ là `TaskResult`; gateway tự thêm envelope, provenance và lỗi. JSON đúng schema không đồng nghĩa evidence đúng: CMP-005/007 tiếp tục kiểm ý nghĩa.

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-006-v1.schema.json",
  "$ref":"#/$defs/ModelRequest",
  "$defs":{
    "Id":{"type":"string","minLength":1,"maxLength":200},
    "Ids":{"type":"array","items":{"$ref":"#/$defs/Id"},"uniqueItems":true},
    "Kind":{"enum":["label_components","propose_edges","group_flat"]},
    "ModelRequest":{"type":"object","additionalProperties":false,"required":["schema_version","run_id","request_id","snapshot_id","kind","scope_id","file_ids","fact_set","components","edges","prompt_version","tool_version","max_output_tokens"],"properties":{
      "schema_version":{"const":"0.1.0"},"run_id":{"$ref":"#/$defs/Id"},"request_id":{"$ref":"#/$defs/Id"},"snapshot_id":{"$ref":"#/$defs/Id"},
      "kind":{"$ref":"#/$defs/Kind"},"scope_id":{"$ref":"#/$defs/Id"},"file_ids":{"$ref":"#/$defs/Ids"},
      "fact_set":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/FactSet"},
      "components":{"type":"array","items":{"$ref":"API-L3GEN-005-v1.schema.json#/$defs/Component"}},
      "edges":{"type":"array","items":{"$ref":"API-L3GEN-005-v1.schema.json#/$defs/Edge"}},
      "flat_units":{"type":"array","minItems":1,"items":{"$ref":"API-L3GEN-005-v1.schema.json#/$defs/Unit"}},
      "prompt_version":{"$ref":"#/$defs/Id"},"tool_version":{"$ref":"#/$defs/Id"},"max_output_tokens":{"type":"integer","minimum":1,"maximum":50000}
    },"allOf":[{"if":{"properties":{"kind":{"const":"group_flat"}}},"then":{"required":["flat_units"],"properties":{"components":{"maxItems":0},"edges":{"maxItems":0}}},"else":{"not":{"required":["flat_units"]}}}]},
    "ComponentLabel":{"type":"object","additionalProperties":false,"required":["component_id","name","description","role","fact_ids"],"properties":{
      "component_id":{"$ref":"#/$defs/Id"},"name":{"type":"string","minLength":1,"maxLength":200},
      "description":{"type":"string","minLength":1,"maxLength":2000},"role":{"type":"string","minLength":1,"maxLength":200},
      "fact_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1}
    }},
    "EdgeLabel":{"type":"object","additionalProperties":false,"required":["edge_id","label","fact_ids"],"properties":{
      "edge_id":{"$ref":"#/$defs/Id"},"label":{"type":"string","minLength":1,"maxLength":200},"fact_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1}
    }},
    "LabelResult":{"type":"object","additionalProperties":false,"required":["kind","component_labels","edge_labels"],"properties":{
      "kind":{"const":"label_components"},"component_labels":{"type":"array","items":{"$ref":"#/$defs/ComponentLabel"}},"edge_labels":{"type":"array","items":{"$ref":"#/$defs/EdgeLabel"}}
    }},
    "EdgeProposal":{"type":"object","additionalProperties":false,"required":["proposal_id","source_component_id","target_component_id","relation_type","fact_ids","reason"],"properties":{
      "proposal_id":{"$ref":"#/$defs/Id"},"source_component_id":{"$ref":"#/$defs/Id"},"target_component_id":{"$ref":"#/$defs/Id"},
      "relation_type":{"$ref":"API-L3GEN-005-v1.schema.json#/$defs/RelationType"},"fact_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":2},
      "reason":{"type":"string","minLength":1,"maxLength":2000}
    }},
    "EdgeResult":{"type":"object","additionalProperties":false,"required":["kind","proposals"],"properties":{
      "kind":{"const":"propose_edges"},"proposals":{"type":"array","items":{"$ref":"#/$defs/EdgeProposal"}}
    }},
    "GroupProposal":{"type":"object","additionalProperties":false,"required":["proposal_id","unit_id","file_ids","reason"],"properties":{
      "proposal_id":{"$ref":"#/$defs/Id"},"unit_id":{"$ref":"#/$defs/Id"},"file_ids":{"allOf":[{"$ref":"#/$defs/Ids"}],"minItems":1},
      "reason":{"type":"string","minLength":1,"maxLength":1000}
    }},
    "GroupResult":{"type":"object","additionalProperties":false,"required":["kind","groups"],"properties":{
      "kind":{"const":"group_flat"},"groups":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/GroupProposal"}}
    }},
    "TaskResult":{"oneOf":[{"$ref":"#/$defs/LabelResult"},{"$ref":"#/$defs/EdgeResult"},{"$ref":"#/$defs/GroupResult"}]},
    "Provenance":{"type":"object","additionalProperties":false,"required":["request_id","provider","model","prompt_version","tool_version","snapshot_id","physical_requests","input_tokens","output_tokens","usage_source"],"properties":{
      "request_id":{"$ref":"#/$defs/Id"},"provider":{"enum":["groq","google"]},"model":{"enum":["openai/gpt-oss-120b","gemini-3.5-flash"]},
      "prompt_version":{"$ref":"#/$defs/Id"},"tool_version":{"$ref":"#/$defs/Id"},"snapshot_id":{"$ref":"#/$defs/Id"},
      "physical_requests":{"type":"integer","minimum":0},"input_tokens":{"type":"integer","minimum":0},"output_tokens":{"type":"integer","minimum":0},
      "usage_source":{"enum":["provider","reserved_upper_bound"]}
    }},
    "GatewayError":{"type":"object","additionalProperties":false,"required":["code","message","retryable","scope"],"properties":{
      "code":{"enum":["INVALID_INPUT","DISCLOSURE_REQUIRED","MISSING_KEY","PAID_ROUTE_DISABLED","CAPABILITY_UNVERIFIED","MASKING_FAILED","WHOLE_FILE_DISCLOSURE","INPUT_TOO_LARGE","TOKEN_ESTIMATE_UNAVAILABLE","RUN_BUDGET_EXHAUSTED","RATE_LIMITED","QUOTA_EXHAUSTED","TIMEOUT","NETWORK_ERROR","PROVIDER_ERROR","SCHEMA_INVALID","WRONG_TASK","CANCELLED"]},
      "message":{"type":"string","minLength":1,"maxLength":1000},"retryable":{"const":false},"scope":{"enum":["task","run"]}
    }},
    "ModelResponse":{"type":"object","additionalProperties":false,"required":["schema_version","request_id","snapshot_id","kind","status","result","error","provenance"],"properties":{
      "schema_version":{"const":"0.1.0"},"request_id":{"$ref":"#/$defs/Id"},"snapshot_id":{"$ref":"#/$defs/Id"},"kind":{"$ref":"#/$defs/Kind"},"status":{"enum":["ok","error"]},
      "result":{"oneOf":[{"$ref":"#/$defs/TaskResult"},{"type":"null"}]},"error":{"oneOf":[{"$ref":"#/$defs/GatewayError"},{"type":"null"}]},
      "provenance":{"type":"array","items":{"$ref":"#/$defs/Provenance"}}
    },"allOf":[{"if":{"properties":{"status":{"const":"ok"}}},"then":{"properties":{"result":{"$ref":"#/$defs/TaskResult"},"error":{"type":"null"},"provenance":{"minItems":1}}},"else":{"properties":{"result":{"type":"null"},"error":{"$ref":"#/$defs/GatewayError"}}}}]},
    "CodeReadRequest":{"type":"object","additionalProperties":false,"required":["request_id","snapshot_id","scope_id","file_id","start_line","line_count"],"properties":{
      "request_id":{"$ref":"#/$defs/Id"},"snapshot_id":{"$ref":"#/$defs/Id"},"scope_id":{"$ref":"#/$defs/Id"},"file_id":{"$ref":"#/$defs/Id"},
      "start_line":{"type":"integer","minimum":1},"line_count":{"type":"integer","minimum":1,"maximum":60}
    }},
    "CodeReadResult":{"type":"object","additionalProperties":false,"required":["status","text","evidence","error_code"],"properties":{
      "status":{"enum":["ok","denied"]},"text":{"type":["string","null"],"maxLength":65536},
      "evidence":{"oneOf":[{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/EvidenceRef"},{"type":"null"}]},
      "error_code":{"enum":[null,"WRONG_TASK","OUTSIDE_SCOPE","WRONG_SNAPSHOT","UNKNOWN_FILE","READ_LIMIT","INVALID_RANGE","WHOLE_FILE_DISCLOSURE","SNAPSHOT_UNAVAILABLE","MASKING_FAILED","SNIPPET_TOO_LARGE"]}
    },"allOf":[{"if":{"properties":{"status":{"const":"ok"}}},"then":{"properties":{"text":{"type":"string"},"evidence":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/EvidenceRef"},"error_code":{"type":"null"}}},"else":{"properties":{"text":{"type":"null"},"evidence":{"type":"null"},"error_code":{"type":"string"}}}}]}
  }
}
```

## 3. Từng tác vụ và invariant ngoài schema

| Kind | Provider/model từ NFR-AI-002 | Input và output được phép |
|---|---|---|
| `label_components` | Groq `openai/gpt-oss-120b`, reasoning effort medium | Một scope component đã chia, facts/chữ ký và cạnh liên quan; output chỉ tên/mô tả/vai trò/nhãn cho ID có sẵn. Có công cụ đọc code. |
| `propose_edges` | Google `gemini-3.5-flash` | Toàn bộ component và FactSet của repository trong một task; output đề xuất cạnh có ID fact đã có. Không công cụ, không source bổ sung. |
| `group_flat` | Google `gemini-3.5-flash` | Toàn bộ flat units, file IDs và facts trong một task/run, chỉ khi có unit flat; output partition theo unit. Không công cụ. |

Tên model và quota ở đây phản ánh nguồn dự án, **không phải xác minh availability hoặc capability hiện tại**. Không tự thay tên model, gọi provider thật hoặc phát sinh chi phí để viết/kiểm contract. Adapter thực tế phải kiểm capability trên cấu hình miễn phí ở M1; chưa xác nhận tool/JSON thì task trả `CAPABILITY_UNVERIFIED`. Groq theo CMP-006 dùng hai pha: tool-capable conversation rồi request JSON strict tách biệt không có tools. Cả hai pha và mọi continuation đều tính ngân sách.

`request_id` duy nhất trong run; gateway từ chối ID trùng đang chạy. Cache in-memory kết quả hoàn tất theo `(run_id,request_id,payload_digest)`; cùng ID/digest trả kết quả cũ không gọi lại, digest khác trả `INVALID_INPUT`. Không hứa provider idempotency sau crash. `scope_id` của label task là `component:<component_id>`; group/proposal là `repository:<snapshot_id>`. Scope đọc giữ nguyên dù model đổi tên component hay gateway retry.

Trước serialize, kiểm snapshot trong envelope/FactSet/component provenance, tất cả file/fact/component/edge IDs trong grant. FactSet cho label là projection các fact thuộc member file và target facts của cạnh đã có; giới hạn này được lập trước task, không lặng lẽ cắt theo token. Với proposal/group, gửi trọn tập đã quy định hoặc trả `INPUT_TOO_LARGE`. Runtime bỏ provenance/limitations không cần cho task khỏi prompt theo prompt version nhưng không được đổi dữ kiện. Không gửi model gold/test answer.

`response.kind`, `result.kind` phải bằng request.kind; provider/model phải đúng bảng; code tự cấp provenance và không tin token/ID báo bởi model. Unknown ID/file, nhãn trùng cùng target, proposal ID trùng và kết quả ngoài scope bị loại. Provider JSON có `facts`, membership trong label, confidence hoặc rule acceptance tự khai đều sai schema. Group file coverage và evidence binding là kiểm semantic ở API-005. Chuỗi annotation được mask và escape khi render; không diễn giải markdown/link làm quyền đọc file.

## 4. Ngân sách và retry

**Budget — chi tiết L3 của NFR-AI-002 r3 và CMP-006 r2 (nguồn ghi trần, chưa ghi cách đếm):** đếm *request vật lý* là mỗi lần gửi HTTP tới provider, kể cả retry, tool continuation và pha JSON; áp trần 40 cho cả run, tổng Gemini 2 bao gồm hai kind và retry. Token mỗi request là input thực gửi cộng output tối đa đã reserve. 6.000 áp Groq, 50.000 áp Gemini. Các trần này là yêu cầu dự án trong bản draft, không phải xác minh quota hay capability hiện tại của provider; vẫn cần kiểm adapter thực tế.

| Budget | Admission và hiệu ứng |
|---|---|
| Groq/run ≤100.000 token | Sum input+output của mọi lần gửi, kể cả thử lại. Reserve upper bound trước network; thiếu chỗ thì dừng mọi task model còn lại. |
| Groq/request ≤6.000; Gemini/request ≤50.000 | Tính system prompt, schema, facts, history, tool results và `max_output_tokens`; quá trần bỏ riêng task, không cắt facts. |
| Gemini/run ≤2; toàn run ≤40 physical sends | Reserve một request atomically trước mỗi lần gửi. Retry của grouping có thể dùng hết hai slot: edge proposal bị bỏ, không có slot thứ ba. |
| Rate/minute, shared credential | Rolling window theo `(provider,credential_fingerprint)` qua các run trong cùng engine: Groq 30 requests/8.000 tokens; Google 5 requests/250.000 tokens. Chờ đủ cả hai, không giữ lock trong lúc chờ. |
| Quota/ngày | Free account limit do provider quyết định; engine giữ ledger trong phạm vi mình thấy và xử lý lỗi thực tế. Không thể cam kết quota còn lại vì các client khác. Không bật billing/paid route. |
| Timeout/retry | 30 giây mỗi physical request từ lúc gửi; chờ scheduler không tính vào 30 giây. Tối đa hai lần thử lại cho network/timeout/503, backoff 1 rồi 2 giây, vẫn phải qua admission. |

Reserve và increment là một transaction dưới shared lock. Nhận usage đáng tin thì settle theo input/output thực; timeout/usage thiếu giữ cả upper bound (`usage_source:reserved_upper_bound`), không trả slot. Estimator phải có bound phù hợp tokenizer/cấu hình model; không tính được thì `TOKEN_ESTIMATE_UNAVAILABLE`, không gửi. Nếu usage thực vượt bound, ghi limitation, dừng model tasks toàn run và không ghi số ước lượng thành số đo provider. Không hứa chặn chi phí chỉ bằng estimator; credential phải được cấu hình free-only, paid allowance = 0 trước network.

429/quota/missing key/schema/ID lỗi không retry; 503 được xử lý như timeout theo L2. Retry không tự mở thêm scope, làm mới budget, đổi provider hoặc rơi sang model tính tiền. Error trả caller luôn `retryable:false` vì gateway đã xử lý retry cho task; caller muốn run mới phải có luồng run riêng. Khi budget toàn run hết, task chưa gửi trả `RUN_BUDGET_EXHAUSTED`; task đã gửi được settle và có thể trả valid result nhưng không khởi tạo request tiếp. Cancel không trả reservation đã gửi và không publish nửa TaskResult.

## 5. Công cụ đọc code và dữ liệu ra ngoài

Chỉ `label_components` có công cụ. Request dùng `file_id` từ manifest và range, không nhận path tùy ý. Engine lookup file trong snapshot đã đóng, kiểm hash và file regular, không theo symlink/reparse point; từ chối snapshot hết hạn hoặc file thay đổi. Đọc qua CMP-002, không đọc source live trên đĩa, không import/execute code. `start_line` 1-based; `line_count` là số dòng yêu cầu, range vượt EOF bị từ chối, không truncate ngầm. Evidence dùng nguyên quy ước dòng/cột và digest của API-004; nội dung trả là đoạn sau masking, digest vẫn chỉ snapshot gốc.

Mỗi scope có tối đa 6 **lần yêu cầu** đọc trên cả task, retry và pha; lần từ chối cũng tiêu quota để chặn vòng lặp. Mỗi lần ≤60 dòng và ≤65.536 Unicode characters sau masking; quá byte/token envelope vẫn bị admission chặn, không cắt đoạn âm thầm. Đếm trước đọc, dùng cùng ledger khi gọi song song. Scope không do model đổi. Công cụ không sinh fact mới; snippet/evidence mới chỉ là dữ liệu hỗ trợ đặt nhãn, CMP-005 không dùng nó thay fact binding.

**D-07 — chi tiết L3 của NFR-SEC-002 r3 ("không gửi nguyên file"), chờ review:** cấm một lần hoặc hợp các range source gửi trong cùng run/provider bao phủ toàn bộ dòng của một file; giữ union range theo `(run,snapshot,file,provider)` độc lập scope. File một dòng không thể đọc qua công cụ; trả `WHOLE_FILE_DISCLOSURE`, task dùng facts hoặc báo limitation. Tính cả range chữ ký/docstring nguyên văn gửi từ FactSet, không chỉ tool response; đổi scope/task không reset union. Kiểm trước mọi egress, kể cả prompt đầu tiên. Nếu FactSet bắt buộc gửi trọn mà vi phạm, trả `WHOLE_FILE_DISCLOSURE` với limitation, không âm thầm cắt facts. Không mở ngoại lệ “file ngắn”. Chính sách này cụ thể hóa “không gửi nguyên file”; cần kiểm ảnh hưởng thực tế khi triển khai.

Masking CMP-004 chạy trên facts, literal, docstring, metadata, tool text và output trước mọi sink. Lỗi masking fail closed. Giá trị key chỉ dùng trong transport header qua credential handle; redact provider exception/header khỏi log. Log chỉ lưu identity/version/counter/error code, không raw prompt/response/source; provenance đủ provider/model/prompt/tool/snapshot/usage. Không xác nhận thay provider về an toàn dữ liệu của gói họ cung cấp.

## 6. Ví dụ và ca kiểm contract

Ví dụ provider output hợp lệ theo `#/$defs/LabelResult` (fixture có component `cmp_a`, fact `f_route` trong scope). Gateway chấp nhận cấu trúc rồi CMP-005 kiểm reference/annotation; model không có quyền đổi membership.

```json
{"kind":"label_components","component_labels":[{"component_id":"cmp_a","name":"User API","description":"Exposes user routes","role":"HTTP interface","fact_ids":["f_route"]}],"edge_labels":[]}
```

Ví dụ partial ở pipeline do task không gửi được; payload kiểm theo `#/$defs/ModelResponse`. Caller giữ static graph theo API-005.

```json
{"schema_version":"0.1.0","request_id":"req_edges","snapshot_id":"s1","kind":"propose_edges","status":"error","result":null,"error":{"code":"INPUT_TOO_LARGE","message":"Input plus reserved output exceeds the Gemini request limit","retryable":false,"scope":"task"},"provenance":[]}
```

| Ca provider giả / invariant dự kiến | Kết quả mong đợi |
|---|---|
| Thiếu/lệch disclosure record hoặc thiếu key | Không gọi mạng; `DISCLOSURE_REQUIRED` hoặc `MISSING_KEY`, không rò credential. |
| Label payload thêm `member_file_ids` | `SCHEMA_INVALID`, cả task lỗi; không trả nửa labels. |
| JSON đúng shape nhưng `component_id` lạ | Bị loại ở kiểm scope/reference; không tạo component. |
| `group_flat` timeout, retry thành công | Hai Gemini sends; `propose_edges` bị `RUN_BUDGET_EXHAUSTED`, static graph vẫn có. |
| 39 sends, Groq cần tool continuation rồi JSON phase | Send thứ 40 được admission; phase tiếp bị chặn, cả task lỗi; không request 41. |
| Groq 5.500 input + 1.000 reserved output | `INPUT_TOO_LARGE`, zero network dù input riêng dưới 6.000. |
| 429 hoặc free quota hết | Dừng task, không retry/đổi model/paid fallback. |
| Tool đọc file ngoài scope, ID khác snapshot, range vượt EOF | `denied`, text/evidence null; lần đọc vẫn tính quota. |
| 6 lần đọc rồi lần 7; hoặc lần 2 hoàn thành toàn file | `READ_LIMIT` hoặc `WHOLE_FILE_DISCLOSURE`; không mở scope mới để né. |
| Secret sentinel trong literal/docstring/provider exception | Không sentinel ở payload/log/output; nếu mask không thể xác định thì không gửi. |
| Hai run cùng credential đồng thời | Admission dùng cùng rolling window; reserve không đua vượt budget/rate. |
| Provider usage thiếu sau timeout | Giữ upper-bound token reservation; provenance không gọi đó là usage thực. |

Các ca trên là yêu cầu kiểm với fake clock/provider và snapshot fixture, chưa là kết quả test/benchmark hay xác minh provider thật. Breaking change ở task kind, scope/quota semantics, required field hoặc provider allocation cần tăng payload major và review CMP-001/002/004/005/007. Budget, disclosure và khóa đã đồng bộ bản nguồn draft; capability, runtime tests và review consumer vẫn cần thực hiện. Draft này không ký approval.
