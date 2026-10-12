```json
{
  "gop_y_cu": [
    {
      "gop_y": "vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": [
        "Đã bỏ việc lấy expected dependency trực tiếp từ bảng alias của checker: audit tự dựng alias_table và resolve_alias. Tuy nhiên, expected vẫn được suy từ source bằng một thuật toán khác, chưa phải gold độc lập cho từng dependency; hai phía vẫn có thể cùng bỏ sót một dạng cú pháp. slice/tools/fr029_checkaudit.py:156, slice/tools/fr029_checkaudit.py:178, slice/tools/fr029_checkaudit.py:253.",
        "Chưa sửa việc dùng chính checker để chọn vị trí decorator được chấp nhận, rồi mutation vị trí đó: hits được tính bằng _decorator_problems và dec=(hits or decs)[0]. slice/tools/fr029_checkaudit.py:124, slice/tools/fr029_checkaudit.py:128.",
        "Chưa sửa việc hạ thông tin HTTP: target không phải literal bị đổi thành unknown; method bị hạ theo regex của audit, không đọc alt_methods. R11 vẫn ghi hai gold_method GET bị hạ. slice/tools/fr029_checkaudit.py:296, slice/tools/fr029_checkaudit.py:328, slice/tools/fr029_checkaudit.py:331, ket-qua-chay/fr029-checkaudit-20261008-r11/audit.json:138.",
        "Phần đối chiếu method/handler và tập tham số route vẫn lấy từ gold; vì vậy không kết luận toàn bộ phép đo là vòng tròn. slice/tools/fr029_checkaudit.py:76, slice/tools/fr029_checkaudit.py:275."
      ]
    },
    {
      "gop_y": "mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": [
        "Đã thêm handler có thật khác, dependency có thật khác, URL cụt, URL mồi và library sai. Đã chạy mutation kể cả khi claim đúng bị từ chối và có bộ đếm mutations. slice/tools/fr029_checkaudit.py:132, slice/tools/fr029_checkaudit.py:258, slice/tools/fr029_checkaudit.py:265, slice/tools/fr029_checkaudit.py:338.",
        "Đã nộp excluded_routes/not_fastapi và non_http_calls như claim âm. R11 thực sự có 1 ca âm route và 13 ca âm HTTP. slice/tools/fr029_checkaudit.py:142, slice/tools/fr029_checkaudit.py:353, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:6, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:11.",
        "Mutation route vẫn tránh mọi method literal trong decorator và chỉ gọi _decorator_problems, không add_route; path/application sai chưa được đo. Mutation dependency cố ý tránh tên xuất hiện trên dòng và tránh dependency cùng tên cuối, nên không thử A.inject thay B.inject. slice/tools/fr029_checkaudit.py:130, slice/tools/fr029_checkaudit.py:140, slice/tools/fr029_checkaudit.py:262.",
        "Mutation HTTP vẫn không đổi method của request/stream, không thử config key hoặc client_at sai. slice/tools/fr029_checkaudit.py:331, slice/tools/fr029_checkaudit.py:345, slice/tools/fr029_checkaudit.py:346.",
        "Chưa sửa nguồn gốc reminder và mẫu số: reminder chỉ cần trùng một tham số bất kỳ của route; tên đối số hoặc literal trong signature vẫn đủ loại gold parameter khỏi mẫu số. slice/tools/fr029_checkaudit.py:275, slice/tools/fr029_checkaudit.py:279.",
        "Chưa sửa phép suspects theo dòng/không xét looks_like và vùng miễn nhiễu thêm ba dòng. slice/tools/fr029_checkaudit.py:371, slice/tools/fr029_checkaudit.py:386, slice/tools/fr029_checkaudit.py:409.",
        "Đã ghi measured=false cho dependency ngoài fr029, nhưng router_level_routes vẫn chỉ khởi tạo 0; HTTP vẫn không có nhánh dev. Exit code chỉ thất bại khi có exception, không khi checker sai. slice/tools/fr029_checkaudit.py:238, slice/tools/fr029_checkaudit.py:239, slice/tools/fr029_checkaudit.py:290, slice/tools/fr029_checkaudit.py:529.",
        "Chưa có chấm heldout độc lập trong công cụ; vẫn dùng các repo cố định và split development. slice/tools/fr029_checkaudit.py:46, slice/tools/fr029_checkaudit.py:69, slice/tools/fr029_checkaudit.py:418, slice/tools/fr029_checkaudit.py:479."
      ]
    },
    {
      "gop_y": "overfit",
      "trang_thai": "mot_phan",
      "bang_chung": [
        "Đã sửa thực chất alias khác module, Annotated nhiều dòng/Security, giữ Class.method và phân biệt Depends(factory) với Depends(factory(...)). slice/l3slice/docfacts.py:376, slice/l3slice/docfacts.py:405, slice/l3slice/docfacts.py:1061, slice/l3slice/docfacts.py:1023; test tại slice/tests/test_checker_counterexamples.py:44, slice/tests/test_checker_counterexamples.py:56, slice/tests/test_checker_counterexamples.py:68.",
        "Đã kiểm tra giá trị return của factory app, theo chuỗi factory ngắn, xác minh receiver import và đọc đúng methods của api_route. Tuy nhiên constructor FastAPI/APIRouter vẫn nhận bằng tên, chưa giải import alias. slice/l3slice/docfacts.py:447, slice/l3slice/docfacts.py:485, slice/l3slice/docfacts.py:499, slice/l3slice/docfacts.py:508; test tại slice/tests/test_checker_counterexamples.py:98, slice/tests/test_checker_counterexamples.py:104, slice/tests/test_checker_counterexamples.py:109, slice/tests/test_checker_counterexamples.py:120.",
        "Đã sửa scalar annotation chuỗi và đổi query thành path ở open_problems. Audit lại gọi dependency_params trực tiếp nên không đo đúng bước đổi này. slice/l3slice/astscan.py:295, slice/l3slice/docfacts.py:982, slice/tools/fr029_checkaudit.py:273; test tại slice/tests/test_checker_counterexamples.py:82, slice/tests/test_checker_counterexamples.py:90.",
        "Đã sửa các ca HTTP cũ về dict đơn giản, library sai, URL từ câu lệnh bên cạnh, literal prefix, comment chứa ngoặc, request nhiều dòng và method là biến bằng phân tích AST. slice/l3slice/docfacts.py:754, slice/l3slice/docfacts.py:764, slice/l3slice/docfacts.py:767, slice/l3slice/docfacts.py:789; test tại slice/tests/test_checker_counterexamples.py:133, slice/tests/test_checker_counterexamples.py:165, slice/tests/test_checker_counterexamples.py:170, slice/tests/test_checker_counterexamples.py:174, slice/tests/test_checker_counterexamples.py:180.",
        "Chưa giải quyết tổng quát scope/module: HTTP clients được gom theo tên trên toàn AST; dependency function vẫn tra bảng toàn snapshot theo tên ngắn, tham số context không được dùng để chọn định nghĩa. Đây là nguồn các phản ví dụ mới đã tái hiện. slice/l3slice/astscan.py:212, slice/l3slice/astscan.py:232, slice/l3slice/docfacts.py:1011, slice/l3slice/docfacts.py:1017, slice/l3slice/docfacts.py:1088."
      ]
    },
    {
      "gop_y": "http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": [
        "Đã xử lý scanner cho import nhiều module, import trực tiếp/đổi tên hàm, constructor alias, gán client qua biến, subclass và requests.session(). slice/l3slice/astscan.py:68, slice/l3slice/astscan.py:116, slice/l3slice/astscan.py:120, slice/l3slice/astscan.py:123, slice/l3slice/astscan.py:152, slice/l3slice/astscan.py:160; test tại slice/tests/test_checker_counterexamples.py:189.",
        "Đã xử lý scanner cho client import trực tiếp từ module khác, container đơn giản, context manager yield, receiver xuống dòng, send và code sau chuỗi nhiều dòng. slice/l3slice/docfacts.py:806, slice/l3slice/astscan.py:154, slice/l3slice/astscan.py:191, slice/l3slice/astscan.py:253, slice/l3slice/astscan.py:14, slice/l3slice/astscan.py:60; test tại slice/tests/test_checker_counterexamples.py:196, slice/tests/test_checker_counterexamples.py:198, slice/tests/test_checker_counterexamples.py:210.",
        "Chưa xử lý bound method lưu vào biến, getattr và client truyền qua đối số không annotation/tên wire. Tôi tái hiện cả ba đều không có HTTP suspect; _bind không truyền loại qua lời gọi và http_lines chỉ nhận Attribute hoặc hàm import trực tiếp. slice/l3slice/astscan.py:201, slice/l3slice/astscan.py:223, slice/l3slice/astscan.py:249, slice/l3slice/astscan.py:254.",
        "Scanner nhận from httpx import get as fetch, nhưng add_http vẫn từ chối fetch(...): call_at chỉ nhận tên nằm trong HTTP_VERBS và fallback cũng chỉ nhận các tên verb cố định. Tôi tái hiện được sự lệch giữa hai đường kiểm. slice/l3slice/astscan.py:116, slice/l3slice/astscan.py:268, slice/l3slice/docfacts.py:700.",
        "Các test HTTP bổ sung chủ yếu kiểm tra có dòng suspect, chưa chứng minh claim đúng cũng được add_http nhận ở từng dạng. slice/tests/test_checker_counterexamples.py:203, slice/tests/test_checker_counterexamples.py:210."
      ]
    }
  ],
  "con_lai": [
    {
      "van_de": "Bộ kiểm giả có chứng minh phân biệt được không?",
      "ket_luan": "Có, ở mức kiểm tra tối thiểu và xét cả vector chỉ số. Bản luôn nhận gây 1045/291/110 lỗi mutation route/dependency/HTTP; bản luôn từ chối gây 358/148/27 false rejection và bỏ 387 gold items. Không thể nói mọi chỉ số luôn đạt. Nhưng chúng không chứng minh oracle đúng, mutation đủ khó hoặc khả năng tổng quát hóa.",
      "bang_chung": "ket-qua-chay/fr029-checkaudit-20261008-r8-accept/summary.json:15, ket-qua-chay/fr029-checkaudit-20261008-r8-accept/summary.json:19, ket-qua-chay/fr029-checkaudit-20261008-r8-accept/summary.json:27; ket-qua-chay/fr029-checkaudit-20261008-r8-reject/summary.json:14, ket-qua-chay/fr029-checkaudit-20261008-r8-reject/summary.json:18, ket-qua-chay/fr029-checkaudit-20261008-r8-reject/summary.json:25, ket-qua-chay/fr029-checkaudit-20261008-r8-reject/summary.json:32."
    },
    {
      "van_de": "Sanity chưa kiểm tra đầy đủ đường chạy thật và chưa gắn phiên bản với r11",
      "ket_luan": "Sanity monkeypatch các hàm được audit gọi, không kiểm tra toàn bộ add_route/submit/open_problems. Báo cáo không lưu hash checker/audit/gold/source để xác nhận r8 và r11 dùng cùng phiên bản. Exit code của cả checker giả vẫn là 0 nếu không có exception.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:471, slice/tools/fr029_checkaudit.py:493, slice/tools/fr029_checkaudit.py:502, slice/tools/fr029_checkaudit.py:506, slice/tools/fr029_checkaudit.py:529."
    },
    {
      "van_de": "Oracle xóa khác biệt header có ý nghĩa",
      "ket_luan": "Audit chuẩn hóa x_custom thành x-custom vô điều kiện, giống checker. Với Header(convert_underscores=False), FastAPI OpenAPI trả x_custom, checker nhắc x-custom nhưng audit vẫn báo reminders_wrong=[] và missed=[]. Đây là lỗi đo đã tái hiện, không chỉ thiếu ca thử.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:232, slice/tools/fr029_checkaudit.py:274, slice/tools/fr029_checkaudit.py:275; slice/l3slice/docfacts.py:1059, slice/l3slice/docfacts.py:1103; C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:483."
    },
    {
      "van_de": "Mẫu số có thể tự mất tham số dependency",
      "ket_luan": "Với def dep(q: str) và def e(q=Depends(dep)), tôi thay riêng dependency_params bằng hàm trả []; audit vẫn báo gold_dep_params=0 và missed=[] dù gold có query q. Tên biến nhận kết quả dependency bị hiểu nhầm là tham số HTTP trực tiếp.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:279, slice/tools/fr029_checkaudit.py:282, slice/tools/fr029_checkaudit.py:284."
    },
    {
      "van_de": "Audit không đo cùng hành vi nhắc tham số mà người dùng nhận",
      "ket_luan": "Audit gọi dependency_params, bỏ qua open_problems và ngữ cảnh path. Với dependency item_id trên /items/{item_id}, checker đã nhắc path đúng nhưng audit lại báo query sai và thiếu path. Reminder cũng không được đối chiếu đúng dependency nguồn.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:273, slice/tools/fr029_checkaudit.py:275; slice/l3slice/docfacts.py:982, slice/l3slice/docfacts.py:983."
    },
    {
      "van_de": "Những số 0 không có phép đo tương ứng",
      "ket_luan": "router_level_routes luôn 0 do không có cập nhật. Dependency chỉ đo 10/33 case; HTTP dev không được thu thập. http.calls được tăng trước các nhánh continue, nên cũng chưa phải số claim chắc chắn đã gọi add_http.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:239, slice/tools/fr029_checkaudit.py:240, slice/tools/fr029_checkaudit.py:290, slice/tools/fr029_checkaudit.py:312, slice/tools/fr029_checkaudit.py:325; ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:3, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:9."
    },
    {
      "van_de": "Mutation vẫn tránh đúng các quan hệ dễ sai",
      "ket_luan": "Tên dependency có trên dòng bị loại khỏi pool âm dù có thể chỉ là literal; cùng tên method khác class cũng bị loại. Route path/application, config key HTTP và client_at không được mutation. Checker hiện tại thực sự nhận sai các dạng này.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:134, slice/tools/fr029_checkaudit.py:262, slice/tools/fr029_checkaudit.py:338; slice/l3slice/docfacts.py:292, slice/l3slice/docfacts.py:358, slice/l3slice/docfacts.py:730, slice/l3slice/docfacts.py:760."
    },
    {
      "van_de": "Recall theo dòng che mất lời gọi",
      "ket_luan": "Một suspect bất kỳ trên cùng dòng đủ đánh dấu gold item; không kiểm tra loại hoặc từng call. Checker cũng lưu coverage HTTP theo dòng bắt đầu. Nộp một trong hai HTTP call cùng dòng làm call còn lại biến mất khỏi suspects.",
      "bang_chung": "slice/tools/fr029_checkaudit.py:371, slice/tools/fr029_checkaudit.py:409; slice/l3slice/docfacts.py:923, slice/l3slice/docfacts.py:940; slice/l3slice/astscan.py:274."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "nhan_nham_route_path",
      "vi_du_code": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/real', name='/fake')\ndef e(): return {}\n# Claim: GET /fake, handler main.py::e,\n# decorator main.py:3-4, application main.py:2,\n# path_parts=[{'kind':'decorator','value':'/fake','at':'main.py:3'}].",
      "hau_qua": "Đã tái hiện add_route trả [] dù path thật là /real. Checker chỉ yêu cầu literal xuất hiện trong đoạn, không buộc nó là đối số path. slice/l3slice/docfacts.py:289, slice/l3slice/docfacts.py:292. Audit chỉ gọi _decorator_problems nên không bắt lỗi này: slice/tools/fr029_checkaudit.py:140.",
      "muc_do": "cao"
    },
    {
      "loai": "nhan_nham_dependency_va_nhac_thua",
      "vi_du_code": "from fastapi import FastAPI, Depends, Query\ndef real(): return 1\ndef other(x: str = Query()): return x\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(real), note: str='other'): return v\n# Claim dependency other tại main.py:6.",
      "hau_qua": "Đã tái hiện add_route nhận dependency other và open_problems nhắc query x, dù route chỉ gọi real. Regex chấp nhận chữ other trong literal. slice/l3slice/docfacts.py:318, slice/l3slice/docfacts.py:358, slice/l3slice/docfacts.py:982.",
      "muc_do": "cao"
    },
    {
      "loai": "thieu_tham_so_do_dependency_trung_ten_module",
      "vi_du_code": "# a.py\nfrom fastapi import Header\ndef dep(x_a: str = Header()): return x_a\n# b.py\nfrom fastapi import Header\ndef dep(x_b: str = Header()): return x_b\n# main.py\nfrom fastapi import FastAPI, Depends\nfrom a import dep\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(dep)): return v",
      "hau_qua": "Đã tái hiện claim dependency được nhận nhưng không nhắc x-a; OpenAPI FastAPI xác nhận x-a là header của route. dependency_params thấy hai def dep toàn snapshot rồi trả [], kể cả khi truyền context='a.py'. slice/l3slice/docfacts.py:1011, slice/l3slice/docfacts.py:1017, slice/l3slice/docfacts.py:1088.",
      "muc_do": "cao"
    },
    {
      "loai": "nhac_sai_ten_header_va_audit_khong_phat_hien",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header\ndef dep(x_custom: str = Header(convert_underscores=False)): return x_custom\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(dep)): return v",
      "hau_qua": "Đã tái hiện checker nhắc x-custom thay vì x_custom; OpenAPI xác nhận tên đúng là x_custom. Audit lại coi hai tên bằng nhau nên báo không sai/không thiếu. slice/l3slice/docfacts.py:1057, slice/l3slice/docfacts.py:1059; slice/tools/fr029_checkaudit.py:232; C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:483.",
      "muc_do": "cao"
    },
    {
      "loai": "thieu_query_khong_annotation",
      "vi_du_code": "from fastapi import FastAPI, Depends\ndef dep(q='abc'): return q\napp = FastAPI()\n@app.get('/e')\ndef e(v=Depends(dep)): return v",
      "hau_qua": "Đã tái hiện không có reminder q dù OpenAPI có query q. Checker chỉ nhắc scalar khi annotation được scalar() nhận; annotation None bị bỏ qua. slice/l3slice/docfacts.py:1046, slice/l3slice/astscan.py:293, slice/l3slice/astscan.py:306.",
      "muc_do": "vua"
    },
    {
      "loai": "nhan_nham_http_do_trung_ten_bien_khac_scope",
      "vi_du_code": "from fastapi import FastAPI\nimport httpx\napp = FastAPI()\ndef remote():\n    c = httpx.Client()\n    return c.get('https://real.example')\n@app.get('/e')\ndef e():\n    c = {'https://fake.example': 1}\n    return c.get('https://fake.example')",
      "hau_qua": "Đã tái hiện dòng 10 vừa thành HTTP suspect vừa được add_http nhận với library=httpx, method=GET và target=https://fake.example. Tên c của remote được dùng để xác minh c trong e, dù đó là dict. slice/l3slice/astscan.py:144, slice/l3slice/astscan.py:212, slice/l3slice/astscan.py:232; slice/l3slice/docfacts.py:764.",
      "muc_do": "cao"
    },
    {
      "loai": "nhan_nham_http_qua_client_at_khong_ton_tai",
      "vi_du_code": "from fastapi import FastAPI\nimport httpx\napp = FastAPI()\n@app.get('/e')\ndef e():\n    cache = {'https://fake.example': 1}\n    return cache.get('https://fake.example')\n# Nộp HTTP tại main.py:7, library=httpx, method=GET,\n# target literal https://fake.example,\n# client_at='not_exist.py:999'.",
      "hau_qua": "Đã tái hiện add_http trả []. Khi file đã import httpx, client_at không được loc xác minh; chỉ cần giá trị truthy là bỏ kiểm receiver. slice/l3slice/docfacts.py:684, slice/l3slice/docfacts.py:686, slice/l3slice/docfacts.py:697, slice/l3slice/docfacts.py:760.",
      "muc_do": "cao"
    },
    {
      "loai": "bo_sot_http_client_truyen_qua_depends",
      "vi_du_code": "from fastapi import FastAPI, Depends\nimport httpx\napp = FastAPI()\ndef get_wire():\n    with httpx.Client() as c:\n        yield c\n@app.get('/e')\ndef e(wire=Depends(get_wire)):\n    return wire.get('https://real.example')",
      "hau_qua": "Đã tái hiện suspects chỉ có route, không có HTTP dòng 9; claim đúng cũng bị từ chối nếu không thêm client_at. Scanner biết factory get_wire nhưng không bind đối số wire từ Depends(get_wire). slice/l3slice/astscan.py:137, slice/l3slice/astscan.py:201, slice/l3slice/astscan.py:223, slice/l3slice/astscan.py:252; slice/l3slice/docfacts.py:764.",
      "muc_do": "cao"
    },
    {
      "loai": "bo_sot_http_client_import_co_annotation",
      "vi_du_code": "# clients.py\nimport httpx\nwire: httpx.Client = httpx.Client()\n# main.py\nfrom fastapi import FastAPI\nfrom clients import wire\napp = FastAPI()\n@app.get('/e')\ndef e(): return wire.get('https://real.example')",
      "hau_qua": "Đã tái hiện không có HTTP suspect trong main.py. module_clients chỉ xuất ast.Assign, bỏ ast.AnnAssign; file gọi không import trực tiếp thư viện nên scan.capable=False. Cùng lỗ hổng AST áp dụng với requests.Session và aiohttp.ClientSession khai báo theo dạng này. slice/l3slice/astscan.py:264, slice/l3slice/docfacts.py:809, slice/l3slice/astscan.py:122, slice/l3slice/docfacts.py:934.",
      "muc_do": "cao"
    },
    {
      "loai": "tu_choi_nham_va_bo_sot_http_thu_hai_cung_dong",
      "vi_du_code": "from fastapi import FastAPI\nimport httpx\napp = FastAPI()\n@app.get('/e')\ndef e():\n    httpx.get('https://a.example'); httpx.post('https://b.example')",
      "hau_qua": "Đã tái hiện claim POST tại main.py:6 bị so với GET đầu tiên nên bị từ chối method/URL. Sau khi nộp GET, POST cũng không còn được nhắc trong suspects. call_at luôn lấy call đầu; coverage HTTP chỉ lưu dòng. slice/l3slice/astscan.py:270, slice/l3slice/astscan.py:274, slice/l3slice/docfacts.py:693, slice/l3slice/docfacts.py:923, slice/l3slice/docfacts.py:940.",
      "muc_do": "cao"
    }
  ],
  "muc_tin_cay": "thap",
  "ly_do": "Thấp nếu dùng các số 0 để kết luận checker đáng tin trên repo mới. Có cải thiện thực chất và sanity phân biệt được hai cực, nhưng r11 chỉ có 27 HTTP gold, 12 literal, dependency đo 10/33 case; còn hai claim HTTP bị hạ thông tin và bốn suspect ngoài gold. Oracle reminder có lỗi chuẩn hóa và mẫu số đã tái hiện; các đường add_route/open_problems không được đo đầy đủ; nhiều phản ví dụ mới vẫn sai dù 23 test cũ qua. Các số 0 chỉ mô tả tập claim và mutation hẹp hiện tại. Bằng chứng: ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:9, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:24, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:26, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:28, ket-qua-chay/fr029-checkaudit-20261008-r11/summary.json:30; slice/tools/fr029_checkaudit.py:140, slice/tools/fr029_checkaudit.py:232, slice/tools/fr029_checkaudit.py:273, slice/tools/fr029_checkaudit.py:282."
}
```

Tôi chỉ đọc file; các phép thử chạy trong RAM bằng Python `-B`, không gọi HTTP ra ngoài.
23 test cũ đều qua khi thay riêng helper ghi file tạm bằng snapshot trong RAM (`slice/tests/test_checker_counterexamples.py:17`; helper gốc ghi file tại `slice/tests/test_docagent.py:106`).
Không đọc `docs/`, `HANDOFF` hay `.aide/evidence/reviews/`.