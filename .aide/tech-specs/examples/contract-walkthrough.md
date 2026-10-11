# Ví dụ xuyên luồng L3 — membership cố định

Ví dụ này giúp hai thành viên kiểm cách dữ liệu đi qua các contract. Đây là **fixture viết tay để kiểm giao diện**, không phải output engine, gold độc lập, kết quả gọi LLM hoặc quyết định thuật toán chia component. `fixture-membership-v1` chỉ dùng tại đây; D-03 vẫn mở.

## 1. Source minh họa

Các đoạn sau được giữ như văn bản UTF-8, xuống dòng LF và có LF cuối file. Script chỉ tính hash/kiểm range; không import, chạy hoặc cài dependency của chúng.

`api/routes.py`

```python
from fastapi import FastAPI
from storage.models import load_items

app = FastAPI()

@app.get("/items", status_code=200)
def list_items():
    return load_items()
```

`storage/models.py`

```python
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)

def load_items():
    return []
```

Ví dụ có một route, một bảng và lời gọi từ handler sang hàm hỗ trợ. **Không có bằng chứng `load_items()` đọc bảng `items`**: việc cùng file không đủ để tạo quan hệ truy cập DB. DB dialect và nullable/FK của cột được để unknown trong fixture; không dùng ví dụ này để kiểm độ đầy đủ adapter SQLAlchemy.

## 2. Đọc từng bước

| Bước / contract | Dữ liệu của ví dụ | Điều cần kiểm |
|---|---|---|
| 002 — Snapshot | Hai file, hash bytes thật, file ID theo path và snapshot ID theo manifest | Đổi một byte phải đổi hash/snapshot; range evidence phải nằm trong file |
| 003 — Inventory | Một unit `.`; cả hai file được xét; framework FastAPI/SQLAlchemy chỉ là nhãn fixture đã điền | Không chạy thuật toán tìm root/flat; `flat:false` cũng được chỉ định trước |
| 004 — Facts | Handler, hàm đích, lời gọi resolved, route GET `/items`, bảng `items` | Fact/evidence ID tính theo công thức draft; unknown giữ lý do, không bịa đọc DB |
| 005 — Model | Nhóm A nhận `api/routes.py`, nhóm B nhận `storage/models.py`; cạnh A → B loại calls; `contract_owners` gán route cho A, bảng cho B | Membership viết tay, confidence inferred; tên nhóm không tham gia ID; partition version luôn được giữ |
| 006 — LLM | Các mẫu request/response độc lập nằm ở API-006; fixture xuyên luồng không gọi provider | MODEL_NOT_RUN là giới hạn rõ ràng, không nói model đã đặt nhãn hoặc đánh giá |
| 007 — VerifiedResult | Giữ inventory/facts/model/evidence; verdict accepted viết trước cho các claim hợp lệ của fixture | Script kiểm tham chiếu/hash/range; **không chạy verifier ngữ nghĩa của sản phẩm** |
| 008 — ResultData/Bundle | JSON giữ nguyên model, export context có phiên bản/slug; mọi artifact cùng hai node và một cạnh | Hash/bytes result.json được tính từ payload thật, không placeholder; không cắt facts theo số node |
| 001 — Consumer | CLI/HTTP đọc bundle này theo schema; mẫu lifecycle/lỗi ở API-001 | Bộ này chưa dựng server/UI; không coi contract hợp lệ là endpoint đã chạy |

## 3. Đầu ra L3 kỳ vọng khi triển khai renderer

- API: route thuộc nhóm A vì `contract_owners` (CMP-005, API-005 §3.2) tìm `declaration_evidence_id` của route nằm trong `api/routes.py`. `response_model_ids` và auth unknown được công bố; không đoán schema response hoặc cơ chế xác thực.
- TBL: bảng thuộc nhóm B qua `contract_owners`. Bảng mô tả vẫn có; dialect unknown nên bảng bị bỏ khỏi DDL (`DDL_TABLE_OMITTED`), khối `sql` chỉ có comment (`DDL_BLOCK_OMITTED`), theo API-008 §3.2.
- Diagram: hai component và một cạnh calls; không thêm DB/external node hoặc cạnh đọc bảng chưa có evidence.
- JSON: giữ cả bảng/route/unknown và evidence; không chỉ hai node trên sơ đồ.

JSON dẫn xuất bên dưới chỉ minh họa **artifact JSON** để kiểm composition và checksum. README/API/TBL/Mermaid do code lát cắt đầu sinh, xem [slice/README.md](../../../slice/README.md); SVG chưa có. Không dùng manifest ví dụ làm chứng nhận đủ bộ export FR-025/027. Ca renderer thành công, partial, lỗi và retry nằm trong API-008.

## 4. Chạy lại và kiểm tra

Chạy từ gốc repository:

```powershell
scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py --report
```

[Script](../../../scripts/check_l3_contracts.py) đọc đúng hai khối Python ở trên, dựng payload viết tay và kiểm từng schema. File dẫn xuất nằm ở `.aide/generated/contract-checks/L3-WALKTHROUGH.json`: các khóa `snapshot`, `inventory`, `facts`, `architecture`, `verified`, `bundle` và `result_json` cho phép theo dõi cùng ID qua từng bước. Chỉ sửa spec/script nguồn rồi chạy lại, không sửa riêng JSON dẫn xuất.

Các ca âm kiểm việc từ chối hash/range sai, tham chiếu lạ, file thuộc hai component, phiên bản bị thiếu, model quá 50 node, owner trỏ component không chứa file khai báo, artifact hash sai, slug/notice sai và payload LLM vượt task. Chúng kiểm chất lượng contract; không thay kiểm an toàn intake, thuật toán chia nhóm, binding thật, accuracy, NFR hay gate.

## 5. Những phần vẫn chưa kết luận

D-03 cần thí nghiệm trên source/gold độc lập trước khi chọn thuật toán. Không suy rằng hai thư mục ở ví dụ này chứng minh chia theo thư mục là tốt nhất. Các nhãn/verdict viết tay chỉ để kiểm giao diện; gold phải được lập và review độc lập với output của sản phẩm/fixture, rồi đánh giá kiến trúc thực tế theo OBS.
