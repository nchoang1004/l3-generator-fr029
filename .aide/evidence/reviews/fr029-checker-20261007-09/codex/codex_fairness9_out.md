```json
{
  "vong8": [
    {
      "muc": "route_factory_bo_qua_prefix_router_cuc_bo",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: từ chối path thiếu /api, nhận path có đủ router_prefix. slice/tests/test_checker_counterexamples.py:896."
    },
    {
      "muc": "http_alias_cuc_bo_tu_thuoc_tinh_client_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua cả suspect và claim GET đúng sau wire=self._wire. slice/tests/test_checker_counterexamples.py:905."
    },
    {
      "muc": "http_annotation_dict_chua_client_bi_coi_la_client",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: dict[str,httpx.Client].get không bị flag và claim HTTP sai bị từ chối. slice/tests/test_checker_counterexamples.py:911."
    },
    {
      "muc": "http_bound_method_luu_tren_instance_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: self.fetch có suspect và claim GET đúng được nhận. slice/tests/test_checker_counterexamples.py:916."
    },
    {
      "muc": "dependency_query_model_bo_truong_list",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: nhắc query tags của Query model có trường list[str]. slice/tests/test_checker_counterexamples.py:929."
    },
    {
      "muc": "dependency_query_model_bo_alias_generator",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca cụ thể to_camel đã sửa: test nhắc sortBy và không nhắc sort_by chạy qua. Không suy rộng kết luận này sang mọi generator tùy biến. slice/tests/test_checker_counterexamples.py:938."
    },
    {
      "muc": "dependency_instance_bo_call_ke_thua",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chạy qua: nhắc header x-tenant từ __call__ kế thừa của callable instance. slice/tests/test_checker_counterexamples.py:949."
    },
    {
      "muc": "http_qua_asyncio_to_thread_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: có suspect HTTP, nhận GET đúng; test từ chối POST sai cũng qua. MockTransport ghi một GET và trả 200. slice/tests/test_checker_counterexamples.py:923; slice/l3slice/astscan.py:507."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Giới hạn phương pháp không đổi. Hai sanity r35 phân biệt được bộ kiểm giả; hash đầu lượt khớp r35 nhưng mã bị sửa đồng thời sau đó. slice/tools/fr029_checkaudit.py:608; slice/tools/fr029_checkaudit.py:651; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r35-sanity-accept/summary.json:20; ket-qua-chay/fr029-checkaudit-20261008-r35-sanity-reject/summary.json:19."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. slice/tools/fr029_checkaudit.py:375; slice/tools/fr029_checkaudit.py:382; slice/tools/fr029_checkaudit.py:390."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: dependency chỉ đo 14/37 bộ; HTTP literal chỉ 12 ca; không có dòng gold nhiều lời gọi. ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:8; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:37; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:44."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về phạm vi mutation. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:367; slice/tools/fr029_checkaudit.py:450."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Tái hiện trên công cụ đo có hash khớp r35: suspect route thay HTTP ngay từ đầu bị báo thiếu; nhưng trả http ban đầu rồi route sau k-1 claim vẫn cho gold_not_flagged=[] và multi_call_unflagged=[]. Route gold bị flag thành http cũng cho gold_not_flagged=[] và not_gold_item=0. Nhánh nhiều call, route recall và miễn noise vẫn bỏ loại. slice/tools/fr029_checkaudit.py:504; slice/tools/fr029_checkaudit.py:515; slice/tools/fr029_checkaudit.py:522; slice/tools/fr029_checkaudit.py:536."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi; r35 vẫn có hai http_gold_vs_rule. slice/tools/fr029_checkaudit.py:133; slice/tools/fr029_checkaudit.py:146; slice/tools/fr029_checkaudit.py:440; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:39."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. slice/tools/fr029_checkaudit.py:38; slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:450."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "RoundEight đạt 8/8; bản chốt sau sửa đổi đồng thời đạt 117/117 test. Tuy nhiên bảy phản ví dụ mới bên dưới vẫn tái hiện. Chưa đủ bằng chứng khái quát hóa cao; không kết luận tác giả cố ý overfit. slice/tests/test_checker_counterexamples.py:893; slice/tests/test_checker_counterexamples.py:959; slice/l3slice/astscan.py:380; slice/l3slice/docfacts.py:1664."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Chạy lại: getattr(wire,'get')(url) có suspect nhưng claim đúng bị từ chối; e(wire) không annotation vẫn không có suspect và claim thiếu client_at bị từ chối. MockTransport xác nhận mỗi dạng thực hiện một GET, trả 200. slice/l3slice/astscan.py:565; slice/l3slice/astscan.py:528; slice/l3slice/docfacts.py:1107; slice/l3slice/docfacts.py:1133."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_nhan_dang_ky_trong_nhanh_da_tat",
      "vi_du_code": "from fastapi import FastAPI,APIRouter\napp=FastAPI()\nr=APIRouter()\n@r.get('/x')\ndef e(): return {}\nENABLE_API=False\nif ENABLE_API:\n    app.include_router(r)\n",
      "hau_qua": "Nhận claim GET /x thuộc app mặc dù nhánh đăng ký không chạy. Bộ dựng cạnh đi qua mọi Call bằng ast.walk, không xét điều kiện bao quanh. slice/l3slice/docfacts.py:640; slice/l3slice/docfacts.py:646.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Với main.py, add_route(route('main.py::e','main.py:4-5','/x',application='main.py:2')) trả []; FastAPI OpenAPI paths={}."
    },
    {
      "loai": "http_bien_co_annotation_mat_nguon_thu_vien",
      "vi_du_code": "import httpx,requests\nwire: httpx.Client=httpx.Client()\ndef e(): return wire.get('https://example.org/x')\n",
      "hau_qua": "Nhận claim library=requests cho lời gọi thực tế dùng httpx. Nhánh AnnAssign thêm tên client nhưng không truyền nguồn vào add(), làm mất client_lib. slice/l3slice/astscan.py:372; slice/l3slice/astscan.py:380; slice/l3slice/docfacts.py:1245.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. http(c,'h.py:3','requests','GET','https://example.org/x') trả []; suspect là http. Thay wire bằng httpx.Client dùng MockTransport: e() trả 200 và ghi một GET."
    },
    {
      "loai": "http_dependency_keyword_bo_mat_client",
      "vi_du_code": "import httpx\nfrom fastapi import FastAPI,Depends\ndef provide(): return httpx.Client()\napp=FastAPI()\n@app.get('/x')\ndef e(wire=Depends(dependency=provide)):\n    return wire.get('https://example.org/x').json()\n",
      "hau_qua": "Không flag lời gọi HTTP ở dòng 7; claim đúng không kèm client_at bị từ chối dù provider tạo client ngay trong file. Resolver HTTP chỉ đọc e.args[0], chưa đọc keyword dependency. Đây là đường nhận diện client, khác ca nhắc tham số dependency đã sửa ở vòng 8. slice/l3slice/astscan.py:398; slice/l3slice/astscan.py:399.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects chỉ chứa route h.py:5; claim HTTP tại h.py:7 báo wire.get không gọi trên client thấy được. TestClient với dependency override trả client MockTransport ghi đúng một GET https://example.org/x."
    },
    {
      "loai": "http_client_lay_tu_dict_bi_bo_sot",
      "vi_du_code": "import httpx\nclients={'primary':httpx.Client()}\ndef e(): return clients['primary'].get('https://example.org/x')\n",
      "hau_qua": "Mất suspect và từ chối claim đúng không kèm client_at khi truy cập client qua dict. Đây là lấy client ra khỏi container, khác dict.get không phải HTTP của vòng 8. Nhánh receiver không theo Subscript tới giá trị container. slice/l3slice/astscan.py:489; slice/l3slice/astscan.py:505; slice/l3slice/astscan.py:547.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects=[]; claim GET tại h.py:3 bị từ chối. Thay clients['primary'] bằng client MockTransport: e() trả 200 và ghi một GET."
    },
    {
      "loai": "http_partial_chua_goi_bi_nhan_la_request",
      "vi_du_code": "from functools import partial\nimport httpx\nwire=httpx.Client()\ndef e(): return partial(wire.get,'https://example.org/x')\n",
      "hau_qua": "Nhận claim GET tại dòng chỉ tạo callable, chưa thực hiện request. virtual_calls chuyển mọi đối số dạng client.get thành lời gọi ảo mà không xác định hàm nhận đối số có thực thi callback hay không. slice/l3slice/astscan.py:515; slice/l3slice/astscan.py:519; slice/l3slice/astscan.py:541.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspect HTTP ở h.py:4; claim GET được nhận với errors=[]. Chạy e() với wire dùng MockTransport trả functools.partial, ghi 0 request."
    },
    {
      "loai": "dependency_alias_kieu_scalar_khong_duoc_mo_rong",
      "vi_du_code": "from uuid import UUID\nfrom fastapi import FastAPI,Depends\nUserId=UUID\ndef dep(user_id: UserId): return user_id\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Không nhắc query user_id dù dependency đã được khai trong claim. scalar() so tên annotation với tập kiểu cố định, không giải alias kiểu. Biến thể Page=Annotated[int,Field(ge=1)] cũng bỏ query page. slice/l3slice/docfacts.py:1664; slice/l3slice/astscan.py:671.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim route main.py:6-7, application main.py:5, dependency dep tại main.py:7 được nhận; reminders=''. OpenAPI có query user_id. Đã chạy thêm biến thể Annotated: reminders='' trong khi OpenAPI có query page."
    },
    {
      "loai": "dependency_path_converter_bi_nhac_thanh_query",
      "vi_du_code": "from fastapi import FastAPI,Depends\ndef dep(item_id: int): return item_id\napp=FastAPI()\n@app.get('/items/{item_id:int}')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query item_id thay vì path item_id. Kiểm vị trí chỉ tìm chuỗi {item_id}, không nhận {item_id:int}. slice/l3slice/docfacts.py:1555; slice/l3slice/docfacts.py:1556.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim route main.py:4-5, application main.py:3, dependency dep tại main.py:5 được nhận. Reminder ghi query 'item_id' tại main.py:2; OpenAPI ghi path 'item_id' tại /items/{item_id}."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: ca prefix factory đã sửa nhưng vẫn nhận đăng ký trong nhánh tắt; phù hợp hỗ trợ rà soát hơn là xác nhận chắc chắn application đang phục vụ route (slice/tests/test_checker_counterexamples.py:896; slice/l3slice/docfacts.py:640). HTTP claim: còn nhận sai thư viện, nhận partial chưa gọi và từ chối một số lời gọi thật (slice/l3slice/astscan.py:380; slice/l3slice/astscan.py:515; slice/l3slice/astscan.py:398). HTTP suspects: vẫn bỏ client qua dependency keyword và container; phép đo nhiều call chưa kiểm loại và r35 không có gold nhiều call (slice/l3slice/astscan.py:398; slice/l3slice/astscan.py:547; slice/tools/fr029_checkaudit.py:536; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:44). Dependency params: các ca vòng 8 đã sửa, nhưng alias kiểu và path converter còn sai; phép đo chỉ bao phủ 14/37 bộ (slice/l3slice/docfacts.py:1664; slice/l3slice/docfacts.py:1555; ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:14). Giới hạn phiên bản: đầu lượt hash khớp r35; mã bị sửa đồng thời. Các phản ví dụ mới và dẫn dòng mã triển khai dùng bản chốt trong RAM, đối chiếu cuối lượt còn khớp file: docfacts=6b47f8b37955bf61, astscan=f77dd944b682d24c, fr029_checkaudit=e009051fc3222ffb. Vì vậy không gán kết quả thử mới cho đúng binary r35; hash r35 được ghi tại ket-qua-chay/fr029-checkaudit-20261008-r35/summary.json:3. RoundEight 8/8 qua ở lượt đầu và bản chốt; bản chốt có 117/117 test qua (slice/tests/test_checker_counterexamples.py:893; slice/tests/test_checker_counterexamples.py:959). Chạy test bằng SourceTools trong RAM, thay riêng helper tạo file tạm và giữ nguyên assertion (slice/tests/test_docagent.py:105; slice/l3slice/source_tools.py:100). Không chạy lại toàn bộ 37 gold; đã đọc báo cáo r35 và hai sanity, đồng thời tự chạy probe công cụ đo. Oracle chạy thực tế: FastAPI 0.115.6, Pydantic 2.10.4, httpx 0.28.1; HTTP dùng MockTransport. Tần suất và mức tin cậy là đánh giá định tính, không phải thống kê."
}
```

Đường dẫn tương đối tính từ `D:/VSF/l3-generator-l3`.
Không sửa file repo; không đọc `docs/`, `HANDOFF` hoặc `.aide/evidence/reviews/`.
Lưu ý phiên bản: mã đã thay đổi trong lúc kiểm toán; JSON phân biệt rõ báo cáo r35 và bản dùng cho các phép thử mới.