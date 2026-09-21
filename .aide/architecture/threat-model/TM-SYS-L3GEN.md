---
uid: "01M312MS4TBJ2HG5CE61ZS719F"
key: "TM-SYS-L3GEN"
type: "threat-model"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "approved"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"constrains":["CMP-L3GEN-INTAKE","CMP-L3GEN-EXTRACT","CMP-L3GEN-PRESENT","CMP-L3GEN-RUN"],"derived_from":["ADR-2026-002"]}
verified_at: 2026-09-21
verified_against: [{"key":"ADR-2026-002","revision":2},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# TM-SYS-L3GEN — Threat model

- **Trạng thái:** approved. Khiêm xác nhận giả định nền ngày 21/09/2026, trong đó
  có điểm then chốt: **web chỉ chạy cục bộ hoặc workspace tin cậy**.
- **Ngày soạn:** 2026-09-21.
- **Chưa có kết quả kiểm thử an toàn.** Tài liệu này liệt kê mối đe doạ và biện pháp thiết
  kế; nó **không** phải bằng chứng hệ thống đã an toàn. NFR-SEC-001 yêu cầu kiểm thử an
  toàn trước khi phát hành web.

## 1. Giả định nền

| Giả định | Hệ quả nếu sai |
|---|---|
| Web chạy trên máy cục bộ hoặc workspace tin cậy, **không** mở ra Internet | Cần authentication, phân quyền và một threat model khác hẳn |
| Người vận hành tin cậy; không có phân quyền nhiều vai | Mọi biện pháp dưới đây đều giả định người chạy có toàn quyền trên máy đó |
| Repository đầu vào **không** tin cậy | Đây là giả định trung tâm của tài liệu này |
| Phase đầu chỉ nhận GitHub public qua HTTPS | Private repository và credential nằm ngoài phạm vi |

Giả định thứ ba là điểm mấu chốt: **source đầu vào là dữ liệu của kẻ tấn công tiềm năng.**
Người dùng có thể phân tích một repository bất kỳ tải từ Internet.

## 2. Tài sản cần bảo vệ

| Tài sản | Vì sao |
|---|---|
| Máy chạy công cụ | Không được để repository đầu vào thực thi bất cứ thứ gì |
| Filesystem ngoài vùng làm việc | Không được đọc hoặc ghi ra ngoài vùng được cấp |
| Bí mật trong repository đầu vào | Không được lộ ra output, log hay payload gửi AI |
| Mạng nội bộ của người dùng | Không được dùng công cụ làm bàn đạp quét mạng trong |
| Tính đúng của kết quả | Kết quả sai lệch có chủ ý cũng là một dạng thiệt hại |

## 3. Bề mặt tấn công

ADR-2026-002 dồn tiếp nhận về một component, nên bề mặt tập trung ở đó.

| Bề mặt | Component | Mức rủi ro |
|---|---|---|
| Nội dung file trong repository | `CMP-L3GEN-EXTRACT` | Cao — nội dung do kẻ tấn công soạn |
| Cấu trúc file ZIP | `CMP-L3GEN-INTAKE` | Cao |
| URL Git và chuỗi chuyển hướng | `CMP-L3GEN-INTAKE` | Cao |
| Đường dẫn thư mục local | `CMP-L3GEN-INTAKE` | Trung bình |
| Dữ liệu gửi tới nhà cung cấp AI | `CMP-L3GEN-PRESENT` | Trung bình |
| Nội dung artifact xuất ra | `CMP-L3GEN-PRESENT` | Trung bình |

## 4. Mối đe doạ và biện pháp

### T-01 — Thực thi code của repository đầu vào

**Kịch bản:** repository chứa `setup.py`, `conftest.py` hoặc module có tác dụng phụ khi
import. Công cụ import nó để "hiểu rõ hơn" và code chạy trên máy người dùng.

**Biện pháp:** bất biến miền #2 cấm tuyệt đối import, chạy, `exec`/`eval`, cài dependency,
chạy Git hook và submodule. Chỉ phân tích cú pháp tĩnh. `CMP-L3GEN-EXTRACT` mục 1 ghi rõ
ràng buộc này.

**Cách kiểm:** repository sentinel tạo file hoặc gọi mạng khi bị import; chạy phân tích và
xác nhận không có tác dụng phụ nào.

**Rủi ro còn lại:** lỗ hổng trong chính thư viện phân tích cú pháp. Giảm bằng cách pin
phiên bản và theo dõi thông báo bảo mật.

### T-02 — Ghi file ra ngoài vùng làm việc

**Kịch bản:** ZIP chứa mục tên `../../../.ssh/authorized_keys`, hoặc symlink trỏ ra ngoài
vùng giải nén.

**Biện pháp:** Boundary guard trong `CMP-L3GEN-INTAKE` kiểm **mọi** mục trước khi ghi.
Đường dẫn thoát vùng và symlink trỏ ra ngoài bị từ chối. Từ chối là **toàn bộ**, không
giải nén phần còn lại.

**Cách kiểm:** ZIP có traversal và symlink; xác nhận không file nào được ghi ra ngoài vùng
xử lý và lỗi được báo rõ.

### T-03 — Dùng công cụ để quét mạng nội bộ

**Kịch bản:** người dùng nhập URL trỏ tới `127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`
(điểm cuối metadata của máy chủ đám mây), hoặc một tên miền công khai chuyển hướng tới đó.

**Biện pháp:** chỉ chấp nhận HTTPS tới GitHub public. Từ chối host khác, địa chỉ
private/loopback/link-local. **Kiểm lại đích kết nối sau khi phân giải DNS và sau mỗi lần
chuyển hướng** — kiểm một lần lúc nhận URL là không đủ, vì tên miền có thể phân giải sang
địa chỉ nội bộ.

**Cách kiểm:** URL nội bộ trực tiếp; tên miền phân giải sang địa chỉ nội bộ; chuỗi chuyển
hướng ra ngoài allowlist.

### T-04 — Bí mật trong repository lộ ra ngoài

**Kịch bản:** repository có `.env` chứa khoá thật. Công cụ đọc cấu hình (FR-014) và ghi
giá trị vào tài liệu xuất ra, hoặc gửi kèm khi gọi AI.

**Biện pháp:** FR-014 yêu cầu hiện **khoá cấu hình và nơi dùng**, không hiện giá trị.
NFR-PRIV-001 cấm đọc `.env` thật và khoá riêng. AI chỉ nhận model tối thiểu đã lọc; đoạn
source chỉ gửi khi có đồng ý riêng và không thuộc phạm vi phase đầu.

**Cách kiểm:** cài bí mật mồi trong `.env`, YAML và URL; kiểm log, output và payload gửi
đi đều không chứa giá trị.

**Rủi ro còn lại được ghi nhận thẳng:** bộ lọc bí mật **không** phát hiện được mọi dạng bí
mật tuỳ ý. NFR-PRIV-001 nói rõ không được coi bộ lọc là bằng chứng phát hiện đủ. Đây là
giới hạn phải công bố cho người dùng, không phải vấn đề sẽ khắc phục hết.

### T-05 — Cạn kiệt tài nguyên

**Kịch bản:** ZIP bom giải nén thành hàng trăm GB; repository có tệp sinh tự động gây bùng
nổ số ứng viên khi phân giải; vòng lặp kế thừa làm bộ phân giải không dừng.

**Biện pháp:** trần tiếp nhận ở NFR-PERF-001 (ZIP 100 MB, giải nén 500 MB, 50.000 file).
Ngân sách của `CMP-L3GEN-RUN` cắt theo thời gian và bộ nhớ. Chạm trần thì kết quả là
`partial` kèm lý do, không treo và không im lặng (bất biến #10).

**Cách kiểm:** ZIP bom; fixture gây nhiều ứng viên và vòng lặp; xác nhận dừng đúng và báo
`partial`.

### T-06 — Đường dẫn máy người dùng lộ trong artifact

**Kịch bản:** người dùng chia sẻ tài liệu xuất ra; nó chứa đường dẫn tuyệt đối để lộ tên
người dùng hoặc cấu trúc thư mục nội bộ.

**Biện pháp:** evidence dùng đường dẫn tương đối so với gốc đầu vào. Đường dẫn tuyệt đối
của vùng làm việc thuộc run metadata, không vào artifact công khai.

**Cách kiểm:** kiểm mọi artifact không chứa đường dẫn tuyệt đối của máy chạy.

### T-07 — Dữ liệu tồn tại quá hạn

**Kịch bản:** người dùng phân tích một repository nhạy cảm; bản sao source còn trên máy
sau nhiều tháng.

**Biện pháp:** NFR-PRIV-001 chốt source tạm của web hết hạn 24 giờ sau trạng thái cuối,
output và metadata giữ tối đa 14 ngày, mỗi repository giữ tối đa 10 lần gần nhất, người
dùng xoá được trước hạn. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn **trước khi**
phục vụ dữ liệu.

**Cách kiểm:** test đồng hồ và dọn dẹp sau hạn; test hủy giữa chừng; test xoá sớm.

**Rủi ro còn lại được ghi nhận thẳng:** máy cá nhân **không** chứng minh được thời điểm
xoá vật lý tuyệt đối khi máy tắt. OQ-L3GEN-005 đã chấp nhận giới hạn này với điều kiện
công bố cho người dùng. Đầu ra của dòng lệnh do người dùng tự quản lý, không theo chính
sách hết hạn này.

### T-08 — Kết quả bị bóp méo có chủ ý

**Kịch bản:** repository được soạn sao cho công cụ kết luận sai — ví dụ tên giống API
framework để tạo quan hệ không có thật, che giấu một lời gọi ra ngoài.

**Biện pháp:** bộ diễn giải chỉ khớp ký hiệu đầy đủ và khoảng phiên bản, không khớp theo
tên ngắn. Quan hệ chưa phân giải không thành cạnh kiến trúc (bất biến #3). Mọi kết luận
đều có bằng chứng truy về nguồn để người đọc tự kiểm.

**Rủi ro còn lại:** phân tích tĩnh **không** phát hiện được mọi cách che giấu. Mục tiêu
của sản phẩm là tài liệu kiến trúc, **không phải** kiểm toán bảo mật. Glossary đã ghi rõ
`finding` không phải kết luận lỗ hổng bảo mật.

## 5. Tóm tắt theo component

| Component | Mối đe doạ chính | Mức |
|---|---|---|
| `CMP-L3GEN-INTAKE` | T-02, T-03, T-05, T-07 | **Cao — chịu phần lớn bề mặt tấn công** |
| `CMP-L3GEN-EXTRACT` | T-01, T-05, T-08 | Cao |
| `CMP-L3GEN-PRESENT` | T-04, T-06 | Trung bình |
| `CMP-L3GEN-RUN` | T-05, T-07 | Trung bình |
| `CMP-L3GEN-INVENTORY` | Không trực tiếp; kế thừa ranh giới của `INTAKE` | Thấp |
| `CMP-L3GEN-ARCH` | Không trực tiếp; chỉ xử lý dữ kiện nội bộ | Thấp |
| `CMP-L3GEN-EVIDENCE` | Không trực tiếp | Thấp |

## 6. Việc phải làm trước khi phát hành web

NFR-SEC-001 ghi: *"Threat model và kiểm thử an toàn bắt buộc trước web release; chưa có
kết quả kiểm."*

| Việc | Trạng thái |
|---|---|
| Threat model | Bản này — **approved** ngày 21/09/2026 |
| Kiểm thử T-01 đến T-08 | **Chưa chạy** |
| Quyết định phạm vi mạng của web | Cục bộ hoặc workspace tin cậy; mở Internet cần quyết định mới |

## 7. Liên kết

- [NFR-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md) — an toàn khi tiếp nhận và phân tích.
- [NFR-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md) — riêng tư và vòng đời dữ liệu.
- [NFR-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md) — trần tài nguyên.
- [ADR-2026-002](../adr/ADR-2026-002.md) — trục chia component.
- [Glossary và bất biến miền](../../domain/glossary-core.md).
