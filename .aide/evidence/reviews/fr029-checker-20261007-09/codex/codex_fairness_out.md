```json
{
  "vong_tron": [
    "Có vòng tròn ở dependency qua alias: route_dependencies() gọi claims._alias_wraps(), rồi lấy claims._aliases làm danh sách dependency đúng để kiểm tra dependency_at(). Nếu bảng alias nhận sai dependency, hai phía có thể cùng sai và vẫn khớp; nếu bảng bỏ sót alias, phép kiểm dependency_lines không tạo ca thử đó. Nguồn: slice/tools/fr029_checkaudit.py:143, slice/tools/fr029_checkaudit.py:159, slice/tools/fr029_checkaudit.py:193, slice/l3slice/docfacts.py:354.",
    "Không phải toàn bộ phép đo đều vòng tròn: route method/handler được đọc từ gold JSON; reminders được đối chiếu với params trong gold; vị trí HTTP cũng lấy từ gold. Tuy nhiên, danh sách dependency đúng được dựng từ AST và bảng alias của checker, không phải một danh sách dependency độc lập trong gold. Nguồn: slice/tools/fr029_checkaudit.py:45, slice/tools/fr029_checkaudit.py:72, slice/tools/fr029_checkaudit.py:192, slice/tools/fr029_checkaudit.py:203, slice/tools/fr029_checkaudit.py:218.",
    "Phép HTTP làm yếu claim trước khi kiểm: target không phải literal đều thành unknown; một số method trong gold cũng thành unknown theo hình dạng lời gọi. Vì thế http_false_rejection=0 không có nghĩa checker chấp nhận đầy đủ thông tin đúng trong gold. Hai ca Kibo ở r4 thuộc trường hợp này, nhưng chính gold cho phép alt_methods=['unknown']; không đủ căn cứ gọi hai ca đó là sửa đáp án trái gold. Vấn đề là audit không đọc alt_methods mà áp dụng phép hạ thông tin chung. Nguồn: slice/tools/fr029_checkaudit.py:224, slice/tools/fr029_checkaudit.py:253, slice/tools/fr029_checkaudit.py:259, ket-qua-chay/fr029-checkaudit-20261008-r4/audit.json:114, D:/VSF/l3-acceptance-gold/kibo/gold.r2.json:4544, D:/VSF/l3-acceptance-gold/kibo/gold.r2.json:4550, D:/VSF/l3-acceptance-gold/kibo/gold.r2.json:4564.",
    "Phép route để chính _decorator_problems chọn đoạn chứng cứ được chấp nhận trong các hàm trùng tên, rồi mutation đoạn đầu tiên được chọn. Đây là phụ thuộc checker khi chọn chứng cứ, chưa phải đáp án độc lập về đúng vị trí decorator. Tuy vậy, nó vẫn ghi false_rejection nếu mọi ứng viên bị từ chối, nên không phải phép luôn đạt. Nguồn: slice/tools/fr029_checkaudit.py:99, slice/tools/fr029_checkaudit.py:117, slice/tools/fr029_checkaudit.py:122, slice/tools/fr029_checkaudit.py:128."
  ],
  "mutation_yeu": [
    "Mutation route quá dễ: chọn method không xuất hiện trong toàn bộ đoạn decorator và dùng handler giả khong_co_ham_nay. Nó không thử method xuất hiện ở trường khác, handler có thật nhưng thuộc route khác, receiver giả, hoặc path/application sai. Audit chỉ gọi _decorator_problems, không kiểm cả add_route. Nguồn: slice/tools/fr029_checkaudit.py:119, slice/tools/fr029_checkaudit.py:129, slice/tools/fr029_checkaudit.py:134.",
    "Mutation dependency yếu hơn mô tả: MUTATIONS nói đổi sang dependency khác trong cùng file, nhưng thực tế luôn dùng khong_co_dependency_nay. Một bộ kiểm chỉ tìm từ có xuất hiện trên dòng cũng vượt qua dạng mutation này; không cần xác định quan hệ Depends hay đúng Class.method. Nguồn: slice/tools/fr029_checkaudit.py:36, slice/tools/fr029_checkaudit.py:197, slice/l3slice/docfacts.py:350.",
    "Mutation HTTP chỉ thêm '/x-audit' vào URL literal và đổi method của lời gọi .get/.post/...; không đổi method của .request/.stream, không đổi library, client_at, khóa config, receiver hoặc vị trí lời gọi. Gold config bị biến thành unknown nên nhánh kiểm config không được đo bằng claim tương ứng. Nguồn: slice/tools/fr029_checkaudit.py:259, slice/tools/fr029_checkaudit.py:265, slice/tools/fr029_checkaudit.py:270, slice/l3slice/docfacts.py:600.",
    "False acceptance của route và HTTP được thử chỉ sau khi claim đúng đã được chấp nhận. Một checker từ chối tất cả vẫn có hai bộ đếm false_acceptance bằng 0, dù false_rejection sẽ tăng. Không có bộ đếm riêng số mutation thực sự chạy để phân biệt 0 lỗi với 0 cơ hội thử. Nguồn: slice/tools/fr029_checkaudit.py:122, slice/tools/fr029_checkaudit.py:127, slice/tools/fr029_checkaudit.py:262, slice/tools/fr029_checkaudit.py:264, slice/tools/fr029_checkaudit.py:403, slice/tools/fr029_checkaudit.py:411.",
    "Bỏ qua ca âm đã có trong gold: excluded_routes và limitations chỉ được dùng để miễn tính nhiễu suspects; non_http_calls không được dùng để thử add_http. Ví dụ registry.get được gold ghi rõ not_fastapi nhưng không được nộp như claim route sai. Nguồn: slice/tools/fr029_checkaudit.py:107, slice/tools/fr029_checkaudit.py:238, slice/tools/fr029_checkaudit.py:280, slice/tests/fixtures/fr029/exclusions.gold.json:51, slice/tests/fixtures/fr029/http_calls.gold.json:187.",
    "Có chỉ số luôn bằng 0: router_level_routes được khởi tạo nhưng không được cập nhật. Toàn bộ audit_dependencies của định dạng v1/dev cũng trả bộ đếm rỗng vì routes={}; http_items không có nhánh dev. Đây là không đo, không phải kiểm thành công. Ngoài ra main trả exit code 0 sau khi ghi báo cáo, kể cả khi đã ghi lỗi checker. Nguồn: slice/tools/fr029_checkaudit.py:184, slice/tools/fr029_checkaudit.py:185, slice/tools/fr029_checkaudit.py:218, slice/tools/fr029_checkaudit.py:233, slice/tools/fr029_checkaudit.py:392, slice/tools/fr029_checkaudit.py:418.",
    "Phép nhắc tham số chưa kiểm đúng nguồn gốc: reminder được coi đúng nếu trùng bất kỳ tham số gold của route; không chứng minh tham số đến từ dependency đang xét. Việc loại tham số trực tiếp còn dựa vào tên đối số hoặc literal bất kỳ trong signature, có thể loại nhầm tham số dependency khỏi mẫu số. Nguồn: slice/tools/fr029_checkaudit.py:199, slice/tools/fr029_checkaudit.py:203, slice/tools/fr029_checkaudit.py:206.",
    "Phép suspects đối chiếu theo dòng, không theo lời gọi và looks_like; một dấu hiệu khác trên cùng dòng cũng có thể làm HTTP được coi là đã đánh dấu. Khi tính nhiễu, HTTP được miễn thêm ba dòng sau span. Số not_gold_item vì thế không tương đương số HTTP/route nhận nhầm đã được xác minh. Nguồn: slice/tools/fr029_checkaudit.py:279, slice/tools/fr029_checkaudit.py:294, slice/tools/fr029_checkaudit.py:300, slice/tools/fr029_checkaudit.py:317.",
    "Các vòng không chứng minh khả năng tổng quát hóa: đều báo 33 ca; r3 có sáu reminder streaming sai tại AgentGPT, r4 hết lỗi đó. Công cụ hiện tại chạy danh sách repo cố định, gồm cả split development; --heldout chỉ xuất packet, không chấm độc lập. Mẫu số gold_dep_params còn đổi từ 70 ở r1 sang 69 ở r2, nên không được quy toàn bộ cải thiện cho checker. Nguồn: ket-qua-chay/fr029-checkaudit-20261008-r1/summary.json:2, ket-qua-chay/fr029-checkaudit-20261008-r1/summary.json:13, ket-qua-chay/fr029-checkaudit-20261008-r2/summary.json:13, ket-qua-chay/fr029-checkaudit-20261008-r3/audit.json:61, ket-qua-chay/fr029-checkaudit-20261008-r4/audit.json:60, slice/tools/fr029_checkaudit.py:65, slice/tools/fr029_checkaudit.py:326, slice/tools/fr029_checkaudit.py:382."
  ],
  "overfit": [
    {
      "luat": "Alias được gộp theo tên trên toàn snapshot, không theo module/import.",
      "vi_du_code": "# a.py\nfrom typing import Annotated\nfrom fastapi import Depends, Header\ndef dep_a(x_a: str = Header()): return x_a\nUserDep = Annotated[str, Depends(dep_a)]\n\n# b.py\nfrom typing import Annotated\nfrom fastapi import Depends, Header\ndef dep_b(x_b: str = Header()): return x_b\nUserDep = Annotated[str, Depends(dep_b)]\n\n# main.py\nfrom fastapi import FastAPI\nfrom a import UserDep\napp = FastAPI()\n@app.get('/')\ndef endpoint(user: UserDep): return user",
      "hau_qua": "Bảng UserDep chứa cả dep_a và dep_b. dependency_at có thể nhận claim dep_b tại dòng endpoint dù route chỉ dùng alias từ a; phép nhắc qua alias cũng có thể kéo tham số của b vào. Nguồn: slice/l3slice/docfacts.py:358, slice/l3slice/docfacts.py:362, slice/l3slice/docfacts.py:363, slice/l3slice/docfacts.py:848.",
      "muc_do": "cao"
    },
    {
      "luat": "Alias chỉ nhận Annotated và Depends trên cùng dòng khai báo.",
      "vi_du_code": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Header\ndef token(x_token: str = Header()): return x_token\nTokenDep = Annotated[\n    str,\n    Depends(token),\n]\napp = FastAPI()\n@app.get('/')\ndef endpoint(t: TokenDep): return t",
      "hau_qua": "Không ghi TokenDep vào bảng alias: claim token tại dòng endpoint bị từ chối, và việc nhắc x-token qua alias bị bỏ sót. Alias dùng Security cũng không được regex Depends nhận. Nguồn: slice/l3slice/docfacts.py:352, slice/l3slice/docfacts.py:359, slice/l3slice/docfacts.py:361, slice/l3slice/docfacts.py:848.",
      "muc_do": "cao"
    },
    {
      "luat": "Class.method bị rút gọn thành tên method khi kiểm chứng và khi đệ quy dependency.",
      "vi_du_code": "from fastapi import FastAPI, Depends, Header\nclass A:\n    @staticmethod\n    def inject(x_a: str = Header()): return x_a\nclass B:\n    @staticmethod\n    def inject(x_b: str = Header()): return x_b\ndef outer(v=Depends(B.inject)): return v\napp = FastAPI()\n@app.get('/')\ndef endpoint(v=Depends(outer)): return v",
      "hau_qua": "Ở dòng Depends(B.inject), claim A.inject vẫn được dependency_at nhận vì chỉ tìm inject. Khi dependency_params đi từ outer tới B.inject, _name_of làm mất B; có hai inject nên trả [] và bỏ x-b. Bộ lọc theo class chỉ giúp khi tên có dấu chấm còn được giữ. Nguồn: slice/l3slice/docfacts.py:350, slice/l3slice/docfacts.py:817, slice/l3slice/docfacts.py:820, slice/l3slice/docfacts.py:862, slice/l3slice/docfacts.py:911.",
      "muc_do": "cao"
    },
    {
      "luat": "Factory dependency được suy từ việc trả về hàm con, không phân biệt Depends(factory) với Depends(factory(...)).",
      "vi_du_code": "from fastapi import FastAPI, Depends, Query\ndef provider(q: str):\n    def inner(x: str = Query(...)): return x\n    return inner\napp = FastAPI()\n@app.get('/')\ndef endpoint(value=Depends(provider)): return {'ok': True}",
      "hau_qua": "FastAPI gọi provider nên q là tham số của dependency. Checker chuyển sang inner, nhắc query x và bỏ q. Cách sửa phù hợp factory AgentGPT không đủ để xác định ngữ nghĩa mọi hàm trả callable. Nguồn: slice/l3slice/docfacts.py:826, slice/l3slice/docfacts.py:830, slice/l3slice/docfacts.py:863; việc FastAPI lấy signature của callable dependency: C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:274.",
      "muc_do": "cao"
    },
    {
      "luat": "_factory_makes_app coi có tạo FastAPI ở đâu đó trong thân hàm là trả về app.",
      "vi_du_code": "from fastapi import FastAPI\nclass Registry:\n    def get(self, path): return lambda fn: fn\ndef build():\n    unused = FastAPI()\n    return Registry()\nrouter = build()\n@router.get('/fake')\ndef fake(): return {}",
      "hau_qua": "Nhận decorator giả: factory có literal FastAPI( nên được coi là tạo receiver hợp lệ dù trả Registry. Không phân tích đối tượng thực sự được return. Nguồn: slice/l3slice/docfacts.py:369, slice/l3slice/docfacts.py:373, slice/l3slice/docfacts.py:394.",
      "muc_do": "cao"
    },
    {
      "luat": "_factory_makes_app không theo chuỗi factory và phụ thuộc tên constructor.",
      "vi_du_code": "from fastapi import FastAPI\ndef build(): return FastAPI()\ndef create(): return build()\napp = create()\n@app.get('/real')\ndef real(): return {}",
      "hau_qua": "Từ chối decorator thật: thân create không chứa FastAPI(/APIRouter( và không có return annotation tương ứng. Một factory dùng import FastAPI as FA cũng gặp cùng giới hạn tên. Nguồn: slice/l3slice/docfacts.py:374, slice/l3slice/docfacts.py:375, slice/l3slice/docfacts.py:394.",
      "muc_do": "cao"
    },
    {
      "luat": "Receiver decorator được import mà không có phép gán cùng file không bị xác minh.",
      "vi_du_code": "# Trích fixture hiện có:\nfrom app.hooks import registry\n@registry.get('/orders/cached')\ndef cached_orders():\n    return []",
      "hau_qua": "_decorator_problems chấp nhận GET vì built rỗng, dù registry là Registry tự viết và gold ghi not_fastapi. Đây là phản ví dụ đã nằm trong corpus, không chỉ giả định repo mới. Nguồn: slice/tests/fixtures/fr029/exclusions/app/routers/orders.py:3, slice/tests/fixtures/fr029/exclusions/app/routers/orders.py:13, slice/tests/fixtures/fr029/exclusions/app/hooks.py:5, slice/tests/fixtures/fr029/exclusions/app/hooks.py:13, slice/tests/fixtures/fr029/exclusions.gold.json:51, slice/l3slice/docfacts.py:392, slice/l3slice/docfacts.py:394.",
      "muc_do": "cao"
    },
    {
      "luat": "_decorator_problems tìm method literal trong toàn bộ decorator api_route.",
      "vi_du_code": "from fastapi import FastAPI\napp = FastAPI()\n@app.api_route('/x', methods=['GET'], name='POST')\ndef endpoint(): return {}",
      "hau_qua": "Claim POST được chấp nhận dù methods chỉ chứa GET, vì POST có trong name. Mutation hiện tại tránh mọi method literal có trong đoạn nên tránh đúng phản ví dụ này. Nguồn: slice/l3slice/docfacts.py:397, slice/l3slice/docfacts.py:398, slice/tools/fr029_checkaudit.py:130.",
      "muc_do": "cao"
    },
    {
      "luat": "Scalar trong dependency mặc định luôn được nhắc là query, không xét path của route.",
      "vi_du_code": "from fastapi import FastAPI, Depends\ndef identify(item_id: int): return item_id\napp = FastAPI()\n@app.get('/items/{item_id}')\ndef endpoint(value=Depends(identify)): return value",
      "hau_qua": "Nhắc thêm query item_id sai, trong khi FastAPI nhận item_id từ path. dependency_params không nhận ngữ cảnh path và luôn phát query cho scalar không marker. Nguồn: slice/l3slice/docfacts.py:811, slice/l3slice/docfacts.py:844; quy tắc thật trong code FastAPI: C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:284, C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:448.",
      "muc_do": "cao"
    },
    {
      "luat": "Scalar chỉ được nhận bằng danh sách tên và vài dạng AST.",
      "vi_du_code": "from fastapi import FastAPI, Depends\ndef search(q: 'str'): return q\napp = FastAPI()\n@app.get('/')\ndef endpoint(value=Depends(search)): return value",
      "hau_qua": "Bỏ nhắc q: annotation chuỗi là ast.Constant nên _scalar trả false, trong khi FastAPI giải annotation chuỗi trước khi phân tích tham số. Nguồn: slice/l3slice/docfacts.py:892, slice/l3slice/docfacts.py:895, slice/l3slice/docfacts.py:903, C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/fastapi/dependencies/utils.py:247.",
      "muc_do": "vua"
    },
    {
      "luat": "CLIENT_NAME và tên Client/Session là dấu hiệu từ vựng, không chứng minh receiver HTTP.",
      "vi_du_code": "import httpx\nclient_cache = {'https://api.example/items': 1}\nvalue = client_cache.get('https://api.example/items')",
      "hau_qua": "suspects đánh dấu thao tác dict vì tên chứa client. Nếu nộp claim library=httpx, method=GET và URL là khóa dict thì add_http cũng chấp nhận: nó kiểm import và hình dạng lời gọi, không kiểm receiver. R4 vẫn có nhiễu session.delete và redis_client.get. Nguồn: slice/l3slice/docfacts.py:568, slice/l3slice/docfacts.py:576, slice/l3slice/docfacts.py:596, slice/l3slice/docfacts.py:755, slice/l3slice/docfacts.py:922, ket-qua-chay/fr029-checkaudit-20261008-r4/audit.json:78, ket-qua-chay/fr029-checkaudit-20261008-r4/audit.json:537.",
      "muc_do": "cao"
    },
    {
      "luat": "add_http không nối library đã khai với receiver thực tế.",
      "vi_du_code": "import httpx\nimport requests\nrequests.get('https://api.example/items')\n# Claim sai: library='httpx', method='GET', target literal như trên.",
      "hau_qua": "Claim sai library vẫn được chấp nhận vì file có import httpx; _http_receivers không được add_http dùng để kiểm danh tính lời gọi. Nguồn: slice/l3slice/docfacts.py:568, slice/l3slice/docfacts.py:576, slice/l3slice/docfacts.py:615.",
      "muc_do": "cao"
    },
    {
      "luat": "_string_rows loại cả dòng đóng chuỗi nhiều dòng.",
      "vi_du_code": "import httpx\nbanner = '''hello\nworld'''; response = httpx.get('https://api.example/items')",
      "hau_qua": "Bỏ sót HTTP thực thi sau dấu đóng chuỗi vì cả dòng nằm trong in_string. Hàm xử lý mọi chuỗi nhiều dòng, không chỉ docstring, và không phân biệt cột chứa chuỗi với cột chứa code. Nguồn: slice/l3slice/docfacts.py:746, slice/l3slice/docfacts.py:749, slice/l3slice/docfacts.py:931, slice/l3slice/docfacts.py:932.",
      "muc_do": "cao"
    },
    {
      "luat": "_url_argument tìm literal và url= trên phần văn bản còn lại, không giới hạn AST của lời gọi.",
      "vi_du_code": "import httpx\nhttpx.get('https://real.example'); note = dict(url='https://decoy.example')\n# Claim URL sai: https://decoy.example",
      "hau_qua": "Chấp nhận URL từ câu lệnh sau vì regex url= quét qua dấu đóng lời gọi. Tương tự, httpx.get('https://real.example' + suffix) có thể được nhận sai là URL literal chỉ gồm tiền tố. Mutation thêm '/x-audit' không thử các literal gây nhiễu có sẵn này. Nguồn: slice/l3slice/docfacts.py:637, slice/l3slice/docfacts.py:638, slice/l3slice/docfacts.py:645, slice/tools/fr029_checkaudit.py:267.",
      "muc_do": "cao"
    },
    {
      "luat": "_call_span đếm ngoặc bằng ký tự thô; việc mở rộng span chỉ cứu kiểm URL.",
      "vi_du_code": "import httpx\nhttpx.get(  # )\n    'https://api.example/items'\n)\nhttpx.request(\n    'GET',\n    'https://api.example/other'\n)",
      "hau_qua": "Nếu dẫn riêng dòng bắt đầu lời gọi, GET thứ nhất bị từ chối URL vì dấu ')' trong comment làm _call_span kết thúc sớm. Request thứ hai bị từ chối method GET vì kiểm method chỉ đọc span đã dẫn, không mở rộng như kiểm URL. Cả hai có thể xảy ra dù các dòng tiếp theo đã được đọc. Nguồn: slice/l3slice/docfacts.py:583, slice/l3slice/docfacts.py:586, slice/l3slice/docfacts.py:597, slice/l3slice/docfacts.py:622, slice/l3slice/docfacts.py:628, slice/l3slice/docfacts.py:630.",
      "muc_do": "vua"
    },
    {
      "luat": "_url_argument của request/stream chỉ bỏ qua positional method khi đó là literal.",
      "vi_du_code": "import httpx\nverb = 'GET'\nhttpx.request(verb, 'https://api.example/items')\n# Claim method unknown, target literal đúng như trên.",
      "hau_qua": "Vẫn từ chối URL đúng: method là biến làm STRING.match thất bại, args bị đặt thành chuỗi rỗng. Claim method unknown không giải quyết được việc nhận URL positional thứ hai. Nguồn: slice/l3slice/docfacts.py:581, slice/l3slice/docfacts.py:642, slice/l3slice/docfacts.py:643, slice/l3slice/docfacts.py:644.",
      "muc_do": "vua"
    }
  ],
  "http_bo_sot": [
    {
      "dang": "Client từ file khác, file gọi không import trực tiếp thư viện; kể cả tên client rõ ràng cũng bị chặn trước CLIENT_NAME. Nguồn: slice/l3slice/docfacts.py:745, slice/l3slice/docfacts.py:752.",
      "vi_du_code": "# clients.py\nimport httpx\nclient = httpx.Client()\n# routes.py\nfrom clients import client\ndef fetch(): return client.get('https://api.example/items')"
    },
    {
      "dang": "Thư viện đứng sau trong import nhiều module: regex http_file không thấy. Nguồn: slice/l3slice/docfacts.py:745.",
      "vi_du_code": "import os, httpx\nhttpx.get('https://api.example/items')"
    },
    {
      "dang": "Import trực tiếp hàm HTTP, gọi không có dấu chấm. Nguồn: slice/l3slice/docfacts.py:66, slice/l3slice/docfacts.py:921.",
      "vi_du_code": "from requests import get\nget('https://api.example/items')\nfrom httpx import get as fetch\nfetch('https://api.example/other')"
    },
    {
      "dang": "Đổi tên constructor bằng from-import: không theo alias constructor. Nguồn: slice/l3slice/docfacts.py:923, slice/l3slice/docfacts.py:947, slice/l3slice/docfacts.py:948, slice/l3slice/docfacts.py:970.",
      "vi_du_code": "from httpx import Client as C\nc = C()\nc.get('https://api.example/items')\n# Cùng vấn đề với requests.Session as S hoặc aiohttp.ClientSession as S."
    },
    {
      "dang": "Gán client qua biến khác: không truyền nhận diện qua phép gán tên. Nguồn: slice/l3slice/docfacts.py:968, slice/l3slice/docfacts.py:979.",
      "vi_du_code": "import httpx\nc = httpx.Client()\nwire = c\nwire.get('https://api.example/items')"
    },
    {
      "dang": "Client là đối số không annotation, tên không chứa client/session/http. Nguồn: slice/l3slice/docfacts.py:755, slice/l3slice/docfacts.py:922, slice/l3slice/docfacts.py:989.",
      "vi_du_code": "import requests\ndef fetch(wire):\n    return wire.get('https://api.example/items')\nfetch(requests.Session())"
    },
    {
      "dang": "Client nằm trong list/dict: HTTP_CALL không khớp receiver kết thúc bằng dấu ']'. Nguồn: slice/l3slice/docfacts.py:754, slice/l3slice/docfacts.py:921.",
      "vi_du_code": "import httpx\npool = [httpx.Client()]\npool[0].get('https://api.example/items')"
    },
    {
      "dang": "Client là lớp con mang tên khác: không theo quan hệ kế thừa. Nguồn: slice/l3slice/docfacts.py:923, slice/l3slice/docfacts.py:965, slice/l3slice/docfacts.py:970.",
      "vi_du_code": "import httpx\nclass Transport(httpx.Client): pass\nwire = Transport()\nwire.get('https://api.example/items')"
    },
    {
      "dang": "requests.session() viết thường: CLIENT_MAKER chỉ nhận Session, và biến wire không được bind là client. Nguồn: slice/l3slice/docfacts.py:923, slice/l3slice/docfacts.py:970; hàm thật tồn tại tại C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/requests/sessions.py:908.",
      "vi_du_code": "import requests\nwire = requests.session()\nwire.get('https://api.example/items')"
    },
    {
      "dang": "Factory context manager yield biến được bind bằng with: returns_client chỉ thu biến từ Assign. Nguồn: slice/l3slice/docfacts.py:956, slice/l3slice/docfacts.py:959, slice/l3slice/docfacts.py:965, slice/l3slice/docfacts.py:987.",
      "vi_du_code": "import aiohttp\nfrom contextlib import asynccontextmanager\n@asynccontextmanager\nasync def connection():\n    async with aiohttp.ClientSession() as c:\n        yield c\nasync def fetch():\n    async with connection() as wire:\n        async with wire.get('https://api.example/items') as response:\n            return await response.text()"
    },
    {
      "dang": "Receiver và dấu chấm nằm ở hai dòng khác nhau: quét từng dòng không nối biểu thức. Nguồn: slice/l3slice/docfacts.py:748, slice/l3slice/docfacts.py:754, slice/l3slice/docfacts.py:921.",
      "vi_du_code": "import httpx\nresponse = (httpx\n    .get('https://api.example/items'))"
    },
    {
      "dang": "Giữ bound method rồi gọi qua biến, hoặc dùng getattr: không có .get( tại chỗ thực thi. Nguồn: slice/l3slice/docfacts.py:66, slice/l3slice/docfacts.py:921.",
      "vi_du_code": "import httpx\nwire = httpx.Client()\nfetch = wire.get\nfetch('https://api.example/items')\ngetattr(wire, 'get')('https://api.example/other')"
    },
    {
      "dang": "Gửi Request bằng .send(): không nằm trong tập method được nhận. Nguồn: slice/l3slice/docfacts.py:66, slice/l3slice/docfacts.py:921; API thật tại C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/httpx/_client.py:879 và C:/Users/dell/AppData/Local/Programs/Python/Python311/Lib/site-packages/requests/sessions.py:752.",
      "vi_du_code": "import httpx\nimport requests\nc = httpx.Client()\nc.send(httpx.Request('GET', 'https://api.example/items'))\ns = requests.Session()\np = requests.Request('GET', 'https://api.example/other').prepare()\ns.send(p)"
    },
    {
      "dang": "HTTP sau dấu đóng chuỗi nhiều dòng bị loại cả dòng. Nguồn: slice/l3slice/docfacts.py:749, slice/l3slice/docfacts.py:932.",
      "vi_du_code": "import requests\ntext = '''a\nb'''; requests.get('https://api.example/items')"
    }
  ],
  "de_xuat": [
    "Tạo gold độc lập cho từng claim gồm vị trí chính xác, dependency đầy đủ module/class, nguồn tham số và tập giá trị được phép. Không lấy expected dependency từ Claims._aliases; chỉ chuyển unknown khi gold cho phép rõ ràng. Nguồn khoảng trống: slice/tools/fr029_checkaudit.py:159, slice/tools/fr029_checkaudit.py:203, slice/tools/fr029_checkaudit.py:255.",
    "Thêm mutation khó nhưng hợp lệ về cú pháp: method nằm trong name/description thay vì methods; handler có thật của route khác; A.inject thay B.inject; URL lấy từ câu lệnh hoặc đối số khác; URL chỉ là tiền tố; library đúng tên nhưng sai receiver; config key có mặt nhưng không phải đích. Nguồn khoảng trống: slice/tools/fr029_checkaudit.py:130, slice/tools/fr029_checkaudit.py:197, slice/tools/fr029_checkaudit.py:267, slice/l3slice/docfacts.py:398, slice/l3slice/docfacts.py:638.",
    "Đưa excluded_routes và non_http_calls vào tập claim âm thực sự; ưu tiên registry được import, dict.get, SQLAlchemy Session và Redis client. Không chỉ miễn chúng khi tính nhiễu suspects. Nguồn ca có sẵn: slice/tests/fixtures/fr029/exclusions.gold.json:51, slice/tests/fixtures/fr029/http_calls.gold.json:187; nhánh audit hiện tại: slice/tools/fr029_checkaudit.py:280.",
    "Thêm repo mẫu dependency theo cặp đối chứng: alias một dòng/nhiều dòng, hai module trùng alias, Security, class method trực tiếp/lồng nhau, Depends(factory)/Depends(factory(...)), factory trả callable qua if hoặc partial, scalar trùng path, annotation chuỗi. Gold ghi cả tham số phải có và tham số tuyệt đối không được nhắc. Nguồn các giả định cần thử: slice/l3slice/docfacts.py:359, slice/l3slice/docfacts.py:817, slice/l3slice/docfacts.py:826, slice/l3slice/docfacts.py:844, slice/l3slice/docfacts.py:862.",
    "Thêm ma trận HTTP từ các dạng http_bo_sot; mỗi ca có bản đổi tên client thành wire, đổi cách import, đổi định dạng dòng nhưng giữ nguyên hành vi. Đo riêng recall của suspects và khả năng add_http chấp nhận claim đúng; bổ sung nhiều lời gọi cùng dòng và code sau dấu đóng chuỗi. Nguồn hai đường kiểm độc lập hiện tại: slice/l3slice/docfacts.py:561, slice/l3slice/docfacts.py:727, slice/l3slice/docfacts.py:931.",
    "Chạy mutation độc lập với kết quả claim đúng; báo số ca dương, ca âm, mutation đã chạy, ca bỏ qua và lỗi công cụ cho từng loại. Kiểm thêm checker giả luôn nhận, luôn từ chối và luôn trả danh sách rỗng để phát hiện phép đo không phân biệt được chất lượng. Không diễn giải router_level_routes=0 hay exit code 0 thành đạt. Nguồn: slice/tools/fr029_checkaudit.py:127, slice/tools/fr029_checkaudit.py:184, slice/tools/fr029_checkaudit.py:264, slice/tools/fr029_checkaudit.py:418.",
    "Đóng băng phiên bản checker, audit, gold và repo cho mỗi lần so sánh; dành repo chưa dùng sửa luật làm tập kiểm cuối. Packet heldout hiện tại cần người chấm độc lập và đáp án được cố định trước khi sửa tiếp. Nguồn: slice/tools/fr029_checkaudit.py:40, slice/tools/fr029_checkaudit.py:65, slice/tools/fr029_checkaudit.py:326, slice/tools/fr029_checkaudit.py:374; mẫu số đã thay đổi: ket-qua-chay/fr029-checkaudit-20261008-r1/summary.json:13, ket-qua-chay/fr029-checkaudit-20261008-r2/summary.json:13.",
    "Đối chiếu suspects theo từng lời gọi/vị trí và đúng loại dấu hiệu; tách route, HTTP, registration, trường hợp chưa xác minh và ca ngoài phạm vi. Bổ sung đo dependency cho v1/dev hoặc ghi rõ chưa đo; thêm gold dependency cấp router/app thay cho bộ đếm luôn 0. Nguồn: slice/tools/fr029_checkaudit.py:141, slice/tools/fr029_checkaudit.py:184, slice/tools/fr029_checkaudit.py:185, slice/tools/fr029_checkaudit.py:279, slice/tools/fr029_checkaudit.py:294, slice/tools/fr029_checkaudit.py:317."
  ]
}
```

Có vòng tròn cục bộ ở phép kiểm alias, không phải toàn bộ gold: `slice/tools/fr029_checkaudit.py:159`.
“Chấp nhận nhầm = 0” chưa chứng minh độ chính xác: mutation yếu và bỏ thử sau khi claim đúng thất bại (`slice/tools/fr029_checkaudit.py:127`, `slice/tools/fr029_checkaudit.py:264`).
Ngay fixture hiện có chứa receiver giả chưa được audit thử như ca âm: `slice/tests/fixtures/fr029/exclusions.gold.json:51`.
Rủi ro HTTP đáng chú ý nằm ở điều kiện import, nhận diện receiver và loại cả dòng chứa chuỗi (`slice/l3slice/docfacts.py:745`, `slice/l3slice/docfacts.py:755`, `slice/l3slice/docfacts.py:932`).
Các phản ví dụ trên được suy trực tiếp từ code; tôi không chạy checker, không sửa file và không đọc các thư mục bị loại trừ.