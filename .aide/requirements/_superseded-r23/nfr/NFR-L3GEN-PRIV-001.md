---
uid: "01M2J06Z59Q60AQHASKCM2CT9A"
key: "NFR-L3GEN-PRIV-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-005","FR-L3GEN-007","FR-L3GEN-010","FR-L3GEN-012","FR-L3GEN-014","FR-L3GEN-016","FR-L3GEN-017"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-PRIV-001 — Quyền riêng tư và vòng đời dữ liệu

- **Nhóm:** Privacy.
- **Trạng thái:** ngưỡng chất lượng và vòng đời dữ liệu đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-010](../fr/FR-L3GEN-010.md), [FR-L3GEN-012](../fr/FR-L3GEN-012.md), [FR-L3GEN-014](../fr/FR-L3GEN-014.md), [FR-L3GEN-016](../fr/FR-L3GEN-016.md), [FR-L3GEN-017](../fr/FR-L3GEN-017.md).

## Yêu cầu có thể kiểm chứng

AI mặc định tắt; phải chủ động bật và biết provider, loại dữ liệu gửi. --no-ai không có outbound ở analyzer; CLI local no-AI không cần mạng; Git URL vẫn cần mạng để lấy repo đã được yêu cầu. Không đọc .env thật, private key hoặc gửi credentials. AI chỉ nhận model tối thiểu đã lọc giá trị nhạy cảm; source snippet cần đồng ý riêng và không thuộc bản đầu. Source tạm của web hết hạn trong 24 giờ sau trạng thái cuối và không được phục vụ sau hạn; output và metadata giữ tối đa 14 ngày. Khi dịch vụ đang chạy, dữ liệu hết hạn phải được dọn đúng hạn; nếu máy tắt qua hạn, lần khởi động kế tiếp phải cleanup trước khi phục vụ dữ liệu. Mỗi repository giữ tối đa 10 lần phân tích gần nhất, vượt thì loại lần cũ nhất. Người dùng xóa được một kết quả trước hạn. Hành vi cụ thể ở AC-L3GEN-017-05 và AC-L3GEN-017-06. CLI output do người dùng quản lý và ghi rõ khác biệt này.

## Điều kiện và cách kiểm

Dùng canary secrets ở .env, YAML và URL, kiểm log/output/payload không có giá trị; kiểm no-AI bằng network interception và phân biệt ingestion/analyzer. Test clock/cleanup sau hạn, hủy/lỗi và xóa sớm. Không coi bộ lọc secret là chứng minh phát hiện mọi bí mật tùy ý.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).


## Chi tiết vòng đời đã chốt tại OQ-005

GitHub repository được nhận diện bằng host/owner/name đã chuẩn hóa, không dùng branch/commit làm identity repository. ZIP dùng digest nội dung các file được tiếp nhận: ZIP khác nội dung là repository khác; không tự gộp ZIP với GitHub. UI nói rõ giới hạn này.

Giới hạn số lần áp dụng cho phiên terminal (completed/partial/failed/cancelled), theo thời điểm kết thúc; phiên đang chạy không bị eviction. Hạn ngày tính từ thời điểm terminal, áp cho cả metadata lỗi. Eviction thực hiện ngay khi phiên chuyển terminal; quá hạn không được trả kết quả. Máy tắt không bảo đảm xóa vật lý đúng giờ: lần khởi động sau phải cleanup trước khi phục vụ dữ liệu, và UI/help công khai giới hạn này. Phase đầu không cam kết SLA xóa vật lý tuyệt đối khi máy tắt; nếu về sau cần SLA đó thì phải chuyển sang dịch vụ luôn chạy và duyệt lại NFR.

Output chỉ giữ source digest, định danh commit nếu có và file/range dòng; không giữ bản sao toàn source hoặc snippet. Sau khi source tạm bị dọn, vẫn xem được vị trí bằng chứng nhưng không hứa mở nội dung source: dùng permalink commit GitHub nếu hợp lệ, hoặc yêu cầu cung cấp lại source đúng digest. Không mở source mới như bằng chứng cũ. Xóa thủ công/eviction dọn output, metadata phiên và source tạm của phiên đó; không giữ tombstone source hay dữ liệu nhạy cảm.
