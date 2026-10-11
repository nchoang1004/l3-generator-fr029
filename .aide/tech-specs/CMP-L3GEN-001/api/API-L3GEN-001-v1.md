---
uid: "01M3B99N5NSY5M7BE6Y6ZK83M2"
key: "API-L3GEN-001-v1"
type: "api-contract"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-001"],"satisfies":["FR-L3GEN-019","FR-L3GEN-024","FR-L3GEN-025","FR-L3GEN-026"],"depends_on":["API-L3GEN-002-v1","API-L3GEN-004-v1","API-L3GEN-007-v1","API-L3GEN-008-v1"],"constrained_by":["NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002","NFR-L3GEN-AI-002"],"governed_by":["ADR-2026-003"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# API-L3GEN-001-v1 — Điều phối lần chạy qua CLI và web cục bộ

## 1. Phạm vi và trạng thái thiết kế

Đây là **bản nháp L3**, dựa trên nguồn ở nhánh `docs/gate-2` commit `5d06f14`: CMP-L3GEN-001 r2, CMP-L3GEN-002 r2, CMP-L3GEN-008 r2, PRD r28 và các FR/AC dưới đây. Chưa có bằng chứng triển khai hoặc nghiệm thu; `draft` không có nghĩa đã qua Architecture, UI/UX hay Contract Gate. Revision 4 bỏ các điểm trái nguồn của revision 3 (giới hạn hàng đợi, hạn chờ, projection ẩn node, `failed` khi còn publish được). Chỗ nào nguồn chưa nói mà contract quy định thêm thì ghi "chi tiết L3". D-03 giữ mở.

CMP-001 sở hữu facade HTTP cho trang web cục bộ và entry point CLI. CMP-002 tiếp nhận source; CMP-008 dựng/trả ResultBundle và artifact; khi mở bằng chứng, CMP-001 gọi CMP-007, rồi CMP-007 dùng reader CMP-002 để kiểm và đọc đúng snapshot. CMP-008 chỉ cung cấp ID tham chiếu trong kết quả. Facade không tự đọc source, tự sửa model hoặc tự sinh artifact. CLI nhận thư mục local, gọi cùng engine trực tiếp, **không khởi động hoặc phụ thuộc web server**.

| Consumer | Contract | Ranh giới |
|---|---|---|
| CLI M1 | `l3gen analyze`, `l3gen retry` (§8) | Thư mục source/output do người dùng chỉ định |
| Web cục bộ M2 của CMP-008 | HTTP `/api/v1` (§6) | ZIP hoặc URL GitHub public HTTPS; chỉ dữ liệu lần chạy trong vòng đời |
| Công cụ đọc JSON | ResultBundle của API-L3GEN-008-v1 | JSON có phiên bản, snapshot và tham chiếu được kiểm |

Không có API liệt kê lịch sử, public job service, webhook, hủy lần chạy hay phục vụ thư mục local qua HTTP trong v1 này. Các endpoint chỉ phục vụ UI cùng origin trên máy cục bộ theo giả định của TM-SYS-L3GEN; mở ra Internet cần thiết kế khác.

## 2. Tiếp nhận, thông báo dữ liệu và hàng đợi

### 2.1 Quy tắc chung

1. Trước khi chạy, UI/CLI hiển thị thông báo `l3gen-egress-v1`: dữ kiện đã trích, tên symbol, đường dẫn tương đối, vị trí, literal như route path, chữ ký hàm/docstring và đoạn code có giới hạn có thể được gửi tới **Groq và Google**. Không gửi cả repository hoặc nguyên file; che giá trị mang dấu hiệu bí mật trước mọi đầu ra. Bộ lọc bí mật có giới hạn; điều khoản của provider do provider công bố.
2. HTTP request chỉ chứa đầu vào và phiên bản thông báo đã hiển thị; không có credential GitHub, khóa model, model override, ngân sách override hoặc đường dẫn máy chủ. `egress_notice_version` ghi nhận phiên bản UI đã trình bày, không phải bằng chứng người dùng đã đọc hoặc một approval gate.
3. URL phải là `https://github.com/<owner>/<repo>`; chấp nhận dấu `/` cuối hoặc hậu tố `.git`, chuẩn hóa trước CMP-002. Cấm userinfo, query, fragment, port tùy ý, URL `tree/blob`, owner/repo rỗng hoặc `.`/`..`; URL không phải GitHub trả `422`. CMP-002 kiểm DNS/redirect, xác minh public và khóa revision khi tạo snapshot. GitHub có thể không phân biệt repo private và repo không tồn tại; khi upstream trả cùng `404`, mã `github_not_found_or_private` nêu đúng giới hạn đó, không đoán nguyên nhân và không hỏi credential.
4. ZIP chỉ một part `archive` và một part text `egress_notice_version`. Không tin MIME, tên file hay Content-Length; giới hạn khi stream và kiểm magic/định dạng. Trần nguồn: 100 MB nén, 500 MB giải nén, 50.000 file; GitHub 120 giây. Chi tiết L3 (NFR-SEC-002 r3 chưa nói rõ): MB là 1.000.000 byte, còn GiB là 2^30 byte. Giới hạn tính trên dữ liệu thực, không theo header.
5. Trước `202`, kiểm cú pháp/schema, giới hạn stream và ZIP có thể đọc được. `202` chỉ xác nhận tiếp nhận, chưa xác nhận snapshot. Kiểm toàn bộ đường dẫn, giải nén, tổng số file/kích thước và truy cập GitHub ở giai đoạn intake; từ chối sau `202` biểu diễn bằng RunView `failed`, không biến thành kết quả rỗng. Không tạo output dở. Theo policy draft API-002, ZIP có đường dẫn thoát vùng hoặc bất kỳ symlink/hardlink nào bị từ chối cả gói; không tạo liên kết trên đĩa. Với thư mục local của CLI, symlink không được đi theo và được ghi excluded/giới hạn. Policy phân biệt ZIP/local này cần review cùng CMP-002.

Sau admission, CMP-001 tạo disclosure record trong runtime từ `egress_notice_version` đã nhận; CLI lấy đúng phiên bản thông báo đã thực sự in ra trước chạy. Record gồm `{run_id, notice_version, providers:[groq,google], data_categories, issued_at}`; `data_categories` là danh sách các loại dữ liệu ở mục 1 của §2.1. Khi intake hoàn tất, engine gắn `snapshot_id` vào record rồi mới cho CMP-006 gửi network. Gateway đối chiếu record với run/snapshot, cả hai provider và phiên bản/phạm vi thông báo; thiếu hoặc lệch trả `DISCLOSURE_REQUIRED`, không gọi model và ghi limitation để pipeline xử lý partial. Record này chỉ chứng minh engine đã thực hiện bước thông báo được quy định; không chứng minh người dùng đã đọc/đồng ý, không tạo consent token hoặc approval gate mới.

### 2.2 Hàng đợi

Theo CMP-001 r2 (§2, §7) và NFR-OPS-001 r1: mỗi lúc chỉ 1 lần chạy; lần sau xếp hàng theo thứ tự đến. Contract chi tiết:

