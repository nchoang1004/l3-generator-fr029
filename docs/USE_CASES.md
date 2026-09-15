# Use Cases — Code → L3 Generator

> Sơ đồ: [usecase-overview.svg](diagrams/usecase-overview.svg)
> Tài liệu này đặc tả phần **requirement** (ai cần gì), tách khỏi [SPEC](../SPEC_Code_to_L3_Generator.md) là phần **giải pháp** (làm thế nào).

---

## 1. Actor

| Actor | Loại | Mô tả | Quan tâm chính |
|---|---|---|---|
| **Developer** | Chính | Người chạy tool trên một repo | Hiểu nhanh một service chưa quen, không phải đọc hết code |
| **Architect / Reviewer** | Chính | Người đọc tài liệu sinh ra, không chạy tool | Đối chiếu thiết kế với code thực tế, phát hiện chỗ lệch |
| **LLM Provider** | Phụ (ngoài) | Dịch vụ LLM được gọi ở UC3, UC4 | — (là dependency, không phải người dùng) |
| **Hệ thống khác** | Phụ (ngoài) | Tool/platform đọc `graph.json` hoặc IAM về sau | Có contract ổn định để tiêu thụ dữ liệu |

**Về phạm vi stack:** giai đoạn hiện tại tool chỉ hỗ trợ Python + FastAPI, nhưng mục tiêu dài hạn là đa ngôn ngữ. Quan trọng hơn: **một repo có thể chứa nhiều service với stack khác nhau** (ví dụ ứng dụng mobile Java và AI service FastAPI trong cùng repo). Tool phải chia repo thành các đơn vị phân tích trước, nhận diện từng đơn vị sau — và khi một đơn vị dùng stack chưa hỗ trợ thì bỏ qua riêng nó, nói rõ ra, chứ không bỏ cả repo và cũng không im lặng.

**Không có actor "quản trị viên".** Tool chạy một lần rồi kết thúc: không lưu state, không đăng nhập, không phân quyền, không ghi gì vào repo đang phân tích.

---

## 2. Đặc tả use case

### UC1 · Sinh tài liệu L3 từ một thư mục source

| | |
|---|---|
| **Actor** | Developer |
| **Tiền điều kiện** | Có đường dẫn tới thư mục chứa ít nhất 1 file `.py` hợp lệ |
| **Kích hoạt** | Chạy `l3gen <path>` |
| **Kết quả** | 4 file trong thư mục output: `L3.md`, `diagram.mmd`, `graph.json`, `IAM.json` |

**Luồng chính:**
1. Developer chỉ định thư mục source
2. Hệ thống **chia repo thành các đơn vị phân tích** theo vị trí file manifest (một service triển khai độc lập = một đơn vị)
3. Hệ thống **nhận diện ngôn ngữ và framework của từng đơn vị**, báo lại danh sách cho người dùng
4. Hệ thống quét, parse, trích xuất từng đơn vị bằng bộ extractor tương ứng với stack của nó
5. Hệ thống resolve tham chiếu xuyên file trong phạm vi mỗi đơn vị
6. Hệ thống sinh tài liệu, sơ đồ và graph — mỗi thực thể mang trường chỉ rõ thuộc service nào
7. Hệ thống báo tóm tắt: danh sách đơn vị (đã phân tích / bị bỏ qua), số file, số thành phần, thời gian chạy

**Luồng thay thế:**
- *2a. Không tìm thấy manifest nào* → coi cả thư mục đầu vào là một đơn vị, nhận diện theo phần mở rộng file, ghi `confidence = partial`
- *2b. Không tìm thấy đơn vị nào có source* → báo lỗi rõ ràng, dừng (exit 1)
- *3a. Một số đơn vị dùng stack chưa hỗ trợ* → **bỏ qua riêng các đơn vị đó**, vẫn phân tích phần còn lại, ghi vào Known Limitations
- *3b. Mọi đơn vị đều chưa hỗ trợ* → dừng, liệt kê từng đơn vị kèm stack đã phát hiện và stack đang hỗ trợ
- *3c. Một đơn vị dùng nhiều framework* → ghi nhận tất cả, chạy extractor của từng cái
- *4a. Gặp file lỗi cú pháp* → bỏ qua file đó, ghi vào Known Limitations, tiếp tục
- *5a. Tham chiếu trỏ ra ngoài phạm vi đơn vị* → đánh dấu chưa resolve được, **không đoán**

