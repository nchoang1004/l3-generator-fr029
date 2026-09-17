---
uid: "01M2J06Z3HXPW1MKV9XBWJR7YW"
key: "GLOSS-L3GEN-001"
type: "glossary"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Thuật ngữ sản phẩm

| Thuật ngữ | Nghĩa dùng trong PRD |
|---|---|
| Repository | Tập source và cấu hình đầu vào tại một snapshot xác định |
| Snapshot | Nội dung cố định có digest; có thể kèm Git commit khi phù hợp |
| Đơn vị phân tích | Phần source được quét chung; manifest/thư mục là dấu hiệu, không chứng minh một service deploy độc lập |
| Service | Đơn vị triển khai khi có bằng chứng; nếu chưa đủ thì chỉ gọi là đơn vị phân tích |
| Component | Nhóm module/class/function cùng một vai trò trong service; có danh sách thành viên và căn cứ nhóm |
| L3 | Trong sản phẩm này: tài liệu cấu trúc bên trong service gồm component, interface, dữ liệu, config, event và dependency; bản kiến trúc ban đầu để người review, không tuyên bố chứng nhận C4 |
| IAM | Mô hình dữ kiện code trung gian, giữ quan sát, tham chiếu, nguồn và nhãn |
| Architecture model | Component và quan hệ được rút ra từ IAM; mọi kết luận phải truy về IAM/source |
| Dependency | Quan hệ có bằng chứng; không tự đồng nghĩa với thứ tự chạy hoặc mọi hành vi runtime |
| exact / inferred | Đọc trực tiếp từ bằng chứng / suy theo quy tắc đã công bố |
| full / partial | Biết đủ thuộc tính đã công bố / còn thuộc tính hoặc binding chưa biết; không phải mức bao phủ tuyệt đối của repo |
| unresolved / ambiguous | Chưa xác định đích / có nhiều đích không đủ bằng chứng lựa chọn |
| External library | Biết tên thư viện ngoài source quét; khác unresolved internal |
| Evidence | Một hoặc nhiều file/range thuộc snapshot và rule hỗ trợ một claim |
| Finding | Cảnh báo cần xác minh; không phải kết luận lỗi nghiệp vụ |
| FR / AC / NFR | Hành vi sản phẩm / trường hợp nghiệm thu hành vi / ràng buộc chất lượng |
| OBS | Định nghĩa cách thu và tính số đo, không bắt buộc dịch vụ telemetry online |
| Baseline | Tập revision được đem review/duyệt cùng nhau; bản đang có chỉ là candidate chưa ký |

Key GLOSS và các type metadata sẽ đối chiếu registry tổ chức tại OQ-L3GEN-001/006; chưa tự nhận đây là registry đã được duyệt.