- Hàng đợi FIFO. Nguồn không đặt sức chứa hoặc hạn chờ, nên contract không từ chối request vì hàng đợi đầy và không tự hủy run đang chờ.
- Request ngắt giữa upload thì xóa upload tạm và không cấp run_id. Chỉ cấp run_id khi admission thành công.
- `queued` chưa có snapshot, stage `queue`, analysis_outcome `null`. ZIP đã nhận được giữ trong workspace riêng; chưa lấy source GitHub hoặc gọi model khi còn chờ.
- Khi có lượt, đặt `started_at`, chuyển `running/intake`. Chi tiết L3: hạn 30 phút của NFR-OPS-001 tính từ `started_at`, gồm intake, phân tích, model, verification, xuất; thời gian chờ không tính vào. Bộ nhớ tối đa 2 GiB/lần chạy. Chạm hạn chạy/bộ nhớ thì dừng giai đoạn đang chạy và trả `partial` với phần đã xong (CMP-001 §4).
- Sau tiến trình chết, lần khởi động tiếp theo đánh dấu các bản ghi `running`/`queued` còn dang dở là `failed/process_interrupted`, xóa staging/output chưa publish (CMP-001 §4); không tự chạy lại request hoặc model.

Đã chốt khi tự review 01/10/2026: giữ đúng nguồn, không giới hạn số run chờ và không có hạn chờ. Muốn giới hạn thì phải sửa NFR-OPS-001/CMP-001 trước (ghi ở bản đối chiếu, mục 6).

## 3. Trạng thái, kết quả và artifact

`run_id`, `snapshot_id`, `evidence_id`, `artifact_id` là chuỗi opaque; client không suy ra thuật toán/hash, thư mục hay thứ tự từ ID. ID không phải đường dẫn. CMP-001 sinh run_id; CMP-002 sinh snapshot_id sau khi snapshot hoàn chỉnh. Bằng chứng và artifact chỉ được giải quyết trong chính run_id/snapshot_id tương ứng.

| `state` | Điều kiện và `analysis_outcome` | Chuyển tiếp |
|---|---|---|
| `queued` | Chưa bắt đầu; outcome null, snapshot null | `running` hoặc `failed` do crash |
| `running` | Đang xử lý; outcome null tới khi CMP-007 kết luận | `completed`, `partial`, `failed` |
| `completed` | Analysis completed và mọi artifact bắt buộc ready, output publish xong | Trạng thái cuối, không mở lại |
| `partial` | Analysis partial hoặc có artifact xuất failed; nêu giới hạn/phạm vi đã xử lý | Trạng thái cuối; retry chỉ thay đổi trạng thái artifact |
| `failed` | Tiếp nhận bị từ chối, không thể publish bộ kết quả nhất quán hoặc tiến trình chết | Trạng thái cuối |

`analysis_outcome` là kết quả phân tích (`completed|partial|failed|null`), không đồng nghĩa với trạng thái ghi file. `artifacts[].status` dùng schema CMP-008 (`pending|ready|failed|retrying`). Ví dụ analysis completed nhưng diagram export failed cho `state: partial`, `analysis_outcome: completed`; retry diagram thành công không chạy lại model và không tự sửa run cuối thành completed. Mọi consumer phải hiển thị được cả kết quả phân tích lẫn trạng thái artifact. Mọi artifact phải cùng tập component và cạnh (CMP-008 r2 §3–4); artifact lệch nhau thì không publish bộ sai. Thất bại publish là `failed`, và lý do vẫn có qua RunView.

`stage`: `queue|intake|inventory|extraction|assembly|verification|export|null`; cuối run là null. `reasons[]` là tóm tắt đã lọc bí mật; danh sách giới hạn/phạm vi chi tiết ở ResultBundle do CMP-007/008 cung cấp. `partial` hoặc `failed` phải có ít nhất một reason. Thời gian lấy source, static analysis, model, export, bộ nhớ đỉnh và output bytes được ghi riêng trong `metrics`; giá trị chưa đo là null, không dùng 0 thay cho chưa đo. Static và model có thể xen kẽ; không cộng các số đo để suy ra duration tổng.

Mọi timestamp là UTC RFC 3339 với hậu tố `Z`; `created_at <= started_at <= finished_at` khi các giá trị tồn tại. Timer deadline/duration dùng clock monotonic; timestamp phục vụ trao đổi và retention dùng clock UTC tin cậy, không kéo dài hạn vì client gửi giờ khác hoặc đồng hồ hệ thống lùi. `finished_at` chỉ được ghi một lần khi chuyển trạng thái cuối. Run failed trước khi bắt đầu có started_at null và analysis_outcome failed; run đã bắt đầu nhưng chưa có snapshot cũng có analysis_outcome failed. `completed`/`partial` luôn có started_at và snapshot_id. `links.self` là route đúng run; `links.result` chỉ khác null khi result_available true, và trỏ đúng route result của run đó. Các phép so sánh thời gian, ID và URL này cần validator ngữ nghĩa.

Chính sách root/flat, phân chia component và rule catalog được resolve theo version đã cấu hình, không do request HTTP chọn. Khi API-003/005 trả policy unavailable hoặc API-007 không thể kiểm, CMP-001 giữ reason cụ thể; không tự chọn thuật toán hoặc tạo model giả. Chỉ publish partial nếu CMP-007/008 xác nhận được bundle hợp lệ với phần đã kiểm và giới hạn rõ; không publish được thì failed/result_unavailable. Bản nháp này không chốt thuật toán phân chia component.

**Lifecycle D-06 trong bản draft:** `completed` và `partial` đều yêu cầu `result_available:true`, chỉ ghi sau khi CMP-008 publish nguyên tử một bundle hợp lệ. Bundle partial có thể có model rỗng hoặc không còn fact dùng được (CMP-007 r2 §4: loại hết kết luận thì trả mô hình rỗng, `partial`); phải công bố rõ phạm vi/giới hạn đã xác định. `failed` do intake/crash hoặc lỗi publish được ghi khi đã dừng và dọn dữ liệu dở, không phải chờ CMP-008 tạo output. Phân tích đã kết luận nhưng không publish được bundle thì giữ nguyên `analysis_outcome` đã xác định (`completed` hoặc `partial`), còn `state:failed`, `result_available:false`, nêu riêng lỗi export. Chưa có kết quả phân tích đã kiểm thì analysis_outcome failed; không dùng lỗi ghi file để sửa kết luận phân tích. Tách `analysis_outcome` khỏi trạng thái ghi file là chi tiết L3; cần kiểm bằng ca lỗi thực tế khi triển khai. Mọi run chưa có bundle đã publish trả `409 result_unavailable` khi đọc result; vẫn đọc được reason trên status. Không lấy artifact pending/failed/retrying làm file hoàn chỉnh.

## 4. Vòng đời, concurrency và retry

