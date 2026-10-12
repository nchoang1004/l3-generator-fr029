```json
{
  "repos": [
    {
      "repo": "lindseystead_ai-pdf-autofiller",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 8,
        "items": []
      },
      "suspects": {
        "http_that": 4,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Repo chỉ có 8 route ứng dụng; đã kiểm toàn bộ, không thể lấy mẫu 15 route khác nhau: GET / (src/pdf_autofiller/api/routes.py:238), GET /playground (src/pdf_autofiller/api/routes.py:244), GET /health (src/pdf_autofiller/api/routes.py:250), GET /version (src/pdf_autofiller/api/routes.py:273), GET /samples/sample_form.pdf (src/pdf_autofiller/api/routes.py:278), POST /inspect (src/pdf_autofiller/api/routes.py:295), POST /preview (src/pdf_autofiller/api/routes.py:344), POST /fill (src/pdf_autofiller/api/routes.py:401).",
    "Không có Depends ở handler/decorator của 8 route đã đọc. Năm handler GET không nhận tham số; ba handler POST nhận Request và File/Form, không phải tham số header/query/cookie/path do dependency: src/pdf_autofiller/api/routes.py:239, src/pdf_autofiller/api/routes.py:245, src/pdf_autofiller/api/routes.py:251, src/pdf_autofiller/api/routes.py:274, src/pdf_autofiller/api/routes.py:279, src/pdf_autofiller/api/routes.py:303, src/pdf_autofiller/api/routes.py:356, src/pdf_autofiller/api/routes.py:426.",
    "Cấp router: APIRouter() không khai dependencies (src/pdf_autofiller/api/routes.py:58). Cấp app: FastAPI(...) và include_router(router) không khai dependencies (src/pdf_autofiller/api/app.py:35, src/pdf_autofiller/api/app.py:59). Danh sách dependencies rỗng của gói phù hợp với source.",
    "UploadGuardMiddleware có __call__ nhưng được đăng ký bằng add_middleware, không phải Depends (src/pdf_autofiller/api/middleware.py:94, src/pdf_autofiller/api/middleware.py:148). Nó gọi guard_mutating_request trực tiếp (src/pdf_autofiller/api/middleware.py:108); hàm này gọi require_api_key (src/pdf_autofiller/api/security.py:206), đọc header trực tiếp từ Request (src/pdf_autofiller/api/security.py:191). Không tính thành dependency hoặc params_thieu.",
    "Phân loại từng suspect: src/pdf_autofiller/client.py:67 = http_that, GET /health; src/pdf_autofiller/client.py:93 = http_that, POST /inspect; src/pdf_autofiller/client.py:124 = http_that, POST /preview; src/pdf_autofiller/client.py:172 = http_that, POST /fill. Receiver http đến từ _client(), trả httpx.Client hoặc client httpx được truyền vào (src/pdf_autofiller/client.py:19, src/pdf_autofiller/client.py:50, src/pdf_autofiller/client.py:190).",
    "Đã quét văn bản toàn repo trong phạm vi được phép cho httpx/requests/aiohttp và đối chiếu receiver: chỉ tìm thấy bốn lời gọi trực tiếp nêu trên, đều có trong suspects; không phát hiện http_bo_sot (src/pdf_autofiller/client.py:67, src/pdf_autofiller/client.py:93, src/pdf_autofiller/client.py:124, src/pdf_autofiller/client.py:172).",
    "Lời gọi qua hàm bọc của dự án, không tính http_bo_sot: self.fill(...) tại src/pdf_autofiller/client.py:204; client.infer_semantics_batch(...) tại src/pdf_autofiller/pipeline.py:109; client.create_json_completion(...) tại src/pdf_autofiller/mapping.py:314. Hai lời gọi SDK OpenAI tại src/pdf_autofiller/field_semantics.py:101 và src/pdf_autofiller/field_semantics.py:140 cũng không phải lời gọi trực tiếp qua httpx/requests/aiohttp; SDK được import tại src/pdf_autofiller/field_semantics.py:24 và khởi tạo tại src/pdf_autofiller/field_semantics.py:65.",
    "decorators_refused của gói rỗng nên không có mục cần phán xét. Tám decorator đã kiểm đều dùng router là APIRouter thật (src/pdf_autofiller/api/routes.py:58), được gắn vào ứng dụng FastAPI (src/pdf_autofiller/api/app.py:35, src/pdf_autofiller/api/app.py:59)."
  ]
}
```