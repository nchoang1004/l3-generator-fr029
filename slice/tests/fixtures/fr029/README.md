# Fixture và gold FR-029

Thư mục này chứa 6 repository FastAPI nhỏ và đáp án độc lập (gold) để chấm công cụ sinh tài liệu FR-029. Gold không dựa trên code của `slice/l3slice/`.

## Mỗi fixture có gì

| Fixture | Ca phủ | Route | Model | Khác |
|---|---|---|---|---|
| `prefix_chain` | `create_app()`; include_router hai tầng; prefix ở `APIRouter(prefix=)` và `include_router(prefix=)`; một router gắn hai lần; `api_route(methods=["GET","POST"])`; `mount` sub app; prefix từ `Settings.API_V1_STR`; prefix từ `os.environ` không default; `/api/v1/...` và `/v1/api/...` | 11 (1 path unknown) | 0 | |
| `params_models` | Pydantic v2; tham số trong `Depends` lồng hai tầng; `Annotated[..., Query()/Header()]`; `Body(embed=True)`; hai body model; `Form`, `File`; `response_model` khác kiểu trả về; status 201, `status.HTTP_204_NO_CONTENT`, mặc định 200, mặc định 307 của `RedirectResponse`; `Optional[int]` không default; alias; model lồng và `list[Model]`; hai lớp `Item` ở hai file | 11 | 5 | |
| `pydantic_v1` | FastAPI 0.99.1 + Pydantic 1.10: `Optional[int]` không default là không bắt buộc | 2 | 1 | |
| `exclusions` | route trong `tests/`, trong file `test_*.py`, router chỉ gắn trong `conftest.py`, route trong `examples/`, decorator `.get` của đối tượng không phải FastAPI; `add_api_route`, `add_route`, `add_websocket_route` | 1 | 0 | 5 route bị loại, 3 giới hạn |
| `http_calls` | httpx, requests, aiohttp; client trong `with`; lớp con `AsyncClient` khai ở file khác; `request("PATCH", ...)`; method động; `stream`; `Session().get`; URL từ cấu hình; URL ghép lúc chạy; alias `hx`; `db.get` (không phải HTTP); `urllib` (giới hạn) | 3 | 0 | 11 lời gọi HTTP, 1 giới hạn |
| `file_roles` | mỗi vai trò trên thang FR-029 một file; file có hai dấu hiệu; `services.py` trên đường gọi (Service); `service_utils.py` không trên đường gọi (Khác); `__init__.py` rỗng | 3 | 2 | 10 vai trò file |

## Các file

- `<tên>/`: repository fixture, có `requirements.txt` ghim version.
- `<tên>.membership.json`: cách chia component cho trước (`fixture-membership-v1`). Phủ mỗi file `.py` và `requirements.txt` đúng một lần.
- `<tên>.oracle.json`: kết quả `app.openapi()` và `app.routes` khi import app thật. Chỉ dùng để dựng gold. Không đưa vào prompt hay input của agent.
- `<tên>.gold.json`: đáp án, định dạng `fr029-gold-v1`.

Trường thêm ngoài định dạng gốc (không bắt buộc khi chấm):

| Trường | Ý nghĩa |
|---|---|
| `routes[].registration` | Chuỗi nơi gắn prefix, từ app vào tới router (chỉ ở `prefix_chain`). `prefix: ""` là không có prefix, `null` là chưa biết |
| `routes[].path_known_suffix` | Phần path biết được khi `path` là `null` |
| `request_body.fields` | Các khóa cấp trên cùng của body khi body bị bọc theo tên tham số hoặc là form |
| `file_roles[].alt_lines` | Dòng khác cũng mang đúng dấu hiệu; chọn dòng nào trong `line` hoặc `alt_lines` đều đúng |
| `http_calls[].method_reason`, `target.reason` | Lý do khi method hoặc đích là `unknown` |
| `non_http_calls` | Lời gọi giống HTTP nhưng không phải; công cụ ghi vào mục HTTP là sai |
| `oracle_versions` | Version gói trong venv lúc chạy oracle |

## Chạy lại oracle

Sandbox là hai venv Python 3.11.9 riêng, không thuộc sản phẩm:

```bash
py -3.11 -m venv <dir>/oracle-venv
<dir>/oracle-venv/Scripts/python -m pip install fastapi==0.115.6 pydantic==2.10.4 pydantic-settings==2.7.1 \
    python-multipart==0.0.20 httpx==0.28.1 requests==2.32.3 aiohttp==3.11.11 sqlalchemy==2.0.36
py -3.11 -m venv <dir>/oracle-venv-pyd1
<dir>/oracle-venv-pyd1/Scripts/python -m pip install fastapi==0.99.1 pydantic==1.10.19
```

Version thực tế đã cài: fastapi 0.115.6, starlette 0.41.3, pydantic 2.10.4, pydantic-core 2.27.2, pydantic-settings 2.7.1; venv v1: fastapi 0.99.1, starlette 0.27.0, pydantic 1.10.19.

Lệnh, chạy từ gốc repository (`F=slice/tests/fixtures/fr029`, `V2`/`V1` là python của hai venv):

