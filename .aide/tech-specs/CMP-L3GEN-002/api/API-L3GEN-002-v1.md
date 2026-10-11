---
uid: "01M3B99N5QEATWY88Q3YPJQJEZ"
key: API-L3GEN-002-v1
type: api-contract
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-002"],"satisfies":["FR-L3GEN-019","FR-L3GEN-020"],"depends_on":["API-L3GEN-001-v1","API-L3GEN-006-v1"],"constrained_by":["NFR-L3GEN-SEC-002","NFR-L3GEN-OPS-001","NFR-L3GEN-AI-002"]}
verified_at: null
verified_against: []
classification: internal
ai_assisted: true
---

# Contract snapshot và đọc source

Draft 25/09/2026, sửa 01/10/2026; theo CMP-L3GEN-002 r2 ở nhánh `docs/gate-2` commit `5d06f14` (r2 chỉ đổi metadata so với r1). Đây là giao diện gọi nội bộ, không phải một HTTP service. Quy ước API cho interface nội bộ là draft cục bộ D-00 như ghi ở [mục lục](../../README.md). Source repository là dữ liệu không tin cậy, không được thực thi. Revision 4 viện dẫn lại nguồn trên git (NFR-SEC-002 r3, NFR-AI-002 r3); các quy tắc đơn vị byte, đọc range và vòng đời là chi tiết L3. Không phải bằng chứng triển khai hoặc phê duyệt Contract Gate.

## 1. Owner và giao diện

Owner CMP-002; CMP-001 tạo snapshot; CMP-003/004 đọc phạm vi; CMP-006 đọc snippet qua quyền đã cấp; CMP-007 kiểm hash và evidence.

| Hàm nội bộ | Input | Output |
|---|---|---|
| `create_snapshot(source, run_id, intake_context)` | SourceSpec hợp lệ, mã run và capability deadline/cancellation do CMP-001 cấp | Snapshot hoặc SnapshotError |
| `read_file(snapshot_id, file_id, reader_context)` | ID đã đăng ký, reader capability gắn với run do CMP-001 cấp | FileRead hoặc SnapshotError; không import |
| `read_range(snapshot_id, file_id, range, access_scope, reader_context)` | Range/scope và reader capability gắn với run do engine cấp | RangeRead hoặc SnapshotError |
| `verify_file(snapshot_id, file_id, reader_context)` | ID trong manifest của chính run trong reader capability | Verification hoặc SnapshotError; không lấy file nguồn mới thay bản snapshot |

`reader_context` là capability nội bộ, không serialize: chứa `run_id`, snapshot ID đã đăng ký, handle workspace riêng của run, mode CLI/web và nguồn trạng thái/expiry của run. CMP-001 cấp khi `create_snapshot` hoàn tất; các reader adapter trong RunContext dùng cùng capability cho CMP-003/004/006/007. Lookup theo `(run_id, snapshot_id, file_id)`, kiểm ID request khớp capability rồi kiểm hạn trước mỗi read/verify; client/model không tự chọn hoặc sửa context. Cùng nội dung có thể tạo cùng snapshot_id ở nhiều run nhưng không có nghĩa chia sẻ workspace, quyền đọc hoặc mốc hết hạn. Run hết hạn hoặc workspace mất thì trả lỗi của run đó; **không tìm bản sao cùng snapshot ở run khác để phục vụ thay**, không gia hạn theo run khác. Capability không phải credential gửi provider, không xuất đường dẫn runtime ra artifact/log.

`SourceSpec` là union đóng sau đây; trường ngoài nhánh bị từ chối. Đây là kiểu runtime, không serialize vào output, log hay prompt:

| Nhánh | Trường bắt buộc và ràng buộc |
|---|---|
| Local | `{kind:"local", path}`; path là thư mục tuyệt đối đã được CMP-001 kiểm không trùng/lồng output; chỉ CLI được cấp nhánh này |
| GitHub | `{kind:"github", url}`; URL repository public đã chuẩn hóa theo API-001 §2.1; chỉ HTTPS; không credential hoặc `ref` tùy chọn trong v1 |
| ZIP | `{kind:"zip", upload_handle}`; handle opaque do facade cấp, gắn đúng run, dùng một lần, trỏ upload đã staging; không phải path do client nhập |

