# l3gen

`l3gen` đọc source code bằng static analysis và sinh tài liệu kiến trúc L3.

Mục tiêu của V2 là trả lời:

- repository có application/component nào;
- application cung cấp API nào;
- component nào phụ thuộc component nào;
- component nào dùng DB, external system hoặc event;
- mỗi kết luận được chứng minh bởi dòng source nào;
- phần nào tool chưa đọc được.

Chi tiết function/call có thể được dùng làm bằng chứng nội bộ. Diagram L3 mục tiêu
không liệt kê mọi function, class hoặc biến.

> **Trạng thái chuyển đổi V2 (16/09/2026):** pipeline hiện đã có inventory, Python
> frontend, resolver/dataflow và adapter FastAPI/SQLAlchemy/HTTP. Output hiện còn thiên
> về route/entity/external và graph mức function/class. Component synthesis và
> architecture projection theo SPEC V2 chưa hoàn chỉnh. Không dùng README này để hiểu
> rằng V2 đã đạt Definition of Done.

## 1. Chạy thử

Yêu cầu Python 3.10 trở lên.

```bash
pip install -e .
l3gen tests/fixtures/python/fastapi/sample_app --no-ai -o out
```

Kết quả hiện tại:

| File | Nội dung |
|---|---|
| `L3.md` | Tài liệu Markdown |
| `diagram.mmd` | Sơ đồ Mermaid rút gọn |
| `graph.json` | Graph hiện tại; còn chứa chi tiết function/class trong giai đoạn chuyển đổi |
| `IAM.json` | Dữ liệu phân tích và kiến trúc hiện tại |
| `inventory.json` | File đã phát hiện, trạng thái và lý do bỏ qua |
| `findings.json` | Finding từ detector/reviewer |
| `descriptions.json` | Chỉ có khi AI sinh mô tả |
| `run.json` | Thông tin lần chạy và thời gian từng bước |

Xem bằng giao diện:

```bash
l3gen ui out
```

UI chỉ đọc output đã sinh; nó không phân tích source lại.

## 2. Output mục tiêu của V2

### L3 document

L3 mục tiêu gồm:

1. coverage;
2. applications và components;
3. API routes;
4. data entities/stores;
5. external systems;
6. events/configurations quan trọng;
7. component dependencies;
8. evidence;
9. findings và known limitations.

### Diagram

Diagram phải tổng quát hóa:

```text
Order API → Order Service → Order Repository → Orders DB
                          └→ Payment Gateway
```

Không dùng diagram chính để vẽ chuỗi mọi function call. Function-level path chỉ dùng
khi người đọc mở evidence.

### Architecture graph

Public graph mục tiêu chứa application/component/API/data/external/event. Graph kỹ
thuật mức function, nếu còn giữ để chẩn đoán, phải được tách hoặc đánh dấu rõ và không
được coi là L3 mặc định.

## 3. Nguyên tắc an toàn và độ tin cậy

- Không import hoặc chạy code của repository đầu vào.
- Không đoán framework chỉ từ tên biến/method.
- Không coi folder hoặc language group là service.
- Không tạo architecture edge từ unresolved raw call.
- Mọi relation L3 phải có evidence về `file:line`.
- `resolved` không có nghĩa câu lệnh chắc chắn được thực thi.
- Điều kiện, phần phụ thuộc runtime và budget phải xuất hiện trong limitations.
- AI không được thêm/sửa/xóa structural fact hoặc edge.

Ví dụ:

```python
disk_manager.mount("/dev/sdb")
```

Không được trở thành `MountApplication` chỉ vì method tên `mount`.

Ví dụ runtime:

```python
handler_name = config["handler"]
handler = getattr(module, handler_name)
handler()
```

Nếu không có configuration, kết quả đúng là `runtime` kèm lý do, không phải chọn
một handler có vẻ phù hợp.

## 4. Phạm vi hiện tại

Frontend phân tích đang tập trung Python. Các adapter hiện có trong source bao gồm:

