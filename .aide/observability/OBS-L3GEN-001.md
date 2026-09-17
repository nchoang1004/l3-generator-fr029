---
uid: "01M2J06Z3X86Z4VPQF6ZNKY1QT"
key: "OBS-L3GEN-001"
type: "observability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"measures":["KPI-L3GEN-003","KPI-L3GEN-004","KPI-L3GEN-005"],"blocked_by":["OQ-L3GEN-004"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Phương pháp đo chất lượng và tái lập

## Phạm vi

Đo sản phẩm mục tiêu, không dùng số test hay benchmark của code hiện có làm bằng chứng đạt PRD. Threshold chuẩn nằm trong NFR; OBS chỉ định nghĩa mẫu và cách đo. Kết quả hiện tại: **not_run**.

## Dataset và người làm đáp án

- Chốt trước ít nhất 3 repo public độc lập có cấu trúc khác nhau (simple app, app factory/layered, monorepo) và pin commit; lựa chọn cuối cùng ở OQ-L3GEN-004.
- Hai người đọc độc lập, chưa nhìn output công cụ, lập route/path/điều kiện, entity/table/column, HTTP, config, event và mẫu cạnh nội bộ; giữ hai bản, ghi disagreement và bản adjudicated (đáp án đã đối chiếu).
- Không chỉ lấy file tool đã phát hiện để làm đáp án. Ghi đầy đủ phạm vi file trước khi chạy; mọi loại loại trừ có lý do.
- Tổng cỡ mẫu đề xuất để báo tỷ lệ tổng hợp: route ≥100, entity ≥20, HTTP ≥30, config ≥30, event ≥20, internal call edge ≥100; component membership ≥30 và component dependency ≥20. Chưa đủ mẫu: báo TP/FP/FN, chưa kết luận đạt tỷ lệ.
- Có bộ micro fixtures cho từng pattern AC; thêm negative cases, alias/shadowing, mount, nested factory, điều kiện, dynamic pattern, unknown table, event identity và config secret.
- SDK/event không có repo đáp ứng thì dùng fixture riêng và công bố dataset category; không gộp thành tỷ lệ real-world.

## Matching và công thức

- TP là dự đoán trùng identity trong đáp án: route dựa method + handler/source range + registration context; bảng dựa entity source; HTTP/config/event dựa callsite/key/binding. Dùng matching một-một.
- Precision = TP/(TP+FP); recall = TP/(TP+FN). Mẫu số bằng 0 → not_evaluated, không ghi 100%.
- Báo riêng precision exact, inferred và toàn bộ; exact precision chỉ dùng dự đoán exact nhưng ground truth vẫn được lập độc lập. Báo recall trong pattern cam kết và recall toàn phạm vi riêng.
- Chấm thuộc tính method/path/prefix/condition/table name/topic/host riêng với số đúng/số kiểm; phát hiện tồn tại không đồng nghĩa đúng thuộc tính.
- Với partial, chấm việc giữ phần biết được và nêu thiếu đúng; không tính giá trị chưa biết là giá trị đã giải đúng.
- Component: con người chốt mapping trước, đo membership bằng tập (component identity, code entity identity); chấm cạnh gộp bằng endpoint+loại. Vai trò nghiệp vụ chưa thống nhất không ép oracle rồi báo exact.
- Evidence coverage = số claim có nguồn hợp lệ / tổng claim khẳng định. Chấm semantic support bằng mẫu người đọc, không chỉ existence của file.

## Thời gian, tài nguyên và tích hợp

Ghi source digest, commit nếu có, config digest, tool/rule/schema version, OS/interpreter/hardware, loại input, thời gian fetch/analyze/render riêng, peak RSS, kích thước output và exit/job status. NFR-L3GEN-PERF-001 sở hữu ngưỡng. Đo determinism theo NFR-L3GEN-DET-001.

KPI-L3GEN-003 đạt khi các nhóm chất lượng thuộc Must đạt ngưỡng và mẫu đủ. KPI-L3GEN-004 đo trên bộ fixture có cài sẵn lỗi cú pháp, file ngoài stack hỗ trợ và quan hệ chưa resolve được: đếm số trường hợp cài sẵn xuất hiện trong phần giới hạn của kết quả, chia cho tổng số trường hợp đã cài. Mẫu số lấy từ fixture, không lấy từ chính output — nếu không thì mọi lần chạy đều ra 100%. KPI-L3GEN-005 đạt khi công cụ đọc độc lập tiêu thụ được JSON/schema, kiểm không có dangling edge, và Mermaid render được; lưu script/version/kết quả.

## Lưu bằng chứng

Mỗi lần đo lưu trong .aide/evidence/tests/<host>-<clone>/<run-id>/, append-only; có input hashes, kết quả passed/failed/not_run và raw counts. Không log secrets. Việc sửa đáp án sau đo có revision và lý do, không xóa kết quả cũ.

