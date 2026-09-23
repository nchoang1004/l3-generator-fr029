---
uid: "01M34AM2AKCTWDBD72J4X3R13C"
key: "NFR-L3GEN-SEC-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-019","FR-L3GEN-021","FR-L3GEN-025","FR-L3GEN-026"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-SEC-002 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** phạm vi đã chốt; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-019](../fr/FR-L3GEN-019.md), [FR-L3GEN-021](../fr/FR-L3GEN-021.md), [FR-L3GEN-025](../fr/FR-L3GEN-025.md), [FR-L3GEN-026](../fr/FR-L3GEN-026.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

## Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-SEC-001 và NFR-L3GEN-PRIV-001 của BL-r14.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** File nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Trần một lần tiếp nhận, giữ từ BL-r14: ZIP nén 100 MB, giải nén 500 MB, 50.000 file. Lấy source từ GitHub timeout 120 giây. Vượt trần thì từ chối kèm lý do. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Trước khi chạy, người dùng được cho biết dữ liệu nào sẽ được gửi tới provider model. Dữ liệu gửi đi gồm: tập dữ kiện đã trích (tên symbol, đường dẫn file, vị trí, giá trị literal như path của route), chữ ký hàm kèm docstring, và các đoạn code model yêu cầu qua công cụ đọc code trong giới hạn của NFR-L3GEN-AI-002. Không gửi nguyên file source hoặc cả repository. Dữ liệu đi tới hai provider: Groq và Google, theo phân việc ở NFR-L3GEN-AI-002; màn hình và dòng lệnh báo rõ cả hai. Điều khoản dùng dữ liệu của gói miễn phí là của provider; công cụ nêu tên provider, không phát biểu thay họ. Giá trị cấu hình mang dấu hiệu bí mật bị che trước khi vào bất kỳ đầu ra nào, kể cả payload gửi model.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Trên web, source đã tiếp nhận và output hết hạn 24 giờ sau trạng thái cuối của lần chạy, và không được phục vụ sau hạn. Mốc 24 giờ cho source giữ từ BL-r14; áp cho output là mới, vì lịch sử 14 ngày của BL-r14 thuộc phase sau. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn trước khi phục vụ dữ liệu. Output của dòng lệnh do người dùng quản lý.

## Điều kiện và cách kiểm

Chạy trên bộ dữ liệu chứa file nén độc hại, đường dẫn thoát vùng giải nén, symlink trỏ ra ngoài, repository vượt trần kích thước, và file cấu hình chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm payload gửi model không chứa giá trị bí mật. Kiểm dữ liệu tạm đã được dọn sau vòng đời đã công bố.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