- Mọi dữ liệu web có `expires_at = finished_at + 24 giờ`; khi chưa kết thúc thì expires_at null. Sau hạn, result/evidence/artifact không được trả, kể cả byte đã có cache. Mỗi request kiểm hạn trước mở tài nguyên; response `Cache-Control: no-store`. Máy khởi động lại dọn dữ liệu quá hạn trước phục vụ. Source/output và manifest được dọn theo NFR-SEC-002. Nếu bản ghi còn tồn tại lúc kiểm hạn trả `410 run_expired`; sau khi đã xóa cả bản ghi trả `404 run_not_found`. Không giữ tombstone để tạo lịch sử riêng.
- Thời điểm kiểm hạn là thời điểm chấp nhận mở dữ liệu; quá hạn trong lúc stream thì ngừng stream, không tiếp tục truyền byte mới. Reader và cleanup dùng lease/khóa ngắn theo run để tránh mở file đã xóa; khóa không được trì hoãn hiệu lực hết hạn. Poll status đồng thời không chạy lại tác vụ.
- POST tạo run **không idempotent**: cùng đầu vào hai lần tạo hai run khác nhau theo CMP-001. Không hỗ trợ `Idempotency-Key`; nếu nhận header này trả `400 idempotency_key_unsupported`, không giả vờ deduplicate. Client không tự retry POST khi chưa biết server đã nhận hay chưa; giữ `Location`/run_id đã nhận để poll. GET không gây tác dụng phụ ngoài kiểm hết hạn/dọn dữ liệu đã đến hạn.
- POST retry artifact chỉ áp dụng cho run cuối `partial`/`completed`, snapshot/model đã kiểm còn khả dụng và artifact `failed` với `error.retryable=true`. CMP-008 sinh lại đúng artifact từ cùng verified model, cùng snapshot và cấu hình export; các artifact ready giữ nguyên byte/hash. Lỗi consistency hoặc thiếu model/snapshot không retry được: `409 artifact_not_retryable`.
- **Đề xuất cần review:** retry là tác vụ export đồng bộ với bộ lập lịch CMP-001, không phải một run mới. Khi engine hoặc retry khác đang chiếm slot thì `409 engine_busy`, không tạo hàng chờ retry riêng. Nếu cùng artifact đang retry, POST lặp trả `202` với RunView hiện tại, không tạo lần thử thứ hai. Nếu đã ready trả `200` với RunView hiện tại. Chỉ khi còn failed sau lần thử trước, POST mới tạo một attempt mới.
- Retry không đổi run_id, snapshot_id, analysis_outcome, state cuối, finished_at, expires_at; không gọi model, không gia hạn 24 giờ. CMP-008 stage/kiểm artifact failed, lắp file đích rồi replace manifest nguyên tử theo API-008 dưới khóa publish; artifact ready giữ byte/hash. Reader pin một bản manifest hoàn chỉnh cho mỗi request; file mới chưa được manifest đánh ready không được phục vụ. Crash sau lắp file nhưng trước manifest để lại file chưa tham chiếu, không giả thành công. Hết hạn trước commit thì không publish manifest, dọn staging/file chưa tham chiếu và ngừng phục vụ. CLI retry dùng cùng quy tắc bảo toàn artifact; output CLI không chịu retention web.

GET result/evidence/artifact chỉ giải tài nguyên từ bundle đã publish của run. Run đang export có thể báo tiến độ artifact nhưng chưa cho tải file trước commit. Response status và result riêng biệt có thể được đọc trước/sau retry; UI tải lại bundle và thay toàn bộ view từ một bản, không ghép artifact list cũ với model/export metadata của bản khác. `retryable` trong Error chỉ hướng dẫn có thể thử thao tác lại sau khi sửa/chờ; không cho phép tự replay POST tạo run có kết quả chưa biết.

## 5. Bảo vệ facade và cấp khóa model

Khóa Groq/Google không nằm trong request body, URL, header HTTP, ResultBundle, log hoặc evidence. Đề xuất nhận khóa tại **prompt cục bộ không echo lúc khởi chạy CLI/web launcher**, chuyển trực tiếp vào bộ nhớ CMP-006 qua tham chiếu runtime ngoài schema lưu trữ; CMP-001/008 không serialize giá trị. Không nhận credential repository dưới bất kỳ hình thức nào. Thiếu khóa không biến thành lỗi input: phần model không chạy, ghi giới hạn và phân tích partial theo NFR-AI-002. Chi tiết L3 (NFR-AI-002 r3 chỉ ghi khóa do người dùng cung cấp lúc chạy, không ghi ra output/log): handle chỉ sống trong tiến trình launcher/CLI, không ghi ra đĩa và không có endpoint rekey. Muốn đổi khóa thì dừng có kiểm soát, đóng provider client/handle và khởi động launcher lại; run bị ngắt xử lý theo §4. Không hứa xóa sạch vật lý mọi bản sao trong RAM của runtime.

Web theo TM-SYS-L3GEN chỉ bind loopback, kiểm `Host` và `Origin` đúng origin UI, không bật CORS cho origin khác; POST bắt buộc `X-L3GEN-Client: web-v1` để chặn form cross-origin đơn giản. Header này không phải credential hoặc cơ chế xác thực. Read HTTP vẫn áp dụng Host/Origin khi có Origin; native client trên máy tin cậy được phép không có Origin. Tham số path phải chỉ giải ID opaque qua manifest của run, không nối thẳng vào filesystem. Mọi lỗi phải lọc provider detail, bí mật và đường dẫn tuyệt đối; thông báo chứa nguyên nhân và cách sửa.

Facade kiểm host/origin trước lookup ID, sau đó expiry của run, quyền sở hữu evidence/artifact, rồi trạng thái sẵn sàng. ID đúng cú pháp nhưng không thuộc run trả 404; không tiết lộ ID đang ở run khác. JSON trùng key và multipart trùng part bị 400, trường ngoài schema bị 422. Lỗi ngoài dự kiến trả 500 internal_error với Error đã lọc, không trả stack trace. 500 trước admission không tạo run; nếu run đã commit nhưng kết nối mất thì client không thể suy ra POST thất bại và không tự lặp. Với stream đã gửi header, lỗi I/O/expiry đóng stream; client phải coi download thiếu là lỗi, không mong một JSON Error sau bytes. Request GET không có body; retry POST có body bị 400.

## 6. OpenAPI 3.1.1

Khối YAML dưới đây là contract HTTP được nhúng trong file chuẩn tắc theo execution guide §A.1/§B.10. Khi trích xuất, đặt YAML và **cả bảy schema** `API-L3GEN-002-v1.schema.json` đến `API-L3GEN-008-v1.schema.json` cùng một thư mục; facade tham chiếu trực tiếp 004/008, còn các schema này tham chiếu tiếp 005/006/007. `$ref` tương đối trỏ tới **sản phẩm trích xuất**, không phải file schema chuẩn tắc riêng. Cú pháp theo [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html). Giới hạn byte, FIFO, clock, kiểm snapshot và invariant trạng thái tại §2–5 là kiểm ngữ nghĩa cần có ngoài schema.