GitHub resolve default branch thành commit cụ thể rồi chỉ lấy cây của commit đó; không lấy metadata của revision A rồi source của revision B. Không resolve được revision thì trả lỗi truy cập, không giả SHA hoặc trả repository rỗng. Commit được giữ trong metadata runtime của intake, không thay cách tính snapshot_id từ bytes/path. Kiểm HTTPS/host allowlist, địa chỉ DNS và đích kết nối sau mỗi redirect; không nhận URL từ file repository, không chạy hook/submodule hoặc tải Git LFS theo cấu hình source. Danh sách host GitHub cần cho adapter tải và cách pin kết nối phải được Security review theo TM T-03 trước code; không chấp nhận wildcard host chỉ vì tên chứa `github`.

`intake_context` chứa mode, workspace handle, nguồn deadline/bộ nhớ/cancellation và kết quả kiểm output của CMP-001. Deadline GitHub tính từ bắt đầu resolve/fetch đến lúc tải xong, tối đa 120 giây cho toàn bộ thao tác, gồm DNS/redirect; retry nội bộ không làm mới hạn. Luôn áp hạn run còn lại nếu ngắn hơn. Chạm deadline/cancel thì dừng I/O, dọn staging và trả lỗi không có snapshot. Trần ZIP 100.000.000 byte nén, 500.000.000 byte giải nén, 50.000 file dùng decimal MB theo API-001 (chi tiết L3; NFR-SEC-002 r3 chưa nói rõ đơn vị). Byte/số entry được đếm khi stream trước bộ lọc phân tích, không tin kích thước khai trong ZIP; ở đúng trần được nhận, vượt trần bị từ chối. Đây không tự thêm trần local/GitHub chưa có trong NFR; cả hai vẫn chịu ngân sách run.

`reader_context` còn mang `reader_kind` và `allowed_file_ids`: CMP-003 chỉ được đọc manifest/config đã cấp để kiểm kê, CMP-004 đọc file source được cấp để phân tích, CMP-007 được verify hash và đọc đúng evidence range đã đăng ký. CMP-006 chỉ đọc range trong `access_scope` do gateway cấp (run/snapshot/request/scope/file IDs, hạn dòng/lần và deadline); không có quyền `read_file`. Scope không được mở rộng bởi tham số request. Quota scope thuộc gateway API-006; CMP-002 kiểm grant và đọc dưới cùng transaction/lease, không tự reset quota. CMP-001/008 không nhận raw file bytes.

`FileRead` là object runtime `{file_id, sha256, encoding, bytes}`: ba trường đầu bằng FileEntry, `bytes` là byte buffer bất biến đã được đối soát SHA-256; không phải base64 trong JSON và không ghi ra ngoài parser được cấp quyền. RangeRead/Verification/SnapshotError có schema ở §3. Mọi hàm trả đúng một success value hoặc SnapshotError, không kèm success payload trong lỗi và không giao một phần snapshot/range. Unknown run/snapshot/file hoặc capability sai được kiểm trước I/O; lỗi không tiết lộ sự tồn tại của file ở run khác.

## 2. Bất biến và ID

