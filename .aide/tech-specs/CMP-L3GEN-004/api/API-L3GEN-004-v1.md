---
uid: "01M3B99N5SJMEVRESN5G0FYYXB"
key: API-L3GEN-004-v1
type: api-contract
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-004"],"satisfies":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-SEC-002"]}
verified_at: null
verified_against: []
classification: internal
ai_assisted: true
---

# Contract dữ kiện tĩnh và bằng chứng

Draft theo CMP-L3GEN-004 r2 ở nhánh `docs/gate-2` commit `5d06f14`, gồm mục "Dữ kiện phục vụ tài liệu L3"; consumer CMP-005/006/007 và CMP-008 qua VerifiedResult. Owner duy nhất của Fact là bộ trích xuất, không phải LLM. Không import hoặc chạy source để lấy schema runtime.

**Revision 5 (02/10/2026, nháp, chờ Architecture Gate BL-r10):** thêm phần của FR-L3GEN-029: route khai không qua decorator và route trong file test (AC-L3GEN-029-05), response `list[Model]` (AC-L3GEN-029-02), lời gọi HTTP qua client và `aiohttp` (AC-L3GEN-029-08). `satisfies` đổi sang FR-L3GEN-028 đến 031 vì FR-019 đến 027 đã superseded. Phần còn lại giữ như r4, chưa đối chiếu với CMP-L3GEN-004 r3 và FR-028, 030, 031.

## 1. Giao diện

Revision 6 (02/10/2026, nháp, chờ Architecture Gate BL-r10): bổ sung `call_text` cho README HTTP. Giữ nguyên văn từ snapshot khi an toàn; lời gọi có đối số credential hoặc header được ghi redacted kèm lý do. Không gửi source ra mạng.

`extract(snapshot, inventory, extractor_version) -> FactSet`.

Một file được trích toàn bộ hoặc bỏ toàn bộ cùng limitation; resolve xuyên file sau bước trích. Không coi không trích được là không có thực thể. Không ném toàn FactSet đi chỉ vì một file parse lỗi. Input version không hỗ trợ hoặc snapshot không khớp thì lỗi terminal `INPUT_CONTRACT_INVALID`/`SNAPSHOT_MISMATCH`.

`EvidenceRef` thuộc snapshot bất biến, path POSIX tương đối, hash bytes file gốc. Range theo API-L3GEN-002-v1. Cùng evidence ID phải luôn ánh xạ cùng tuple snapshot/file/hash/range. Một declaration có thể được nhiều fact tham chiếu.

ID fact trong draft: `fact:` + SHA256 của JSON array canonical `[snapshot_id,path,kind,start_line,start_column,end_line,end_column,semantic_key]`. `semantic_key` là symbol/registration context hoặc index cú pháp ổn định khi cùng AST sinh nhiều fact; không dùng tên do model đặt hoặc thứ tự chạy. Evidence ID tương tự với prefix `ev:` và bỏ kind/semantic_key. Cấm trùng ID có payload khác; phải báo `IDENTITY_COLLISION`, không ghi đè. CMP-004 r2 chỉ yêu cầu cùng snapshot và cùng phiên bản bộ nhận diện thì cùng mã định danh; cách tính ID ở đây (D-04) là chi tiết L3. ID ổn định trong cùng snapshot; không cam kết giữ ID khi source thay đổi.

## 2. Kiểu dữ liệu và ý nghĩa

`FieldValue` tách trạng thái với giá trị. known có value và evidence_ids; unknown/not_applicable/redacted có reason và không có value. Redacted không giữ secret dưới trường khác. `unknown` là chưa xác định; `not_applicable` chỉ khi có cơ sở trường không áp dụng. Empty array là đã biết danh sách rỗng, không thay cho unknown.

`resolution` áp cho quan hệ: resolved phải có target_fact_ids tồn tại, unresolved có mảng rỗng và resolution_reason; ambiguity/runtime-dependent nằm trong lý do, không chọn một đích ngẫu nhiên. not_applicable cho declaration. Confidence exact/inferred và completeness full/partial độc lập; inferred/partial bắt buộc có lý do. Known không có nghĩa runtime đã xác nhận.

Mỗi kind bắt buộc đủ các tên thuộc tính sau, kể cả khi giá trị là unknown. Kiểu dưới đây là kiểu của `FieldValue.value` khi state=known; thực thi bằng semantic validator sau JSON Schema, không được bỏ qua.