```yaml
openapi: 3.1.1
info:
  title: L3GEN local run facade
  version: 1.0.0-draft
  description: Draft owned by CMP-L3GEN-001; local same-origin web only.
jsonSchemaDialect: https://json-schema.org/draft/2020-12/schema
servers:
  - url: /
    description: Current loopback origin hosting the local UI.
security: []
tags:
  - name: runs
  - name: results
paths:
  /api/v1/runs/github:
    post:
      operationId: createGitHubRun
      tags: [runs]
      summary: Admit one public GitHub analysis run
      description: Non-idempotent; 202 is admission, not proof of a valid snapshot.
      parameters:
        - $ref: '#/components/parameters/WebClient'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GitHubRequest'
            example:
              github_url: https://github.com/example/service
              egress_notice_version: l3gen-egress-v1
      responses:
        '202':
          $ref: '#/components/responses/RunAccepted'
        '400':
          $ref: '#/components/responses/BadRequest'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '415':
          $ref: '#/components/responses/UnsupportedMediaType'
        '422':
          $ref: '#/components/responses/InvalidInput'
        '503':
          $ref: '#/components/responses/Unavailable'
  /api/v1/runs/zip:
    post:
      operationId: createZipRun
      tags: [runs]
      summary: Admit a ZIP upload for one analysis run
      description: Enforce stream size even without Content-Length; never use upload filename as a path.
      parameters:
        - $ref: '#/components/parameters/WebClient'
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              additionalProperties: false
              required: [archive, egress_notice_version]
              properties:
                archive:
                  type: string
                  format: binary
                  contentMediaType: application/zip
                  description: One ZIP, at most 100000000 compressed bytes (decimal MB proposal).
                egress_notice_version:
                  type: string
                  const: l3gen-egress-v1
            encoding:
              archive:
                contentType: application/zip
              egress_notice_version:
                contentType: text/plain
      responses:
        '202':
          $ref: '#/components/responses/RunAccepted'
        '400':
          $ref: '#/components/responses/BadRequest'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '413':
          $ref: '#/components/responses/InputTooLarge'
        '415':
          $ref: '#/components/responses/UnsupportedMediaType'
        '422':
          $ref: '#/components/responses/InvalidInput'
        '503':
          $ref: '#/components/responses/Unavailable'
  /api/v1/runs/{run_id}:
    parameters:
      - $ref: '#/components/parameters/RunId'
    get:
      operationId: getRun
      tags: [runs]
      summary: Read status, stage, reasons and artifact statuses for one run
      responses:
        '200':
          $ref: '#/components/responses/RunStatus'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '404':
          $ref: '#/components/responses/NotFound'
        '410':
          $ref: '#/components/responses/Expired'
  /api/v1/runs/{run_id}/result:
    parameters:
      - $ref: '#/components/parameters/RunId'
    get:
      operationId: getRunResult
      tags: [results]
      summary: Read the published bundle used by every web view
      description: Search/filter is client-side over this same bundle; no separate history/search API.
      responses:
        '200':
          description: Published complete or partial bundle from CMP-L3GEN-008.
          headers:
            Cache-Control:
              $ref: '#/components/headers/NoStore'
          content:
            application/json:
              schema:
                $ref: 'API-L3GEN-008-v1.schema.json#/$defs/ResultBundle'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '410':
          $ref: '#/components/responses/Expired'
  /api/v1/runs/{run_id}/evidence/{evidence_id}:
    parameters:
      - $ref: '#/components/parameters/RunId'
      - $ref: '#/components/parameters/EvidenceId'
    get:
      operationId: getEvidence
      tags: [results]
      summary: Open a redacted evidence excerpt after CMP-007 verifies the snapshot
      responses:
        '200':
          description: Verified excerpt; never source content from a changed or missing file.
          headers:
            Cache-Control:
              $ref: '#/components/headers/NoStore'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EvidenceView'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '410':
          $ref: '#/components/responses/Expired'
  /api/v1/runs/{run_id}/artifacts/{artifact_id}:
    parameters:
      - $ref: '#/components/parameters/RunId'
      - $ref: '#/components/parameters/ArtifactId'
    get:
      operationId: downloadArtifact
      tags: [results]
      summary: Download one ready artifact resolved from its run manifest
      responses:
        '200':
          description: Complete ready artifact; download filename is generated and sanitized by CMP-008.
          headers:
            Cache-Control:
              $ref: '#/components/headers/NoStore'
            Content-Disposition:
              schema: {type: string}
              description: attachment with a sanitized filename; never a local absolute path.
            X-Content-Type-Options:
              schema: {type: string, const: nosniff}
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '410':
          $ref: '#/components/responses/Expired'
  /api/v1/runs/{run_id}/artifacts/{artifact_id}/retry:
    parameters:
      - $ref: '#/components/parameters/RunId'
      - $ref: '#/components/parameters/ArtifactId'
    post:
      operationId: retryArtifact
      tags: [results]
      summary: Retry a failed retryable artifact without rerunning analysis
      description: No request body. Duplicate while retrying coalesces; already ready is a no-op.
      parameters:
        - $ref: '#/components/parameters/WebClient'
      responses:
        '200':
          $ref: '#/components/responses/RunStatus'
        '202':
          $ref: '#/components/responses/RunAccepted'
        '400':
          $ref: '#/components/responses/BadRequest'
        '403':
          $ref: '#/components/responses/ForbiddenOrigin'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '410':
          $ref: '#/components/responses/Expired'
        '503':
          $ref: '#/components/responses/Unavailable'
components:
  parameters:
    WebClient:
      in: header
      name: X-L3GEN-Client
      required: true
      schema: {type: string, const: web-v1}
      description: Local UI marker, not an authentication secret.
    RunId:
      in: path
      name: run_id
      required: true
      schema:
        $ref: '#/components/schemas/OpaqueId'
    EvidenceId:
      in: path
      name: evidence_id
      required: true
      schema:
        $ref: '#/components/schemas/OpaqueId'
    ArtifactId:
      in: path
      name: artifact_id
      required: true
      schema:
        $ref: '#/components/schemas/OpaqueId'
  headers:
    NoStore:
      schema: {type: string, const: no-store}
    RetryAfter:
      schema: {type: integer, minimum: 1}
      description: Suggested delay in seconds, not a capacity guarantee.
  responses:
    RunAccepted:
      description: Admitted run or artifact retry; poll Location. No conclusion of analysis success.
      headers:
        Location:
          schema: {type: string, format: uri-reference}
          description: /api/v1/runs/{run_id}
        Retry-After:
          $ref: '#/components/headers/RetryAfter'
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/RunView'
    RunStatus:
      description: Current RunView; terminal state does not imply every artifact is ready.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/RunView'
    BadRequest:
      description: Malformed JSON/multipart, unexpected retry body, or unsupported Idempotency-Key.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    ForbiddenOrigin:
      description: Host/Origin check failed or local UI header is missing/invalid.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    InputTooLarge:
      description: Upload exceeds compressed byte limit; staging is removed and no run is admitted.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    UnsupportedMediaType:
      description: Request or archive part media type is unsupported.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    InvalidInput:
      description: Invalid input/schema, corrupt ZIP, or missing/current notice version mismatch.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Run is unknown/purged, or evidence/artifact does not belong to this run.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Conflict:
      description: Result not published, snapshot mismatch, artifact not ready/not retryable, or engine busy.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Expired:
      description: Run retention expired; no source/result/artifact content is returned.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unavailable:
      description: Engine cannot admit work; no new run/retry accepted.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    UnexpectedFailure:
      description: Unexpected failure; sanitized details only. Never automatically replay a creation POST.
      headers:
        Cache-Control:
          $ref: '#/components/headers/NoStore'
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  schemas:
    OpaqueId:
      type: string
      minLength: 1
      maxLength: 128
      pattern: '^[A-Za-z0-9_:-]+$'
      description: Opaque identifier. Do not interpret as a path, digest, UUID, or ULID.
    GitHubRequest:
      type: object
      additionalProperties: false
      required: [github_url, egress_notice_version]
      properties:
        github_url:
          type: string
          format: uri
          maxLength: 2048
          pattern: '^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$'
          description: Additional semantic checks in section 2 reject dot segments and non-repository forms.
        egress_notice_version:
          type: string
          const: l3gen-egress-v1
    Reason:
      type: object
      additionalProperties: false
      required: [code, message, action]
      properties:
        code: {type: string, minLength: 1, maxLength: 80}
        message: {type: string, minLength: 1}
        action: {type: string, minLength: 1}
    Error:
      type: object
      additionalProperties: false
      required: [code, message, action, retryable, run_id, field]
      properties:
        code: {type: string, minLength: 1, maxLength: 80}
        message: {type: string, minLength: 1}
        action: {type: string, minLength: 1}
        retryable: {type: boolean}
        run_id:
          oneOf:
            - $ref: '#/components/schemas/OpaqueId'
            - type: 'null'
        field: {type: [string, 'null']}
    Metrics:
      type: object
      additionalProperties: false
      required: [intake_ms, static_analysis_ms, model_ms, export_ms, peak_memory_bytes, output_bytes]
      properties:
        intake_ms: {type: [integer, 'null'], minimum: 0}
        static_analysis_ms: {type: [integer, 'null'], minimum: 0}
        model_ms: {type: [integer, 'null'], minimum: 0}
        export_ms: {type: [integer, 'null'], minimum: 0}
        peak_memory_bytes: {type: [integer, 'null'], minimum: 0}
        output_bytes: {type: [integer, 'null'], minimum: 0}
    RunView:
      type: object
      additionalProperties: false
      required: [run_id, snapshot_id, state, stage, analysis_outcome, created_at, started_at, finished_at, expires_at, result_available, reasons, artifacts, metrics, links]
      properties:
        run_id:
          $ref: '#/components/schemas/OpaqueId'
        snapshot_id:
          oneOf:
            - $ref: '#/components/schemas/OpaqueId'
            - type: 'null'
        state: {type: string, enum: [queued, running, completed, partial, failed]}
        stage:
          type: [string, 'null']
          enum: [queue, intake, inventory, extraction, assembly, verification, export, null]
        analysis_outcome:
          type: [string, 'null']
          enum: [completed, partial, failed, null]
        created_at: {type: string, format: date-time}
        started_at: {type: [string, 'null'], format: date-time}
        finished_at: {type: [string, 'null'], format: date-time}
        expires_at: {type: [string, 'null'], format: date-time}
        result_available: {type: boolean}
        reasons:
          type: array
          items:
            $ref: '#/components/schemas/Reason'
        artifacts:
          type: array
          items:
            $ref: 'API-L3GEN-008-v1.schema.json#/$defs/Artifact'
        metrics:
          $ref: '#/components/schemas/Metrics'
        links:
          type: object
          additionalProperties: false
          required: [self, result]
          properties:
            self: {type: string, format: uri-reference}
            result: {type: [string, 'null'], format: uri-reference}
      allOf:
        - if:
            properties: {state: {const: queued}}
          then:
            properties:
              stage: {const: queue}
              snapshot_id: {type: 'null'}
              analysis_outcome: {type: 'null'}
              started_at: {type: 'null'}
              finished_at: {type: 'null'}
              expires_at: {type: 'null'}
              result_available: {const: false}
              artifacts: {maxItems: 0}
        - if:
            properties: {state: {const: running}}
          then:
            properties:
              stage: {type: string, enum: [intake, inventory, extraction, assembly, verification, export]}
              started_at: {type: string, format: date-time}
              finished_at: {type: 'null'}
              expires_at: {type: 'null'}
              result_available: {const: false}
        - if:
            properties: {state: {enum: [completed, partial, failed]}}
          then:
            properties:
              stage: {type: 'null'}
              analysis_outcome: {type: string, enum: [completed, partial, failed]}
              finished_at: {type: string, format: date-time}
              expires_at: {type: string, format: date-time}
              artifacts:
                items:
                  properties: {status: {enum: [ready, failed, retrying]}}
        - if:
            properties: {state: {const: completed}}
          then:
            properties:
              analysis_outcome: {const: completed}
              started_at: {type: string, format: date-time}
              snapshot_id: {type: string}
              result_available: {const: true}
              artifacts:
                items:
                  properties: {status: {const: ready}}
        - if:
            properties: {state: {enum: [partial, failed]}}
          then:
            properties:
              reasons: {minItems: 1}
        - if:
            properties: {state: {const: partial}}
          then:
            properties:
              snapshot_id: {type: string}
              result_available: {const: true}
              analysis_outcome: {enum: [completed, partial]}
              started_at: {type: string, format: date-time}
        - if:
            properties: {state: {const: failed}}
          then:
            properties:
              result_available: {const: false}
              artifacts: {maxItems: 0}
        - if:
            properties: {result_available: {const: true}}
          then:
            properties:
              links:
                properties:
                  result: {type: string, format: uri-reference}
          else:
            properties:
              links:
                properties:
                  result: {type: 'null'}
    CliResult:
      type: object
      additionalProperties: false
      required: [schema_version, command, exit_code, run_id, state, analysis_outcome, output_directory, files, reasons, metrics]
      properties:
        schema_version: {const: 0.1.0}
        command: {enum: [analyze, retry, null]}
        exit_code: {enum: [0, 2, 3, 4, 75, 130]}
        run_id:
          oneOf:
            - $ref: '#/components/schemas/OpaqueId'
            - type: 'null'
        state: {enum: [completed, partial, failed, null]}
        analysis_outcome: {enum: [completed, partial, failed, null]}
        output_directory:
          type: [string, 'null']
          minLength: 1
          description: Local absolute output path when a published bundle exists; never forwarded to model or HTTP.
        files:
          type: array
          items:
            type: object
            additionalProperties: false
            required: [artifact_id, path]
            properties:
              artifact_id:
                $ref: '#/components/schemas/OpaqueId'
              path:
                type: string
                minLength: 1
                description: Ready artifact path relative to output_directory, resolved through the manifest.
        reasons:
          type: array
          items:
            $ref: '#/components/schemas/Reason'
        metrics:
          $ref: '#/components/schemas/Metrics'
      allOf:
        - if:
            properties: {run_id: {type: 'null'}}
          then:
            properties:
              state: {type: 'null'}
              analysis_outcome: {type: 'null'}
              output_directory: {type: 'null'}
              files: {maxItems: 0}
              reasons: {minItems: 1}
        - if:
            properties: {output_directory: {type: 'null'}}
          then:
            properties:
              files: {maxItems: 0}
        - if:
            properties: {command: {const: analyze}, exit_code: {const: 0}}
          then:
            properties:
              run_id: {type: string}
              state: {const: completed}
              analysis_outcome: {const: completed}
              output_directory: {type: string}
    EvidenceView:
      type: object
      additionalProperties: false
      required: [run_id, snapshot_id, evidence, content, redacted]
      properties:
        run_id:
          $ref: '#/components/schemas/OpaqueId'
        snapshot_id:
          $ref: '#/components/schemas/OpaqueId'
        evidence:
          $ref: 'API-L3GEN-004-v1.schema.json#/$defs/EvidenceRef'
        content:
          type: string
          description: Only the referenced excerpt, with secret-like values redacted, after digest verification.
        redacted:
          type: boolean
          description: True if redaction changed the excerpt. False is not a guarantee that no secret exists.
```

