```json
{
  "repos": [
    {
      "repo": "Caoyongqi912_case_auto_hub",
      "dependencies": {
        "params_dung": 1,
        "params_sai": [],
        "params_thieu": [
          {
            "dep": "Authentication()",
            "in": "header",
            "name": "Authorization",
            "source": "app/controller/__init__.py:24; app/controller/file/__init__.py:41"
          }
        ]
      },
      "deps_bo_sot": {
        "routes_kiem": 30,
        "items": [
          {
            "route": "POST /file/interface/upload",
            "dependency": "Authentication(): biến thể instance dùng __call__, thiếu header Authorization; đây là route đại diện cho lỗi lặp lại",
            "cap": "handler",
            "source": "app/controller/file/__init__.py:35; app/controller/file/__init__.py:41; app/controller/__init__.py:24"
          },
          {
            "route": "GET /play/case/detail",
            "dependency": "GetPlayCaseByCaseId qua Depends(): query caseId",
            "cap": "handler",
            "source": "app/controller/play/play_case.py:39; app/controller/play/play_case.py:40; app/schema/play/playCaseSchema.py:51; app/schema/play/playCaseSchema.py:53"
          },
          {
            "route": "GET /project/env/queryBy",
            "dependency": "FilterByEnvSchema qua Depends(): query id, uid, description, host, port, project_id",
            "cap": "handler",
            "source": "app/controller/project/project.py:145; app/controller/project/project.py:146; app/schema/base/env.py:21; app/schema/base/env.py:6; app/schema/base/env.py:7; app/schema/base/env.py:9; app/schema/base/env.py:10; app/schema/base/env.py:11; app/schema/base/env.py:12"
          },
          {
            "route": "GET /project/env/detail",
            "dependency": "EnvField qua Depends(): query id, uid, description, host, port, project_id",
            "cap": "handler",
            "source": "app/controller/project/project.py:154; app/controller/project/project.py:155; app/schema/base/env.py:5; app/schema/base/env.py:6; app/schema/base/env.py:7; app/schema/base/env.py:9; app/schema/base/env.py:10; app/schema/base/env.py:11; app/schema/base/env.py:12"
          }
        ]
      },
      "suspects": {
        "http_that": 2,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [
        {
          "at": "common/notifyManager.py:296",
          "code": "response = await self.api_sender(url=Config.WeChatBaseUrl, method=\"post\", params={\"key\": push_config.push_value}, json=_, headers={\"Content-Type\": \"application/json\"})"
        },
        {
          "at": "utils/report.py:151",
          "code": "response = await self.sender(url=Config.WeChatBaseUrl, method=\"post\", params={\"key\": self._push_value}, json=_, headers={\"Content-Type\": \"application/json\"}, **kwargs)"
        },
        {
          "at": "croe/interface/executor/interface_executor.py:158",
          "code": "ctx.response = await self.http(method=ctx.interface.interface_method, **ctx.request_info)"
        }
      ],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source, không sửa file, không chạy hoặc import mã repo. Đường dẫn source tương đối với D:/VSF/l3-heldout-repos2/Caoyongqi912_case_auto_hub. Khi đánh số dòng đã xử lý cả CRLF, LF và CR. Loại tests/, test_*.py và conftest.py theo phạm vi yêu cầu.",
    "Authentication có hai cách dùng thực sự khác nhau. query isAdmin trong gói được tính đúng một lần vì POST /interfaceResult/pageCaseResult dùng Depends(Authentication), khiến FastAPI phân tích constructor có isAdmin: bool = False (app/controller/interface/interfaceResultController.py:25; app/controller/interface/interfaceResultController.py:26; app/controller/__init__.py:21). Tuy nhiên, tham số này không được áp dụng cho Depends(Authentication()) hoặc Depends(Authentication(isAdmin=True)): các instance lấy header Authorization từ __call__ (app/controller/file/__init__.py:41; app/controller/project/module.py:13; app/controller/__init__.py:24). Vì gói gộp theo tên Authentication, không thể dùng danh sách hiện tại chung cho mọi route.",
    "JenkinsWebhookAuth có params rỗng là đúng với cách đăng ký hiện tại: cả hai handler truyền class bằng Depends(JenkinsWebhookAuth), không truyền instance; class không có constructor nhận request, nên FastAPI không gọi tiếp __call__ để lấy X-Jenkins-Token (app/controller/interface/interfaceTaskController.py:237; app/controller/play/play_task.py:123; app/controller/__init__.py:37; app/controller/__init__.py:54). Header có alias X-Jenkins-Token chỉ thuộc chữ ký __call__, không phải tham số dependency được kích hoạt ở hai handler này. Không tính header đó là thiếu.",
    "params_thieu đối chiếu hai mục đã có trong gói. Ba class hoàn toàn vắng khỏi gói được liệt kê cùng toàn bộ query của chúng trong deps_bo_sot: caseId tại app/schema/play/playCaseSchema.py:53 và sáu trường EnvField tại app/schema/base/env.py:6, app/schema/base/env.py:7, app/schema/base/env.py:9, app/schema/base/env.py:10, app/schema/base/env.py:11, app/schema/base/env.py:12. Các model này được dùng qua Depends(), nên các trường scalar trở thành query; không phải trường hợp model body thông thường. Mục Authentication() trong deps_bo_sot trình bày riêng biến thể callable instance theo quy ước bổ sung, cùng lỗi header đã ghi trong params_thieu.",
    "Mẫu 30 route gồm 24 route đầu tiên ở 24 module: GET /file/ui_case/uid={uid} (app/controller/file/__init__.py:25); POST /interfaceCase/insert (app/controller/interface/interfaceCaseController.py:57); POST /interface/page (app/controller/interface/interfaceController.py:50); POST /interface/global/insert_header (app/controller/interface/interfaceGlobalController.py:23); POST /interface/group/insert (app/controller/interface/interfaceGroupController.py:32); POST /interfaceResult/pageCaseResult (app/controller/interface/interfaceResultController.py:25); POST /interface/task/insert (app/controller/interface/interfaceTaskController.py:34); GET /play/case/detail (app/controller/play/play_case.py:39); GET /play/config/locator/list (app/controller/play/play_config.py:19); POST /play/step/insert (app/controller/play/play_step.py:22); POST /play/stepGroup/insert (app/controller/play/play_step_group.py:19); POST /play/task/insertTask (app/controller/play/play_task.py:22); POST /aps/job/add (app/controller/project/aps_job.py:21); GET /project/config/queryTB (app/controller/project/db_config.py:26); POST /module/insert (app/controller/project/module.py:12); POST /project/insert_variable (app/controller/project/project.py:25); POST /project/push/insertConfig (app/controller/project/push_config.py:22); GET /statistics/all (app/controller/statistics/__init__.py:16); POST /hub/caseConfig/page (app/controller/test_case/case_config.py:29); POST /hub/plan/insert (app/controller/test_case/case_plan.py:43); POST /hub/mindCase/insert (app/controller/test_case/mind_case.py:12); POST /hub/req/insertRequirement (app/controller/test_case/requirements.py:20); GET /department/query (app/controller/user/department.py:29); POST /user/pageUser (app/controller/user/user.py:26).",
    "Sáu route bổ sung để đủ 30: GET /project/env/queryBy (app/controller/project/project.py:145); GET /project/env/detail (app/controller/project/project.py:154); POST /interface/task/execute_by_jenkins (app/controller/interface/interfaceTaskController.py:234); POST /play/task/executeJenkins (app/controller/play/play_task.py:120); POST /file/interface/upload (app/controller/file/__init__.py:35); POST /user/login (app/controller/user/user.py:117). Đã đọc chữ ký handler và decorator của từng route trong mẫu.",
    "Cấp app: không khai báo dependencies ở FastAPI hoặc include_router (main.py:122; main.py:127; main.py:131). Cấp router: các router của mẫu không khai báo dependencies (app/controller/file/__init__.py:22; app/controller/interface/interfaceCaseController.py:52; app/controller/interface/interfaceController.py:36; app/controller/interface/interfaceGlobalController.py:19; app/controller/interface/interfaceGroupController.py:27; app/controller/interface/interfaceResultController.py:22; app/controller/interface/interfaceTaskController.py:29; app/controller/play/play_case.py:36; app/controller/play/play_config.py:16; app/controller/play/play_step.py:19; app/controller/play/play_step_group.py:16; app/controller/play/play_task.py:18; app/controller/project/aps_job.py:18; app/controller/project/db_config.py:21; app/controller/project/module.py:9; app/controller/project/project.py:22; app/controller/project/push_config.py:19; app/controller/statistics/__init__.py:13; app/controller/test_case/case_config.py:24; app/controller/test_case/case_plan.py:39; app/controller/test_case/mind_case.py:9; app/controller/test_case/requirements.py:17; app/controller/user/department.py:18; app/controller/user/user.py:22). Không có dependency cấp decorator trong 30 decorator đã dẫn.",
    "Phân loại từng suspect: common/httpxClient.py:110 là http_that vì self.client trả httpx.AsyncClient được tạo tại common/httpxClient.py:65, import tại common/httpxClient.py:9. croe/a_manager/script_manager.py:350 là http_that vì client được tạo bằng httpx.AsyncClient tại croe/a_manager/script_manager.py:349. Hai mục này bao phủ toàn bộ suspects của gói; không có mục thuộc bốn nhóm còn lại. decorators_refused trong gói rỗng nên không có mục cần phán xét.",
    "http_bo_sot liệt kê ba điểm gọi HTTP gián tiếp qua lớp bọc HttpxClient, không phải ba sink thư viện mới: self.api_sender được tạo tại common/notifyManager.py:271; self.sender tại utils/report.py:37; self.http tại croe/interface/executor/interface_executor.py:78. Cả ba đi qua common/httpxClient.py:68, common/httpxClient.py:88 tới lời gọi httpx tại common/httpxClient.py:110 đã có trong suspects. Nếu chỉ thống kê lời gọi trực tiếp API httpx/requests/aiohttp thì số bỏ sót trực tiếp là 0; danh sách ba mục thể hiện các điểm sử dụng lớp bọc theo nghĩa HTTP qua httpx.",
    "Có lời gọi HTTP khác ngoài suspects: getattr(self.client, api_info.method.lower()) tại common/locust_client/locustUser.py:73, thuộc DynamicApiUser(FastHttpUser) tại common/locust_client/locustUser.py:35, import Locust tại common/locust_client/locustUser.py:13. Không đưa vào http_bo_sot vì mục này chỉ xét httpx/requests/aiohttp; cũng không cộng vào suspects.http_khac vì dòng đó không nằm trong suspects của gói."
  ]
}
```