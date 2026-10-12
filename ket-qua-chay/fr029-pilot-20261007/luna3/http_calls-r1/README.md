# http_calls — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:e834022c8ce97e51ed00b4473d50845bf3d6339716cd565a545bc0ea2d0c2d8b`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/DON-HANG/api/API-HTTP-CALLS-DON-HANG-v1.md](tech-specs/DON-HANG/api/API-HTTP-CALLS-DON-HANG-v1.md) — component Đơn hàng

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:5`

### Đơn hàng

- Package `app/`
  - `app/clients.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/routes.py:23`, `app/clients.py:21`, `app/inventory_client.py:4`
  - `app/config.py` — Cấu hình (exact) — `app/config.py:4`
  - `app/db.py` — Model bảng (exact) — `app/db.py:15`
  - `app/inventory_client.py` — Hạ tầng (exact) — `app/inventory_client.py:4`
  - `app/routes.py` — Route (exact) — `app/routes.py:10`

## Lời gọi HTTP ra ngoài

| Component | Thư viện, method | Đích | Bằng chứng |
|---|---|---|---|
| Đơn hàng | httpx, GET | https://rates.example.com/v1/latest (exact) | app/clients.py:13: `return httpx.get("https://rates.example.com/v1/latest")` |
| Đơn hàng | httpx, POST | https://ship.example.com/orders (exact) | app/clients.py:18: `c.post("https://ship.example.com/orders", json={"id": order_id})` |
| Đơn hàng | httpx, PUT | khóa cấu hình INVENTORY_URL (exact) | app/clients.py:23: `return await client.put(settings.INVENTORY_URL, json={"sku": sku})` |
| Đơn hàng | httpx, PATCH | https://users.example.com/profile (exact) | app/clients.py:28: `return client.request("PATCH", "https://users.example.com/profile", json={"id": user_id})` |
| Đơn hàng | httpx, unknown — Phương thức được truyền qua tham số method. | unknown — URL được truyền qua tham số url. | app/clients.py:33: `return client.request(method, url)` |
| Đơn hàng | httpx, GET | https://reports.example.com/daily.csv (exact) | app/clients.py:37: `with httpx.stream("GET", "https://reports.example.com/daily.csv") as response:` |
| Đơn hàng | requests, GET | https://audit.example.com/ping (exact) | app/clients.py:42: `return requests.Session().get("https://audit.example.com/ping")` |
| Đơn hàng | requests, POST | khóa cấu hình PAYMENT_URL (exact) | app/clients.py:46: `return requests.post(settings.PAYMENT_URL, json={"amount": amount})` |
| Đơn hàng | aiohttp, GET | https://weather.example.com/today (exact) | app/clients.py:51: `async with session.get("https://weather.example.com/today") as resp:` |
| Đơn hàng | httpx, GET | unknown — URL được nội suy từ các tham số base và user_id. | app/clients.py:56: `return httpx.get(f"{base}/users/{user_id}")` |
| Đơn hàng | httpx, DELETE | https://cache.example.com/purge (exact) | app/clients.py:60: `return hx.delete("https://cache.example.com/purge")` |

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại app/clients.py:64 — Dùng urllib.request.urlopen để thực hiện yêu cầu HTTP; thư viện này không thuộc danh sách thư viện HTTP được lập danh mục.
- `CLAIMS_REJECTED`: 1 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
