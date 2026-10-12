# Review gold FR-029: 6 fixture `fr029/` và `fr029_e2e`

Người review: Claude (agent độc lập), 07/10/2026. Chỉ đọc. Không chạy code fixture.

## Kết luận

Không tìm thấy giá trị chính sai (A), alternate nhận đáp án sai (B) hay mục bị bỏ sót (C) trong 6 fixture của `fr029/`. Mọi `file:dòng` trong gold đã được in ra và khớp source. Route, tham số, body, response, status và trường model khớp oracle. Có 2 lỗi nhỏ ở `fr029_e2e.gold.json`: gold thiếu `alt_lines` cho hai file. Vì vậy công cụ trích đúng một dòng dấu hiệu khác vẫn bị chấm sai (xếp loại E, nguyên nhân nằm ở gold). Có 8 chỗ gold là phán đoán theo cách đọc FR-029 (D). Các chỗ này không sai, nhưng bộ chấm so khớp chính xác và không có alternate, nên cách đọc khác của công cụ sẽ bị tính sai.

## Đã kiểm gì

| Fixture | Route | Tham số | Body / response / status | Model (trường) | HTTP | Vai trò file | Giới hạn / bị loại / out_of_scope | Đối chiếu oracle |
|---|---|---|---|---|---|---|---|---|
| prefix_chain | 11 (gồm `registration`) | 4 | 11 / 11 / 11 | 0 | — | — | 0 / 0 / — | Có, gồm `mounted_openapi` |
| params_models | 11 | 12 | 11 / 11 / 11 (5 có body) | 5 (17) | — | — | 0 / 0 / — | Có |
| pydantic_v1 | 2 | 2 | 2 / 2 / 2 | 1 (3) | — | — | 0 / 0 / — | Có, gồm `allow_none` |
| exclusions | 1 | 0 | 1 / 1 / 1 | 0 | — | — | 3 / 5 / 2 nhóm | Có |
| http_calls | 3 | 3 | 3 / 3 / 3 | 0 | 11 + 1 `non_http_calls` | — | 1 / 0 / — | Có (chỉ route) |
| file_roles | 3 | 1 | 3 / 3 / 3 | 2 (5) | — | 10 (6 dòng alt) | 0 / 0 / — | Có |
| fr029_e2e | 2 | 2 | 2 / 2 / 2 | 3 (6) | 1 | 4 | 1 / 1 / 1 nhóm | Không có oracle; đọc source |

Kiểm thêm:

- Membership của cả 7 fixture phủ mỗi file `.py` và `requirements.txt` đúng một lần (kiểm bằng script).
- Mọi `declared_at`, `models[].line`, `http_calls[].where`, `limitations[].where`, `excluded_routes[].where`, `file_roles[].line/alt_lines` đều trỏ đúng dòng mang dấu hiệu.
- Gold có 5 trường `alt_lines` (6 dòng thay thế), đều ở `file_roles.gold.json`, đều đúng dấu hiệu. Không có `alt_roles`, `alt_methods`, `accept_alt_target`, `alt_where`, `alt_names`, `alt_types`, `optional`, `dynamic`.
- Đếm trong README fixture (11 route, 5 model, 5 bị loại, 11 lời gọi HTTP, 10 vai trò…) khớp gold.

## Phát hiện