```bash
export MSYS_NO_PATHCONV=1   # Git Bash: giữ nguyên giá trị bắt đầu bằng "/"
python slice/tools/fr029_oracle.py --python "$V2" --fixture $F/prefix_chain --target "app.main:create_app()" --env ADMIN_PREFIX=/__ENV_ADMIN_PREFIX__ --out $F/prefix_chain.oracle.json
python slice/tools/fr029_oracle.py --python "$V2" --fixture $F/params_models --target app.main:app --out $F/params_models.oracle.json
python slice/tools/fr029_oracle.py --python "$V1" --fixture $F/pydantic_v1  --target app.main:app --out $F/pydantic_v1.oracle.json
python slice/tools/fr029_oracle.py --python "$V2" --fixture $F/exclusions   --target app.main:app --out $F/exclusions.oracle.json
python slice/tools/fr029_oracle.py --python "$V2" --fixture $F/http_calls   --target app.main:app --out $F/http_calls.oracle.json
python slice/tools/fr029_oracle.py --python "$V2" --fixture $F/file_roles   --target app.main:app --out $F/file_roles.oracle.json
```

Oracle chạy với `PYTHONDONTWRITEBYTECODE=1`, không ghi `__pycache__` vào fixture, không cần mạng.

## Gold được dựng thế nào

- Route, tham số, body, response, status, trường model: lấy từ oracle, rồi lọc theo FR-029 và thêm `declared_at` bằng cách đọc source. `declared_at` là dòng decorator.
- Bị loại, giới hạn, lời gọi HTTP, vai trò file: viết tay từ source và FR-028/FR-029.
- Mọi `file:dòng` trong gold đã được in ra và đối chiếu với source (07/10/2026).
- Gold chưa được người thứ hai review.

## Chỗ gold là phán đoán

Mỗi file gold có mục `notes` ghi chi tiết. Các phán đoán chính:

1. Bỏ route tài liệu FastAPI tự sinh (`/docs`, `/redoc`, `/openapi.json`, `/docs/oauth2-redirect`), kể cả dưới `/sub`.
2. `prefix_chain`: route admin có `path: null` vì prefix lấy từ `os.environ["ADMIN_PREFIX"]` không default. Oracle phải đặt giá trị giả để import được.
3. `prefix_chain`: prefix `/api/v1` lấy từ default của `Settings`; oracle chạy khi không đặt biến môi trường.
4. `prefix_chain`: handler hàm lồng ghi `app/main.py::root`, không ghi qualname `create_app.<locals>.root`.
5. `prefix_chain`: route của sub app mount có trong gold (AC-01 nói "gắn qua mount").
6. `params_models`: tên header ghi theo tên HTTP (`x-token`), không theo tên biến Python.
7. `params_models`: kiểu của `UploadFile` ghi `string` (bỏ format `binary`).
8. `params_models`: body form/file có `models: []` và `embedded: false`; các trường nằm ở `request_body.fields`.
9. `params_models`: status 307 của `RedirectResponse` ghi `status_source: default`.
10. `params_models`: model `Item` của `items.py` chỉ là model của API vì route `/items/{item_id}/full`; ở `/items/{item_id}` nó bị `response_model` ghi đè.
11. `pydantic_v1`: `nullable` lấy từ `allow_none` của Pydantic v1, vì OpenAPI của FastAPI 0.99 không ghi nullable.
12. `exclusions`: router production chỉ gắn trong `conftest.py` ghi lý do `test`; router trong `app/routers/test_selfcheck.py` (không gắn vào đâu) cũng ghi `test` theo tên file.
13. `exclusions`: chọn `examples/` làm thư mục ngoài phạm vi vì file trong đó không import code repository (FR-028). Trong membership, file này nằm ở component kind `other` tên "Ngoài phạm vi".
14. `exclusions`: `/health` khai qua `add_api_route` có trong OpenAPI của oracle nhưng gold bỏ, chỉ ghi ở `limitations` theo FR-029.
15. `http_calls`: đích từ cấu hình ghi tên trường `Settings` (`INVENTORY_URL`, `PAYMENT_URL`), không ghi `settings.` phía trước.
16. `http_calls`: dòng tạo client (`httpx.Client()`, `aiohttp.ClientSession()`) không phải lời gọi HTTP. `where` của lời gọi là dòng chứa lời gọi method.
17. `file_roles`: `line` là dòng dấu hiệu đầu tiên; dòng khác cùng dấu hiệu nằm ở `alt_lines`. Model bảng chấp nhận cả dòng `class` và dòng `__tablename__`.
18. `file_roles`: `services.py` đọc `settings.MAX_ORDER_QUANTITY`. Bảng FR-029 không coi đây là dấu hiệu Cấu hình, nên file là Service. Bằng chứng Service là dòng gọi `repository`.
19. `file_roles`: file `__init__.py` rỗng thuộc component Khác nên không có trong `file_roles`. Vai trò Khác ghi nhãn `exact`, `line: null`.
20. Membership của mọi fixture là đầu vào giả định, viết tay cho hợp lý theo FR-028; gold không chấm phần chia component.