- Tạo bản sao riêng của source cho run, băm bytes nguyên bản; không chuyển CRLF/LF để băm. Encoding là cách đọc, không thay nội dung đã hash. Local copy phải đọc đúng regular file đã kiểm, không theo link bị đổi giữa kiểm và mở. Phát hiện file thay đổi trong lúc copy trả SOURCE_CHANGED, không âm thầm dùng bytes không khớp digest. Snapshot là cây bytes đã copy, không tuyên bố filesystem local có transaction toàn cây tại một thời điểm.
- Path tương đối POSIX, phân biệt hoa/thường theo snapshot; cấm path tuyệt đối, segment rỗng/`.`/`..`, backslash, NUL và đi ra ngoài workspace. Cấm drive prefix, UNC, Windows alternate data stream và tên bị filesystem đích diễn giải khác. Không chuẩn hóa Unicode làm đổi tên: tên không thể round-trip hoặc trùng đích do hoa/thường/Unicode/trailing-dot-space thì từ chối, không ghi đè. Local separator được đổi sang `/` trước tính ID; backslash trong entry ZIP bị từ chối. ZIP giữ nguyên root tương đối, không tự bỏ thư mục đầu; adapter GitHub chỉ bỏ wrapper do chính giao thức tải tạo ra.
- `file_id = "file:" + SHA256(UTF8(path))`; `snapshot_id = "snap:" + SHA256(UTF8(canonical_manifest))`. Canonical manifest là mảng các bộ ba `[[path,sha256,byte_size], ...]` sắp path theo Unicode code point, JSON UTF-8 không escape ký tự Unicode thông thường, không space, không BOM. Dấu quote/backslash/control phải escape đúng JSON, byte_size dùng số nguyên thập phân không số 0 thừa; tên chứa surrogate không hợp lệ bị từ chối. Mảng rỗng là `[]`. Cùng cây bytes và path cho cùng snapshot_id; không chứa timestamp/run_id, encoding hoặc excluded. Vì vậy snapshot ID chứng minh tập file đã copy, không chứng minh excluded/coverage giống nhau giữa các run; consumer giữ riêng excluded theo run.
- Symlink/hardlink archive không được tạo liên kết trên đĩa; từ chối ZIP chứa liên kết, file mã hóa hoặc entry không phải regular file/directory. Local symlink, junction/reparse point và special file không theo, ghi excluded entry; local hardlink được copy bytes thành regular file riêng, không tạo hardlink tới source. Đây là policy thận trọng cần review với CMP-002 hiện có.
- Source/output trùng hoặc lồng nhau bị từ chối trước phân tích. Snapshot không giao đi nếu fetch/unzip/copy chưa xong; lỗi thì dọn workspace dở.
- Mọi read kiểm ID trong manifest và đường dẫn đã resolve vẫn ở workspace; hash kiểm trên chính bytes của handle sẽ đọc, không verify file rồi mở lại path khác. Range dùng dòng 1-based, cột 0-based theo Unicode code point sau decode, end exclusive. Không dùng byte offset AST trực tiếp làm cột Unicode.
- Null ở cả hai cột nghĩa là toàn bộ các dòng từ start_line đến end_line inclusive; trường hợp có cột dùng vị trí start/end half-open. Không cho chỉ một cột null. Range phải tồn tại trong file và không rỗng.
- CMP-004 được đọc cả file để phân tích; CMP-003 chỉ đọc manifest/config theo grant kiểm kê. CMP-006 luôn bị giới hạn bởi scope, số lần và số dòng ở NFR-AI; model không tự cấp access_scope. D-07 là chi tiết L3 của NFR-SEC-002 r3 ("không gửi nguyên file"): hợp các range nguồn gửi tới cùng provider trong run, kể cả chữ ký/docstring nguyên văn và qua nhiều scope, không được phủ toàn file. Gateway chặn trước khi gửi và ghi limitation, kể cả file nhỏ.
- Hash kiểm trên bytes nguyên bản trước khi che bí mật; đoạn trả cho UI/model được che bí mật và ghi `redacted:true/false`, không dùng hash snippet đã che thay hash file gốc. Không ghi secret vào lỗi/log.

**Đề xuất quy ước decode cần review:** UTF-8/UTF-8 BOM được nhận diện; Python có encoding declaration hợp lệ thì parser/reader dùng cùng codec đã pin. Không đoán encoding với replacement character: không decode chắc chắn được thì encoding null và đọc range trả ENCODING_UNSUPPORTED. BOM không tính vào cột. LF, CRLF và CR được coi là một ranh giới dòng; ký tự xuống dòng không tính vào cột. File kết thúc bằng newline không tạo thêm một dòng dữ liệu rỗng; file 0 byte không có range hợp lệ. Nội dung RangeRead giữ line ending đã decode trong đoạn; vị trí vẫn trỏ file gốc trước che bí mật, nên chiều dài text đã che không dùng tính lại range.