| # | Loại | Gold, đường dẫn JSON | Source | Gold ghi | Nên ghi | Lý do |
|---|---|---|---|---|---|---|
| 1 | E (do gold) | `fr029_e2e.gold.json` `file_roles[2]` (`app/api/items.py`) | `app/api/items.py:15` `@router.get("/{item_id}")` | `line: 9`, không có `alt_lines` | thêm `alt_lines: [15]` | Dòng 15 cũng là decorator route. README fixture dòng 30 và mục 17: dòng khác cùng dấu hiệu phải nằm ở `alt_lines`. `file_roles.gold.json` làm đúng cho ca tương tự (`orders.py` alt 15). Công cụ trích dòng 15 sẽ bị chấm sai `line`. |
| 2 | E (do gold) | `fr029_e2e.gold.json` `file_roles[3]` (`app/schemas.py`) | `app/schemas.py:13` `class ItemOut(BaseModel):` | `line: 8`, không có `alt_lines` | thêm `alt_lines: [13]` | `ItemOut` là response model của cả hai route. Cùng lý do với #1. Dòng 4 (`Tag`) chỉ là model lồng, không phải dấu hiệu. |
| 3 | D | Mọi gold, `routes[*].status` | vd. `params_models` oracle: mọi route có tham số có thêm `422` | chỉ status khai hoặc mặc định (`[200]`, `[201]`…) | giữ, hoặc ghi rõ quy tắc | FR-029 dòng 122 "status code khai trong code". 422 do FastAPI tự thêm. Bộ chấm so cả danh sách nên công cụ ghi `[200, 422]` bị tính sai. |
| 4 | D | `file_roles.gold.json` `routes[1].status` | `app/api/orders.py:19` `raise HTTPException(status_code=404)` | `[200]` | giữ hoặc thêm cách chấp nhận `[200, 404]` | "Khai trong code" có thể hiểu gồm `HTTPException`. Gold đã ghi lý do trong `notes`. |
| 5 | D | `exclusions.gold.json` `excluded_routes[2]`; `routes` không có `/debug/state` | `app/routers/internal.py:6` `@router.get("/debug/state")` | route bị loại, lý do `test` | tùy người dùng quyết | FR-029 dòng 93 chỉ loại route khai trong file test hoặc thư mục ngoài phạm vi. `internal.py` là file production; chỉ nơi gắn nằm trong `conftest.py`. Gold `notes` đã ghi đang chờ quyết định. |
| 6 | D | `http_calls.gold.json` `http_calls[2].target`, `http_calls[7].target` | `app/clients.py:23` `client.put(settings.INVENTORY_URL, ...)`; `:46` `requests.post(settings.PAYMENT_URL, ...)` | `config`, `INVENTORY_URL` / `PAYMENT_URL` | giữ; cân nhắc thêm `accept_alt_target` | FR-029 dòng 84 "khóa cấu hình chứa URL". Công cụ ghi `settings.INVENTORY_URL` hoặc giá trị mặc định ở `app/config.py:5` sẽ bị tính sai. |
| 7 | D | `http_calls.gold.json` `limitations[0].where` | `app/clients.py:1` `import urllib.request`; `:64` `urllib.request.urlopen(...)` | `app/clients.py:64` | giữ; cân nhắc `alt_where: ["app/clients.py:1"]` | FR-029 dòng 87 "kèm nơi dùng" nghiêng về dòng 64. Công cụ ghi dòng import sẽ thành một FN và một FP. |
| 8 | D | `params_models.gold.json` `routes[1].params[2].name`, `routes[3].params[0].name` | `app/routes.py:22` `x_token: Annotated[str \| None, Header()]`; `app/deps.py:17` `x_tenant_id` | `x-token`, `x-tenant-id` | giữ | Đúng tên HTTP theo oracle. FR-029 dòng 53 chỉ nói "tên". Công cụ ghi tên biến Python bị tính sai cả bộ `params`. |
| 9 | D | `file_roles.gold.json` `file_roles[8].line/alt_lines` (`services.py`) | `app/services.py:5` `def place_order(...)`; `:7` `repository.save_order(...)` | 7, alt 11 | giữ | FR-029 không nói dòng bằng chứng nào cho Service. Gold chọn dòng gọi repository. Công cụ chọn dòng `def` hoặc dòng import sẽ bị tính sai. |
| 10 | D | `prefix_chain.gold.json` `routes[0].handler` | `app/main.py:15` `def root():` (lồng trong `create_app`) | `app/main.py::root` | giữ | Qualname thật là `create_app.<locals>.root`. Bộ chấm so `handler` chính xác. |

Tóm tắt: A 0, B 0, C 0, D 8, E 2.

## Giới hạn của review này

- Không chạy oracle hay code fixture. Tin dữ liệu đã ghi trong `*.oracle.json`; chỉ đối chiếu chéo với source bằng mắt.
- `fr029_e2e` không có oracle. Path, tham số, model đã suy theo luật FastAPI 0.115 khi đọc source, chưa chạy.
- Không kiểm `slice/tools/fr029_oracle.py`. Không chạy bộ chấm trên một `result.json` thật.
- Không kiểm định dạng `message` của giới hạn trong `result.json`. Bộ chấm lấy từ đầu tiên của `message` làm `kind` (`fr029_score.py` dòng 107-109). Nếu công cụ không mở đầu bằng `add_api_route`… hoặc `unsupported_http_library`, mọi giới hạn sẽ là FN dù gold đúng.
- Không đánh giá cách chia component trong membership, ngoài việc phủ đủ file. Gold không chấm phần này.
- Không đọc `ket-qua-chay/`, `docs/HANDOFF.md`, `docs/FR029-*.md`, review và diary khác.
