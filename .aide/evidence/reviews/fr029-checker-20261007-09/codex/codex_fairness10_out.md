```json
{
  "vong9": [
    {
      "muc": "route_nhan_dang_ky_trong_nhanh_da_tat",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca ENABLE_API=False đã bị từ chối; test chạy qua. Bộ dựng cạnh gọi _never_runs trước khi nhận đăng ký. slice/tests/test_checker_counterexamples.py:1038; slice/l3slice/docfacts.py:647. Kết luận giới hạn ở dạng điều kiện đã thử."
    },
    {
      "muc": "http_bien_co_annotation_mat_nguon_thu_vien",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: từ chối requests, nhận httpx cho biến được chú thích httpx.Client. AnnAssign hiện truyền nguồn tạo client và giữ thư viện annotation. slice/tests/test_checker_counterexamples.py:1044; slice/l3slice/astscan.py:392."
    },
    {
      "muc": "http_dependency_keyword_bo_mat_client",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: có suspect HTTP và nhận claim đúng với Depends(dependency=provide). Resolver hiện đọc keyword dependency. slice/tests/test_checker_counterexamples.py:1050; slice/l3slice/astscan.py:412."
    },
    {
      "muc": "http_client_lay_tu_dict_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca dict chứa client của vòng 9 có suspect và nhận claim đúng; test chạy qua. slice/tests/test_checker_counterexamples.py:1057; slice/l3slice/astscan.py:384; slice/l3slice/astscan.py:519."
    },
    {
      "muc": "http_partial_chua_goi_bi_nhan_la_request",
      "trang_thai": "mot_phan",
      "bang_chung": "Claim tại partial(wire.get, url) đã bị từ chối, test chạy qua. Tuy nhiên tự chạy lại vẫn nhận suspects=[{'at':'h.py:4','looks_like':'http'}] ở dòng chỉ tạo partial. virtual_calls loại partial nhưng http_lines vẫn tính đối số wire.get như một lời gọi. slice/tests/test_checker_counterexamples.py:1063; slice/l3slice/astscan.py:532; slice/l3slice/astscan.py:558."
    },
    {
      "muc": "dependency_alias_kieu_scalar_khong_duoc_mo_rong",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua cho cả UserId=UUID và Page=Annotated[int,Field(ge=1)]: nhắc user_id và page. Sửa hiện áp dụng alias module-level trong cùng file. slice/tests/test_checker_counterexamples.py:1068; slice/l3slice/docfacts.py:1701."
    },
    {
      "muc": "dependency_path_converter_bi_nhac_thanh_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: /items/{item_id:int} nhắc path item_id, không nhắc query item_id. slice/tests/test_checker_counterexamples.py:1078; slice/l3slice/docfacts.py:1557."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Hai báo cáo sanity r38 phân biệt được bộ kiểm giả. Hash đầu và cuối lượt này ổn định, khớp r38. Giới hạn phương pháp vẫn còn: thay riêng các phương thức và lấy hash file cuối lượt chạy. slice/tools/fr029_checkaudit.py:608; slice/tools/fr029_checkaudit.py:651; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:3; ket-qua-chay/fr029-checkaudit-20261009-r38-sanity-accept/summary.json:20; ket-qua-chay/fr029-checkaudit-20261009-r38-sanity-reject/summary.json:19."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. slice/tools/fr029_checkaudit.py:375; slice/tools/fr029_checkaudit.py:382."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: r38 đo dependency ở 14/37 bộ, 12 HTTP literal và 0 dòng gold nhiều lời gọi. Các số 0 lỗi không chứng minh phần chưa được đo. ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:8; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:14; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:37; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:44."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về phạm vi mutation. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:367; slice/tools/fr029_checkaudit.py:450."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã tự chạy lại probe công cụ đo: loại route thay HTTP ngay từ đầu bị báo thiếu; nhưng HTTP đổi thành route sau k-1 claim vẫn cho gold_not_flagged=[] và multi_call_unflagged=[]. Route gold bị gắn http cũng cho gold_not_flagged=[] và not_gold_item=0. Kiểm loại mới chỉ có ở recall HTTP ban đầu. slice/tools/fr029_checkaudit.py:504; slice/tools/fr029_checkaudit.py:515; slice/tools/fr029_checkaudit.py:522; slice/tools/fr029_checkaudit.py:536."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi; r38 vẫn có 2 http_gold_vs_rule. slice/tools/fr029_checkaudit.py:133; slice/tools/fr029_checkaudit.py:146; slice/tools/fr029_checkaudit.py:440; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:39."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. slice/tools/fr029_checkaudit.py:38; slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:450."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "125/125 test trong module phản ví dụ chạy qua bằng helper RAM; riêng RoundNineCodex 7/7 và RoundNine 9/9. Tuy nhiên sáu ca mới bên dưới vẫn tái hiện; chưa đủ bằng chứng khái quát hóa cao, không suy diễn tác giả cố ý overfit. slice/tests/test_checker_counterexamples.py:17; slice/tests/test_checker_counterexamples.py:959; slice/tests/test_checker_counterexamples.py:1035; slice/l3slice/astscan.py:412; slice/l3slice/docfacts.py:790."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Chạy lại không đổi: getattr(wire,'get')(url) có suspect nhưng claim đúng bị từ chối; e(wire) không annotation, không binding client trong file vẫn không có suspect và claim thiếu client_at bị từ chối. slice/l3slice/astscan.py:584; slice/l3slice/astscan.py:545; slice/l3slice/docfacts.py:1133; slice/l3slice/docfacts.py:1262."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_danh_sach_router_trong_bien_lam_lot_claim_thieu_prefix",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nr=APIRouter(prefix='/items')\n@r.get('/x')\ndef e(): return {}\nrouters=[r]\nfor router in routers:\n    app.include_router(router, prefix='/api')\n",
      "hau_qua": "Nhận claim GET /x thuộc app dù đường dẫn thực là /api/items/x. Resolver chỉ mở rộng vòng lặp có iterable trực tiếp là List/Tuple; biến routers tạo cạnh chưa giải được, khiến kiểm đăng ký trả thành công. slice/l3slice/docfacts.py:664; slice/l3slice/docfacts.py:771; slice/l3slice/docfacts.py:790.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_route(route('main.py::e','main.py:4-5','/x',application='main.py:2')) trả []; TestClient GET /x trả 404, GET /api/items/x trả 200."
    },
    {
      "loai": "http_tham_so_che_bien_client_toan_cuc_van_duoc_nhan",
      "vi_du_code": "import httpx\nwire = httpx.Client()\ndef e(wire):\n    return wire.get('https://example.org/x')\n",
      "hau_qua": "Nhận claim chắc chắn HTTP dựa vào biến toàn cục cùng tên, dù receiver thực là tham số che biến đó. Tham số không annotation không chặn việc rơi về tập clients toàn file; _binds cũng không tính tham số. slice/l3slice/astscan.py:443; slice/l3slice/astscan.py:494; slice/l3slice/astscan.py:508.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim httpx/GET/https://example.org/x tại h.py:4 trả []; có suspect HTTP. Gọi e({'https://example.org/x':'cached'}) trả 'cached'; MockTransport ghi 0 request."
    },
    {
      "loai": "http_client_qua_async_exit_stack_bi_bo_sot",
      "vi_du_code": "import httpx\nfrom contextlib import AsyncExitStack\nasync def e():\n    async with AsyncExitStack() as stack:\n        wire = await stack.enter_async_context(httpx.AsyncClient())\n        return await wire.get('https://example.org/x')\n",
      "hau_qua": "Không flag lời gọi HTTP và từ chối claim đúng không có client_at. makes() loại lời gọi phương thức trước khi nhận ra enter_async_context trả lại client được đưa vào. slice/l3slice/astscan.py:262; slice/l3slice/astscan.py:274; slice/l3slice/astscan.py:389.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects=[]; claim tại h.py:6 báo receiver không phải client thấy được. asyncio.run(e()) với AsyncClient dùng MockTransport trả 200 và ghi đúng một GET https://example.org/x."
    },
    {
      "loai": "http_provider_cau_hinh_bang_partial_bi_bo_sot",
      "vi_du_code": "from functools import partial\nimport httpx\nfrom fastapi import FastAPI, Depends\ndef provide(base_url): return httpx.Client(base_url=base_url)\nget_client = partial(provide, base_url='https://example.org')\napp=FastAPI()\n@app.get('/x')\ndef e(wire=Depends(get_client)):\n    return {'status': wire.get('https://example.org/x').status_code}\n",
      "hau_qua": "Không nối callable partial với provider tạo client, nên bỏ suspect HTTP và từ chối claim đúng. Đây là partial được FastAPI thực thi để cấp dependency, khác partial chỉ được tạo ở phản ví dụ vòng 9. slice/l3slice/astscan.py:270; slice/l3slice/astscan.py:276; slice/l3slice/astscan.py:412.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects chỉ có route h.py:7; claim HTTP h.py:9 bị từ chối. TestClient GET /x trả {'status':200}; MockTransport ghi đúng một GET https://example.org/x."
    },
    {
      "loai": "dependency_alias_query_la_hang_bi_nhac_sai_ten",
      "vi_du_code": "from fastapi import FastAPI, Depends, Query\nPAGE = 'pageSize'\ndef dep(page_size: int = Query(10, alias=PAGE)): return page_size\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query page_size thay vì pageSize. Nhánh đọc alias chỉ nhận ast.Constant và âm thầm dùng tên tham số khi alias là Name. slice/l3slice/docfacts.py:1685; slice/l3slice/docfacts.py:1689.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Route main.py:5-6, application main.py:4, dependency dep tại main.py:6 được nhận. Reminder ghi query 'page_size'; OpenAPI chạy thật ghi query 'pageSize'."
    },
    {
      "loai": "dependency_header_dung_lai_qua_bien_bi_nhac_thanh_query",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header\ntenant_header = Header(alias='X-Tenant')\ndef dep(tenant: str = tenant_header): return tenant\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query tenant thay vì header X-Tenant. Default là Name không được giải tới đối tượng Header; nhánh scalar coi tham số chưa có marker. slice/l3slice/docfacts.py:1660; slice/l3slice/docfacts.py:1664; slice/l3slice/docfacts.py:1666.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Route main.py:5-6, application main.py:4, dependency dep tại main.py:6 được nhận. Reminder ghi query 'tenant'; OpenAPI chạy thật ghi header 'X-Tenant'."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: các ca sửa có tiến bộ nhưng đăng ký không giải được vẫn có thể làm lọt claim thiếu prefix (slice/tests/test_checker_counterexamples.py:1038; slice/l3slice/docfacts.py:790). HTTP claim: còn nhận sai do phạm vi tên và từ chối lời gọi thật qua quản lý context hoặc provider partial (slice/l3slice/astscan.py:508; slice/l3slice/astscan.py:274; slice/l3slice/astscan.py:412). HTTP suspects: bỏ sót các dạng đó, vẫn flag partial chưa gọi; phép đo recall còn bỏ loại trong nhánh nhiều call và route (slice/l3slice/astscan.py:558; slice/tools/fr029_checkaudit.py:515; slice/tools/fr029_checkaudit.py:536). Dependency params: các ca vòng 9 qua nhưng biến chứa alias/marker còn gây nhắc sai; phạm vi gold chỉ 14/37 bộ (slice/l3slice/docfacts.py:1664; slice/l3slice/docfacts.py:1685; ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:14). Các mức tin cậy và tần suất là đánh giá định tính, không phải tỷ lệ thống kê."
}
```

Đường dẫn tương đối tính từ `D:/VSF/l3-generator-l3`.
Không sửa file repo; không đọc `docs/`, `HANDOFF`, `.aide/evidence/reviews/`.
Sandbox chặn thư mục tạm: tôi thay riêng helper bằng `SourceTools` trong RAM, giữ nguyên assertion (`slice/tests/test_docagent.py:105`; `slice/l3slice/source_tools.py:100`).
Oracle dùng FastAPI 0.115.6, Pydantic 2.10.4, httpx 0.28.1; HTTP chạy qua MockTransport.
Đã đọc báo cáo r38 và hai sanity, không chạy lại toàn bộ 37 gold.
Hash triển khai đầu/cuối lượt ổn định và khớp r38 (`ket-qua-chay/fr029-checkaudit-20261009-r38/summary.json:3`).