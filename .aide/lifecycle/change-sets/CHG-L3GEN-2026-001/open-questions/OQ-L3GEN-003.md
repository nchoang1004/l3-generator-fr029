---
uid: "01M2J06Z3PC3FFNMP5HZX88KZV"
key: "OQ-L3GEN-003"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm và Hoàng"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-003 — Chốt ma trận pattern và adapter hỗ trợ

## Quyết định cuối cùng ngày 18/09/2026

**Người quyết định:** Khiêm và Hoàng trong phạm vi quyền mentor đã trao cho nhóm.

**Ma trận pattern là gì:** đây là hợp đồng phạm vi của analyzer, liệt kê cụ thể cú pháp, framework API và dạng file mà công cụ cam kết nhận diện (`supported`), chỉ nhận diện có giới hạn (`partial`) hoặc chưa hỗ trợ (`unsupported`). Ma trận không phải bằng chứng code đã làm xong; capability chỉ được báo đạt sau khi fixture và phép đo tương ứng pass.

**Đã chốt:** nguồn chuẩn là NFR-L3GEN-COMP-001 revision 8.

- Phase đầu dùng Python 3.10–3.12; FastAPI decorator trực tiếp cùng `include_router`/`app.mount` resolve tĩnh; SQLAlchemy declarative `Column`; `requests`/`httpx`; `os.getenv`/`os.environ`/Pydantic `BaseSettings`; `confluent_kafka`; `requirements.txt` và `[project].dependencies`.
- SQLModel, `mapped_column`, `add_api_route` và dependency resolution động không thuộc phase đầu.
- YAML chỉ được diễn giải khi file được chỉ định là application config và có mapping tĩnh. Key lồng nhau chuẩn hóa bằng dấu chấm; sequence, anchor/merge, custom tag hoặc template động phải ghi partial/unsupported, không đoán.
- Java roadmap dùng Java 17/Spring Boot 3.x, annotation route trực tiếp, Jakarta Persistence, `@Value`, Spring Kafka và Maven `pom.xml`. Reflection, custom annotation, đăng ký động, Gradle và resolution động nằm ngoài phạm vi ban đầu của phase Java.
- Pattern ngoài ma trận phải xuất hiện trong phần giới hạn; không được im lặng bỏ qua hoặc báo repository không có dữ kiện.

**Kết quả:** OQ được đóng và không còn chặn FR-003/004/014/015/018 hoặc NFR-COMP. Java vẫn thuộc phase sau theo OQ-002.

## Câu hỏi gốc — đã giải quyết

Product đã chốt hai stack: Python/FastAPI là stack thứ nhất, Java/Spring Boot là stack thứ hai, event giới hạn ở Kafka. Phần này đã vào NFR-L3GEN-COMP-001, FR-L3GEN-015 và PRD mục IV.

Phần chưa chốt là **ma trận pattern cụ thể** trong từng stack:

1. Phía Python: SQLModel, `mapped_column` và `add_api_route` thuộc phạm vi bắt buộc hay phase mở rộng.
2. Phía Java: annotation nào của Spring Boot, ORM nào và thư viện Kafka nào được coi là hỗ trợ.
3. Schema YAML cấu hình nào được phép diễn giải.

- **Owner theo vai:** Tech Lead được mentor chỉ định.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-003, FR-L3GEN-004, FR-L3GEN-014, FR-L3GEN-015 và NFR-L3GEN-COMP-001.
- **Cách xử lý trong bản nháp:** Không nói hỗ trợ mọi repo; công bố pattern cụ thể và cảnh báo phần chưa hỗ trợ.
- **Trả lời một phần, ngày 17/09/2026.** Product đã chốt phần chọn stack và phạm vi event như nêu ở trên. Phần ma trận pattern trong từng stack vẫn cần Tech Lead quyết.

## Ảnh hưởng khi chưa chốt — lịch sử

FR-L3GEN-003 và FR-L3GEN-004 hiện có AC cho Java (AC-003-06, AC-004-06) nhưng cố ý viết ở mức nguyên tắc, vì ma trận annotation chưa có. Không thể lập implementation target cho phần Java trước khi Tech Lead chốt mục 2 ở trên.

Pattern ngoài ma trận phải hiện ở phần giới hạn của kết quả, không im lặng bỏ qua.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


## Phương án chuẩn bị review ngày 17/09/2026 — lịch sử

Ma trận tối thiểu đề xuất đã đặt tại NFR-L3GEN-COMP-001 để chỉ có một nguồn: Java 17/Spring Boot 3.x, annotation HTTP trực tiếp, Jakarta Persistence, @Value, Spring Kafka literal; Python theo ma trận hiện có. SQLModel/mapped_column/add_api_route đề xuất mở rộng sau. FR-018 đề xuất requirements.txt, pyproject.toml [project].dependencies và Maven pom.xml dependency trực tiếp; Gradle và resolution động ngoài bản đầu.

Phương án đã được chấp nhận và cụ thể hóa tại quyết định ngày 18/09/2026. Fixture/repo dùng để đo vẫn được xử lý ở OQ-004; việc chốt ma trận không đồng nghĩa capability đã triển khai hoặc đã pass benchmark.
