```json
{
  "vong7": [
    {
      "muc": "route_bo_qua_thu_tu_include_router",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca cụ thể vòng 7 đã qua: từ chối thứ tự sai và nhận thứ tự đúng. slice/tests/test_checker_counterexamples.py:825; slice/l3slice/docfacts.py:722."
    },
    {
      "muc": "route_nhieu_decorator_chon_nham_router",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca route trên application của decorator thứ hai đã qua; kiểm đăng ký thử từng decorator. slice/tests/test_checker_counterexamples.py:835; slice/l3slice/docfacts.py:696."
    },
    {
      "muc": "ket_qua_json_bi_nhan_la_client_do_constructor_long",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca cụ thể đã qua: không flag data.get và từ chối claim HTTP sai; makes() không còn coi kết quả phương thức là client. slice/tests/test_checker_counterexamples.py:841; slice/l3slice/astscan.py:260."
    },
    {
      "muc": "http_qua_asyncio_to_thread_bi_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Chạy lại: suspects có h.py:3 loại http, nhưng claim GET đúng vẫn bị từ chối vì không thấy lời gọi .get/.post. MockTransport xác nhận thực hiện GET và trả 200. Test mới chỉ kiểm suspect. slice/tests/test_checker_counterexamples.py:854; slice/l3slice/astscan.py:486; slice/l3slice/astscan.py:558; slice/l3slice/docfacts.py:1082."
    },
    {
      "muc": "http_client_qua_property_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test cả suspect và nhận claim đúng đã qua; có nhánh theo property trả client. slice/tests/test_checker_counterexamples.py:859; slice/l3slice/astscan.py:180."
    },
    {
      "muc": "dependency_query_model_nhac_ten_bien_thay_vi_truong",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca trường scalar q đã qua: nhắc q, không nhắc f. Chưa suy rộng sang mọi loại trường model; phản ví dụ mới bên dưới có trường list. slice/tests/test_checker_counterexamples.py:866; slice/l3slice/docfacts.py:1615."
    },
    {
      "muc": "dependency_keyword_dependency_mat_tham_so_long",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test nhắc header x-tenant qua Depends(dependency=inner) đã qua; resolver đọc keyword dependency. slice/tests/test_checker_counterexamples.py:876; slice/l3slice/docfacts.py:1627."
    },
    {
      "muc": "dependency_import_doi_ten_Header_nhac_sai_vi_tri",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Header as H đã qua: nhắc header x-tenant, không nhắc query x_tenant. slice/tests/test_checker_counterexamples.py:884; slice/l3slice/docfacts.py:1637."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Giới hạn phương pháp không đổi. Hash đầu/cuối lượt này khớp R33; hai báo cáo sanity vẫn phân biệt bộ kiểm giả. slice/tools/fr029_checkaudit.py:609; slice/tools/fr029_checkaudit.py:652; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r33-sanity-accept/summary.json:25; ket-qua-chay/fr029-checkaudit-20261008-r33-sanity-reject/summary.json:27."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. slice/tools/fr029_checkaudit.py:375; slice/tools/fr029_checkaudit.py:382; slice/tools/fr029_checkaudit.py:390."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: dependency đo 14/37 bộ, HTTP literal 12 ca; bốn repo mới vẫn có gold_dep_params=0 và literal=0. ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:37; ket-qua-chay/fr029-checkaudit-20261008-r33/audit.json:210; ket-qua-chay/fr029-checkaudit-20261008-r33/audit.json:262; ket-qua-chay/fr029-checkaudit-20261008-r33/audit.json:314; ket-qua-chay/fr029-checkaudit-20261008-r33/audit.json:366."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về công cụ đo. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:367; slice/tools/fr029_checkaudit.py:449."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Chạy lại probe: suspect route tại dòng hai HTTP gold call bị nhánh recall HTTP phát hiện thiếu cả hai. Nhưng khi suspects() trả http ban đầu rồi chỉ trả route sau k-1 claim, audit vẫn trả gold_not_flagged=[] và multi_call_unflagged=[]. Nhánh nhiều call vẫn chỉ kiểm at; route recall và miễn noise vẫn bỏ loại. R33 có multi_call_lines=0. slice/tools/fr029_checkaudit.py:503; slice/tools/fr029_checkaudit.py:514; slice/tools/fr029_checkaudit.py:516; slice/tools/fr029_checkaudit.py:535; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:44."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi; R33 vẫn có hai gold_vs_rule. slice/tools/fr029_checkaudit.py:133; slice/tools/fr029_checkaudit.py:146; slice/tools/fr029_checkaudit.py:408; slice/tools/fr029_checkaudit.py:439; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:39."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về công cụ đo và nguồn gold. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:449; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:984; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:995."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "101/101 test qua, gồm cả RoundSeven và RoundSevenCodex; bảy ca mới bên dưới vẫn tái hiện. Có tiến bộ nhưng chưa đủ bằng chứng khái quát hóa cao; không kết luận tác giả cố ý overfit. slice/tests/test_checker_counterexamples.py:739; slice/tests/test_checker_counterexamples.py:822; slice/l3slice/astscan.py:294; slice/l3slice/docfacts.py:1618."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Chạy lại: getattr(wire,'get')(url) có suspect nhưng claim đúng bị từ chối; e(wire) không annotation vẫn suspects=[]. MockTransport xác nhận cả hai thực hiện GET. slice/tests/test_checker_counterexamples.py:896; slice/l3slice/astscan.py:475; slice/l3slice/astscan.py:508; slice/l3slice/astscan.py:558; slice/l3slice/docfacts.py:1082."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_factory_bo_qua_prefix_router_cuc_bo",
      "vi_du_code": "from fastapi import FastAPI,APIRouter\ndef create_app():\n    app=FastAPI()\n    r=APIRouter(prefix='/api')\n    @r.get('/x')\n    def e(): return {}\n    app.include_router(r)\n    return app\napp=create_app()\n",
      "hau_qua": "Nhận claim /x thiếu /api. _router_prefix chỉ đọc tree.body, bỏ constructor router trong factory. slice/l3slice/docfacts.py:668; slice/l3slice/docfacts.py:671; slice/l3slice/docfacts.py:726.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. main.py; add_route(route('main.py::e','main.py:5-6','/x',application='main.py:3'))=[]; OpenAPI thực tế chỉ có /api/x. Dùng helper tại slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "http_alias_cuc_bo_tu_thuoc_tinh_client_bi_bo_sot",
      "vi_du_code": "import httpx\nclass API:\n    def __init__(self): self._wire=httpx.Client()\n    def e(self):\n        wire=self._wire\n        return wire.get('https://real.example')\n",
      "hau_qua": "Mất suspect và từ chối claim đúng khi lấy client từ thuộc tính sang biến cục bộ. makes() không truyền nhận diện client qua biểu thức Attribute. slice/l3slice/astscan.py:242; slice/l3slice/astscan.py:253; slice/l3slice/astscan.py:361; slice/l3slice/docfacts.py:1204.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. main.py; suspects=[]; claim HTTP GET tại main.py:6 bị lỗi 'wire.get ... không gọi trên client HTTP thấy được'. Thay _wire bằng client dùng MockTransport: e() trả 200, ghi đúng một request https://real.example. Helper claim tại slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "http_annotation_dict_chua_client_bi_coi_la_client",
      "vi_du_code": "import httpx\ndef e(clients: dict[str,httpx.Client]):\n    return clients.get('primary')\n",
      "hau_qua": "Flag dict.get và nhận claim HTTP sai. typed_client() tìm class client ở bất kỳ nút nào trong annotation, kể cả kiểu giá trị của dict. slice/l3slice/astscan.py:284; slice/l3slice/astscan.py:294; slice/l3slice/astscan.py:414.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. main.py; suspects=[{'at':'main.py:3','looks_like':'http'}]; http(c,'main.py:3','httpx','GET','primary')=[]. Runtime e({'primary':wire}) trả chính wire; MockTransport ghi 0 request. Helper claim tại slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "http_bound_method_luu_tren_instance_bi_bo_sot",
      "vi_du_code": "import httpx\nclass API:\n    def __init__(self):\n        self._wire=httpx.Client()\n        self.fetch=self._wire.get\n    def e(self): return self.fetch('https://real.example')\n",
      "hau_qua": "Mất suspect và từ chối claim đúng qua bound method lưu trên instance. Nhánh alias phương thức chỉ nhận đích ast.Name, không nhận self.fetch. slice/l3slice/astscan.py:197; slice/l3slice/astscan.py:201; slice/l3slice/astscan.py:506; slice/l3slice/astscan.py:558.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. main.py; suspects=[]; claim tại main.py:6 bị lỗi không có lời gọi .get/.post. Gắn self.fetch với wire.get dùng MockTransport: e() trả 200 và ghi một GET https://real.example. Helper claim tại slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "dependency_query_model_bo_truong_list",
      "vi_du_code": "from typing import Annotated\nfrom fastapi import FastAPI,Depends,Query\nfrom pydantic import BaseModel\nclass Filters(BaseModel):\n    tags: list[str]=[]\ndef dep(f: Annotated[Filters,Query()]): return f\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Không nhắc query tags mặc dù FastAPI nhận mảng query. Nhánh mở rộng Query model lọc chỉ trường scalar. slice/l3slice/docfacts.py:1615; slice/l3slice/docfacts.py:1618; slice/l3slice/astscan.py:594.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim main.py::e, decorator main.py:8-9, application main.py:7, dependency dep tại main.py:9 được nhận; reminders=''. OpenAPI có query tags kiểu array[string]. Helper tại slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_query_model_bo_alias_generator",
      "vi_du_code": "from typing import Annotated\nfrom fastapi import FastAPI,Depends,Query\nfrom pydantic import BaseModel,ConfigDict\nfrom pydantic.alias_generators import to_camel\nclass Filters(BaseModel):\n    model_config=ConfigDict(alias_generator=to_camel)\n    sort_by: str=''\ndef dep(f: Annotated[Filters,Query()]): return f\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query sort_by không tồn tại và bỏ sortBy thực tế. _model_fields chỉ đọc alias/validation_alias literal từ Field, không áp dụng alias_generator. slice/l3slice/docfacts.py:1680; slice/l3slice/docfacts.py:1684; slice/l3slice/docfacts.py:1687.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim main.py::e, decorator main.py:10-11, application main.py:9, dependency dep tại main.py:11 được nhận. Reminder ghi query 'sort_by' tại main.py:7; OpenAPI chỉ có query sortBy. Helper tại slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_instance_bo_call_ke_thua",
      "vi_du_code": "from fastapi import FastAPI,Depends,Header\nclass Base:\n    def __call__(self,x_tenant: str=Header()): return x_tenant\nclass Tenant(Base): pass\ntenant=Tenant()\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)): return {}\n",
      "hau_qua": "Bỏ header của callable instance có __call__ kế thừa. Nhánh tenant=Tenant() chỉ tìm trực tiếp trong thân Tenant, không dùng bộ giải kế thừa _class_method. slice/l3slice/docfacts.py:1535; slice/l3slice/docfacts.py:1540; slice/l3slice/docfacts.py:1644.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Claim main.py::e, decorator main.py:7-8, application main.py:6, dependency tenant tại main.py:8 được nhận; reminders=''. OpenAPI có header x-tenant bắt buộc. Helper tại slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: hai ca cụ thể vòng 7 đã sửa, nhưng vẫn nhận path thiếu prefix trong app factory; chưa đủ tin cậy cao cho application/path đầy đủ (slice/tests/test_checker_counterexamples.py:825; slice/tests/test_checker_counterexamples.py:835; slice/l3slice/docfacts.py:671). HTTP claim: còn nhận dict.get thành HTTP và từ chối các lời gọi thật qua alias/thread/getattr (slice/l3slice/astscan.py:294; slice/l3slice/astscan.py:558; slice/l3slice/docfacts.py:1082). HTTP suspects: vẫn bỏ lời gọi qua biến lấy từ thuộc tính và bound method trên instance; số gold_items_not_flagged=0 chưa chứng minh bao phủ repo mới, đặc biệt phép đo nhiều call chưa kiểm loại và R33 không có dòng nhiều call (slice/l3slice/astscan.py:253; slice/l3slice/astscan.py:201; slice/tools/fr029_checkaudit.py:535; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:43; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:44). Dependency params: các ca scalar và marker vòng 7 đã sửa, nhưng còn bỏ list, nhắc sai alias_generator và bỏ __call__ kế thừa; phép đo chỉ phủ 14/37 bộ (slice/l3slice/docfacts.py:1618; slice/l3slice/docfacts.py:1684; slice/l3slice/docfacts.py:1540; ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:14). Giới hạn xác minh: chạy 101/101 test phản ví dụ bằng snapshot SourceTools trong RAM, thay helper tools_for tạo file tạm và giữ nguyên assertion vì môi trường chặn ghi cả thư mục tạm (slice/tests/test_docagent.py:105; slice/l3slice/source_tools.py:100). Không chạy lại toàn bộ 37 gold; đọc báo cáo R33 và đối chiếu code. Hash đầu/cuối ổn định, khớp R33: docfacts=05c98d616f1be139, astscan=be845470450e39f4, audit=2c72037dd339f0c1 (ket-qua-chay/fr029-checkaudit-20261008-r33/summary.json:3). Oracle cho các probe mới: FastAPI 0.115.6, Pydantic 2.10.4, httpx 0.28.1; HTTP dùng MockTransport, không gửi mạng ngoài. tan_suat_uoc và tin_cay là đánh giá định tính, không phải kết quả thống kê."
}
```

Đường dẫn tương đối trong JSON tính từ `D:/VSF/l3-generator-l3`.
Không sửa file repo; không đọc `docs/`, `HANDOFF` hoặc `.aide/evidence/reviews/`.