## 7. Ví dụ và bảng lỗi

### 7.1 Request đúng và dữ liệu status

```http
POST /api/v1/runs/github HTTP/1.1
Content-Type: application/json
X-L3GEN-Client: web-v1
Origin: http://127.0.0.1:8000

{"github_url":"https://github.com/example/service","egress_notice_version":"l3gen-egress-v1"}
```

Ví dụ `202` khi đang có lần chạy khác, run này xếp hàng; các ID và thời gian chỉ là dữ liệu minh họa, không phải run đã thực hiện. Header `Location: /api/v1/runs/run_demo_01`, `Retry-After: 2`, `Cache-Control: no-store`.

```json
{
  "run_id": "run_demo_01",
  "snapshot_id": null,
  "state": "queued",
  "stage": "queue",
  "analysis_outcome": null,
  "created_at": "2026-09-25T08:00:00Z",
  "started_at": null,
  "finished_at": null,
  "expires_at": null,
  "result_available": false,
  "reasons": [],
  "artifacts": [],
  "metrics": {"intake_ms": null, "static_analysis_ms": null, "model_ms": null, "export_ms": null, "peak_memory_bytes": null, "output_bytes": null},
  "links": {"self": "/api/v1/runs/run_demo_01", "result": null}
}
```

Ví dụ lần chạy kết thúc partial do model không chạy và diagram lỗi; file ready có thể tải ngay. `result_available=true` nghĩa ResultBundle hợp lệ đã publish, không có nghĩa mọi artifact đã tạo.

