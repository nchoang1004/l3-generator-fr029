```json
{
  "vong3": [
    {
      "muc": "PVD01_nhan_nham_route_path",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test cũ chạy qua; path được lấy từ đối số decorator, không lấy name='/fake'. slice/tests/test_checker_counterexamples.py:229; slice/l3slice/docfacts.py:489."
    },
    {
      "muc": "PVD02_dependency_trong_literal",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test cũ chạy qua; chuỗi literal bị loại trước khi tìm tên dependency. Đây là kết luận cho phản ví dụ cũ, chưa chứng minh tên nằm đúng trong Depends. slice/tests/test_checker_counterexamples.py:236; slice/l3slice/docfacts.py:361."
    },
    {
      "muc": "PVD03_dependency_trung_ten_module",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chọn dependency theo module chạy qua. slice/tests/test_checker_counterexamples.py:243; slice/l3slice/docfacts.py:1111."
    },
    {
      "muc": "PVD04_header_convert_underscores_false",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test giữ x_custom chạy qua; phép đo chỉ lowercase header, không đồng nhất '_' với '-'. slice/tests/test_checker_counterexamples.py:251; slice/tools/fr029_checkaudit.py:251."
    },
    {
      "muc": "PVD05_query_khong_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test tham số không annotation chạy qua; nhánh ann is None vẫn được xử lý. slice/tests/test_checker_counterexamples.py:258; slice/l3slice/docfacts.py:1149."
    },
    {
      "muc": "PVD06_http_trung_bien_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca c là client ở hàm khác nhưng là dict trong hàm đang xét chạy qua. Kết luận này áp dụng khi không dùng client_at để vượt kiểm receiver. slice/tests/test_checker_counterexamples.py:267; slice/l3slice/astscan.py:297."
    },
    {
      "muc": "PVD07_client_at_khong_ton_tai_va_khong_lien_quan",
      "trang_thai": "mot_phan",
      "bang_chung": "Hai test từ chối vị trí không tồn tại và client khác tên đều qua. Tuy nhiên client_at chỉ đối chiếu cách viết tên receiver; tôi tái hiện cache ở hai scope khác nhau vẫn làm dict.get được nhận như HTTP. slice/tests/test_checker_counterexamples.py:280; slice/tests/test_checker_counterexamples.py:372; slice/l3slice/docfacts.py:836; slice/l3slice/docfacts.py:839."
    },
    {
      "muc": "PVD08_http_client_qua_depends",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Cả provider cùng file và provider import trực tiếp từ module khác đều có test chạy qua. slice/tests/test_checker_counterexamples.py:286; slice/tests/test_checker_counterexamples.py:326; slice/l3slice/docfacts.py:878."
    },
    {
      "muc": "PVD09_import_client_co_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test tìm HTTP suspect cho client có AnnAssign được import sang module khác chạy qua. Kết luận giới hạn ở quét suspect của ca cũ. slice/tests/test_checker_counterexamples.py:293; slice/l3slice/astscan.py:385."
    },
    {
      "muc": "PVD10_hai_http_call_cung_dong",
      "trang_thai": "da_xu_ly",
      "bang_chung": "GET+POST và GET(a)+GET(b) đều chạy qua; checker thử các candidate theo claim và lưu vị trí cột. slice/tests/test_checker_counterexamples.py:298; slice/tests/test_checker_counterexamples.py:378; slice/l3slice/docfacts.py:755; slice/l3slice/docfacts.py:814."
    },
    {
      "muc": "con_lai_01_sanity_co_phan_biet",
      "trang_thai": "da_xu_ly",
      "bang_chung": "R16-accept báo 1362/291/110 false acceptance route/dependency/HTTP; r16-reject báo 148/27 false rejection dependency/HTTP và 387 gold item không được flag. Riêng 710 route false rejection trên 358 checked là số sự kiện lỗi, không phải số route lỗi duy nhất. ket-qua-chay/fr029-checkaudit-20261008-r16-accept/summary.json:20; ket-qua-chay/fr029-checkaudit-20261008-r16-accept/summary.json:24; ket-qua-chay/fr029-checkaudit-20261008-r16-accept/summary.json:32; ket-qua-chay/fr029-checkaudit-20261008-r16-reject/summary.json:18; ket-qua-chay/fr029-checkaudit-20261008-r16-reject/summary.json:37; slice/tools/fr029_checkaudit.py:127; slice/tools/fr029_checkaudit.py:147."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Ba báo cáo r16 lưu cùng hash code, nhưng bản chốt kiểm toán hiện tại có docfacts=0fea548db8e9d688 và astscan=a785cb2bba1fb395, khác r16; audit=70add74780ced806 vẫn khớp. Chưa có hash gold/source; sanity vẫn thay hàm con, chưa chạy trọn add_route/submit; exit code chỉ phụ thuộc exception. ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r16-accept/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r16-reject/summary.json:3; slice/tools/fr029_checkaudit.py:521; slice/tools/fr029_checkaudit.py:565; slice/tools/fr029_checkaudit.py:590."
    },
    {
      "muc": "con_lai_03_oracle_xoa_khac_biet_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Đọc code xác nhận _key giữ khác biệt x_custom/x-custom; so reminder và gold dùng khóa này. slice/tools/fr029_checkaudit.py:251; slice/tools/fr029_checkaudit.py:325; slice/tools/fr029_checkaudit.py:329."
    },
    {
      "muc": "con_lai_04_mau_so_mat_dependency_param",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Tái chạy e(v=Depends(dep), note: str='q') với dependency_params=[]: gold_dep_params=1 và missed chứa query q. Literal trong signature không còn làm mất mẫu số của phản ví dụ cũ. slice/tools/fr029_checkaudit.py:256; slice/tools/fr029_checkaudit.py:332."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã chạy open_problems: monkeypatch hàm này trả [] nay làm audit báo thiếu query q. Tuy nhiên probe vẫn được gán trực tiếp vào routes, bỏ qua add_route/submit; phép chấm chỉ so tên/vị trí tham số, chưa xác minh nguồn dependency và dòng bằng chứng đúng. slice/tools/fr029_checkaudit.py:316; slice/tools/fr029_checkaudit.py:322; slice/tools/fr029_checkaudit.py:331."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Có trường measured và dependency_cases_measured=10/33, nhưng vẫn bỏ dependency cấp app/router; http_items không có nhánh dev; calls tăng trước các nhánh continue. Không thể đọc các số 0 thành đã kiểm đủ phạm vi. slice/tools/fr029_checkaudit.py:213; slice/tools/fr029_checkaudit.py:285; slice/tools/fr029_checkaudit.py:342; slice/tools/fr029_checkaudit.py:364; slice/tools/fr029_checkaudit.py:376; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:14."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã thêm mutation path nhưng chỉ hỏi _decorator_paths, chưa nộp claim đầy đủ để kiểm application/prefix. Pool dependency vẫn loại tên trùng phần cuối hoặc xuất hiện trên dòng. HTTP chưa mutation config key/client_at; request/stream không vào nhánh mutation method. slice/tools/fr029_checkaudit.py:135; slice/tools/fr029_checkaudit.py:144; slice/tools/fr029_checkaudit.py:308; slice/tools/fr029_checkaudit.py:390; slice/tools/fr029_checkaudit.py:398."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Checker đếm call, nhưng audit vẫn bỏ looks_like và multiplicity. Tái cấp một suspect loại route tại dòng chứa hai HTTP gold call: gold_items=2, gold_not_flagged=[], not_gold_item=0. Vùng miễn noise vẫn kéo dài thêm ba dòng. slice/l3slice/docfacts.py:1008; slice/tools/fr029_checkaudit.py:423; slice/tools/fr029_checkaudit.py:438; slice/tools/fr029_checkaudit.py:461."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Đường reminder đã cải thiện, nhưng route vẫn nhờ checker chọn decorator; expected path lấy từ source; HTTP config bị hạ thành unknown, method bị điều chỉnh theo regex và không đọc alt_methods. R16 còn hai gold_vs_rule. slice/tools/fr029_checkaudit.py:125; slice/tools/fr029_checkaudit.py:138; slice/tools/fr029_checkaudit.py:348; slice/tools/fr029_checkaudit.py:380; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:33."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã tăng mutation route lên 1362, nhưng các quan hệ application/prefix/config/client_at vẫn thiếu phép đo; heldout vẫn chỉ xuất packet cho người khác chấm. slice/tools/fr029_checkaudit.py:135; slice/tools/fr029_checkaudit.py:390; slice/tools/fr029_checkaudit.py:470; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:10."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "46 test của bản chốt đều qua, gồm sửa thực chất cho bảy ca vòng 3 và hai test HTTP mới thêm trong lúc kiểm toán. Tuy nhiên constructor app vẫn nhận theo tên; dependency còn tra bảng tên và danh sách scalar hẹp. Các phản ví dụ mới bên dưới đều tái hiện trên cùng bản chốt. slice/tests/test_checker_counterexamples.py:308; slice/tests/test_checker_counterexamples.py:389; slice/tests/test_checker_counterexamples.py:397; slice/l3slice/docfacts.py:551; slice/l3slice/docfacts.py:1097; slice/l3slice/astscan.py:442."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Tái chạy bản chốt: bound method và import get as fetch nay vừa được flag vừa nhận claim; getattr được flag nhưng claim vẫn bị từ chối; tham số wire không annotation vẫn suspects=[]. slice/tests/test_checker_counterexamples.py:389; slice/tests/test_checker_counterexamples.py:397; slice/l3slice/astscan.py:153; slice/l3slice/astscan.py:333; slice/l3slice/docfacts.py:747; slice/l3slice/docfacts.py:769."
    },
    {
      "muc": "v3_ghep_method_va_path_tu_hai_decorator",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test GET /write bị từ chối và POST /write được nhận chạy qua. _decorator_paths lọc theo method. slice/tests/test_checker_counterexamples.py:311; slice/l3slice/docfacts.py:504."
    },
    {
      "muc": "v3_sqlalchemy_session_annotation_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Session của SQLAlchemy không được flag/nhận như HTTP chạy qua. Annotation nay phải dẫn tới class thuộc thư viện HTTP. slice/tests/test_checker_counterexamples.py:320; slice/l3slice/astscan.py:207."
    },
    {
      "muc": "v3_bo_sot_http_provider_import_tu_module_khac",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test provider yield client ở clients.py, handler dùng Depends ở main.py chạy qua cả suspect và claim. slice/tests/test_checker_counterexamples.py:326; slice/l3slice/docfacts.py:893."
    },
    {
      "muc": "v3_dependency_dang_class_mat_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test Depends(Filters) nhắc query q và không nhắc self chạy qua; đã đọc __init__. slice/tests/test_checker_counterexamples.py:333; slice/l3slice/docfacts.py:1099."
    },
    {
      "muc": "v3_dependency_import_doi_ten_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test from deps import dep as tenant nhắc x-tenant chạy qua; đã giải tên import khi không tìm thấy định nghĩa tên alias. slice/tests/test_checker_counterexamples.py:342; slice/l3slice/docfacts.py:1103."
    },
    {
      "muc": "v3_alias_annotated_header_mat_reminder",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test alias Header cùng file nhắc X-Tenant chạy qua. Alias import đổi tên vẫn có lỗi riêng bên dưới. slice/tests/test_checker_counterexamples.py:348; slice/l3slice/docfacts.py:383; slice/l3slice/docfacts.py:1145."
    },
    {
      "muc": "v3_dict_get_sau_response_json_bi_coi_la_http",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test chỉ đếm một HTTP call, nhận URL thật và từ chối target='id' chạy qua. Receiver dạng call phải là constructor/provider client. slice/tests/test_checker_counterexamples.py:357; slice/l3slice/astscan.py:331; slice/l3slice/astscan.py:352."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_sai_application_va_thieu_prefix_van_duoc_nhan",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI, APIRouter\napp=FastAPI()\nadmin=FastAPI()\nr=APIRouter()\n@r.get('/x')\ndef e(): return {}\napp.include_router(r,prefix='/api')\n# Dùng helper route trong test_checker_counterexamples.py:25:\n# route('main.py::e','main.py:5-6','/x',application='main.py:3')\n# và cùng claim nhưng application='main.py:2'.",
      "hau_qua": "Cả hai add_route đều trả []; OpenAPI của admin không có route, còn app chỉ có /api/x. Checker kiểm dòng tạo app và literal từng phần nhưng không buộc chuỗi đăng ký đầy đủ, đúng application. slice/l3slice/docfacts.py:258; slice/l3slice/docfacts.py:269; slice/l3slice/docfacts.py:304; slice/l3slice/docfacts.py:352.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. Chạy hai claim trên bản chốt và dựng OpenAPI bằng FastAPI 0.115.6: app=['/api/x'], admin=[]. Helper claim: slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "nhan_khoa_header_lam_cau_hinh_dich_http",
      "vi_du_code": "# h.py\nimport httpx\nfrom types import SimpleNamespace\nsettings=SimpleNamespace(API_KEY='demo', URL='https://real.example')\ndef e():\n    return httpx.get(settings.URL, headers={'X-Key': settings.API_KEY})\n# add_http({'at':'h.py:5','library':'httpx','method':'GET',\n# 'target':{'kind':'config','value':'settings.API_KEY'}})",
      "hau_qua": "Claim sai đích trả []; nhánh config chỉ kiểm khóa xuất hiện trong toàn lời gọi, không kiểm nó là biểu thức URL. slice/l3slice/docfacts.py:797; slice/l3slice/docfacts.py:802.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. add_http=[]; chạy hàm với httpx.MockTransport xác nhận request.url='https://real.example', lấy từ settings.URL. Nhánh gây lỗi: slice/l3slice/docfacts.py:802."
    },
    {
      "loai": "annotation_client_khong_giu_thu_vien",
      "vi_du_code": "# h.py\nimport httpx\nimport requests\ndef e(wire: httpx.Client):\n    return wire.get('https://real.example')\n# add_http({'at':'h.py:4','library':'requests','method':'GET',\n# 'target':{'kind':'literal','value':'https://real.example'}})",
      "hau_qua": "Claim library=requests được nhận dù annotation ghi httpx.Client. _bind ghi tên vào clients nhưng không lưu thư viện của annotation; kiểm library chỉ từ chối khi suy được recv_lib. slice/l3slice/astscan.py:276; slice/l3slice/docfacts.py:832.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_http=[]; truyền httpx.Client dùng MockTransport vào e nhận status 200. Điểm mất provenance: slice/l3slice/astscan.py:277."
    },
    {
      "loai": "dependency_callable_instance_mat_header",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI, Depends, Header\nclass Tenant:\n    def __call__(self, x_tenant: str = Header()): return x_tenant\ntenant=Tenant()\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)): return {}\n# route('main.py::e','main.py:6-7','/x',application='main.py:5',\n#       deps=[('tenant','main.py:7')])",
      "hau_qua": "Route được nhận nhưng không nhắc header x-tenant. Resolver hỗ trợ class->__init__, chưa theo instance->__call__. slice/l3slice/docfacts.py:1097; slice/l3slice/docfacts.py:1099; slice/l3slice/docfacts.py:1118.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_route=[], reminder dependency rỗng; OpenAPI có header x-tenant bắt buộc. Đường phát reminder: slice/l3slice/docfacts.py:1066."
    },
    {
      "loai": "dependency_literal_enum_mat_query",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI, Depends\nfrom typing import Literal\nfrom enum import Enum\nclass Order(str, Enum):\n    asc='asc'\n    desc='desc'\ndef filters(sort: Literal['name','date']='name', order: Order=Order.asc): return sort\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(filters)): return {}\n# route('main.py::e','main.py:9-10','/x',application='main.py:8',\n#       deps=[('filters','main.py:10')])",
      "hau_qua": "Không nhắc cả sort và order. scalar chỉ nhận tập tên dựng sẵn, Optional/Annotated và một số union; không nhận Literal hoặc Enum. slice/l3slice/astscan.py:442; slice/l3slice/astscan.py:445; slice/l3slice/docfacts.py:1149.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. add_route=[], reminder rỗng; OpenAPI xác nhận hai query parameter sort và order. Nhánh bỏ sót: slice/l3slice/astscan.py:455."
    },
    {
      "loai": "annotated_marker_import_doi_ten_mat_header",
      "vi_du_code": "# params.py\nfrom typing import Annotated\nfrom fastapi import Header\nTenant=Annotated[str,Header(alias='X-Tenant')]\n# main.py\nfrom fastapi import FastAPI, Depends\nfrom params import Tenant as TenantHeader\ndef dep(x: TenantHeader): return x\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n# route('main.py::e','main.py:5-6','/x',application='main.py:4',\n#       deps=[('dep','main.py:6')])",
      "hau_qua": "Alias Header cùng file đã sửa nhưng alias import đổi tên vẫn mất X-Tenant. _alias_markers lấy defs bằng tên cục bộ TenantHeader rồi lọc theo module, không đổi sang tên gốc Tenant. slice/l3slice/docfacts.py:386; slice/l3slice/docfacts.py:392; slice/l3slice/docfacts.py:394.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Snapshot hai file trả add_route=[], reminder rỗng; nạp module trong RAM, OpenAPI có header X-Tenant bắt buộc. Resolver gây lỗi: slice/l3slice/docfacts.py:383."
    },
    {
      "loai": "http_client_lifespan_app_state_bi_bo_sot",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI\nfrom contextlib import asynccontextmanager\nimport httpx\nfrom routes import router\n@asynccontextmanager\nasync def lifespan(app):\n    async with httpx.AsyncClient() as wire:\n        app.state.wire=wire\n        yield\napp=FastAPI(lifespan=lifespan)\napp.include_router(router)\n# routes.py\nfrom fastapi import APIRouter, Request\nrouter=APIRouter()\n@router.get('/x')\nasync def e(request: Request):\n    r=await request.app.state.wire.get('https://real.example')\n    return r.json()",
      "hau_qua": "suspects chỉ có route routes.py:3, không có HTTP routes.py:5. Truyền client qua app.state sang module không import HTTP không được nối kiểu; scan.capable=False làm bỏ quét HTTP. slice/l3slice/astscan.py:124; slice/l3slice/astscan.py:142; slice/l3slice/docfacts.py:878; slice/l3slice/docfacts.py:1019.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. Chạy snapshot hai file trên bản chốt xác nhận thiếu suspect. Gán AsyncClient dùng MockTransport vào app.state.wire rồi gọi handler với Starlette Request trả {'ok':true}. Điểm bỏ quét: slice/l3slice/docfacts.py:1019."
    },
    {
      "loai": "client_at_trung_ten_nhung_khac_scope",
      "vi_du_code": "# h.py\nimport httpx\ndef remote():\n    cache=httpx.Client()\n    return cache\ndef local():\n    cache={'id':7}\n    return cache.get('id')\n# add_http({'at':'h.py:7','library':'httpx','method':'GET',\n# 'client_at':'h.py:3','target':{'kind':'literal','value':'id'}})",
      "hau_qua": "Biến thể mới của lỗ hổng client_at: cùng tên cache ở hai scope làm claim dict.get được nhận. Đối chiếu tên bằng regex không chứng minh binding; khi có client_at, nhánh kiểm receiver bị bỏ qua. slice/l3slice/docfacts.py:836; slice/l3slice/docfacts.py:839.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_http=[] trên bản chốt; thực thi local() trả số 7, không gọi HTTP. Nhánh cho vượt kiểm: slice/l3slice/docfacts.py:839."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "thap"
  },
  "ly_do": "Route: các test decorator/method/path cơ bản đã qua, nhưng nhận sai application và thiếu prefix; audit chưa kiểm trọn claim nên mức vừa (slice/tests/test_checker_counterexamples.py:311; slice/l3slice/docfacts.py:258; slice/tools/fr029_checkaudit.py:144). HTTP claim: vẫn nhận config key nằm trong header, nhầm thư viện của client có annotation và nhận dict.get qua client_at khác scope nên mức thấp (slice/l3slice/docfacts.py:802; slice/l3slice/astscan.py:276; slice/l3slice/docfacts.py:839). HTTP suspects: bound method/getattr đã cải thiện nhưng client truyền qua app.state và tham số không annotation vẫn lọt; audit recall theo dòng che sai loại và thiếu call nên mức thấp (slice/l3slice/astscan.py:153; slice/l3slice/astscan.py:333; slice/l3slice/docfacts.py:1019; slice/tools/fr029_checkaudit.py:423). Dependency params: callable instance, Literal/Enum và alias marker import đổi tên đều bỏ sót; phép đo chỉ bao phủ 10/33 case nên mức thấp (slice/l3slice/docfacts.py:386; slice/l3slice/docfacts.py:1099; slice/l3slice/astscan.py:445; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:14). R16 chỉ có 27 HTTP gold, 12 literal và còn hai gold_vs_rule; số 0 không đủ chứng minh tổng quát hóa (ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:29; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:31; ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:33). Bản chốt trong RAM: docfacts=0fea548db8e9d688, astscan=a785cb2bba1fb395, audit=70add74780ced806, tests=83e04c8cff9d7330; khác phiên bản checker ghi trong r16 (ket-qua-chay/fr029-checkaudit-20261008-r16-real/summary.json:3). tan_suat_uoc là đánh giá định tính về dạng code, không phải tỷ lệ đã đo trên một mẫu repo."
}
```

46 test của bản chốt đều qua; cả 8 phản ví dụ mới vẫn tái hiện được (`slice/tests/test_checker_counterexamples.py:308`, `:389`, `:397`).
Bảy phản ví dụ mới của vòng 3 đã được sửa đúng cho ca cụ thể.
Đã chạy Python với `-B`, dùng snapshot trong RAM và MockTransport; không sửa file repo, không gọi HTTP ra ngoài.
Không đọc `docs/`, `HANDOFF` hoặc `.aide/evidence/reviews/`.
Mã thay đổi trong lúc kiểm toán; lượt xác nhận cuối dùng cùng một bản chốt trong RAM, không đổi đến hết lượt chạy.