| kind | Thuộc tính bắt buộc và kiểu known |
|---|---|
| route | method: string uppercase HTTP; path: string bắt đầu `/`; handler: string FQN; registration_context: string; request_model_ids/response_model_ids: array ID; status_codes: array integer 100–599; parameters: array Parameter; auth: array string |
| request_model, response_model | name: string; fields: array ModelField |
| table | name: string; dialect: string; columns: array Column |
| http_call | method: string, unknown khi không đọc được; url: string URL nguyên văn, bỏ query, unknown kèm lý do khi không phải literal; target_unit_id: string ID khi xác định được; library: `httpx`, `requests` hoặc `aiohttp`; call_text: nguyên văn biểu thức gọi, redacted kèm lý do nếu chứa credential/header; url_config_key: khóa cấu hình khi xác định được |
| config | key: string; source_kind: string; value: JSON đã che bí mật |
| event | action: publish hoặc consume; broker: string định danh đã che; topic: string; payload: JSON Schema hoặc unknown |
| library | name: string; version: string; manifest: relative path; used: boolean hoặc unknown |
| symbol | name: string FQN; local_name: string tên trong file (`Cls.method`, `outer.inner`, `__module__`); symbol_kind: function/class/module/variable; signature: string, unknown hoặc not_applicable |
| reference | reference_kind: calls (lời gọi), depends (`Depends(...)` của FastAPI), reads (nhắc tới class bảng mà không gọi), import, inherits; source_symbol: string; target_symbol: string hoặc unknown; call_text: chữ của biểu thức gọi (`ast.unparse`) |

ModelField = `{name, type, required, nullable}`; mỗi mục là FieldValue, type.value là JSON Schema object. Column = `{name,type,primary_key,foreign_key,nullable}` theo CMP-004 r2 và AC-027-02; mỗi mục FieldValue, foreign_key.value = `{table,column}`, type.value là tên kiểu SQL của dialect đã biết. Parameter = `{name,in,required,schema}` với từng mục FieldValue; in.value ∈ path/query/header/cookie. Required, nullable, primary_key, used known phải boolean. Không coi thiếu nullable là false; status code mặc định chỉ dùng khi adapter rule chứng minh và ghi rule provenance, không bịa từ phỏng đoán.

Route identity chứa registration_context để hai app cùng method/path không bị gộp. `registration_context` là chuỗi `file::biến` từ application xuống router, nối bằng `->`; biến cục bộ của app factory ghi `file::hàm.biến`. Route có thêm `condition` (string hoặc not_applicable): điều kiện của các lệnh `if` bao quanh lần đăng ký. Router không được gắn vào application nào thì không sinh route; limitation `ROUTER_NOT_MOUNTED` giữ lại handler. File test theo FR-L3GEN-028 "Phạm vi phân tích" (thư mục `tests/`, `test/`; file `test_*.py`, `*_test.py`, `conftest.py`) không sinh route; application và router khai trong file test cũng không tạo đường gắn. Lời gọi `add_api_route`, `add_api_websocket_route`, `add_route`, `add_websocket_route` không sinh route; mỗi lời gọi một limitation `ROUTE_NOT_DECORATOR` ghi `file:dòng` (AC-L3GEN-029-05). Fact route partial có thể biết hậu tố nhưng chưa biết prefix: path để unknown, thêm optional `path_suffix` known và limitation; không dùng suffix như full path. Loại relation ở architecture không thay identity route.

Route có thêm `bodies` (khi có body): mảng `{direction: request|response, model_id, status: integer|null, media_type, required: boolean|null}`. Mỗi phần tử gắn một model fact với status và media type, để CMP-008 dựng `content` của OpenAPI mà không phải gán mọi model cho mọi status. `required` chỉ có giá trị ở body request: `true` khi tham số không có giá trị mặc định (quy tắc `fastapi-defaults-v1`), `false` khi có; body response ghi `null`. Body response có `array: true` khi response là `list[Model]` (cũng `List`, `Sequence`, `set`); không có trường này là một object. Table có thêm `name_rule` khi tên bảng lấy theo quy tắc framework.

Giá trị lấy theo mặc định của framework chỉ được dùng khi adapter nêu tên quy tắc. Fact đó mang `confidence: inferred`, `confidence_reason` ghi tên quy tắc. Các quy tắc của adapter `slice-ast-v3`:

| Quy tắc | Nội dung |
|---|---|
| `fastapi-defaults-v1` | Body là Pydantic model dùng media type `application/json`; không khai `response_model` thì kiểu trả về của handler là response model |
| `fastapi-status-default-v1` | Decorator không có `status_code` thì status là `[200]`. Route ghi `status_rule` known; verifier chỉ giữ khi decorator không có `status_code` (thêm 02/10/2026) |
| `starlette-status-constant-v1` | `status_code=status.HTTP_201_CREATED` (hằng của `fastapi.status`/`starlette.status`) thì status là số trong tên hằng. Route ghi `status_rule` known; verifier kiểm evidence có `HTTP_<mã>_` (thêm 02/10/2026) |
| `settings-default-v1` | Prefix `settings.X`, với `settings = Settings()` hoặc `settings = get_settings()` (hàm có kiểu trả về là class Settings), ở mức module hoặc trong hàm, và `Settings` kế thừa `BaseSettings` có field `X` mặc định là chuỗi literal, lấy giá trị mặc định đó. Không dùng khi một class con trong repo khai field `X` khác giá trị. Evidence của phần prefix là literal ở dòng khai field; route ghi `prefix_rule` known. Biến môi trường có thể ghi đè lúc chạy nên luôn inferred (thêm 02/10/2026) |
| `sqlalchemy-defaults-v1` | Không khai `primary_key` thì là False; không khai `nullable` thì là `not primary_key`, riêng `Mapped[...]` và SQLModel theo `Optional` |
| `sqlalchemy-type-v1` | Kiểu SQLAlchemy/Python → token SQL, chỉ khi dialect đã được chứng minh qua `Base.metadata.create_all(engine)` |
| `sqlmodel-default-tablename-v1` | Class SQLModel `table=True` không khai `__tablename__` thì tên bảng là tên class viết thường (golden D14) |

Lời gọi HTTP: hàm của module (`httpx.get`, `requests.post`, `aiohttp.request`) và method của client (`httpx.Client`, `httpx.AsyncClient`, `requests.Session`, `aiohttp.ClientSession`). Client được nhận khi biến được gán từ hàm tạo client trong khối `with`, trong cùng hàm, ở mức module, hoặc `self.x` trong cùng class, hay khi tham số có chú thích kiểu là client; không nhận theo tên biến. Method `request` lấy method từ đối số đầu nếu là literal. URL lấy thẳng từ cấu hình (`settings.X` với `settings` là instance của lớp `BaseSettings`, `os.getenv("X")`, `os.environ["X"]`) thì thêm `url_config_key` known là `X`. Không lấy lời gọi trong file test. Thư viện HTTP khác (`urllib.request`, `http.client`, `urllib3`, `httpcore`, `pycurl`, `treq`, `niquests`, `grequests`, `tornado.httpclient`) ghi limitation `HTTP_LIBRARY_UNSUPPORTED` kèm nơi import (AC-L3GEN-029-08).

Tên bảng do một hàm trong repo tính lúc import (ví dụ `declared_attr`) vẫn là unknown, vì adapter không chạy code.

Các thuộc tính bổ sung phục vụ binding/ownership dưới đây cũng là `FieldValue`. Adapter chưa trích được phải ghi unknown và lý do khi tính năng sử dụng thuộc tính đó; consumer không suy từ tên hoặc tự điền. Thiếu thuộc tính trong payload được xử lý như không đủ ngữ cảnh, không như giá trị rỗng đã biết.

| Phạm vi | Thuộc tính / kiểu known | Consumer |
|---|---|---|
| route | `handler_fact_id`: ID symbol fact; `application_id`: ID ứng dụng phân biệt các registration trong cùng unit | CMP-008 hiển thị handler; tách dòng theo application, không gộp hai application cùng method/path |
| route, table, event | `declaration_evidence_id`: ID evidence của nơi khai báo route (decorator hoặc lời gọi đăng ký), khai báo bảng, hoặc call site publish/consume | CMP-005 chọn owner theo API-005 §3.2; không lấy tùy ý evidence đầu tiên |
| http_call | `target_application_id`: ID khớp route.application_id; `binding_fact_ids`: các fact config/reference chứng minh target_unit_id/base URL | Rule http-binding; method/path giống nhau chưa đủ |
| event | `namespace`: namespace/config context đã phân giải, hoặc not_applicable khi broker không có khái niệm này (Kafka); `serialization_context`: định dạng giao tiếp có bằng chứng | Rule event-binding, cùng với broker và topic; không coi hai unknown là bằng nhau |
| config | `scope_id`: phạm vi cấu hình đã nhận diện; `binding_fact_ids`: các fact chứng minh reference/đích, kết hợp target_fact_ids khi resolution=resolved | Rule config-binding |
| table | `database_identity`, `schema_name`: string nhận diện DB/schema đã che bí mật | Chỉ gộp table khi đủ identity; không gộp theo name đơn lẻ |