```json
{
  "run_id": "run_demo_01",
  "snapshot_id": "snap:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "state": "partial",
  "stage": null,
  "analysis_outcome": "partial",
  "created_at": "2026-09-25T08:00:00Z",
  "started_at": "2026-09-25T08:01:00Z",
  "finished_at": "2026-09-25T08:03:00Z",
  "expires_at": "2026-09-26T08:03:00Z",
  "result_available": true,
  "reasons": [
    {"code": "model_key_missing", "message": "Bước model không chạy; kết quả chỉ gồm phần đã kiểm từ code.", "action": "Xem giới hạn; cung cấp khóa qua launcher cục bộ nếu muốn chạy phân tích mới."},
    {"code": "artifact_export_failed", "message": "Diagram image chưa sinh thành công.", "action": "Thử lại artifact art_diagram_demo_0001."}
  ],
  "artifacts": [
    {"artifact_id": "art_readme_demo_00001", "kind": "readme", "path": "README.md", "media_type": "text/markdown", "status": "ready", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bytes": 1200, "error": null},
    {"artifact_id": "art_diagram_demo_0001", "kind": "diagram_image", "path": "architecture.svg", "media_type": "image/svg+xml", "status": "failed", "sha256": null, "bytes": null, "error": {"code": "RENDER_FAILED", "reason": "Renderer chưa tạo được file hợp lệ.", "retryable": true}}
  ],
  "metrics": {"intake_ms": 2400, "static_analysis_ms": 11200, "model_ms": 0, "export_ms": 1700, "peak_memory_bytes": 134217728, "output_bytes": 1200},
  "links": {"self": "/api/v1/runs/run_demo_01", "result": "/api/v1/runs/run_demo_01/result"}
}
```

GET result trả trực tiếp `API-L3GEN-008-v1#ResultBundle`, không bọc thêm `{result: ...}` và không tự dựng lại graph. Schema bundle và artifact manifest ở [API-L3GEN-008-v1](../../CMP-L3GEN-008/api/API-L3GEN-008-v1.md). UI tìm/lọc trên bundle đó và dùng evidence_id để mở bằng chứng; nội dung evidence phải qua kiểm digest lúc mở.

Ví dụ evidence response hợp lệ về schema (digest và ID minh họa, không phải bằng chứng từ repository đã chạy). Hai cột null biểu diễn trọn dòng, không được null riêng một cột; vị trí bình thường dùng hai số nguyên theo API-004.

```json
{"run_id":"run_demo_01","snapshot_id":"snap:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","evidence":{"id":"ev:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","snapshot_id":"snap:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","file_id":"file:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","path":"app/routes.py","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","start_line":10,"end_line":10,"start_column":null,"end_column":null},"content":"@router.get(\"/items\")","redacted":false}
```

### 7.2 Request sai và lỗi có cách sửa

Request chứa trường ngoài schema bị từ chối; không ghi nguyên request vào log:

```json
{"github_url":"https://github.com/example/service","egress_notice_version":"l3gen-egress-v1","repository_token":"not-a-real-token"}
```

HTTP `422`, body:

```json
{"code":"unknown_field","message":"Request chứa trường repository_token không được hỗ trợ.","action":"Bỏ trường này; chỉ sử dụng repository GitHub public và không gửi credential.","retryable":false,"run_id":null,"field":"repository_token"}
```

HTTP `409` khi snapshot thay đổi hoặc mất file; **không có `content`**:

```json
{"code":"snapshot_mismatch","message":"Snapshot không còn khớp; không thể mở bằng chứng này.","action":"Chạy phân tích mới trên source hiện tại để tạo snapshot mới.","retryable":false,"run_id":"run_demo_01","field":null}
```