**Ràng buộc:** Không bao giờ import hoặc thực thi code của repo đang phân tích (SPEC mục 3.2).

---

### UC2 · Chạy không cần AI

| | |
|---|---|
| **Actor** | Developer |
| **Quan hệ** | `«extend»` UC1 |
| **Kích hoạt** | Cờ `--no-ai`, **hoặc** tự động khi không có API key |
| **Kết quả** | Tài liệu đầy đủ nhưng không có cột "Mô tả" và mục "Review Findings" |

Use case này tồn tại vì hai lý do độc lập: (a) giai đoạn đầu dự án chưa có phần AI nhưng vẫn phải chạy được toàn bộ pipeline; (b) khi trình bày mà không có mạng hoặc API lỗi, tool vẫn phải cho ra kết quả.

**Đây là ràng buộc kiến trúc, không chỉ là một tùy chọn CLI:** tầng phân tích tĩnh không được phụ thuộc tầng AI theo bất kỳ chiều nào.

---

### UC3 · Bổ sung mô tả dễ đọc cho từng thành phần

| | |
|---|---|
| **Actor** | Developer (thụ hưởng) · LLM Provider (hệ thống ngoài) |
| **Quan hệ** | `«extend»` UC1 |
| **Tiền điều kiện** | Có API key; UC1 đã tạo xong dữ liệu |
| **Kết quả** | Mỗi route/entity/external call có thêm 1-2 câu mô tả |

**Ràng buộc cứng:** LLM chỉ được trả về trường mô tả. Không có đường nào để nó thêm/sửa/xoá một route hay entity. Ràng buộc này được cưỡng chế bằng schema, không bằng lời nhắc trong prompt (SPEC mục 8.3).

**Luồng thay thế:** *Gọi LLM thất bại* → thử lại tối đa 2 lần, vẫn hỏng thì tiếp tục không có mô tả, ghi vào Known Limitations. Không mất kết quả phân tích tĩnh.

---

### UC4 · Cảnh báo chỗ nghi ngờ thiếu sót

| | |
|---|---|
| **Actor** | Architect / Reviewer (thụ hưởng) · LLM Provider |
| **Quan hệ** | `«extend»` UC1 |
| **Kết quả** | Danh sách cảnh báo, mỗi cảnh báo kèm vị trí bằng chứng cụ thể |

Bốn loại cảnh báo được phép: tham chiếu không resolve được; route có handler rỗng hoặc không resolve được; entity không nơi nào dùng tới; external call không thấy xử lý lỗi bao quanh.

**Ràng buộc cứng:**
- Chỉ tạo cảnh báo, **không sửa dữ liệu** của UC1
- Mỗi cảnh báo bắt buộc trỏ về `file:line` cụ thể
- Không được tự tạo loại cảnh báo mới ngoài bốn loại trên
- **Nhận dữ liệu độc lập với UC3** — không đọc mô tả do UC3 sinh ra, để lỗi của bước này không lây sang bước kia

---

### UC5 · Tra nguồn gốc một dòng về `file:line`

| | |
|---|---|
| **Actor** | Architect / Reviewer |
| **Quan hệ** | `«include»` trong UC1 |
| **Kết quả** | Mọi dòng dữ liệu trong tài liệu đều dẫn về đúng vị trí trong source |

Đây là use case định nghĩa giá trị cốt lõi của sản phẩm: người đọc **không phải tin tool**, họ kiểm chứng được. Nếu một dòng không tra ngược được, đó là lỗi nghiêm trọng chứ không phải thiếu sót nhỏ.

---

### UC6 · Xem mức tin cậy và giới hạn đã biết

| | |
|---|---|
| **Actor** | Architect / Reviewer |
| **Quan hệ** | `«include»` trong UC1 |
| **Kết quả** | Mỗi dòng có nhãn `exact`/`partial`/`inferred`; mục "Known Limitations" luôn hiện diện |

Người đọc cần biết **tài liệu này đáng tin tới đâu**, không chỉ nội dung của nó. Mục Known Limitations bắt buộc xuất hiện kể cả khi rỗng — sự vắng mặt của nó khiến người đọc phải tự đoán.

---