- FastAPI/Starlette ở phạm vi rule hiện có;
- SQLAlchemy/SQLModel;
- httpx/requests.

File ngôn ngữ khác vẫn được inventory ghi nhận nhưng chưa có frontend tương ứng.

Những phần của đề bài gốc chưa hoàn chỉnh trong V2:

- component synthesis cho service/business/repository layer;
- event/queue relationship;
- configuration relationship ở mức kiến trúc;
- component-level Mermaid/graph contract;
- phân biệt đầy đủ declared registration với potentially reachable;
- framework version range trong registry.

## 5. CLI

```bash
l3gen <source-dir> [options]
```

| Tùy chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `-o, --output <dir>` | `./l3-output` | Nơi ghi kết quả |
| `--no-ai` | tắt | Không gọi AI |
| `--exclude <name>` | danh sách mặc định | Thư mục bỏ qua; dùng nhiều lần được |
| `--fail-on-empty` | tắt | Exit 1 nếu không có route/entity |
| `-v, --verbose` | tắt | In metrics chi tiết |
| `--version` | | In phiên bản |

UI:

```bash
l3gen ui <output-dir> [-p PORT] [--no-browser]
```

Mã thoát:

| Mã | Nghĩa |
|---|---|
| 0 | Thành công |
| 1 | Lỗi input hoặc điều kiện `--fail-on-empty` |
| 2 | Lỗi không lường trước |

## 6. AI là tùy chọn

Không có API key, tool tự chạy static-only. Muốn bảo đảm không gọi AI:

```bash
l3gen <source-dir> --no-ai -o out
```

Cài dependency AI:

```bash
pip install -e ".[ai]"
```

Biến môi trường:

- `L3GEN_API_KEY`;
- `ANTHROPIC_API_KEY` nếu biến trên không có.

AI chỉ viết description hoặc diễn đạt lại finding đã có. Structural artifacts phải
giống nhau khi bật/tắt AI.

## 7. Giới hạn

Static analysis không thể biết dữ liệu chỉ xuất hiện lúc runtime, ví dụ environment,
database-loaded plugin, reflection hoặc dynamic import.

Các giới hạn implementation cần kiểm chứng thêm:

- source root/module trùng tên;
- context sensitivity khi một function được gọi với nhiều object khác nhau;
- application factory tạo nhiều instance;
- conditional/unreached registration;
- adapter compatibility theo framework version;
- budget/candidate truncation;
- memory/thời gian trên repository lớn.

Không dùng số test, precision/recall hoặc benchmark cũ như bằng chứng cho V2. Các con
số chỉ được đưa trở lại README sau khi chạy trên đúng contract và source hiện tại.

## 8. Tài liệu

| File | Nội dung |
|---|---|
| [ARCHITECTURE_V2_IDEA.md](docs/ARCHITECTURE_V2_IDEA.md) | Pipeline và ranh giới phân tích |
| [USE_CASES.md](docs/USE_CASES.md) | Nhu cầu người dùng |
| [SCENARIOS.md](docs/SCENARIOS.md) | Hành vi cần đạt |
| [SPEC_Code_to_L3_Generator.md](SPEC_Code_to_L3_Generator.md) | Contract V2 |
| [HANDOFF.md](docs/HANDOFF.md) | Hiện trạng và việc tiếp theo |
| [AGENTIC_SDLC_LOG.md](docs/AGENTIC_SDLC_LOG.md) | Nhật ký quyết định/thay đổi |

EVALUATION và examples đang tạm hoãn trong giai đoạn chốt requirement.

## 9. Phát triển

Cài dependency dev và chạy test:

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Việc cần làm tiếp theo không phải mở rộng resolver cho mọi Python pattern. Thứ tự là:

1. viết acceptance test cho architecture relation;
2. tạo Architecture IAM/projection;
3. component synthesis;
4. đổi Markdown/Mermaid/graph/UI sang component view;
5. đo đóng góp của resolver và chỉ đơn giản hóa dựa trên kết quả;
6. sau đó mới cập nhật EVALUATION/examples.
