```json
{
  "vong4": [
    {
      "muc": "PVD01_nhan_nham_route_path",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại test: từ chối '/fake' lấy từ name=, nhận '/real' từ đối số path. slice/tests/test_checker_counterexamples.py:229."
    },
    {
      "muc": "PVD02_dependency_trong_literal",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test loại tên dependency chỉ xuất hiện trong literal vẫn qua. Kết luận giới hạn ở ca này; dependency_at vẫn tìm tên trong văn bản sau khi bỏ literal. slice/tests/test_checker_counterexamples.py:236; slice/l3slice/docfacts.py:368."
    },
    {
      "muc": "PVD03_dependency_trung_ten_module",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chọn đúng dependency được import từ a.py, không lấy b.py, vẫn qua. slice/tests/test_checker_counterexamples.py:243."
    },
    {
      "muc": "PVD04_header_convert_underscores_false",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test giữ x_custom vẫn qua; checker tôn trọng convert_underscores=False. slice/tests/test_checker_counterexamples.py:251; slice/l3slice/docfacts.py:1321."
    },
    {
      "muc": "PVD05_query_khong_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test nhắc query q không annotation vẫn qua. slice/tests/test_checker_counterexamples.py:258; slice/l3slice/docfacts.py:1308."
    },
    {
      "muc": "PVD06_http_trung_bien_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test phân biệt c là client ở hàm remote và dict ở hàm e vẫn qua. slice/tests/test_checker_counterexamples.py:267; slice/l3slice/astscan.py:311."
    },
    {
      "muc": "PVD07_client_at_khong_ton_tai_va_khong_lien_quan",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Các ca vị trí không tồn tại, receiver khác tên, và cùng tên nhưng thuộc hai hàm đều bị từ chối. Đây là xác nhận các ca đã nêu, không chứng minh mọi binding client_at. slice/tests/test_checker_counterexamples.py:280; slice/tests/test_checker_counterexamples.py:372; slice/tests/test_checker_counterexamples.py:453; slice/l3slice/docfacts.py:956."
    },
    {
      "muc": "PVD08_http_client_qua_depends",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test provider cùng file và provider import trực tiếp đều qua cho suspect và claim. slice/tests/test_checker_counterexamples.py:286; slice/tests/test_checker_counterexamples.py:326."
    },
    {
      "muc": "PVD09_import_client_co_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test suspect cho AnnAssign được import trực tiếp vẫn qua. slice/tests/test_checker_counterexamples.py:293."
    },
    {
      "muc": "PVD10_hai_http_call_cung_dong",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test GET+POST và GET(a)+GET(b) cùng dòng đều qua; claim lưu thêm col_offset. Đây là thuộc tính checker, khác vấn đề chấm recall theo dòng. slice/tests/test_checker_counterexamples.py:298; slice/tests/test_checker_counterexamples.py:378; slice/l3slice/docfacts.py:931."
    },
    {
      "muc": "v3_ghep_method_va_path_tu_hai_decorator",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test từ chối GET /write, nhận POST /write vẫn qua. slice/tests/test_checker_counterexamples.py:311; slice/l3slice/docfacts.py:621."
    },
    {
      "muc": "v3_sqlalchemy_session_annotation_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test không flag và không nhận SQLAlchemy Session.get như HTTP vẫn qua. slice/tests/test_checker_counterexamples.py:320; slice/l3slice/astscan.py:205."
    },
    {
      "muc": "v3_bo_sot_http_provider_import_tu_module_khac",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test provider được import trực tiếp từ clients.py vẫn qua. slice/tests/test_checker_counterexamples.py:326; slice/l3slice/docfacts.py:1019."
    },
    {
      "muc": "v3_dependency_dang_class_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Depends(Filters) lấy query q từ __init__, bỏ self, vẫn qua. slice/tests/test_checker_counterexamples.py:333; slice/l3slice/docfacts.py:1247."
    },
    {
      "muc": "v3_dependency_import_doi_ten_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test from deps import dep as tenant vẫn nhắc x-tenant. slice/tests/test_checker_counterexamples.py:342; slice/l3slice/docfacts.py:1262."
    },
    {
      "muc": "v3_alias_annotated_header_mat_reminder",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test alias Annotated chứa Header cùng file vẫn qua. slice/tests/test_checker_counterexamples.py:348; slice/l3slice/docfacts.py:1304."
    },
    {
      "muc": "v3_dict_get_sau_response_json_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chỉ tính HTTP call thật, từ chối target='id' của dict.get, vẫn qua. slice/tests/test_checker_counterexamples.py:357; slice/l3slice/astscan.py:366."
    },
    {
      "muc": "v4_route_sai_application_va_thieu_prefix_van_duoc_nhan",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca cụ thể đã sửa: thiếu include_prefix bị từ chối, admin không đăng ký router bị từ chối, claim đủ prefix được nhận. Prefix tại constructor APIRouter còn lỗi riêng bên dưới. slice/tests/test_checker_counterexamples.py:389; slice/l3slice/docfacts.py:598; slice/l3slice/docfacts.py:601."
    },
    {
      "muc": "v4_nhan_khoa_header_lam_cau_hinh_dich_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test từ chối API_KEY trong headers và nhận URL trong đối số URL qua. Kiểm tra mới giới hạn vào biểu thức URL khi không có config_at. slice/tests/test_checker_counterexamples.py:400; slice/l3slice/docfacts.py:987."
    },
    {
      "muc": "v4_annotation_client_khong_giu_thu_vien",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca một tham số wire: httpx.Client đã giữ thư viện và từ chối requests. Hai hàm dùng cùng tên tham số còn lỗi riêng bên dưới. slice/tests/test_checker_counterexamples.py:408; slice/l3slice/astscan.py:287."
    },
    {
      "muc": "v4_dependency_callable_instance_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test tenant=Tenant(); Depends(tenant) nhắc x-tenant qua. Resolver đã theo instance tới __call__. slice/tests/test_checker_counterexamples.py:414; slice/l3slice/docfacts.py:1255."
    },
    {
      "muc": "v4_dependency_literal_enum_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test nhắc cả sort và order qua; scalar đã nhận Literal và Enum. slice/tests/test_checker_counterexamples.py:423; slice/l3slice/astscan.py:472; slice/l3slice/astscan.py:481."
    },
    {
      "muc": "v4_annotated_marker_import_doi_ten_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Tenant được import thành TenantHeader vẫn nhắc X-Tenant qua. Resolver đã tra tên gốc của import. slice/tests/test_checker_counterexamples.py:434; slice/l3slice/docfacts.py:395."
    },
    {
      "muc": "v4_http_client_lifespan_app_state_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test request.app.state.wire ở module khác được flag qua. Checker thu thập thuộc tính state chứa client trên các cây AST. slice/tests/test_checker_counterexamples.py:444; slice/l3slice/docfacts.py:1026."
    },
    {
      "muc": "v4_client_at_trung_ten_nhung_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test cache trong remote và cache dict trong local bị từ chối qua; có kiểm tra hàm bao quanh khi receiver là Name và hai vị trí cùng file. slice/tests/test_checker_counterexamples.py:453; slice/l3slice/docfacts.py:956."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Hash ba file ban đầu khớp r20, nhưng code đã đổi trong phiên: bản chốt dùng docfacts=a243d5957f49fb89, astscan=ee184e05ad13f85b, audit=7940242948d70dca. R20 ghi sanity='không'. Sanity vẫn thay hàm con, chưa đi trọn add_route/submit; exit code chỉ dựa trên exception. Gold mới có hash A/B đã đối chiếu khớp, nhưng báo cáo chạy chưa gắn hash toàn bộ gold/source. ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:7; slice/tools/fr029_checkaudit.py:556; slice/tools/fr029_checkaudit.py:598; slice/tools/fr029_checkaudit.py:625; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:987."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Có gọi open_problems nhưng vẫn gán trực tiếp probe.routes. Tái hiện reminder ghi dependency FAKE, nonexistent.py:999 nhưng đúng query q: reminders=1, reminders_wrong=[], missed=[]. Nguồn dependency và dòng bằng chứng chưa được chấm. slice/tools/fr029_checkaudit.py:347; slice/tools/fr029_checkaudit.py:353; slice/tools/fr029_checkaudit.py:356."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Có measured, r20 đo dependency trên 14/37 case. Vẫn bỏ dependency cấp app/router; http_items không có nhánh dev; calls tăng trước các nhánh bỏ qua. Bốn repo mới đều có gold_dep_params=0 và literal=0, nên các số 0 lỗi ở đó không chứng minh hai năng lực này. slice/tools/fr029_checkaudit.py:241; slice/tools/fr029_checkaudit.py:316; slice/tools/fr029_checkaudit.py:373; slice/tools/fr029_checkaudit.py:395; ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:188; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:234; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:280; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:326."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Thêm kiểm đăng ký nhưng chỉ hỏi route có dưới ít nhất một app và chỉ ghi lỗi không được include_router; chưa nộp claim đầy đủ để mutation application/prefix. Dependency vẫn tránh tên trùng phần cuối hoặc xuất hiện trên dòng. HTTP chưa mutation config_at/client_at/config key; mutation method vẫn yêu cầu verb trực tiếp. slice/tools/fr029_checkaudit.py:186; slice/tools/fr029_checkaudit.py:187; slice/tools/fr029_checkaudit.py:339; slice/tools/fr029_checkaudit.py:421; slice/tools/fr029_checkaudit.py:429."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Checker vẫn theo số call, nhưng audit chưa sửa việc bỏ looks_like và multiplicity. Tái cấp một suspect loại route tại dòng có hai HTTP gold call: suspects=1, gold_items=2, gold_not_flagged=[], not_gold_item=0. Vùng miễn noise vẫn kéo thêm ba dòng. slice/l3slice/docfacts.py:1153; slice/tools/fr029_checkaudit.py:454; slice/tools/fr029_checkaudit.py:469; slice/tools/fr029_checkaudit.py:492."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Route vẫn dùng checker chọn decorator và lấy expected path từ source. HTTP config vẫn bị đổi thành unknown; method có thể bị hạ thành unknown theo regex, alt_methods chưa được đọc. R20 còn hai gold_vs_rule. slice/tools/fr029_checkaudit.py:132; slice/tools/fr029_checkaudit.py:145; slice/tools/fr029_checkaudit.py:373; slice/tools/fr029_checkaudit.py:411; slice/tools/fr029_checkaudit.py:414; ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:35."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã đưa bốn repo mới có gold vào phép đo; tôi chạy lại bốn repo và thu cùng kết quả chính. Tuy nhiên 1549 route mutation chưa kiểm đầy đủ application/prefix; HTTP thiếu mutation quan hệ cấu hình/client. Gold ghi hai người viết là Claude Opus/Sonnet, reviewed_by_human=false, không phải hai người chấm độc lập đã được xác minh. slice/tools/fr029_checkaudit.py:53; slice/tools/fr029_checkaudit.py:160; slice/tools/fr029_checkaudit.py:421; ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:10; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:983; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:995."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "Có sửa thực chất: 57/57 test bản chốt qua, gồm RoundFour, RoundThreeLeftovers và các test HeldOutFindings vừa thêm. Tuy nhiên bảy dạng code mới bên dưới vẫn sai; constructor app còn nhận theo tên và provenance HTTP còn dùng bảng tên toàn file. slice/tests/test_checker_counterexamples.py:386; slice/tests/test_checker_counterexamples.py:460; slice/tests/test_checker_counterexamples.py:494; slice/l3slice/docfacts.py:668; slice/l3slice/astscan.py:291."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Bound method/import đổi tên vẫn qua test, app.state đã được flag. Tái chạy: getattr(wire,'get')(url) được flag nhưng claim vẫn bị từ chối; e(wire) không annotation vẫn suspects=[]. slice/tests/test_checker_counterexamples.py:444; slice/tests/test_checker_counterexamples.py:497; slice/tests/test_checker_counterexamples.py:505; slice/l3slice/astscan.py:376; slice/l3slice/docfacts.py:886; slice/l3slice/astscan.py:348."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_bo_prefix_tai_constructor_APIRouter",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nr=APIRouter(prefix='/v1')\n@r.get('/x')\ndef e(): return {}\napp.include_router(r)\n# File main.py. Nộp route('main.py::e','main.py:4-5','/x',application='main.py:2').",
      "hau_qua": "Claim thiếu /v1 được nhận. Đồ thị đăng ký chỉ yêu cầu vị trí include_router/mount có prefix, không bắt buộc prefix tại constructor APIRouter. slice/l3slice/docfacts.py:534; slice/l3slice/docfacts.py:548; slice/l3slice/docfacts.py:601.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có, bản chốt: add_route=[]; FastAPI 0.115.6 OpenAPI chỉ có /v1/x. Dùng helper tại slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "config_at_cua_client_khac_duoc_nhan",
      "vi_du_code": "import httpx\nfrom types import SimpleNamespace\nsettings=SimpleNamespace(A='https://a.example',B='https://b.example')\na=httpx.Client(base_url=settings.A)\nb=httpx.Client(base_url=settings.B)\ndef e(): return a.get('/x')\n# File h.py. add_http({'at':'h.py:6','library':'httpx','method':'GET','target':{'kind':'config','value':'settings.B','config_at':'h.py:5'}}).",
      "hau_qua": "Nhận đích cấu hình của b cho lời gọi trên a. config_at chỉ cần chứa khóa và base_url; nhánh kiểm URL bỏ qua khi có config_at, chưa buộc nó vào receiver. slice/l3slice/docfacts.py:917; slice/l3slice/docfacts.py:987.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có, bản chốt: add_http=[]; gọi e với a dùng MockTransport xác nhận URL https://a.example/x. Helper claim tại slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "thu_vien_client_bi_tron_giua_hai_scope",
      "vi_du_code": "import httpx\nimport requests\ndef a(wire: httpx.Client): return wire.get('https://a.example')\ndef b(wire: requests.Session): return wire.get('https://b.example')\n# File h.py. Nộp hai claim tại h.py:4, method GET, literal https://b.example; lần lượt library=requests và library=httpx.",
      "hau_qua": "Claim đúng requests bị từ chối, claim sai httpx được nhận. client_lib.setdefault giữ thư viện đầu tiên theo tên wire trên toàn file; lib_of không phân biệt hàm. slice/l3slice/astscan.py:190; slice/l3slice/astscan.py:291; slice/l3slice/docfacts.py:949.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có, bản chốt: requests trả lỗi 'client ... được tạo từ httpx'; httpx trả []. Hai lời gọi kiểm dùng helper tại slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "http_client_qua_import_module_bi_bo_sot",
      "vi_du_code": "# clients.py\nimport httpx\nwire=httpx.Client()\n\n# routes.py\nimport clients\ndef e(): return clients.wire.get('https://real.example')",
      "hau_qua": "Không có HTTP suspect; claim đúng cũng bị từ chối nếu không bổ sung client_at. Resolver chỉ nối imported client khi import có tên thành viên, bỏ import clients. slice/l3slice/docfacts.py:1013; slice/l3slice/astscan.py:128; slice/l3slice/docfacts.py:1164.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có, snapshot hai file: suspects=[]; add_http tại routes.py:2 bị từ chối. Thực thi e với clients.wire là httpx.Client dùng MockTransport trả 200. Cơ chế dựng claim tại slice/tests/test_checker_counterexamples.py:17."
    },
    {
      "loai": "http_client_qua_alias_Annotated_Depends_bi_bo_sot",
      "vi_du_code": "# clients.py\nimport httpx\nfrom typing import Annotated\nfrom fastapi import Depends\ndef get_wire():\n    with httpx.Client() as c: yield c\nWire=Annotated[httpx.Client,Depends(get_wire)]\n\n# routes.py\nfrom fastapi import FastAPI\nfrom clients import Wire\napp=FastAPI()\n@app.get('/x')\ndef e(wire: Wire): return wire.get('https://real.example')",
      "hau_qua": "Chỉ flag route, bỏ HTTP trong handler. Alias import Wire không được phân giải thành client/provider trước khi quyết định scan.capable. slice/l3slice/docfacts.py:1015; slice/l3slice/docfacts.py:1019; slice/l3slice/astscan.py:144; slice/l3slice/docfacts.py:1164.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có, bản chốt: suspects chỉ chứa routes.py:4 loại route; claim HTTP tại routes.py:5 bị từ chối. FastAPI xác nhận dependency là get_wire; gọi handler với MockTransport trả 200. Helper snapshot tại slice/tests/test_checker_counterexamples.py:17."
    },
    {
      "loai": "dependency_functools_partial_mat_header",
      "vi_du_code": "from fastapi import FastAPI,Depends,Header\nfrom functools import partial\ndef check(scope, x_tenant: str=Header()): return x_tenant\ntenant=partial(check,'read')\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)): return {}\n# File main.py. route('main.py::e','main.py:6-7','/x',application='main.py:5',deps=[('tenant','main.py:7')]).",
      "hau_qua": "Route được nhận nhưng không nhắc header x-tenant. Resolver instance chỉ xử lý constructor của class trong snapshot, không theo partial tới callable gốc. slice/l3slice/docfacts.py:1255; slice/l3slice/docfacts.py:1277.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có, bản chốt: add_route=[], reminder dependency rỗng; OpenAPI có header x-tenant. Hàm lọc reminder tại slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_long_Annotated_Depends_khong_doi_so_mat_query",
      "vi_du_code": "from fastapi import FastAPI,Depends\nfrom typing import Annotated\nclass Filters:\n    def __init__(self,q: str=''): self.q=q\ndef outer(f: Annotated[Filters,Depends()]): return f\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(outer)): return {}\n# File main.py. route('main.py::e','main.py:7-8','/x',application='main.py:6',deps=[('outer','main.py:8')]).",
      "hau_qua": "Không theo Depends() tới Filters nên mất query q. Nhánh suy dependency từ annotation chỉ nhận ast.Name/ast.Attribute, trong khi Annotated là ast.Subscript. slice/l3slice/docfacts.py:1302; slice/l3slice/docfacts.py:1330.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có, bản chốt: add_route=[], reminder dependency rỗng; OpenAPI có query q. Hàm lọc reminder tại slice/tests/test_checker_counterexamples.py:32."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: các ca decorator/method và đăng ký đơn giản đã cải thiện, nhưng vẫn nhận đường dẫn thiếu router prefix; audit chưa kiểm đầy đủ claim application/path (slice/tests/test_checker_counterexamples.py:389; slice/l3slice/docfacts.py:601; slice/tools/fr029_checkaudit.py:186). HTTP claim: còn nhận sai config_at và nhầm thư viện giữa hai scope, là lỗi chấp nhận thông tin sai (slice/l3slice/docfacts.py:917; slice/l3slice/astscan.py:291). HTTP suspects: còn bỏ import module và alias Annotated; recall theo dòng của audit vẫn che sai loại và thiếu call (slice/l3slice/docfacts.py:1013; slice/l3slice/astscan.py:144; slice/tools/fr029_checkaudit.py:454). Dependency params: các ca class, callable instance, marker alias, Literal/Enum và Pydantic/Union đã có test qua; còn bỏ partial và Depends() lồng trong Annotated, nên chưa đạt cao (slice/tests/test_checker_counterexamples.py:414; slice/tests/test_checker_counterexamples.py:423; slice/tests/test_checker_counterexamples.py:473; slice/l3slice/docfacts.py:1330). Tôi chạy lại bốn repo mới, xác nhận tổng 48 route và 6 HTTP call, nhưng cả bốn đều không có dependency parameter trong mẫu số và không kiểm URL literal; không dùng các số 0 đó để suy ra bao phủ rộng (ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:165; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:211; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:257; ket-qua-chay/fr029-checkaudit-20261008-r20-real/audit.json:303). Bản chốt cố định trong RAM: docfacts=a243d5957f49fb89, astscan=ee184e05ad13f85b, audit=7940242948d70dca, tests=819462af8d12400b; hash không đổi trong lượt xác nhận cuối, khác mốc r20 (ket-qua-chay/fr029-checkaudit-20261008-r20-real/summary.json:3). Các test được chạy nguyên assertion, chỉ thay helper tạo file tạm bằng SourceTools từ dữ liệu RAM vì môi trường chặn ghi (slice/tests/test_docagent.py:105; slice/l3slice/source_tools.py:100). tan_suat_uoc là ước lượng định tính về dạng code, không phải tỷ lệ đã đo; các mức tin_cay cũng không phải khoảng tin cậy thống kê."
}
```

57/57 test bản chốt qua; tám ca cụ thể vòng 4 đã được sửa (`slice/tests/test_checker_counterexamples.py:386`).
Bảy phản ví dụ mới còn tái hiện; ca Pydantic được sửa trong phiên nên không tính là lỗi còn mở (`slice/tests/test_checker_counterexamples.py:473`).
Chỉ đọc repo; thử nghiệm trong RAM, dùng Python `-B`, OpenAPI và MockTransport, không gọi HTTP ra ngoài.
Không đọc `docs/`, `HANDOFF` hoặc `.aide/evidence/reviews/`.