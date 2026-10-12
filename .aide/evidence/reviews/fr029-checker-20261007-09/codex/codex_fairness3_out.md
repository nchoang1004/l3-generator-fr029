```json
{
  "vong2": [
    {
      "muc": "PVD01_nhan_nham_route_path",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca /real với name='/fake' đã bị từ chối; test tương ứng chạy qua. Checker đọc đối số path của decorator thay vì chỉ tìm literal. slice/l3slice/docfacts.py:295; slice/l3slice/docfacts.py:467; slice/tests/test_checker_counterexamples.py:229."
    },
    {
      "muc": "PVD02_dependency_trong_literal",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Checker loại chuỗi literal trước khi tìm tên dependency; test real/other chạy qua. Việc này sửa đúng phản ví dụ cũ, chưa chứng minh tên được tìm thấy thực sự là đối số Depends. slice/l3slice/docfacts.py:359; slice/tests/test_checker_counterexamples.py:236."
    },
    {
      "muc": "PVD03_dependency_trung_ten_module",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Đã dùng context và import để chọn định nghĩa khi có nhiều def dep; test nhắc x-a và không nhắc x-b chạy qua. slice/l3slice/docfacts.py:1047; slice/tests/test_checker_counterexamples.py:243."
    },
    {
      "muc": "PVD04_header_convert_underscores_false",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Test giữ x_custom chạy qua. Checker đọc convert_underscores=False; audit không còn đồng nhất dấu '_' và '-'. Tôi ép checker trả x-custom: audit nay báo cả reminders_wrong và missed x_custom. slice/l3slice/docfacts.py:1096; slice/tools/fr029_checkaudit.py:232; slice/tests/test_checker_counterexamples.py:251."
    },
    {
      "muc": "PVD05_query_khong_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Nhánh ann is None đã được thêm; test dep(q='abc') nhắc query q chạy qua. slice/l3slice/docfacts.py:1083; slice/tests/test_checker_counterexamples.py:258."
    },
    {
      "muc": "PVD06_http_trung_bien_khac_scope",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca c là client trong remote nhưng là dict trong e đã được xử lý: claim dict bị từ chối và không sinh HTTP suspect; test chạy qua. Cách sửa xét binding trong hàm bao quanh. slice/l3slice/astscan.py:247; slice/l3slice/astscan.py:279; slice/tests/test_checker_counterexamples.py:267."
    },
    {
      "muc": "PVD07_client_at_khong_ton_tai",
      "trang_thai": "mot_phan",
      "bang_chung": "client_at='nope.py:999' nay bị loc từ chối, test chạy qua. Tuy nhiên tôi tái hiện client_at trỏ tới một httpx.Client có thật nhưng không liên quan vẫn làm cache.get được nhận như HTTP: add_http trả []. Chưa kiểm quan hệ giữa client_at và receiver. slice/tests/test_checker_counterexamples.py:280; slice/l3slice/docfacts.py:706; slice/l3slice/docfacts.py:787."
    },
    {
      "muc": "PVD08_http_client_qua_depends",
      "trang_thai": "mot_phan",
      "bang_chung": "Provider và handler cùng file như phản ví dụ cũ đã được xử lý; test chạy qua. Provider import từ clients.py vẫn không được truyền loại sang tham số Depends, tái hiện trong phản ví dụ mới bên dưới. slice/tests/test_checker_counterexamples.py:286; slice/l3slice/astscan.py:238; slice/l3slice/docfacts.py:834."
    },
    {
      "muc": "PVD09_import_client_co_annotation",
      "trang_thai": "da_xu_ly",
      "bang_chung": "module_clients đã xuất cả AnnAssign; test wire: httpx.Client import sang file khác nay tìm thấy HTTP suspect và chạy qua. Kết luận này áp dụng cho quét suspects của phản ví dụ cũ. slice/l3slice/astscan.py:338; slice/tests/test_checker_counterexamples.py:293."
    },
    {
      "muc": "PVD10_hai_http_call_cung_dong",
      "trang_thai": "mot_phan",
      "bang_chung": "GET+POST cùng dòng đã chạy qua: chọn call theo method, lưu theo cột và đếm số claim. Nhưng tôi chạy GET(a); GET(b): claim a được nhận, claim b bị so với a rồi từ chối; còn một suspect không thể giải quyết bằng claim b đúng. slice/tests/test_checker_counterexamples.py:298; slice/l3slice/astscan.py:344; slice/l3slice/docfacts.py:767; slice/l3slice/docfacts.py:974."
    },
    {
      "muc": "con_lai_01_sanity_co_phan_biet",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Xác nhận mức phân biệt tối thiểu: r12-accept có 1045/291/110 false acceptance route/dependency/HTTP; r12-reject có 358/148/27 false rejection và 387 gold item không được flag. Đây chưa phải bằng chứng oracle đúng hoặc tổng quát hóa tốt. ket-qua-chay/fr029-checkaudit-20261008-r12-accept/summary.json:20; ket-qua-chay/fr029-checkaudit-20261008-r12-accept/summary.json:24; ket-qua-chay/fr029-checkaudit-20261008-r12-accept/summary.json:32; ket-qua-chay/fr029-checkaudit-20261008-r12-reject/summary.json:19; ket-qua-chay/fr029-checkaudit-20261008-r12-reject/summary.json:23; ket-qua-chay/fr029-checkaudit-20261008-r12-reject/summary.json:30; ket-qua-chay/fr029-checkaudit-20261008-r12-reject/summary.json:37."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã lưu hash ba file code; tôi tính lại và khớp r13. Tuy nhiên hash docfacts/astscan của r12-accept và r12-reject khác r13; chưa có hash gold/source. Sanity vẫn monkeypatch các hàm con, không kiểm toàn bộ add_route/submit/open_problems; exit code chỉ dựa trên exception. slice/tools/fr029_checkaudit.py:482; slice/tools/fr029_checkaudit.py:519; slice/tools/fr029_checkaudit.py:544; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r12-accept/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r12-reject/summary.json:3."
    },
    {
      "muc": "con_lai_03_oracle_xoa_khac_biet_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Tái thử với gold x_custom và reminder giả x-custom: audit báo reminders_wrong=['header x-custom'] và missed=['header x_custom']. _key chỉ lowercase header. slice/tools/fr029_checkaudit.py:232; slice/tools/fr029_checkaudit.py:279."
    },
    {
      "muc": "con_lai_04_mau_so_mat_dependency_param",
      "trang_thai": "mot_phan",
      "bang_chung": "Ca e(q=Depends(dep)) đã sửa: khi ép dependency_params=[], audit đếm gold_dep_params=1 và báo thiếu q. Nhưng với e(v=Depends(dep), note: str='q'), cùng gold query q và cùng checker rỗng, audit vẫn trả gold_dep_params=0, missed=[] vì literal trong signature. slice/tools/fr029_checkaudit.py:287; slice/tools/fr029_checkaudit.py:293."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã truyền context và đổi query thành path theo gold path; ca /items/{item_id} nay không báo sai/thiếu. Nhưng audit vẫn gọi dependency_params trực tiếp. Tôi thay open_problems bằng hàm trả []: audit vẫn báo một reminder đúng, không thiếu gì. Chưa kiểm đường nhắc thực tế và nguồn dependency của từng tham số. slice/tools/fr029_checkaudit.py:275; slice/tools/fr029_checkaudit.py:278; slice/l3slice/docfacts.py:1011."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã bỏ trường router_level_routes=0 gây hiểu nhầm. Tuy nhiên vẫn không theo dependency ở app/router; dependency chỉ đo 10/33 case; http_items không có nhánh dev; calls vẫn tăng trước các nhánh continue. slice/tools/fr029_checkaudit.py:194; slice/tools/fr029_checkaudit.py:238; slice/tools/fr029_checkaudit.py:301; slice/tools/fr029_checkaudit.py:323; slice/tools/fr029_checkaudit.py:336; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:8; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:14."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "chua",
      "bang_chung": "Audit route vẫn chỉ kiểm method/handler qua _decorator_problems; không mutation path/application. Pool dependency vẫn loại tên cùng phần cuối và tên xuất hiện trên dòng. HTTP chưa mutation config key/client_at; method request/stream cũng không nằm trong nhánh mutation method. slice/tools/fr029_checkaudit.py:134; slice/tools/fr029_checkaudit.py:140; slice/tools/fr029_checkaudit.py:263; slice/tools/fr029_checkaudit.py:349; slice/tools/fr029_checkaudit.py:357."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Checker đã đếm nhiều call trên một dòng. Audit vẫn dùng tập tọa độ dòng, bỏ looks_like và không đếm từng call. Tôi cấp một suspect looks_like='route' tại dòng chứa hai HTTP gold call: audit báo gold_items=2, gold_not_flagged=[]. Vùng miễn noise vẫn kéo dài thêm ba dòng. slice/l3slice/docfacts.py:953; slice/tools/fr029_checkaudit.py:382; slice/tools/fr029_checkaudit.py:397; slice/tools/fr029_checkaudit.py:420."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Expected dependency dùng thuật toán riêng nhưng vẫn suy từ source; checker vẫn chọn decorator để đem mutation. HTTP config bị hạ thành unknown, method vẫn bị hạ theo regex và không đọc alt_methods. R13 còn hai gold_vs_rule. slice/tools/fr029_checkaudit.py:124; slice/tools/fr029_checkaudit.py:156; slice/tools/fr029_checkaudit.py:307; slice/tools/fr029_checkaudit.py:339; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:33."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Có mutation tên thật, URL mồi và claim âm; r13 ghi 1045/291/110 mutation và 1/13 negative route/HTTP. Các quan hệ khó vẫn chưa đo như con_lai_07; heldout chỉ xuất packet, chưa chấm độc lập. slice/tools/fr029_checkaudit.py:429; slice/tools/fr029_checkaudit.py:490; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:10."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "34 test chạy qua, gồm các sửa đổi RoundTwo; đây là cải thiện thực chất. Tuy nhiên suy loại HTTP vẫn nhận Client/Session bằng regex annotation, constructor app vẫn nhận theo tên FastAPI/APIRouter, và dependency vẫn dựa vào bảng FunctionDef theo tên. Các dạng mới bên dưới tiếp tục sai. slice/tests/test_checker_counterexamples.py:226; slice/l3slice/astscan.py:228; slice/l3slice/docfacts.py:521; slice/l3slice/docfacts.py:1125."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã mở rộng nhiều dạng client và sửa hai ca RoundTwo. Tôi chạy lại bound method, getattr và tham số wire không annotation: cả ba vẫn suspects=[]. from httpx import get as fetch được scanner flag nhưng add_http vẫn từ chối fetch(...). slice/l3slice/astscan.py:298; slice/l3slice/astscan.py:307; slice/l3slice/astscan.py:347; slice/l3slice/docfacts.py:725."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "ghep_method_va_path_tu_hai_decorator",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI\napp = FastAPI()\n@app.get('/read')\n@app.post('/write')\ndef e(): return {}\n# Claim: GET /write, handler main.py::e,\n# decorator main.py:3-5, application main.py:2,\n# path_parts=[{'kind':'decorator','value':'/write','at':'main.py:4'}].",
      "hau_qua": "add_route trả [] dù OpenAPI chỉ có GET /read và POST /write. Kiểm method và kiểm path độc lập, không buộc cùng decorator. slice/l3slice/docfacts.py:255; slice/l3slice/docfacts.py:295; slice/l3slice/docfacts.py:447; slice/l3slice/docfacts.py:477.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Chạy add_route với claim trên và dựng OpenAPI bằng FastAPI 0.115.6; xác nhận GET /write không tồn tại."
    },
    {
      "loai": "sqlalchemy_session_annotation_bi_coi_la_http",
      "vi_du_code": "# h.py\nimport httpx\nfrom sqlalchemy.orm import Session\ndef load(db: Session, model, pk):\n    return db.get(model, pk)\n# Claim tại h.py:4: library=httpx, method=GET,\n# target={'kind':'unknown','reason':'?'}",
      "hau_qua": "Scanner flag h.py:4 là HTTP và add_http trả [] cho thao tác database. Regex Client|Session không xác minh annotation đến từ thư viện nào. slice/l3slice/astscan.py:228; slice/l3slice/astscan.py:267; slice/l3slice/astscan.py:280; slice/l3slice/docfacts.py:787.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. Chạy scanner và claim như trên. Kiểm chứng Session.get bằng SQLAlchemy 2.0.52 với SQLite trong RAM: trả bản ghi User, không phải HTTP. Nguồn API: C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/sqlalchemy/orm/session.py:3591."
    },
    {
      "loai": "bo_sot_http_provider_import_tu_module_khac",
      "vi_du_code": "# clients.py\nimport httpx\ndef get_wire():\n    with httpx.Client() as c:\n        yield c\n# main.py\nfrom fastapi import FastAPI, Depends\nfrom clients import get_wire\napp = FastAPI()\n@app.get('/e')\ndef e(wire=Depends(get_wire)):\n    return wire.get('https://real.example')",
      "hau_qua": "suspects chỉ có route main.py:4, thiếu HTTP main.py:6. Claim HTTP đúng cũng bị từ chối nếu không thêm client_at. Liên module chỉ nhập client đã gán và subclass, chưa nhập provider trả/yield client. slice/l3slice/docfacts.py:834; slice/l3slice/astscan.py:138; slice/l3slice/astscan.py:238.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. Chạy snapshot hai file; HTTP suspect không xuất hiện. Chạy provider và handler với httpx.MockTransport nhận response 200 tại https://real.example, không gọi mạng."
    },
    {
      "loai": "dependency_dang_class_mat_query",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI, Depends\nclass Filters:\n    def __init__(self, q: str = ''):\n        self.q = q\napp = FastAPI()\n@app.get('/e')\ndef e(filters=Depends(Filters)): return {}",
      "hau_qua": "Nộp route cùng dependency Filters được nhận nhưng open_problems không nhắc query q. Bộ tra chỉ tìm FunctionDef tên Filters, không chuyển class sang __init__. slice/l3slice/docfacts.py:1042; slice/l3slice/docfacts.py:1054; slice/l3slice/docfacts.py:1125.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_route=[], reminder dependency=[]; OpenAPI FastAPI 0.115.6 có query q."
    },
    {
      "loai": "dependency_import_doi_ten_mat_header",
      "vi_du_code": "# deps.py\nfrom fastapi import Header\ndef dep(x_tenant: str = Header()): return x_tenant\n# main.py\nfrom fastapi import FastAPI, Depends\nfrom deps import dep as tenant\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(tenant)): return {}",
      "hau_qua": "Claim dependency tenant được nhận nhưng không nhắc x-tenant. Tra định nghĩa theo tenant trả rỗng; bước xử lý import chỉ chạy khi đã có nhiều định nghĩa cùng tên, nên không giải alias này. slice/l3slice/docfacts.py:363; slice/l3slice/docfacts.py:1043; slice/l3slice/docfacts.py:1047; slice/l3slice/docfacts.py:1054.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Snapshot hai file trả add_route=[], reminder=[]; nạp module trong RAM rồi dựng OpenAPI xác nhận header x-tenant bắt buộc."
    },
    {
      "loai": "alias_annotated_header_mat_reminder",
      "vi_du_code": "# main.py\nfrom fastapi import FastAPI, Depends, Header\nfrom typing import Annotated\nTenant = Annotated[str, Header(alias='X-Tenant')]\ndef dep(tenant: Tenant): return tenant\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(dep)): return {}",
      "hau_qua": "Route và dependency được nhận nhưng thiếu reminder X-Tenant. Alias resolver chỉ lấy Depends/Security, không mở rộng alias Annotated chứa Header/Query/Cookie. slice/l3slice/docfacts.py:397; slice/l3slice/docfacts.py:1085; slice/l3slice/astscan.py:384.",
      "tan_suat_uoc": "cao",
      "da_tai_hien": "Có. add_route=[], reminder=[]; OpenAPI FastAPI 0.115.6 có header X-Tenant bắt buộc."
    },
    {
      "loai": "dict_get_sau_response_json_bi_coi_la_http",
      "vi_du_code": "# h.py\nimport httpx\ndef fetch_id():\n    return httpx.get('https://api.example/item').json().get('id')",
      "hau_qua": "Scanner đếm hai HTTP call dù chỉ có một. Claim GET với URL thật bị từ chối; claim GET target literal 'id' lại được nhận vì chọn get ngoài cùng và suy receiver từ root httpx. slice/l3slice/astscan.py:45; slice/l3slice/astscan.py:283; slice/l3slice/astscan.py:304; slice/l3slice/astscan.py:350; slice/l3slice/docfacts.py:813.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. http_lines={3:2}; URL thật bị báo sai target; target='id' được nhận. Chạy biểu thức với MockTransport trả JSON {'id':7} cho kết quả 7, không gọi mạng."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "thap"
  },
  "ly_do": "Route: có bằng chứng tốt cho decorator/method/handler cơ bản và 358 claim trong tập đo, nhưng chưa kiểm đủ quan hệ method-path-application; phản ví dụ stacked decorator vẫn được nhận sai (slice/tools/fr029_checkaudit.py:140; slice/l3slice/docfacts.py:295; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:18). HTTP claim: còn nhận thao tác database, nhận dict.get sau JSON, và cho client_at không liên quan vượt kiểm receiver (slice/l3slice/astscan.py:267; slice/l3slice/docfacts.py:787). HTTP suspects: provider liên module và ba dạng đã nêu vòng 2 vẫn lọt; audit recall theo dòng có thể báo đủ dù sai loại hoặc thiếu call (slice/l3slice/docfacts.py:834; slice/l3slice/astscan.py:298; slice/tools/fr029_checkaudit.py:420). Dependency params: class, import đổi tên và alias Header đều là dạng thực dụng nhưng bị bỏ sót; phép đo vẫn có lỗi mẫu số và không chạy open_problems (slice/l3slice/docfacts.py:1043; slice/l3slice/docfacts.py:1085; slice/tools/fr029_checkaudit.py:275; slice/tools/fr029_checkaudit.py:293). R13 chỉ có 27 HTTP gold, 12 literal và dependency được đo trên 10/33 case; các số 0 không đủ suy ra độ tin cậy cao trên repo mới (ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:29; ket-qua-chay/fr029-checkaudit-20261008-r13/summary.json:31). tan_suat_uoc là đánh giá định tính về dạng code, không phải tần suất đã đo trên mẫu repo."
}
```

Đã chạy 34 test hiện có bằng snapshot trong RAM: tất cả qua, gồm lớp `RoundTwo` (`slice/tests/test_checker_counterexamples.py:226`).
Bảy phản ví dụ mới đều được tự chạy tái hiện; không sửa file repo và không gọi HTTP ra ngoài.
Không đọc `docs/`, `HANDOFF` hoặc `.aide/evidence/reviews/`.