| Mã | HTTP trước admission / trên GET-POST retry | Sau admission | Cách xử lý |
|---|---|---|---|
| `invalid_json`, `invalid_multipart`, `unexpected_body` | 400 | — | Sửa request đúng content/schema |
| `idempotency_key_unsupported` | 400 | — | Bỏ header; không gửi lại POST chưa rõ kết quả một cách tự động |
| `origin_rejected` | 403 | — | Mở UI trên đúng origin loopback |
| `unsupported_media_type` | 415 | — | Dùng JSON hoặc một ZIP multipart đúng endpoint |
| `unknown_field`, `invalid_github_url`, `notice_version_mismatch`, `invalid_zip` | 422 | `failed` nếu chỉ phát hiện khi intake | Sửa đầu vào hoặc tải lại UI có thông báo hiện hành |
| `compressed_size_exceeded` | 413 | — | ZIP tối đa 100 MB |
| `expanded_size_exceeded`, `file_count_exceeded`, `unsafe_archive_path` | — | `failed` | Sửa ZIP, tôn trọng 500 MB/50.000 file; không bỏ qua entry độc hại |
| `github_not_found_or_private`, `github_access_denied`, `github_timeout` | — | `failed` | Kiểm URL/public hoặc thử lại bằng run mới; không nhập credential |
| `process_interrupted` | — | `failed` | Run mới; không tự phục hồi tác vụ model |
| `run_not_found`, `evidence_not_found`, `artifact_not_found` | 404 | — | Kiểm ID thuộc đúng run; có thể dữ liệu đã bị dọn |
| `result_unavailable`, `artifact_not_ready` | 409 | — | Poll run nếu còn chạy; nếu failed đọc lý do |
| `snapshot_mismatch` | 409 | — | Phân tích mới; không hiển thị source đã đổi |
| `artifact_not_retryable`, `engine_busy` | 409 | — | Sửa nguyên nhân hoặc chờ engine; không retry model |
| `run_expired` | 410 | — | Chạy mới; dữ liệu cũ không được phục vụ |
| `engine_unavailable` | 503 | — | Sửa/khởi động engine rồi gửi request mới |
| `time_budget_exceeded`, `memory_budget_exceeded`, `model_quota_exhausted`, `model_key_missing`, `analysis_unit_failed` | — | `partial` | Xem ResultBundle giới hạn/phạm vi đã xử lý |

## 8. CLI M1

Cú pháp dưới đây là **giao diện draft** cho tên lệnh/flag/exit code; hành vi input/output/read-only là từ FR-019 và FR-025. CLI chạy engine in-process, không gọi các route HTTP.

```text
l3gen analyze --source <directory> --output <directory> [--json]
l3gen retry --output <directory> --artifact <artifact_id> [--json]
```

`analyze` xác minh source là thư mục đọc được, output hoặc cha của output ghi được, đường dẫn đã chuẩn hóa/giải liên kết và hai cây không trùng hoặc bao nhau theo cả hai hướng. **Đề xuất:** output đã tồn tại phải rỗng; từ chối output không rỗng thay vì ghi đè file. Thất bại validation không tạo output dở. Không chạy/import/cài dependency của source. Source chỉ được đọc qua snapshot CMP-002.

CLI luôn in thông báo dữ liệu tới Groq/Google trước bước đầu tiên có thể gọi model; nhận khóa qua prompt cục bộ không echo theo §5, không qua flag trên command line. Thiếu khóa vẫn cho phân tích phần code với partial có lý do. Không có flag tự đổi provider/gói trả phí. Chế độ thường in đường dẫn các file **thực sự ready**, trạng thái cuối và giới hạn; đường dẫn tuyệt đối chỉ xuất ở console cục bộ khi cần chỉ chỗ lưu, không lọt vào artifact/evidence/payload model. `--json` dành stdout cho đúng một object kết quả CLI theo `CliResult` ở §6, gồm `schema_version`, `command`, `exit_code`, `run_id`, `state`, `analysis_outcome`, `output_directory` (null nếu chưa publish), `files` (chỉ file ready), `reasons` và `metrics`. Thông báo trước chạy, tiến độ và chẩn đoán đi stderr. Đây là wrapper CLI, không phải ResultBundle hoặc RunView web; `exit_code` phải bằng mã thoát tiến trình. Khi chưa admission, run/state/outcome là null; metric chưa đo là null, không điền 0 giả. Với retry thành công, exit 0 không sửa state partial của run gốc.

`retry` đọc manifest/bundle đã kiểm của output, giải artifact_id qua manifest, không nhận source mới; lỗi không được retry khi snapshot/model đã kiểm không còn đủ. Không cập nhật artifact ready, không chạy lại phân tích/model. Output CLI do người dùng quản lý, không tự xóa sau 24 giờ.

| Exit | `analyze` | `retry` |
|---|---|---|
| 0 | Completed, tất cả artifact bắt buộc ready | Artifact ready, kể cả đã ready trước lệnh |
| 2 | Sai cú pháp, source/output sai hoặc intake bị từ chối; có cách sửa | Manifest/ID không hợp lệ hoặc artifact không retryable |
| 3 | Partial có phạm vi đã xử lý và giới hạn; có thể một artifact failed | Đã thử nhưng artifact vẫn failed; artifact ready khác giữ nguyên |
| 4 | Engine không thể publish kết quả nhất quán hoặc lỗi nội bộ | Lỗi nội bộ khi retry, không làm hỏng file đã publish |
| 75 | Engine đang bận, chưa bắt đầu run này | Engine đang bận, chưa bắt đầu retry |
| 130 | Người dùng ngắt: cố dừng có kiểm soát, chỉ publish phần hợp lệ nếu đủ điều kiện, không giả completed | Ngừng retry, bỏ staging, giữ artifact ready |

CLI một lần gọi có thể chờ FIFO khi dùng cùng engine coordinator; nếu không thể kết nối coordinator/giữ khóa cục bộ thì báo exit 75, không tạo engine thứ hai dùng chung quota. Cơ chế coordinator/khóa dùng chung giữa các tiến trình là đề xuất cần review; yêu cầu cuối cùng vẫn là tối đa một lần chạy đồng thời. Ctrl-C của CLI là tín hiệu tiến trình, không tạo route cancel HTTP hoặc cam kết hủy từ UI.

Ví dụ lỗi output bao source: `l3gen analyze --source C:\work\service --output C:\work` kết thúc exit 2, nêu `source_output_overlap`, không tạo file. Ví dụ thành công: `l3gen analyze --source C:\work\service --output C:\results\service` in file L3/diagram/JSON ready và exit 0; nếu model hết quota thì exit 3 cùng thông báo rõ phạm vi còn thiếu.

Ví dụ lỗi trước admission, chưa có run và chưa đo tài nguyên:

```json
{"schema_version":"0.1.0","command":"analyze","exit_code":2,"run_id":null,"state":null,"analysis_outcome":null,"output_directory":null,"files":[],"reasons":[{"code":"source_output_overlap","message":"Source và output bao nhau.","action":"Chọn output nằm ngoài cây source."}],"metrics":{"intake_ms":null,"static_analysis_ms":null,"model_ms":null,"export_ms":null,"peak_memory_bytes":null,"output_bytes":null}}
```

### 8.1. Binding cho consumer web — đầu vào UI cấp 4

Bảng này mô tả cách UI dùng contract, chưa phải UIS đã duyệt. Khi nhóm có UXF/SCR/UID được review, gắn ID màn hình/field thực tế vào UIS; không tạo ID hoặc approval thay nhóm.