### UC7 · Xuất graph cho hệ thống khác dùng

| | |
|---|---|
| **Actor** | Developer (chạy) · Hệ thống khác (tiêu thụ) |
| **Kết quả** | File `graph.json` với cấu trúc node/edge ổn định |

Use case này phục vụ tiêu chí "có contract rõ để tích hợp vào platform lớn sau này". Ở phạm vi hiện tại chỉ là file tĩnh — chưa có API truy vấn.

**Ràng buộc:** mọi edge trong graph phải truy ngược được về đúng một phần tử dữ liệu do UC1 tạo ra. Graph là cách trình bày khác của cùng dữ liệu, không phải nguồn tri thức mới.

---

### UC8 · Xem kết quả trên giao diện web *(phần mở rộng)*

| | |
|---|---|
| **Actor** | Developer · Architect / Reviewer |
| **Kích hoạt** | `l3gen ui ./l3-output/` |
| **Tiền điều kiện** | Đã chạy UC1 và có `IAM.json` + `graph.json` trong thư mục output |
| **Kết quả** | Giao diện web tĩnh với 6 màn hình: Tổng quan, API Routes, DB Entities, Dependency Graph, Review Findings, Known Limitations |

**Ràng buộc kiến trúc:** UI là **lớp phủ đặt lên trên**, không phải một phần của lõi:
- Chỉ đọc `IAM.json` / `graph.json` đã sinh sẵn, **không tự phân tích lại source code**
- Xoá toàn bộ thư mục UI đi thì CLI vẫn chạy đúng như cũ
- Không hiển thị thông tin nào không có trong dữ liệu gốc
- Phải phân biệt được bằng mắt đâu là dữ liệu từ AST, đâu là mô tả do AI sinh

**Lý do đưa vào phạm vi:** đọc bảng Markdown nhiều cột khá vất vả, và một đồ thị tương tác cho thấy quan hệ giữa các thành phần rõ hơn hẳn sơ đồ tĩnh. Với người xem lần đầu, đây là cách nhanh nhất để nắm được cấu trúc một service.

Chi tiết màn hình và quy tắc hiển thị: SPEC mục 13.

---

### UC9 · Xem sơ đồ phụ thuộc dạng Mermaid

| | |
|---|---|
| **Actor** | Developer · Architect / Reviewer |
| **Kết quả** | File Mermaid render được trực tiếp trên GitLab/GitHub |

Khi graph quá lớn (>40 node), sơ đồ trong tài liệu được rút gọn, bản đầy đủ nằm ở `graph.json`. Đây là đường xem nhanh ngay trong tài liệu, không cần mở giao diện web (UC8).

---

## 3. Ma trận actor × use case

| Use case | Developer | Architect/Reviewer | LLM Provider | Hệ thống khác |
|---|:---:|:---:|:---:|:---:|
| UC1 Sinh tài liệu | ● | | | |
| UC2 Chạy không cần AI | ● | | | |
| UC3 Bổ sung mô tả | ○ | ○ | ● | |
| UC4 Cảnh báo thiếu sót | | ○ | ● | |
| UC5 Tra nguồn gốc | ○ | ● | | |
| UC6 Mức tin cậy | ○ | ● | | |
| UC7 Xuất graph | ● | | | ● |
| UC8 Giao diện web *(mở rộng)* | ● | ● | | |
| UC9 Sơ đồ Mermaid | ● | ● | | |

● tham gia trực tiếp · ○ thụ hưởng kết quả

---

## 4. Ngoài phạm vi

Những use case **không** thuộc sản phẩm này, ghi rõ để tránh hiểu nhầm là thiếu sót:

- Chỉnh sửa tài liệu sinh ra từ trong tool (tool chỉ sinh, người sửa bằng công cụ khác)
- Lưu lịch sử các lần chạy, so sánh giữa hai lần
- Chạy tự động trong CI khi có commit mới
- Phân tích ngôn ngữ/framework ngoài Python + FastAPI
- Quản lý người dùng, phân quyền, đăng nhập
- Truy vấn graph qua API (chỉ xuất file tĩnh)
- Chỉnh sửa dữ liệu từ giao diện web (UI chỉ để xem, không ghi ngược lại)
- Giao diện web có backend, database hoặc lưu phiên làm việc (chỉ là site tĩnh đọc JSON)
