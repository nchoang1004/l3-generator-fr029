---
uid: "01M2J06Z54XVJ0QPKEB14CW1C7"
key: "NFR-L3GEN-COMP-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 9
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-008","FR-L3GEN-013","FR-L3GEN-014","FR-L3GEN-015","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-COMP-001 — Stack và môi trường được hỗ trợ

- **Nhóm:** Compatibility.
- **Trạng thái:** phạm vi pattern đã chốt tại OQ-L3GEN-003; chưa có kết quả kiểm capability hoặc nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-014](../fr/FR-L3GEN-014.md), [FR-L3GEN-015](../fr/FR-L3GEN-015.md).

## Yêu cầu có thể kiểm chứng

Ma trận pattern là hợp đồng phạm vi của analyzer: mỗi hàng nêu cú pháp/API/dạng file được cam kết nhận diện, phần chỉ nhận diện có giới hạn và phần không hỗ trợ. `supported` vẫn phải qua fixture và ngưỡng NFR trước khi được báo đạt; ma trận không phải bằng chứng implementation.

OQ-L3GEN-002 chốt Python/FastAPI là stack nghiệm thu phase đầu. Java/Spring Boot nằm trong roadmap phase sau và không được báo đạt ngày 09/10.

| Phase / nhóm | Supported | Partial | Unsupported hoặc để phase sau |
|---|---|---|---|
| Python runtime | Cú pháp Python 3.10–3.12 | Cấu trúc động giữ source/evidence nếu đọc được | Cú pháp ngoài dải đã công bố |
| FastAPI route | `@app`/`@router.get/post/put/patch/delete`; `include_router` và `app.mount` khi target/prefix resolve tĩnh | Factory hoặc prefix biểu thức nhưng còn giữ được evidence | `add_api_route`, registration/reflection không resolve tĩnh |
| Python data | SQLAlchemy declarative `Base`/`declarative_base`, `Column`, `ForeignKey`, `relationship` trực tiếp | Tên bảng/quan hệ biểu thức được giữ unknown kèm evidence | SQLModel, `mapped_column`, XML hoặc ORM khác trong phase đầu |
| HTTP outbound | `requests` và `httpx` | URL ghép được một phần giữ biểu thức và nhãn partial | SDK/client khác chưa có adapter |
| Config Python | `os.getenv`, `os.environ[...]`, Pydantic `BaseSettings`; `.env.example` chỉ lấy tên khóa | Key động giữ biểu thức; không đọc giá trị môi trường thật | Đọc `.env` thật hoặc suy giá trị secret |
| YAML application config | File được người dùng/cấu hình chỉ định là application config; mapping tĩnh; key lồng nhau chuẩn hóa bằng dấu chấm | Sequence hoặc template còn giữ được đường dẫn/evidence | Tự diễn giải YAML tùy ý; anchor/merge, custom tag hoặc template động không resolve |
| Kafka Python | `confluent_kafka` producer/consumer với topic literal | Topic động giữ biểu thức và nhãn partial | Broker khác Kafka hoặc Kafka SDK khác chưa có adapter |
| Manifest Python | `requirements.txt`; `[project].dependencies` trong `pyproject.toml`; giữ nguyên constraint khai báo | Import-to-package mapping không chắc chắn ghi unknown | Dependency bắc cầu hoặc resolution động |
| Java roadmap | Java 17, Spring Boot 3.x; annotation route trực tiếp; Jakarta Persistence; `@Value`; Spring Kafka; Maven `pom.xml` dependency trực tiếp | Giá trị annotation/property biểu thức nhưng còn evidence | Reflection, custom annotation, registration động, Gradle, Maven profile/property động và ORM/broker khác |

Hai stack dùng chung contract kết quả nhưng không dùng chung rule. Pattern ngoài ma trận phải hiện trong phần giới hạn, không được im lặng bỏ qua. Event chỉ hỗ trợ Kafka; broker khác nằm ngoài phạm vi.

Phiên bản runtime của chính công cụ được chọn và pin ở thiết kế.

Môi trường sử dụng đề xuất: CLI trên Windows 11 và Ubuntu 24.04, hỗ trợ tên file/path Unicode và có dấu cách; web trên Chrome và Edge. Phiên bản browser ổn định dùng để kiểm được ghi cụ thể tại thời điểm kiểm; Mermaid renderer/version pin ở contract.

## Điều kiện và cách kiểm

Chạy cùng bộ supported fixtures trên cả hai OS; ghi interpreter, package/rule/renderer/browser versions. Lỗi cú pháp do version ngoài phạm vi phải được báo rõ. Có ma trận supported/partial/unsupported thay cho một checkbox hỗ trợ cả ngôn ngữ.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).