| Tác vụ người dùng | Contract / dữ liệu | Hành vi UI bắt buộc |
|---|---|---|
| Gửi repository | POST `/api/v1/runs/github` hoặc `/api/v1/runs/zip` | Hiển thị egress notice trước submit; không có field credential/model key. Chỉ theo dõi run sau khi nhận ID; không tự gửi lại POST khi timeout chưa rõ kết quả. |
| Theo dõi | GET `/api/v1/runs/{run_id}` → RunView | Poll tối đa một request đang chờ, cách ít nhất 2 giây khi queued/running hoặc artifact đang retrying; tôn trọng Retry-After, tăng chờ khi lỗi mạng. Dừng khi terminal và không còn retry, hoặc expired/rời màn hình. Không bịa % từ tên stage. |
| Mở tổng quan/chi tiết | GET `/api/v1/runs/{run_id}/result` → ResultBundle | Chỉ mở khi result_available. Tổng quan, sơ đồ và tìm/lọc dùng cùng tập component/cạnh của bundle; không ẩn hay thêm node. |
| Phân biệt giới hạn | RunView.reasons, ResultBundle.result.limitations, render_notices | Hiển thị cả giới hạn phân tích và giới hạn xuất; không coi artifact ready là analysis completed. Unknown/partial giữ nhãn và lý do. |
| Hiểu phạm vi | ResultBundle.result.inventory | Hiển thị unit/path/mức hỗ trợ và excluded kèm reason trước kết luận kiến trúc; file được xét chưa có nghĩa parse thành công. Đọc thêm limitations, không tự tính accuracy/coverage từ node count. |
| Mở nguồn | GET `/api/v1/runs/{run_id}/evidence/{evidence_id}` | Chỉ gửi ID từ bundle; kiểm tra response vẫn thuộc run đang xem trước render. Lỗi mismatch/expired không thay bằng file source mới. |
| Tải/thử lại | GET artifact hoặc POST artifact `/retry` | Chỉ tải ready; chỉ cho retry khi failed/retryable. Không retry tự động liên tục; đang retry thì theo dõi RunView, cập nhật manifest rồi mới tải. |
| Lỗi 409/410/404 | Error.code/message/action | 409 hiển thị đúng lý do; 410 hoặc run không còn tồn tại thì ngừng polling, xóa nội dung source/result trong UI và hướng dẫn chạy lại. Không lưu source/result vào localStorage. |

Khi người dùng đổi run, hủy request phía client hoặc bỏ response của run cũ; không cho evidence/result cũ hiện dưới tên run mới. Chặn submit lặp khi request đang chờ chỉ là UX, không thay kiểm concurrency tại server. Lỗi mạng lúc POST chưa rõ admission cần báo trạng thái chưa xác định và cho người dùng chủ động xử lý, không tự tạo nhiều phiên.

## 9. Traceability và kiểm contract cần thực hiện

| AC/NFR nguồn | Phần contract | Tình huống kiểm cần có (chưa phải bằng chứng pass) |
|---|---|---|
| AC-019-01/02/03 | §8 | Thư mục đúng; không đọc/không ghi được; bao nhau cả hai chiều; không để output dở |
| AC-019-04/05; NFR-SEC-002 | §2, POST source | ZIP hỏng/bom/thoát vùng; symlink; GitHub private/không tồn tại/timeout/redirect nội bộ; không nhận credential |
| AC-024-01..04 | §3, ResultBundle | File parse/encoding lỗi, thiếu reader, quota/budget; partial và giới hạn vẫn rõ |
| AC-025-01/02/04 | GET result/artifact, API-008 | Cùng snapshot/version/model; không dangling reference/cạnh lệch; mức component |
| AC-025-03 | POST retry, §4/8 | Artifact lỗi retry được, ready giữ byte/hash, không chạy lại model hoặc gia hạn retention |
| AC-026-01 | GET run, §3 | Mỗi stage/state/reason; `queued` là chi tiết L3 cho lần chạy đang xếp hàng theo CMP-001 r2 |
| AC-026-02/03 | GET result/evidence | Các góc nhìn dùng cùng bundle, tìm/lọc và mở evidence đã kiểm snapshot |
| NFR-OPS-001 | §2/3/4 | Hàng đợi FIFO; một active run; đo riêng thời gian/memory/output; 30 phút/2 GiB |
| NFR-SEC-002; NFR-AI-002 | §4/5 | 24 giờ, restart qua hạn, không cache dữ liệu quá hạn; egress notice hai provider, secret không lưu |

Trước implement: trích YAML/schema, validate OpenAPI và JSON Schema, resolve mọi `$ref`, chạy valid/invalid examples và kiểm semantics ID/snapshot/state/time. OpenAPI diff quyết định breaking theo execution guide; chưa có consumer ack hoặc baseline đã duyệt được suy ra từ việc tạo tài liệu.

## 10. Checklist review consumer và triển khai

| Điểm cần review | Chủ trì | Điều kiện trước khi chốt |
|---|---|---|
| Trạng thái queued và restart queued; có cần giới hạn số run chờ không | Tech Lead + Product + Architect | Giới hạn chờ chưa có trong nguồn; muốn thêm thì sửa NFR-OPS-001/CMP-001 trước |
| Decimal MB cho trần ZIP và upload ngắt | Tech Lead + QA | Xác nhận đơn vị, kiểm boundary byte và upload ngắt |
| CLI command/flag/exit codes, output rỗng và coordinator đa tiến trình | Tech Lead | Kiểm M1/M2 cùng quota, source/output read-only |
| Prompt cấp khóa ngoài HTTP, lifetime/rekey của launcher và bí mật chỉ ở CMP-006 | Tech Lead + Security | Review NFR-AI-002/TM T-11 và interface runtime CMP-006 |
| Loopback/Host/Origin/X-L3GEN-Client | Tech Lead + Security | Review threat model cho web cục bộ, kiểm DNS rebinding/CSRF |
| Retry không đổi state cuối; engine busy thay vì hàng chờ retry; expiry lúc stream | Tech Lead + Product + QA | Đối chiếu AC-025-03 và lifecycle UI, chứng minh không phục vụ sau hạn |

## Nguồn

- [CMP-L3GEN-001](../../../architecture/l2/CMP-L3GEN-001.md), [CMP-L3GEN-002](../../../architecture/l2/CMP-L3GEN-002.md), [CMP-L3GEN-007](../../../architecture/l2/CMP-L3GEN-007.md), [CMP-L3GEN-008](../../../architecture/l2/CMP-L3GEN-008.md).
- [FR-L3GEN-019](../../../requirements/_superseded-r28/fr/FR-L3GEN-019.md), [FR-L3GEN-024](../../../requirements/_superseded-r28/fr/FR-L3GEN-024.md), [FR-L3GEN-025](../../../requirements/_superseded-r28/fr/FR-L3GEN-025.md), [FR-L3GEN-026](../../../requirements/_superseded-r28/fr/FR-L3GEN-026.md) (đã superseded từ PRD rev 31; revision 5 chỉ sửa link).
- [NFR-L3GEN-OPS-001](../../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-SEC-002](../../../requirements/nfr/NFR-L3GEN-SEC-002.md), [NFR-L3GEN-AI-002](../../../requirements/nfr/NFR-L3GEN-AI-002.md), [TM-SYS-L3GEN](../../../architecture/threat-model/TM-SYS-L3GEN.md).
- [Execution guide §A.1, §B.10, §C.2](../../../../docs/agentic-sdlc-execution-guide.md).