`handler_fact_id`, `binding_fact_ids`, `target_fact_ids` phải giải về fact còn hợp lệ trong cùng snapshot; `declaration_evidence_id` phải có trong evidence của fact. Application ID chỉ là registration identity tĩnh do extractor cấp ổn định, không tự chứng minh app triển khai độc lập. Các trường này là lựa chọn contract draft phục vụ D-01/D-10, cần review adapter trước khi cam kết hỗ trợ rule tương ứng.

## 3. JSON Schema

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-004-v1.schema.json",
  "$ref":"#/$defs/FactSet",
  "$defs":{
    "ExtractionError":{
      "type":"object","additionalProperties":false,"required":["code","message","retryable"],
      "properties":{"code":{"enum":["INPUT_CONTRACT_INVALID","SNAPSHOT_MISMATCH","SNAPSHOT_UNAVAILABLE","EXTRACTOR_VERSION_UNAVAILABLE","IDENTITY_COLLISION","INTERNAL_INVARIANT"]},"message":{"type":"string","minLength":1},"retryable":{"const":false}}
    },
    "EvidenceRef":{
      "type":"object","additionalProperties":false,
      "required":["id","snapshot_id","file_id","path","sha256","start_line","end_line","start_column","end_column"],
      "properties":{
        "id":{"type":"string","minLength":1},"snapshot_id":{"type":"string","minLength":1},"file_id":{"type":"string","minLength":1},
        "path":{"type":"string","minLength":1},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$"},
        "start_line":{"type":"integer","minimum":1},"end_line":{"type":"integer","minimum":1},
        "start_column":{"type":["integer","null"],"minimum":0},"end_column":{"type":["integer","null"],"minimum":0}
      },
      "oneOf":[{"properties":{"start_column":{"type":"integer"},"end_column":{"type":"integer"}}},{"properties":{"start_column":{"type":"null"},"end_column":{"type":"null"}}}]
    },
    "Limitation":{
      "type":"object","additionalProperties":false,"required":["code","message","stage","affected_ids"],
      "properties":{"code":{"type":"string","minLength":1},"message":{"type":"string","minLength":1},"stage":{"type":"string","minLength":1},"affected_ids":{"type":"array","items":{"type":"string"},"uniqueItems":true}}
    },
    "FieldValue":{
      "oneOf":[
        {"type":"object","additionalProperties":false,"required":["state","value","evidence_ids"],"properties":{"state":{"const":"known"},"value":{},"evidence_ids":{"type":"array","minItems":1,"uniqueItems":true,"items":{"type":"string","minLength":1}}}},
        {"type":"object","additionalProperties":false,"required":["state","reason"],"properties":{"state":{"enum":["unknown","not_applicable","redacted"]},"reason":{"type":"string","minLength":1}}}
      ]
    },
    "Fact":{
      "type":"object","additionalProperties":false,
      "required":["id","unit_id","kind","attributes","evidence","resolution","target_fact_ids","confidence","completeness"],
      "properties":{
        "id":{"type":"string","minLength":1},"unit_id":{"type":"string","minLength":1},
        "kind":{"enum":["route","request_model","response_model","table","http_call","config","event","library","reference","symbol"]},
        "attributes":{"type":"object","minProperties":1,"additionalProperties":{"$ref":"#/$defs/FieldValue"}},
        "evidence":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/EvidenceRef"}},
        "resolution":{"enum":["resolved","unresolved","not_applicable"]},
        "target_fact_ids":{"type":"array","uniqueItems":true,"items":{"type":"string","minLength":1}},
        "resolution_reason":{"type":"string","minLength":1},
        "confidence":{"enum":["exact","inferred"]},"confidence_reason":{"type":"string","minLength":1},
        "completeness":{"enum":["full","partial"]},"completeness_reason":{"type":"string","minLength":1}
      },
      "allOf":[
        {"if":{"properties":{"confidence":{"const":"inferred"}}},"then":{"required":["confidence_reason"]}},
        {"if":{"properties":{"completeness":{"const":"partial"}}},"then":{"required":["completeness_reason"]}},
        {"if":{"properties":{"resolution":{"const":"resolved"}}},"then":{"properties":{"target_fact_ids":{"minItems":1}}},"else":{"properties":{"target_fact_ids":{"maxItems":0}}}},
        {"if":{"properties":{"resolution":{"const":"unresolved"}}},"then":{"required":["resolution_reason"]}}
      ]
    },
    "FactSet":{
      "type":"object","additionalProperties":false,
      "required":["schema_version","snapshot_id","extractor_version","facts","limitations"],
      "properties":{
        "schema_version":{"const":"0.1.0"},"snapshot_id":{"type":"string","minLength":1},
        "extractor_version":{"type":"string","minLength":1},
        "facts":{"type":"array","items":{"$ref":"#/$defs/Fact"}},
        "limitations":{"type":"array","items":{"$ref":"#/$defs/Limitation"}}
      }
    }
  }
}
```

Known.value bất kỳ ở schema khung là để hỗ trợ các kind; kiểm bảng kiểu mục 2 là bắt buộc trước khi publish. Không dùng một lần JSON Schema pass để tuyên bố FactSet đúng ngữ nghĩa. Snapshot/file/hash/range, ID, crossref, evidence_ids ở mọi FieldValue lồng nhau cần được đối chiếu.

`extractor_version` bắt buộc lưu cả khi FactSet rỗng hoặc là projection gửi model. Phiên bản đại diện parser/adapter/rule bundle đã pin; consumer không được tự thay khi copy hoặc lọc facts. Khi loại fact làm hỏng một reference, CMP-007 tạo bản công bố mới với `resolution:unresolved`, `target_fact_ids:[]`, lý do và completeness partial; các FieldValue tham chiếu fact bị loại chuyển unknown có lý do. FactSet gốc bất biến vẫn ở engine phục vụ chẩn đoán trong vòng đời run, không được renderer dùng thay bản đã kiểm.

Kiểm typed attributes phải duyệt cả object/array lồng nhau: known ID trong request/response model, handler và binding phải trỏ đúng kind/cùng snapshot; evidence cho thuộc tính thuộc index cùng run; tên field trùng trong một model/table và parameter trùng `(in,name)` phải được phát hiện. Không đánh giá registry/framework mới chỉ bằng việc payload qua schema.

Lỗi terminal ném exception nội bộ mang payload `ExtractionError`; CMP-001 quyết định run outcome, không xuất FactSet chưa kiểm. Version extractor không khả dụng không tự đổi sang version khác. Parse/encoding lỗi riêng file đi vào limitations và giữ dữ kiện file khác; không biến mọi lỗi file thành exception toàn run.

## 4. Ví dụ và kiểm chứng

Ví dụ giá trị partial: `{"state":"unknown","reason":"Prefix lấy từ biến môi trường tại runtime"}`. Ví dụ secret: `{"state":"redacted","reason":"Giá trị có dấu hiệu credential"}`. Cả hai không được renderer biến thành empty string hoặc `null` trong mô tả như thể đã biết giá trị.

| Ca | Kết quả mong đợi |
|---|---|
| `foo(); bar()` trên một dòng | Hai fact ID khác nhau, range không trùng nhầm |
| Route `/v1` + `/orders` ở cùng registration | Full path `/v1/orders`, evidence gồm khai báo và registration |
| Prefix động | Path unknown/partial; suffix có thể giữ riêng; không chấm như đã resolve full path. Ngoại lệ: field settings có mặc định literal theo `settings-default-v1` (inferred) |
| Hai app cùng GET `/orders` | Hai route fact với registration_context khác nhau |
| Table name tạo lúc chạy | unknown; không suy từ tên class |
| Import alias có nhiều đích khả dĩ | unresolved, không tạo architecture edge |
| File parse lỗi giữa unit có file tốt | Giữ file tốt, limitation chỉ rõ file lỗi |

AC-021-01 đến 05, AC-023-01/02, AC-024-01/03/04. Ví dụ kiểm ở bộ L3 chỉ xác minh contract, không phải gold độc lập của analyzer.
