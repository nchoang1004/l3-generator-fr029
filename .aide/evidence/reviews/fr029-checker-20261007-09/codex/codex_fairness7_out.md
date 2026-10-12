```json
{
  "vong6": [
    {
      "muc": "route_nhan_thu_tu_prefix_sai",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Chạy lại trên bản khớp hash R30: thứ tự /v1/api/x bị từ chối, /api/v1/x được nhận. slice/tests/test_checker_counterexamples.py:655."
    },
    {
      "muc": "helper_dang_ky_khong_lien_quan_vo_hieu_kiem_prefix",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca helper attach chưa được gọi không còn làm claim thiếu /api được nhận; test qua trên R30. Chỉ xác nhận ca cụ thể vòng 6. slice/tests/test_checker_counterexamples.py:665."
    },
    {
      "muc": "config_base_url_duoc_nhan_du_url_tuyet_doi_ghi_de",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Claim settings.URL bị chặn; claim URL tuyệt đối thực tế được nhận; test qua trên R30. slice/tests/test_checker_counterexamples.py:679."
    },
    {
      "muc": "thuoc_tinh_client_trung_ten_giua_hai_class",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca self.client là dict trong Cache không còn bị flag hoặc nhận claim HTTP; test qua trên R30. slice/tests/test_checker_counterexamples.py:688."
    },
    {
      "muc": "client_xuat_lai_qua_package_init_bi_bo_sot",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Ca from infra import wire qua __init__.py đã có suspect và nhận claim đúng; test qua trên R30. slice/tests/test_checker_counterexamples.py:701."
    },
    {
      "muc": "dependency_class_ke_thua_init_mat_header",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Đã nhắc header x-tenant từ constructor lớp cha; test qua trên R30. slice/tests/test_checker_counterexamples.py:708."
    },
    {
      "muc": "dependency_pydantic_field_alias_nhac_sai_query",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Nhắc sortBy và không nhắc sort_by; test qua trên R30. slice/tests/test_checker_counterexamples.py:717."
    },
    {
      "muc": "partial_keyword_bi_coi_la_tham_so_khong_the_ghi_de",
      "trang_thai": "da_xu_ly",
      "bang_chung": "Keyword limit của partial được giữ trong reminder; test qua trên R30. slice/tests/test_checker_counterexamples.py:726."
    },
    {
      "muc": "con_lai_02_sanity_duong_chay_va_phien_ban",
      "trang_thai": "mot_phan",
      "bang_chung": "Giới hạn phương pháp không đổi. Hash đầu phiên khớp R30; sanity accept nhận 131 mutation thiếu prefix, sanity reject từ chối 17 ca không cần prefix. Repo sau đó bị sửa đồng thời, nên R30 không đại diện bản cuối phiên. slice/tools/fr029_checkaudit.py:609; slice/tools/fr029_checkaudit.py:652; slice/tools/fr029_checkaudit.py:685; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:3; ket-qua-chay/fr029-checkaudit-20261008-r30-sanity-accept/summary.json:25; ket-qua-chay/fr029-checkaudit-20261008-r30-sanity-reject/summary.json:27."
    },
    {
      "muc": "con_lai_05_audit_khac_reminder_nguoi_dung",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: vẫn gán probe.routes trực tiếp và không chấm đúng dependency/vị trí bằng chứng của reminder. slice/tools/fr029_checkaudit.py:375; slice/tools/fr029_checkaudit.py:382; slice/tools/fr029_checkaudit.py:390."
    },
    {
      "muc": "con_lai_06_so_0_khong_co_phep_do",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: dependency đo 14/37 bộ; HTTP literal chỉ 12; bốn repo mới vẫn không có gold dependency params và phép kiểm HTTP literal. slice/tools/fr029_checkaudit.py:268; slice/tools/fr029_checkaudit.py:401; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:14; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:37; ket-qua-chay/fr029-checkaudit-20261008-r30/audit.json:210; ket-qua-chay/fr029-checkaudit-20261008-r30/audit.json:262; ket-qua-chay/fr029-checkaudit-20261008-r30/audit.json:314; ket-qua-chay/fr029-checkaudit-20261008-r30/audit.json:366."
    },
    {
      "muc": "con_lai_07_mutation_tranh_quan_he_de_sai",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về công cụ đo: mutation đăng ký vẫn qua hàm con, chưa kiểm đầy đủ claim application/prefix và quan hệ config_at/client_at; vẫn tránh dependency trùng tên cuối. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:367; slice/tools/fr029_checkaudit.py:449."
    },
    {
      "muc": "con_lai_08_recall_theo_dong_che_mat_call",
      "trang_thai": "mot_phan",
      "bang_chung": "Đã sửa kiểm loại cho HTTP recall: tái hiện suspect route trên dòng hai HTTP gold call nay báo thiếu cả hai. Đã thêm kiểm k-1 claim. Tuy nhiên, giả lập suspects() trả http lúc đầu rồi chỉ trả route sau k-1 claim vẫn cho gold_not_flagged=[] và multi_call_unflagged=[]: nhánh nhiều call chỉ kiểm at, không kiểm loại. Route recall và miễn noise vẫn bỏ loại; vùng miễn noise vẫn cộng ba dòng. R30 có multi_call_lines=0. slice/tools/fr029_checkaudit.py:497; slice/tools/fr029_checkaudit.py:503; slice/tools/fr029_checkaudit.py:514; slice/tools/fr029_checkaudit.py:516; slice/tools/fr029_checkaudit.py:535; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:44."
    },
    {
      "muc": "gop_y_cu_vong_tron",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi: checker tham gia chọn decorator, expected literal lấy từ source; config bị chuyển thành unknown và method có thể bị hạ thành unknown. R30 còn hai gold_vs_rule. slice/tools/fr029_checkaudit.py:133; slice/tools/fr029_checkaudit.py:146; slice/tools/fr029_checkaudit.py:408; slice/tools/fr029_checkaudit.py:439; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:39."
    },
    {
      "muc": "gop_y_cu_mutation_yeu",
      "trang_thai": "mot_phan",
      "bang_chung": "Không đổi về công cụ đo và nguồn gold; metadata vẫn ghi Claude Opus/Sonnet, reviewed_by_human=false. slice/tools/fr029_checkaudit.py:207; slice/tools/fr029_checkaudit.py:449; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:984; D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json:995."
    },
    {
      "muc": "gop_y_cu_overfit",
      "trang_thai": "mot_phan",
      "bang_chung": "Có tiến bộ thực chất: 83/83 test qua trên bản khớp R30, gồm RoundSix và HeldOutFindings mới. Nhưng tám ca mới dưới đây vẫn tái hiện trên bản bổ sung trong phiên; chưa đủ bằng chứng khái quát hóa cao. Không suy luận tác giả cố ý overfit. slice/tests/test_checker_counterexamples.py:463; slice/tests/test_checker_counterexamples.py:472; slice/tests/test_checker_counterexamples.py:481; slice/tests/test_checker_counterexamples.py:506; slice/tests/test_checker_counterexamples.py:652."
    },
    {
      "muc": "gop_y_cu_http_bo_sot",
      "trang_thai": "mot_phan",
      "bang_chung": "Getattr động đã được kiểm suspect, nhưng test mới không kiểm nhận claim. Tái hiện getattr(wire,'get')(url): claim GET đúng vẫn bị từ chối; e(wire) không annotation vẫn suspects=[]. slice/tests/test_checker_counterexamples.py:472; slice/l3slice/astscan.py:489; slice/l3slice/astscan.py:536; slice/l3slice/astscan.py:458."
    }
  ],
  "phan_vi_du_moi": [
    {
      "loai": "route_bo_qua_thu_tu_include_router",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nouter=APIRouter()\ninner=APIRouter()\n@inner.get('/x')\ndef e(): return {}\napp.include_router(outer)\nouter.include_router(inner)\n",
      "hau_qua": "Nhận route /x trên app dù app chưa có route đó: include_router sao chép các route đang tồn tại, nhưng checker chỉ dựng đồ thị cạnh, không xét thời điểm đăng ký. slice/l3slice/docfacts.py:600; slice/l3slice/docfacts.py:622; slice/l3slice/docfacts.py:706.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. main.py; add_route(route('main.py::e','main.py:5-6','/x',application='main.py:2'))=[]; thực thi FastAPI cho app.openapi()['paths']={}. Helper claim: slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "route_nhieu_decorator_chon_nham_router",
      "vi_du_code": "from fastapi import FastAPI, APIRouter\napp=FastAPI()\nother=FastAPI()\na=APIRouter()\nb=APIRouter()\n@a.get('/x')\n@b.get('/x')\ndef e(): return {}\napp.include_router(a)\nother.include_router(b)\n",
      "hau_qua": "Từ chối route có thật trên other vì kiểm đăng ký luôn lấy decorator thuộc a đầu tiên. slice/l3slice/docfacts.py:687; slice/l3slice/docfacts.py:692.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. Claim main.py::e, decorator main.py:6-8, application main.py:3 bị lỗi 'a ... không được include_router/mount vào other'; OpenAPI của other có GET /x. Helper claim: slice/tests/test_checker_counterexamples.py:25."
    },
    {
      "loai": "ket_qua_json_bi_nhan_la_client_do_constructor_long",
      "vi_du_code": "import httpx\ndef e():\n    data=httpx.Client().get('https://real.example').json()\n    return data.get('id')\n",
      "hau_qua": "Flag data.get và nhận claim HTTP sai tại dòng 4. makes() thấy constructor ở bất cứ đâu trong biểu thức rồi coi toàn bộ kết quả là client, kể cả sau json(). slice/l3slice/astscan.py:239; slice/l3slice/astscan.py:244; slice/l3slice/astscan.py:448.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects gồm h.py:3 và h.py:4; http(c,'h.py:4','httpx','GET','id')=[]. MockTransport ghi đúng một request https://real.example; e() trả 1 từ dict {'id':1}. Helper claim: slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "http_qua_asyncio_to_thread_bi_bo_sot",
      "vi_du_code": "import asyncio, httpx\nc=httpx.Client()\nasync def e(): return await asyncio.to_thread(c.get, 'https://real.example')\n",
      "hau_qua": "Không có suspect; claim HTTP đúng cũng bị từ chối vì lời gọi trực tiếp là to_thread, còn c.get được truyền như callable. Đây là dạng chuyển HTTP đồng bộ ra khỏi event loop. slice/l3slice/astscan.py:467; slice/l3slice/astscan.py:471; slice/l3slice/astscan.py:536.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects=[]; claim h.py:3 bị lỗi không có lời gọi .get/.post/...; asyncio.run(e()) với MockTransport thực sự gửi GET https://real.example và nhận 200. Helper claim: slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "http_client_qua_property_bi_bo_sot",
      "vi_du_code": "import httpx\nclass API:\n    def __init__(self): self._wire=httpx.Client()\n    @property\n    def transport(self): return self._wire\n    def e(self): return self.transport.get('https://real.example')\n",
      "hau_qua": "Không theo property trả client: mất suspect và từ chối claim đúng nếu không bổ sung client_at. slice/l3slice/astscan.py:451; slice/l3slice/astscan.py:454; slice/l3slice/astscan.py:481.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. Suspects=[]; claim h.py:6 báo transport.get không gọi trên client HTTP thấy được. API().e() với MockTransport gửi GET https://real.example và nhận 200. Helper claim: slice/tests/test_checker_counterexamples.py:127."
    },
    {
      "loai": "dependency_query_model_nhac_ten_bien_thay_vi_truong",
      "vi_du_code": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Query\nfrom pydantic import BaseModel\nclass Filters(BaseModel):\n    q: str=''\ndef dep(f: Annotated[Filters, Query()]): return f\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query f không tồn tại và bỏ query q thực tế. Nhánh Query() xuất tên đối số, không mở rộng model. slice/l3slice/docfacts.py:1591; slice/l3slice/docfacts.py:1597.",
      "tan_suat_uoc": "vua",
      "da_tai_hien": "Có. add_route=[] với dependency dep tại main.py:9; reminder ghi query 'f' tại main.py:6. OpenAPI chỉ có query q. Helper route/reminder: slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_keyword_dependency_mat_tham_so_long",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header\ndef inner(x_tenant: str=Header()): return x_tenant\ndef dep(v=Depends(dependency=inner)): return v\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Bỏ header của dependency lồng khi callable được truyền bằng keyword dependency=. Resolver chỉ lấy e.args[0]; nhánh không có positional argument tìm annotation thay thế. slice/l3slice/docfacts.py:1599; slice/l3slice/docfacts.py:1604.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. add_route=[] với dependency dep tại main.py:6; reminders=''; OpenAPI có header x-tenant bắt buộc. Helper route/reminder: slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    },
    {
      "loai": "dependency_import_doi_ten_Header_nhac_sai_vi_tri",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header as H\ndef dep(x_tenant: str=H()): return x_tenant\napp=FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)): return {}\n",
      "hau_qua": "Nhắc query x_tenant thay vì header x-tenant. Khác ca alias Annotated đã sửa: đây là đổi tên trực tiếp marker Header; tên H không được chuẩn hóa trước khi phân loại. slice/l3slice/docfacts.py:1580; slice/l3slice/docfacts.py:1582; slice/l3slice/docfacts.py:1590.",
      "tan_suat_uoc": "thap",
      "da_tai_hien": "Có. add_route=[] với dependency dep tại main.py:5; reminder ghi query 'x_tenant'; OpenAPI chỉ có header x-tenant bắt buộc. Helper route/reminder: slice/tests/test_checker_counterexamples.py:25; slice/tests/test_checker_counterexamples.py:32."
    }
  ],
  "tin_cay": {
    "route": "vua",
    "http_claim": "thap",
    "http_suspects": "thap",
    "dependency_params": "vua"
  },
  "ly_do": "Route: các ca prefix vòng 6 đã sửa, nhưng vẫn nhận đăng ký chưa xảy ra và từ chối đăng ký đúng khi có nhiều decorator; chưa đủ tin cậy cao cho application/path hoàn chỉnh (slice/tests/test_checker_counterexamples.py:655; slice/l3slice/docfacts.py:600; slice/l3slice/docfacts.py:687). HTTP claim: vẫn nhận dict.get thành HTTP, đồng thời từ chối callable dispatch/property có thật (slice/l3slice/astscan.py:239; slice/l3slice/astscan.py:454; slice/l3slice/astscan.py:536). HTTP suspects: có cải thiện rõ nhưng còn bỏ HTTP qua thread/property; số gold_items_not_flagged=0 không chứng minh bao phủ repo mới, nhất là multi_call_lines=0 và nhánh kiểm nhiều call còn bỏ loại (slice/l3slice/astscan.py:471; slice/tools/fr029_checkaudit.py:535; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:43). Dependency params: các ca constructor kế thừa, Field alias và partial keyword đã sửa; còn nhầm query model, marker đổi tên và dependency keyword, trong khi phép đo chỉ bao phủ 14/37 bộ (slice/tests/test_checker_counterexamples.py:708; slice/tests/test_checker_counterexamples.py:717; slice/tests/test_checker_counterexamples.py:726; slice/l3slice/docfacts.py:1597; slice/l3slice/docfacts.py:1599; ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:14). Giới hạn phiên: đầu phiên chạy 83/83 test với ba hash đúng R30; không chạy lại toàn bộ 37 gold, chỉ đọc báo cáo và đối chiếu code (ket-qua-chay/fr029-checkaudit-20261008-r30/summary.json:3). Repo bị sửa đồng thời sau đó. Tám ca mới được chạy lại trong một lượt có hash trước/sau ổn định: docfacts=0e4f9e75f7aad330, astscan=33a850ebf536b3f2, audit=2c72037dd339f0c1. Số dòng docfacts/astscan của các ca mới chỉ bản này đã giữ trong RAM, không phải bản R30 hoặc mọi sửa đổi sau đó. Lượt bổ sung có 91/92 test qua; assertion tại slice/tests/test_checker_counterexamples.py:784 thất bại, với helper reminder lọc chuỗi tại slice/tests/test_checker_counterexamples.py:33; không gán thất bại này cho R30. Snapshot thử nghiệm được tạo bằng SourceTools trong RAM, giữ nguyên assertion của test (slice/l3slice/source_tools.py:100). Oracle runtime: FastAPI 0.115.6, Pydantic 2.13.4, httpx 0.28.1; HTTP dùng MockTransport. tan_suat_uoc và tin_cay là đánh giá định tính, không phải tần suất hoặc khoảng tin cậy thống kê."
}
```

Tám phản ví dụ cụ thể vòng 6 đã được xử lý; các giới hạn đo lường vẫn chỉ xử lý một phần.
Repo thay đổi đồng thời, nên cần dùng hash trong JSON để phân biệt các lượt kiểm.
Không sửa file repo, không gọi HTTP ra ngoài, không đọc các thư mục bị loại trừ.