## 3. Schema snapshot v0.1.0

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-002-v1.schema.json",
  "$ref":"#/$defs/Snapshot",
  "$defs":{
    "FileId":{"type":"string","pattern":"^file:[0-9a-f]{64}$"},
    "SnapshotId":{"type":"string","pattern":"^snap:[0-9a-f]{64}$"},
    "Digest":{"type":"string","pattern":"^[0-9a-f]{64}$"},
    "Range":{
      "type":"object","additionalProperties":false,
      "required":["start_line","end_line","start_column","end_column"],
      "properties":{
        "start_line":{"type":"integer","minimum":1},"end_line":{"type":"integer","minimum":1},
        "start_column":{"type":["integer","null"],"minimum":0},"end_column":{"type":["integer","null"],"minimum":0}
      },
      "oneOf":[
        {"properties":{"start_column":{"type":"null"},"end_column":{"type":"null"}}},
        {"properties":{"start_column":{"type":"integer"},"end_column":{"type":"integer"}}}
      ]
    },
    "RangeRead":{
      "type":"object","additionalProperties":false,
      "required":["snapshot_id","file_id","sha256","range","content","redacted"],
      "properties":{
        "snapshot_id":{"$ref":"#/$defs/SnapshotId"},"file_id":{"$ref":"#/$defs/FileId"},"sha256":{"$ref":"#/$defs/Digest"},
        "range":{"$ref":"#/$defs/Range"},"content":{"type":"string"},"redacted":{"type":"boolean"}
      }
    },
    "Verification":{
      "type":"object","additionalProperties":false,
      "required":["snapshot_id","file_id","status","expected_sha256","actual_sha256"],
      "properties":{
        "snapshot_id":{"$ref":"#/$defs/SnapshotId"},"file_id":{"$ref":"#/$defs/FileId"},
        "status":{"enum":["matched","missing","mismatch"]},"expected_sha256":{"$ref":"#/$defs/Digest"},
        "actual_sha256":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]}
      },
      "allOf":[{"if":{"properties":{"status":{"const":"missing"}}},"then":{"properties":{"actual_sha256":{"type":"null"}}},"else":{"properties":{"actual_sha256":{"$ref":"#/$defs/Digest"}}}}]
    },
    "SnapshotError":{
      "type":"object","additionalProperties":false,
      "required":["code","message","action","retryable","operation","run_id","snapshot_id","file_id"],
      "properties":{
        "code":{"enum":["SOURCE_INVALID","SOURCE_DENIED","SOURCE_CHANGED","SOURCE_OUTPUT_OVERLAP","GITHUB_NOT_FOUND_OR_PRIVATE","GITHUB_ACCESS_DENIED","GITHUB_FETCH_FAILED","ZIP_INVALID","PATH_ESCAPE","PATH_COLLISION","LINK_NOT_ALLOWED","INTAKE_LIMIT","FETCH_TIMEOUT","RUN_CANCELLED","SNAPSHOT_MISSING","SNAPSHOT_MISMATCH","RANGE_INVALID","READ_SCOPE_DENIED","ENCODING_UNSUPPORTED","MASKING_FAILED","EXPIRED","IO_ERROR"]},
        "message":{"type":"string","minLength":1},"action":{"type":"string","minLength":1},"retryable":{"const":false},
        "operation":{"enum":["create_snapshot","read_file","read_range","verify_file"]},"run_id":{"type":"string","minLength":1},
        "snapshot_id":{"oneOf":[{"$ref":"#/$defs/SnapshotId"},{"type":"null"}]},"file_id":{"oneOf":[{"$ref":"#/$defs/FileId"},{"type":"null"}]}
      }
    },
    "FileEntry":{
      "type":"object","additionalProperties":false,
      "required":["file_id","path","sha256","byte_size","encoding"],
      "properties":{
        "file_id":{"type":"string","pattern":"^file:[0-9a-f]{64}$"},
        "path":{"type":"string","minLength":1},
        "sha256":{"type":"string","pattern":"^[0-9a-f]{64}$"},
        "byte_size":{"type":"integer","minimum":0},
        "encoding":{"type":["string","null"],"minLength":1}
      }
    },
    "Snapshot":{
      "type":"object","additionalProperties":false,
      "required":["schema_version","snapshot_id","files","excluded"],
      "properties":{
        "schema_version":{"const":"0.1.0"},
        "snapshot_id":{"type":"string","pattern":"^snap:[0-9a-f]{64}$"},
        "files":{"type":"array","items":{"$ref":"#/$defs/FileEntry"}},
        "excluded":{"type":"array","items":{
          "type":"object","additionalProperties":false,"required":["path","reason"],
          "properties":{"path":{"type":"string","minLength":1},"reason":{"type":"string","minLength":1}}
        }}
      }
    }
  }
}
```

Schema chỉ kiểm shape; uniqueness, canonical digest, path confinement, limit và range cần validator ngữ nghĩa. `encoding:null` là chưa decode được; không có nghĩa file rỗng. Parser ghi limitation nếu file cần đọc mà encoding không hỗ trợ. `files` được sắp path như canonical manifest; file_id/path duy nhất và digest/size phải khớp bytes. `excluded` ghi đường dẫn tương đối an toàn kèm lý do, không đưa nội dung file vào reason. Không có file vừa ở files vừa bị excluded cùng path.

Range phải có `start_line <= end_line`; nếu cùng dòng và có cột thì start_column < end_column. Hai cột phải nằm trong độ dài dòng đã decode; full-line range được dùng cho dòng rỗng tồn tại, còn range numeric zero-length bị từ chối. Với Verification, matched đòi actual_sha256 = expected_sha256; mismatch đòi khác; missing chỉ áp file đã có trong manifest nay mất. ID không được đăng ký trả SnapshotError, không dùng missing để cho phép tra file tùy ý. read_file/read_range chuyển missing/mismatch thành SNAPSHOT_MISSING/SNAPSHOT_MISMATCH và không trả bytes/content. `retryable:false` nghĩa caller không tự lặp tác vụ; người dùng vẫn có thể khởi tạo run mới sau khi sửa lỗi.

## 4. Lỗi và lifecycle

| Code | Hành vi |
|---|---|
| SOURCE_INVALID / SOURCE_DENIED | Dừng intake, hướng dẫn sửa; không tạo artifact |
| SOURCE_CHANGED | Dừng copy; yêu cầu giữ source ổn định rồi tạo run mới |
| SOURCE_OUTPUT_OVERLAP | Từ chối source/output lồng nhau |
| GITHUB_NOT_FOUND_OR_PRIVATE / GITHUB_ACCESS_DENIED / GITHUB_FETCH_FAILED | Nêu đúng upstream cho phép biết; không suy private từ 404 và không hỏi credential |
| ZIP_INVALID / PATH_ESCAPE / PATH_COLLISION / LINK_NOT_ALLOWED | Từ chối toàn ZIP, dọn dữ liệu dở; lỗi path local cũng không giao snapshot |
| INTAKE_LIMIT / FETCH_TIMEOUT / RUN_CANCELLED | Vượt trần hoặc hết deadline/cancel; không giao snapshot thiếu; reason ghi rõ loại limit |
| SNAPSHOT_MISSING / SNAPSHOT_MISMATCH | Không trả code mới làm evidence cũ |
| RANGE_INVALID / READ_SCOPE_DENIED | Không đọc; giữ lý do, không tự mở rộng phạm vi |
| ENCODING_UNSUPPORTED / MASKING_FAILED | Không trả range chưa decode/che bí mật an toàn; caller ghi limitation |
| EXPIRED | Không phục vụ snapshot web sau expiry |
| IO_ERROR | Lỗi I/O đã lọc đường dẫn/bí mật; dọn phần chưa publish, không ghi nội dung exception thô |

Source web hết hạn theo run trong reader_context; CLI output do người dùng quản lý. Runtime filesystem paths không xuất ra ngoài. Snapshot bất biến; readers song song được, cleanup phải phối hợp với việc đọc qua owner để không trả dữ liệu sau hạn. Cleanup/lease cũng gắn `(run_id, snapshot_id)`, không chỉ snapshot_id, để dọn run A không xóa workspace còn hiệu lực của run B có cùng nội dung. Không xem cleanup như không cần đồng bộ chỉ vì source read-only.

Kiểm expiry/cancellation lúc nhận đọc và ngay trước trả bytes; nếu hết hạn trong lúc đọc/verify thì bỏ buffer và trả EXPIRED. Lease không gia hạn quyền đọc. CLI workspace tạm chỉ giữ trong vòng đời coordinator hoặc phiên retry được cấp quyền; kết thúc phiên phải dọn theo owner. Không tự lưu source thô vào output để hỗ trợ retry. Nếu mở `l3gen retry` ở tiến trình sau mà model/snapshot cần thiết không còn, API-001 trả artifact_not_retryable/exit 2; không đọc lại cây source để dựng bằng chứng cũ. Cách lưu material đã kiểm cho retry qua tiến trình cần review cùng CMP-008, chưa phải cam kết bền vững sau restart.

Admission/cancellation sau khi chưa có snapshot ánh xạ `state:failed`, `analysis_outcome:failed` ở API-001, reason giữ nguyên nguyên nhân gốc. Nếu hết ngân sách trước snapshot, không có nội dung đã kiểm để tạo bundle partial; ResultBundle bắt buộc `snapshot_id`, nên không publish được và run là `failed` (chi tiết L3, cùng nhóm "Tiếp nhận từ chối" của CMP-001 r2 §4). Lỗi range riêng lẻ trong phân tích không xóa snapshot hợp lệ; caller ghi limitation và xử lý phần còn lại. Lỗi mở evidence sau run không đổi kết luận run đã publish, chỉ từ chối nội dung của request đó.

## 5. Ví dụ và ca kiểm contract

Snapshot rỗng có digest thật của UTF-8 `[]`; đây là fixture hợp đồng, không phải phân tích repository đã chạy. Intake rỗng hợp lệ; CMP-003 phải phân loại empty, CMP-001 không được trả completed rỗng theo AC-020-02.

```json
{"schema_version":"0.1.0","snapshot_id":"snap:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945","files":[],"excluded":[]}
```

Ví dụ Range hợp lệ về shape cho trọn dòng 2 đến 3; kiểm file cụ thể còn phải xác nhận hai dòng tồn tại:

```json
{"start_line":2,"end_line":3,"start_column":null,"end_column":null}
```

Ví dụ lỗi trước snapshot; message/action không chứa URL upstream có query, credential hoặc absolute path:

```json
{"code":"FETCH_TIMEOUT","message":"Không lấy xong source GitHub trong 120 giây.","action":"Kiểm kết nối và URL public, rồi bắt đầu lần chạy mới.","retryable":false,"operation":"create_snapshot","run_id":"run_demo_01","snapshot_id":null,"file_id":null}
```

| Ca | Mong đợi |
|---|---|
| Cùng bytes/path qua ZIP và local | Cùng snapshot_id dù run_id khác |
| Hai run cùng snapshot, run A hết hạn còn run B chưa hết | Reader A trả EXPIRED, không fallback sang B; reader B tiếp tục dùng workspace B |
| Cùng file, chỉ CRLF đổi thành LF | Hash khác; không nhận như snapshot cũ |
| ZIP có `../outside.py` hoặc liên kết | Từ chối trước khi ghi ra ngoài |
| Model xin file đúng tên nhưng khác snapshot | READ_SCOPE_DENIED hoặc SNAPSHOT_MISSING |
| File đổi sau snapshot, mở evidence | SNAPSHOT_MISMATCH, không trả đoạn mới |
| Range chứa ký tự tiếng Việt trước callsite | Đánh đúng cột Unicode đã quy định |
| Một cột null hoặc start sau end | RANGE_INVALID; không cắt ngầm để thành range khác |
| CMP-003 xin raw code hoặc CMP-006 gọi read_file | READ_SCOPE_DENIED trước đọc bytes |
| 100.000.000 byte nén và thêm một byte | Ca đầu còn được kiểm tiếp, ca sau INTAKE_LIMIT; Content-Length không quyết định |
| Link bị đổi sau kiểm, path trùng do hoa/thường, entry mã hóa | Từ chối có nguyên nhân; không tạo file bên ngoài hoặc ghi đè |
| Expiry đến giữa verify và trả range | EXPIRED, không trả buffer đã đọc |
| Source local đổi trong khi copy | SOURCE_CHANGED; không snapshot thiếu/không khớp |

AC: 019-02/03/04/05, 020-01/02, 023-03. Đây là test specification, chưa phải test đã chạy. Link/encoding, decimal MB và D-06/D-07 đã có policy draft; vẫn cần review/kiểm allowlist GitHub thực tế, kết nối đã pin và retry qua tiến trình; không thay quyết định phân chia component còn mở.

## Nguồn

- [CMP-L3GEN-002](../../../architecture/l2/CMP-L3GEN-002.md), [FR-L3GEN-019](../../../requirements/_superseded-r28/fr/FR-L3GEN-019.md), [FR-L3GEN-020](../../../requirements/_superseded-r28/fr/FR-L3GEN-020.md) (đã superseded từ PRD rev 31; revision 5 chỉ sửa link).
- [NFR-L3GEN-SEC-002](../../../requirements/nfr/NFR-L3GEN-SEC-002.md), [NFR-L3GEN-OPS-001](../../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-AI-002](../../../requirements/nfr/NFR-L3GEN-AI-002.md), [TM-SYS-L3GEN](../../../architecture/threat-model/TM-SYS-L3GEN.md).
- [API-L3GEN-001-v1](../../CMP-L3GEN-001/api/API-L3GEN-001-v1.md), [API-L3GEN-006-v1](../../CMP-L3GEN-006/api/API-L3GEN-006-v1.md).
