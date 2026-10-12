<!-- Báo cáo agent Claude chấm held-out, trích nguyên văn từ bản ghi phiên, nhận lúc 2026-10-08T09:26:33Z -->

```json
{"repos": [{"repo": "ncoevoet_facet",
  "dependencies": {"params_dung": 5,
    "params_sai": [{"dep": "require_share_client", "in": "query", "name": "album_id", "ly_do": "Cả hai route dùng dependency này đều có {album_id} trong path (/api/shared/album/{album_id}/picks). FastAPI gắn tham số album_id: int của dependency vào path, không phải query", "source": "api/auth.py:338-339; api/routers/proofing.py:142,146,186,189"}],
    "params_thieu": []},
  "deps_bo_sot": {"routes_kiem": 21, "items": []},
  "suspects": {"http_that": 0, "http_khac": 5, "registration": 1, "can_giai_thich": 0, "nhieu": []},
  "http_bo_sot": [],
  "decorators_refused_judgement": []}],
 "ghi_chu": [
  "get_optional_user (api/auth.py:190-193) chỉ có Request và HTTPBearer (_bearer_scheme, auth.py:42). Đó là security nên không có tham số. Cookie được đọc thủ công qua request.cookies (auth.py:200), không khai báo bằng Cookie(), nên params rỗng là đúng. require_authenticated, require_edition, require_auth và require_scan_access (auth.py:226,249,258,286) chỉ lồng Depends, nên params rỗng là đúng.",
  "hide_toggle_params: cả 5 query hide_* đúng (api/db_helpers.py:359-365).",
  "Cả repo không có dependencies=[...] ở decorator, APIRouter() hay FastAPI() (api/__init__.py:328; api/routers/*.py dòng APIRouter). Không có Annotated[..., Depends] và không có lớp có __call__. Ngoài _bearer_scheme, chỉ có 7 hàm được dùng trong Depends, đúng bằng 7 mục trong gói. require_superadmin được định nghĩa (auth.py:275) nhưng không route nào dùng.",
  "21 route đã kiểm: albums:400, burst_culling:553, capsules:107, export:872, faces:154, filter_options:80, folders:28, gallery:679, health:59, health:65, immich:209, lightroom:166, persons:123, scan:138, timeline:70, stats:123, search:618, proofing:142, proofing:186, webdav dav_get (đăng ký qua add_api_route ở webdav.py:329), spa_fallback (api/__init__.py:477).",
  "Suspects: webdav.py:329 add_api_route là registration thật. 5 dòng urlopen của urllib (api/updates.py:60, models/vlm_backend.py:108, plugins/__init__.py:333 và 480, sync/immich.py:125) là http_khac.",
  "app.mount('/assets', StaticFiles) ở api/__init__.py:474 không có trong suspects. Đây là mount file tĩnh, không phải route API. Có thể coi là một registration ngoài decorator; nêu để người chấm tự quyết, không tính lỗi.",
  "Ngoài thư mục test, httpx chỉ được dùng ở scripts/bench/_common.py:97 (client.request) và scripts/bench_async_db.py:35 (client.get). Cả hai file chỉ import stdlib và httpx, không import code repo, nên bị FR-028 loại khỏi phạm vi. Vì vậy không tính là bỏ sót. Điểm còn mơ hồ: scripts/bench/scoring_throughput.py:45 có import utils của repo và import _common, nhưng chính _common.py thì không import code repo.",
  "Không tìm thấy lời gọi requests hay aiohttp ở đâu trong repo. Trong tests/ không có lời gọi httpx, requests hay aiohttp dạng .get/.post/Client.",
  "decorators_refused rỗng. Số route trong gói (197) khớp với số tôi đếm: 196 @router.* cộng 1 @app.get trong api/."]}
```
Tóm tắt (repo ncoevoet_facet):
- Dependencies: 5 tham số đúng (5 query hide_* của hide_toggle_params). 1 tham số sai: require_share_client ghi album_id là query, nhưng route có {album_id} trong path nên FastAPI coi đó là tham số path. Không thiếu tham số nào.
- Bỏ sót dependency: không có, đã kiểm 21 route. Cả repo không dùng dependencies= ở cấp decorator, router hay app.
- Suspects: 1 registration (add_api_route của webdav) và 5 http_khac (urlopen của urllib). Không có dòng nào là nhiễu.
- Bỏ sót HTTP: không có. Hai lời gọi httpx đều nằm trong scripts/ không import code repo, nên FR-028 loại khỏi phạm vi.
- decorators_refused rỗng, đúng như mong đợi. Có một app.mount StaticFiles chưa được đưa vào suspects; tôi chỉ ghi chú, không tính lỗi.
