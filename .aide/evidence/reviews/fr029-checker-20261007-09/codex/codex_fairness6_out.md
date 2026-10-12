```json
{
  "vong5": [
    {
      "muc": "route_bo_prefix_tai_constructor_APIRouter",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: thiếu /v1 bị từ chối; thêm router_prefix đúng thì được nhận. Xác nhận ca cụ thể, không suy rộng sang mọi chuỗi prefix. slice/tests/test_checker_counterexamples.py:506; slice/l3slice/docfacts.py:569."
    },
    {
      "muc": "config_at_cua_client_khac_duoc_nhan",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: lời gọi trên a không còn nhận config_at tạo b; config_at tạo a được nhận. slice/tests/test_checker_counterexamples.py:525; slice/l3slice/docfacts.py:965."
    },
    {
      "muc": "thu_vien_client_bi_tron_giua_hai_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: hai tham số wire giữ đúng httpx/requests theo hàm; claim sai thư viện bị chặn. slice/tests/test_checker_counterexamples.py:536; slice/l3slice/astscan.py:382."
    },
    {
      "muc": "http_client_qua_import_module_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: import clients; clients.wire.get được flag và claim đúng được nhận. slice/tests/test_checker_counterexamples.py:552; slice/l3slice/docfacts.py:1071."
    },
    {
      "muc": "http_client_qua_alias_Annotated_Depends_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: Wire import trực tiếp từ module định nghĩa được nhận diện; HTTP suspect và claim đều đúng. slice/tests/test_checker_counterexamples.py:558; slice/l3slice/docfacts.py:1081."
    },
    {
      "muc": "dependency_functools_partial_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: partial(check,'read') nhắc x-tenant và bỏ scope đã gán theo vị trí. Trường hợp gán bằng keyword có lỗi khác bên dưới. slice/tests/test_checker_counterexamples.py:567; slice/l3slice/docfacts.py:1338."
    },
    {
      "muc": "dependency_long_Annotated_Depends_khong_doi_so_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại: outer chứa Annotated[Filters,Depends()] đã nhắc query q. slice/tests/test_checker_counterexamples.py:577; slice/l3slice/docfacts.py:1420."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Hash hiện tại khớp r26 và không đổi trong lượt kiểm toán. Sanity đã giả thêm _registration_problems: accept nhận cả 131 mutation bỏ prefix; reject từ chối cả 17 ca không cần prefix. Vẫn kiểm qua hàm con, chưa trọn add_route/submit; exit code chỉ theo exception; chưa gắn hash toàn bộ gold/source. slice/tools/fr029_checkaudit.py:583; slice/tools/fr029_checkaudit.py:626; slice/tools/fr029_checkaudit.py:657; ket-qua-chay/fr029-checkaudit-20261008-r26/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r26-sanity-accept/summary.json:25; ket-qua-chay/fr029-checkaudit-20261008-r26-sanity-reject/summary.json:27."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. Tái hiện reminder ghi dependency FAKE, nonexistent.py:999 nhưng đúng query q: reminders=1, reminders_wrong=[], missed=[]. Vẫn gán trực tiếp probe.routes và chỉ chấm tên/vị trí tham số HTTP, không xác minh dependency hay dòng bằng chứng. slice/tools/fr029_checkaudit.py:374; slice/tools/fr029_checkaudit.py:381; slice/tools/fr029_checkaudit.py:389."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: dependency đo trên 14/37 case; bỏ dependency cấp app/router; HTTP thiếu nhánh dev và tăng calls trước nhánh bỏ qua. Bốn repo mới vẫn gold_dep_params=0, literal=0. slice/tools/fr029_checkaudit.py:265; slice/tools/fr029_checkaudit.py:400; slice/tools/fr029_checkaudit.py:422; ket-qua-chay/fr029-checkaudit-20261008-r26/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r26/audit.json:204; ket-qua-chay/fr029-checkaudit-20261008-r26/audit.json:254; ket-qua-chay/fr029-checkaudit-20261008-r26/audit.json:304; ket-qua-chay/fr029-checkaudit-20261008-r26/audit.json:354."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Có tiến bộ: thêm 131 mutation bỏ toàn bộ prefix, đều bị chặn. Tuy nhiên chỉ gọi _registration_problems; chưa mutation application cụ thể, giá trị/thứ tự prefix qua claim đầy đủ, config_at/client_at/config key. Dependency vẫn tránh tên trùng phần cuối. slice/tools/fr029_checkaudit.py:187; slice/tools/fr029_checkaudit.py:190; slice/tools/fr029_checkaudit.py:206; slice/tools/fr029_checkaudit.py:366; slice/tools/fr029_checkaudit.py:448; ket-qua-chay/fr029-checkaudit-20261008-r26/summary.json:24."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi. Tái hiện một suspect loại route tại dòng có hai HTTP gold call: suspects=1, gold_items=2, gold_not_flagged=[], not_gold_item=0. Vẫn bỏ loại và số lượng call khi chấm recall; vùng miễn noise vẫn cộng ba dòng. slice/tools/fr029_checkaudit.py:481; slice/tools/fr029_checkaudit.py:496; slice/tools/fr029_checkaudit.py:519."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Phép đo prefix mới có dùng path gold, nhưng kiểm route cũ vẫn dùng checker chọn decorator và lấy expected literal từ source. HTTP config vẫn chuyển thành unknown; method có thể bị hạ thành unknown; không đọc alt_methods. R26 còn hai gold_vs_rule. slice/tools/fr029_checkaudit.py:132; slice/tools/fr029_checkaudit.py:145; slice/tools/fr029_checkaudit.py:197; slice/tools/fr029_checkaudit.py:406; slice/tools/fr029_checkaudit.py:438; ket-qua-chay/fr029-checkaudit-20261008-r26/summary.json:39."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Thêm phép đo bỏ prefix nhưng giới hạn application và quan hệ HTTP vẫn còn. Gold được dẫn vẫn ghi tác giả Claude Opus/Sonnet và reviewed_by_human=false; không đủ để khẳng định hai người chấm độc lập đã xác minh. slice/tools/fr029_checkaudit.py:206; slice/tools/fr029_checkaudit.py:448; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:983; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:995."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "Có sửa thực chất: 67/67 test qua, gồm RoundFive và HeldOutFindings. Tuy nhiên tám ca mới dưới đây vẫn sai; đây là bằng chứng giới hạn khái quát hóa, không chứng minh tác giả cố ý overfit. slice/tests/test_checker_counterexamples.py:460; slice/tests/test_checker_counterexamples.py:503; slice/l3slice/docfacts.py:598; slice/l3slice/astscan.py:413."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Các ca import module/Annotated trực tiếp đã sửa. Tái chạy phần còn lại: getattr(wire,'get')(url) được flag nhưng claim bị từ chối; e(wire) không annotation vẫn suspects=[]. slice/tests/test_checker_counterexamples.py:552; slice/tests/test_checker_counterexamples.py:558; slice/l3slice/astscan.py:446; slice/l3slice/astscan.py:493; slice/l3slice/astscan.py:417."
    },
    {
      "muc": "PVD01_nhan_nham_route_path",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test phân biệt path với name, qua. slice/tests/test_checker_counterexamples.py:229."
    },
    {
      "muc": "PVD02_dependency_trong_literal",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test loại tên chỉ nằm trong literal, qua. slice/tests/test_checker_counterexamples.py:236."
    },
    {
      "muc": "PVD03_dependency_trung_ten_module",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test chọn đúng dependency theo import, qua. slice/tests/test_checker_counterexamples.py:243."
    },
    {
      "muc": "PVD04_header_convert_underscores_false",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test giữ x_custom, qua. slice/tests/test_checker_counterexamples.py:251."
    },
    {
      "muc": "PVD05_query_khong_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test nhắc query không annotation, qua. slice/tests/test_checker_counterexamples.py:258."
    },
    {
      "muc": "PVD06_http_trung_bien_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test client và dict cùng tên trong hai hàm, qua. slice/tests/test_checker_counterexamples.py:267."
    },
    {
      "muc": "PVD07_client_at_khong_ton_tai_va_khong_lien_quan",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Các test vị trí không tồn tại, receiver khác tên và khác scope đều qua. slice/tests/test_checker_counterexamples.py:280; slice/tests/test_checker_counterexamples.py:372; slice/tests/test_checker_counterexamples.py:453."
    },
    {
      "muc": "PVD08_http_client_qua_depends",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test provider cùng file và import trực tiếp đều qua. slice/tests/test_checker_counterexamples.py:286; slice/tests/test_checker_counterexamples.py:326."
    },
    {
      "muc": "PVD09_import_client_co_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test client AnnAssign import trực tiếp qua. slice/tests/test_checker_counterexamples.py:293."
    },
    {
      "muc": "PVD10_hai_http_call_cung_dong",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test GET+POST và hai GET khác URL cùng dòng đều qua; lỗi phép đo recall được đánh giá riêng. slice/tests/test_checker_counterexamples.py:298; slice/tests/test_checker_counterexamples.py:378."
    },
    {
      "muc": "v3_ghep_method_va_path_tu_hai_decorator",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test ghép sai method/path qua. slice/tests/test_checker_counterexamples.py:311."
    },
    {
      "muc": "v3_sqlalchemy_session_annotation_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test loại SQLAlchemy Session.get qua. slice/tests/test_checker_counterexamples.py:320."
    },
    {
      "muc": "v3_bo_sot_http_provider_import_tu_module_khac",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test provider import trực tiếp qua. slice/tests/test_checker_counterexamples.py:326."
    },
    {
      "muc": "v3_dependency_dang_class_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test class có __init__ trực tiếp qua. slice/tests/test_checker_counterexamples.py:333."
    },
    {
      "muc": "v3_dependency_import_doi_ten_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test dependency import đổi tên qua. slice/tests/test_checker_counterexamples.py:342."
    },
    {
      "muc": "v3_alias_annotated_header_mat_reminder",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test alias Annotated chứa Header qua. slice/tests/test_checker_counterexamples.py:348."
    },
    {
      "muc": "v3_dict_get_sau_response_json_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test loại dict.get sau response.json qua. slice/tests/test_checker_counterexamples.py:357."
    },
    {
      "muc": "v4_route_sai_application_va_thieu_prefix_van_duoc_nhan",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca cụ thể app không đăng ký router và thiếu include_prefix vẫn bị chặn. slice/tests/test_checker_counterexamples.py:389."
    },
    {
      "muc": "v4_nhan_khoa_header_lam_cau_hinh_dich_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test khóa trong headers thay vì đối số URL qua. slice/tests/test_checker_counterexamples.py:400."
    },
    {
      "muc": "v4_annotation_client_khong_giu_thu_vien",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test annotation giữ đúng thư viện qua. slice/tests/test_checker_counterexamples.py:408."
    },
    {
      "muc": "v4_dependency_callable_instance_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test instance theo __call__ qua. slice/tests/test_checker_counterexamples.py:414."
    },
    {
      "muc": "v4_dependency_literal_enum_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Literal/Enum nhắc query qua. slice/tests/test_checker_counterexamples.py:423."
    },
    {
      "muc": "v4_annotated_marker_import_doi_ten_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test marker alias import đổi tên qua. slice/tests/test_checker_counterexamples.py:434."
    },
    {
      "muc": "v4_http_client_lifespan_app_state_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test client từ lifespan qua app.state được flag, qua. slice/tests/test_checker_counterexamples.py:444."
    },
    {
      "muc": "v4_client_at_trung_ten_nhung_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test client_at cùng tên trong hàm khác bị chặn, qua. slice/tests/test_checker_counterexamples.py:453."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_nhan_thu_tu_prefix_sai",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nr=APIRouter(prefix='/v1')\n@r.get('/x')\ndef e(): return {}\napp.include_router(r,prefix='/api')\n",
      "hau_qua": "Nhận path /v1/api/x dù route thật là /api/v1/x. Kiểm đăng ký gom vị trí thành tập hợp, không kiểm thứ tự prefix. slice/l3slice/docfacts.py:598; slice/l3slice/docfacts.py:618.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. File main.py; route('main.py::e','main.py:4-5','/x',application='main.py:2'), thay path_parts bằng router_prefix('/v1',main.py:3), include_prefix('/api',main.py:6), decorator('/x',main.py:4), theo đúng thứ tự này. add_route=[]; OpenAPI chỉ có /api/v1/x. Helper claim: slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "helper_dang_ky_khong_lien_quan_vo_hieu_kiem_prefix",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nr=APIRouter()\n@r.get('/x')\ndef e(): return {}\napp.include_router(r,prefix='/api')\ndef attach(target,router):\n    target.include_router(router)\n",
      "hau_qua": "Chỉ cần tồn tại helper chưa được gọi, checker nhận claim thiếu /api trên chuỗi đăng ký vốn đã xác định đầy đủ. _edges_open là cờ toàn snapshot và làm bỏ qua yêu cầu prefix. slice/l3slice/docfacts.py:555; slice/l3slice/docfacts.py:618.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. File main.py; add_route(route('main.py::e','main.py:4-5','/x',application='main.py:2'))=[]; _edges_open=True; OpenAPI chỉ có /api/x. Ca đối chứng dùng helper với tham số tên app bị chặn, nên lỗi phụ thuộc cách resolver xử lý tên. Helper claim: slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "config_base_url_duoc_nhan_du_url_tuyet_doi_ghi_de",
      "vi_du_code": "import httpx\nfrom types import SimpleNamespace\nsettings=SimpleNamespace(URL='https://base.example')\nc=httpx.Client(base_url=settings.URL)\ndef e(): return c.get('https://other.example/x')\n",
      "hau_qua": "Nhận settings.URL là đích cấu hình dù lời gọi dùng URL tuyệt đối khác. config_at đúng client vẫn không chứng minh base_url quyết định đích của lời gọi. slice/l3slice/docfacts.py:941; slice/l3slice/docfacts.py:1045.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. File h.py; add_http({'at':'h.py:5','library':'httpx','method':'GET','target':{'kind':'config','value':'settings.URL','config_at':'h.py:4'}})=[]; chạy e với httpx.MockTransport thu URL https://other.example/x. Đường kiểm: slice/l3slice/docfacts.py:938."
    },
    {
      "loai": "thuoc_tinh_client_trung_ten_giua_hai_class",
      "vi_du_code": "import httpx\nclass Remote:\n    def __init__(self): self.client=httpx.Client()\nclass Cache:\n    def __init__(self): self.client={'id':1}\n    def e(self): return self.client.get('id')\n",
      "hau_qua": "Flag dict.get như HTTP và nhận cả claim HTTP sai. client_attrs chỉ giữ tên thuộc tính, không giữ class/receiver sở hữu. slice/l3slice/astscan.py:305; slice/l3slice/astscan.py:413; slice/l3slice/astscan.py:438.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. File h.py; suspects=[{'at':'h.py:6','looks_like':'http'}]; http(c,'h.py:6','httpx','GET','id')=[]; thực thi Cache().e() trả 1, không gọi HTTP. Helper claim: slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "client_xuat_lai_qua_package_init_bi_bo_sot",
      "vi_du_code": "# FILE infra/transport.py\nimport httpx\nwire=httpx.Client()\n\n# FILE infra/__init__.py\nfrom .transport import wire\n\n# FILE routes.py\nfrom infra import wire\ndef e(): return wire.get('https://real.example')\n",
      "hau_qua": "Không có HTTP suspect và claim đúng bị từ chối nếu không thêm client_at. _exports không theo chuỗi xuất lại; module trung gian không chứa tên thư viện bị trả export rỗng. slice/l3slice/docfacts.py:1078; slice/l3slice/docfacts.py:1115.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. Dựng ba module trong RAM, không tính dòng chú thích FILE vào nội dung file. suspects=[]; claim routes.py:2 bị lỗi không thấy HTTP client/không import httpx. Chạy e với MockTransport thu https://real.example. Đường kiểm: slice/l3slice/docfacts.py:1018."
    },
    {
      "loai": "dependency_class_ke_thua_init_mat_header",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header\nclass Base:\n    def __init__(self,x_tenant: str=Header()): self.x_tenant=x_tenant\nclass Tenant(Base): pass\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(Tenant)): return {}\n",
      "hau_qua": "Không nhắc header x-tenant của constructor kế thừa. Resolver chỉ tìm __init__ trong thân class hiện tại; nhánh kế tiếp xử lý trường model, không theo constructor lớp cha. slice/l3slice/docfacts.py:1323; slice/l3slice/docfacts.py:1326.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. File main.py; route decorator main.py:6-7, application main.py:5, dependency Tenant tại main.py:7. add_route=[]; reminders=''; OpenAPI có header x-tenant. Helper kiểm reminder: slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_pydantic_field_alias_nhac_sai_query",
      "vi_du_code": "from fastapi import FastAPI, Depends\nfrom pydantic import BaseModel, Field\nclass Filters(BaseModel):\n    sort_by: str=Field('name',alias='sortBy')\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(Filters)): return {}\n",
      "hau_qua": "Nhắc query sort_by và bỏ query thật sortBy. _model_fields chỉ lưu tên Python, annotation và dòng; bỏ Field(alias=...). slice/l3slice/docfacts.py:1328; slice/l3slice/docfacts.py:1445.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. File main.py; route decorator main.py:6-7, application main.py:5, dependency Filters tại main.py:7. add_route=[]; reminder ghi query 'sort_by' tại main.py:4; OpenAPI chỉ có query sortBy. Helper kiểm reminder: slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "partial_keyword_bi_coi_la_tham_so_khong_the_ghi_de",
      "vi_du_code": "from fastapi import FastAPI, Depends\nfrom functools import partial\ndef filters(limit: int=10): return limit\ntenant=partial(filters,limit=20)\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)): return v\n",
      "hau_qua": "Bỏ query limit mặc dù keyword đã gán trong partial vẫn là default có thể ghi đè. Bản sửa gom cả keyword vào bound rồi loại khỏi reminder. slice/l3slice/docfacts.py:1347; slice/l3slice/docfacts.py:1389.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. File main.py; route decorator main.py:6-7, application main.py:5, dependency tenant tại main.py:7. add_route=[]; reminders=''; OpenAPI có query limit. FastAPI TestClient: GET /x trả 20, GET /x?limit=99 trả 99. Helper kiểm reminder: slice/tests/test_checker_counterexamples.py:32."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: nhận diện decorator và các ca đăng ký trực tiếp đã có tiến bộ, nhưng chưa đáng tin cao cho application/path hoàn chỉnh vì nhận thứ tự prefix sai và bị helper không liên quan làm bỏ kiểm prefix (slice/tests/test_checker_counterexamples.py:506; slice/l3slice/docfacts.py:598; slice/l3slice/docfacts.py:618). HTTP claim: còn chấp nhận đích cấu hình không quyết định URL và nhận dict.get thành HTTP qua thuộc tính trùng tên; đây là lỗi nhận thông tin sai, không chỉ thiếu hỗ trợ cú pháp (slice/l3slice/docfacts.py:1045; slice/l3slice/astscan.py:413). HTTP suspects: sửa được import module/Annotated trực tiếp nhưng vẫn bỏ chuỗi xuất lại qua package và tham số không annotation; phép đo recall theo dòng còn che sai loại/thiếu call nên không dùng gold_items_not_flagged=0 để kết luận bao phủ cao (slice/l3slice/docfacts.py:1115; slice/l3slice/astscan.py:417; slice/tools/fr029_checkaudit.py:481). Dependency params: xử lý được nhiều dạng trực tiếp, class, instance, Annotated và partial theo vị trí; còn sai với constructor kế thừa, alias trường Pydantic và keyword partial (slice/tests/test_checker_counterexamples.py:472; slice/tests/test_checker_counterexamples.py:567; slice/l3slice/docfacts.py:1324; slice/l3slice/docfacts.py:1347; slice/l3slice/docfacts.py:1445). Đã chạy nguyên assertion của 67 test, chỉ thay helper tạo snapshot bằng SourceTools trong RAM; không chạy lại toàn bộ 37 bộ gold. Số liệu r26 và hai sanity được đọc đối chiếu với code; hash đầu/cuối phiên khớp báo cáo: docfacts=977de8b6761e3f3b, astscan=0bc7c45db547f1ae, audit=f79c06c33a006776 (slice/tests/test_docagent.py:105; slice/l3slice/source_tools.py:100; ket-qua-chay/fr029-checkaudit-20261008-r26/summary.json:3). Các snippet mới dùng cấu trúc claim của helper route/http/reminders hiện có; đối chiếu runtime bằng FastAPI 0.115.6, Pydantic 2.10.4 và httpx 0.28.1. tan_suat_uoc là nhận định định tính về dạng code, không phải tần suất đo trên corpus; tin_cay cũng không phải khoảng tin cậy thống kê."
}
```

“da_xu_ly” xác nhận ca cụ thể đã nêu; các biến thể mới được đánh giá riêng.
Chỉ đọc repo; thử nghiệm trong RAM bằng Python `-B`, không gọi HTTP ra ngoài.
Không đọc `docs/`, `HANDOFF` hay `.aide/evidence/reviews/`.