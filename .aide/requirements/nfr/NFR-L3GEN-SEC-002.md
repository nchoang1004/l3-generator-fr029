---
uid: "01M34AM2AKCTWDBD72J4X3R13C"
key: "NFR-L3GEN-SEC-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-SEC-002 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** revision 4 (02/10/2026): provider đổi sang OpenRouter theo NFR-L3GEN-AI-002; đợt này chỉ có dòng lệnh. Revision 5 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: bằng chứng kiểm trên snapshot gốc, đầu ra hiện bản đã che; phần ZIP, GitHub, web chỉ áp khi có FR tương ứng. Revision 6 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: dữ liệu gửi model dẫn về một chỗ (NFR-L3GEN-AI-002); thông báo trước khi gửi có AC. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../fr/FR-L3GEN-028.md), [FR-L3GEN-029](../fr/FR-L3GEN-029.md), [FR-L3GEN-030](../fr/FR-L3GEN-030.md), [FR-L3GEN-031](../fr/FR-L3GEN-031.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

## Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-SEC-001 và NFR-L3GEN-PRIV-001 của BL-r14.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** Đợt này chỉ nhận thư mục cục bộ qua dòng lệnh: thư mục source và output không được lồng nhau, công cụ không ghi vào cây source, symlink trỏ ra ngoài thư mục source không được đọc. Phần còn lại của đoạn này chỉ áp khi có FR nhận ZIP hoặc GitHub (phase sau): file nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Trần một lần tiếp nhận, giữ từ BL-r14: ZIP nén 100 MB, giải nén 500 MB, 50.000 file. Lấy source từ GitHub timeout 120 giây. Vượt trần thì từ chối kèm lý do. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Dữ liệu gửi tới provider model đúng như mục "Đầu vào gửi cho model" của NFR-L3GEN-AI-002, không thêm gì ngoài danh sách đó. Không gửi nguyên file source hoặc cả repository. Trước request đầu tiên, dòng lệnh in tên provider, tên model và loại dữ liệu sẽ gửi (AC-L3GEN-028-01). Dữ liệu đi tới OpenRouter, chuyển tiếp tới nhà cung cấp model; dòng lệnh báo tên provider và model trước khi gửi. Điều khoản dùng dữ liệu là của provider; công cụ nêu tên, không phát biểu thay họ.

**Bí mật trong dòng code.** Code kiểm bằng chứng nguyên văn trên snapshot gốc. Dòng chứa giá trị mang dấu hiệu bí mật (mật khẩu trong URL kết nối, khóa API, token) hiện ở mọi đầu ra và trong payload gửi model với giá trị đã che, kèm đánh dấu "đã che". Giá trị gốc không xuất hiện trong output, log hay payload.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Dòng lệnh không giữ source hay dữ liệu tạm ngoài thư mục output người dùng chỉ định; dữ liệu tạm xóa khi lần chạy kết thúc. Khi có FR web: source đã tiếp nhận và output hết hạn 24 giờ sau trạng thái cuối của lần chạy, và không được phục vụ sau hạn. Mốc 24 giờ cho source giữ từ BL-r14; áp cho output là mới, vì lịch sử 14 ngày của BL-r14 thuộc phase sau. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn trước khi phục vụ dữ liệu. Output của dòng lệnh do người dùng quản lý.

## Điều kiện và cách kiểm

Đợt này chạy trên bộ dữ liệu chứa symlink trỏ ra ngoài, source và output lồng nhau, file cấu hình và URL kết nối chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm dòng lệnh in thông báo trước request đầu tiên, và payload chỉ chứa các mục của NFR-L3GEN-AI-002. Kiểm dòng chứa bí mật vẫn qua bước kiểm nguyên văn, còn output, log và payload gửi model chỉ có bản đã che. Kiểm dữ liệu tạm đã được dọn khi lần chạy kết thúc. Khi có FR ZIP hoặc GitHub, thêm file nén độc hại, đường dẫn thoát vùng giải nén và repository vượt trần.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
