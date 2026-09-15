"""Dựng ground_truth.json từ kết quả đọc tay repo Netflix/dispatch.

Cách đọc tay (ghi lại để ai cũng làm lại được):

- Prefix của 8 router: đọc tay `src/dispatch/api.py` và `src/dispatch/main.py`.
- Đường dẫn từng route: đọc chuỗi hằng trong decorator `@router.<verb>("...")`.
  Đã kiểm tra trong phạm vi KHÔNG có `add_api_route`, không đăng ký route trong
  vòng lặp hay trong `if`, không có decorator bọc ngoài, không có `include_router`.
- Tên bảng: dispatch không khai `__tablename__`. Lớp `Base` ở
  `database/core.py:95` có `declared_attr` sinh tên bảng bằng
  `resolve_table_name(class_name)` → snake_case. Đối chiếu chéo bằng chuỗi
  `ForeignKey("<tên_bảng>.id")` có thật trong source.
- Lời gọi ra ngoài: quét toàn repo, loại bỏ docstring, chú thích kiểu, lớp
  exception, và biến local trùng tên `requests`.

Chạy: python evaluation/_build_ground_truth.py
"""

import json
import pathlib

REPO = "sample-repos/dispatch"
COMMIT = "dd2837e82a0bf5565b1b4b4b91ea30b7262d4061"
MOUNT = "/api/v1"

# Đọc tay từ api.py (dòng 176-215) + main.py (dòng 262-268).
PREFIX = {
    "src/dispatch/case/views.py": "/{organization}/cases",
    "src/dispatch/case/type/views.py": "/{organization}/case_types",
    "src/dispatch/case/priority/views.py": "/{organization}/case_priorities",
    "src/dispatch/case/severity/views.py": "/{organization}/case_severities",
    "src/dispatch/incident/views.py": "/{organization}/incidents",
    "src/dispatch/incident/type/views.py": "/{organization}/incident_types",
    "src/dispatch/incident/priority/views.py": "/{organization}/incident_priorities",
    "src/dispatch/incident/severity/views.py": "/{organization}/incident_severities",
}

# (file, dòng, METHOD, đường dẫn trong decorator, tên hàm)
ROUTES_RAW = [
    ("case/views.py", 78, "GET", "/{case_id}", "get_case"),
    ("case/views.py", 93, "GET", "/{case_id}/participants/minimal", "get_case_participants_minimal"),
    ("case/views.py", 107, "GET", "/{case_id}/participants", "get_case_participants"),
    ("case/views.py", 126, "GET", "", "get_cases"),
    ("case/views.py", 152, "GET", "/minimal", "get_cases_minimal"),
    ("case/views.py", 162, "POST", "", "create_case"),
    ("case/views.py", 236, "POST", "/{case_id}/resources/conversation", "create_case_channel"),
    ("case/views.py", 260, "POST", "/{case_id}/resources", "create_case_resources"),
    ("case/views.py", 286, "PUT", "/{case_id}", "update_case"),
    ("case/views.py", 339, "PUT", "/{case_id}/escalate", "escalate_case"),
    ("case/views.py", 384, "DELETE", "/{case_id}", "delete_case"),
    ("case/views.py", 417, "POST", "/{case_id}/join", "join_case"),
    ("case/views.py", 439, "DELETE", "/{case_id}/remove/{email}", "remove_participant_from_case"),
    ("case/views.py", 462, "POST", "/{case_id}/add/{email}", "add_participant_to_case"),
    ("case/views.py", 486, "POST", "/{case_id}/event", "create_custom_event"),
    ("case/views.py", 513, "PATCH", "/{case_id}/event", "update_custom_event"),
    ("case/views.py", 545, "POST", "/{case_id}/exportTimeline", "export_timeline_event"),
    ("case/views.py", 574, "DELETE", "/{case_id}/event/{event_uuid}", "delete_custom_event"),
    ("case/type/views.py", 15, "GET", "", "get_case_types"),
    ("case/type/views.py", 21, "POST", "", "create_case_type"),
    ("case/type/views.py", 35, "PUT", "/{case_type_id}", "update_case_type"),
    ("case/type/views.py", 56, "GET", "/{case_type_id}", "get_case_type"),
    ("case/priority/views.py", 20, "GET", "", "get_case_priorities"),
    ("case/priority/views.py", 26, "POST", "", "create_case_priority"),
    ("case/priority/views.py", 40, "PUT", "/{case_priority_id}", "update_case_priority"),
    ("case/priority/views.py", 67, "GET", "/{case_priority_id}", "get_case_priority"),
    ("case/severity/views.py", 20, "GET", "", "get_case_severities"),
    ("case/severity/views.py", 26, "POST", "", "create_case_severity"),
    ("case/severity/views.py", 41, "PUT", "/{case_severity_id}", "update_case_severity"),
    ("case/severity/views.py", 68, "GET", "/{case_severity_id}", "get_case_severity"),
    ("incident/views.py", 76, "GET", "", "get_incidents"),
    ("incident/views.py", 102, "GET", "/{incident_id}", "get_incident"),
    ("incident/views.py", 117, "POST", "", "create_incident"),
    ("incident/views.py", 163, "POST", "/{incident_id}/resources", "create_incident_resources"),
    ("incident/views.py", 183, "PUT", "/{incident_id}", "update_incident"),
    ("incident/views.py", 219, "DELETE", "/{incident_id}", "delete_incident"),
    ("incident/views.py", 252, "POST", "/{incident_id}/join", "join_incident"),
    ("incident/views.py", 274, "POST", "/{incident_id}/subscribe", "subscribe_to_incident"),
    ("incident/views.py", 296, "DELETE", "/{incident_id}/remove/{email}", "remove_participant_from_incident"),
    ("incident/views.py", 319, "POST", "/{incident_id}/add/{email}", "add_participant_to_incident"),
    ("incident/views.py", 342, "POST", "/{incident_id}/report/tactical", "create_tactical_report"),
    ("incident/views.py", 365, "GET", "/{incident_id}/report/tactical/generate", "generate_tactical_report"),
    ("incident/views.py", 393, "POST", "/{incident_id}/report/executive", "create_executive_report"),
    ("incident/views.py", 417, "POST", "/{incident_id}/event", "create_custom_event"),
    ("incident/views.py", 442, "PATCH", "/{incident_id}/event", "update_custom_event"),
    ("incident/views.py", 474, "POST", "/{incident_id}/exportTimeline", "export_timeline_event"),
    ("incident/views.py", 503, "DELETE", "/{incident_id}/event/{event_uuid}", "delete_custom_event"),
    ("incident/views.py", 534, "GET", "/metric/forecast", "get_incident_forecast"),
    ("incident/views.py", 596, "GET", "/{incident_id}/regenerate", "generate_summary"),
    ("incident/type/views.py", 15, "GET", "", "get_incident_types"),
    ("incident/type/views.py", 21, "POST", "", "create_incident_type"),
    ("incident/type/views.py", 35, "PUT", "/{incident_type_id}", "update_incident_type"),
    ("incident/type/views.py", 59, "GET", "/{incident_type_id}", "get_incident_type"),
    ("incident/priority/views.py", 20, "GET", "", "get_incident_priorities"),
    ("incident/priority/views.py", 26, "POST", "", "create_incident_priority"),
    ("incident/priority/views.py", 40, "PUT", "/{incident_priority_id}", "update_incident_priority"),
    ("incident/priority/views.py", 66, "GET", "/{incident_priority_id}", "get_incident_priority"),
    ("incident/severity/views.py", 20, "GET", "", "get_incident_severities"),
    ("incident/severity/views.py", 26, "POST", "", "create_incident_severity"),
    ("incident/severity/views.py", 40, "PUT", "/{incident_severity_id}", "update_incident_severity"),
    ("incident/severity/views.py", 66, "GET", "/{incident_severity_id}", "get_incident_severity"),
]

routes = []
for short, line, method, path, func in ROUTES_RAW:
    f = "src/dispatch/" + short
    full = (PREFIX[f] + path) or "/"
    routes.append(
        {
            "method": method,
            "path": full,  # sau khi ghép prefix của include_router
            "path_with_mount": MOUNT + full,  # thêm prefix của app.mount()
            "file": f,
            "line": line,
            "function": func,
            "router_prefix": PREFIX[f],
        }
    )

# (class, file, dòng, tên bảng, bằng chứng của tên bảng)
ENTITIES_RAW = [
    ("Case", "src/dispatch/case/models.py", 81, "case",
     'ForeignKey("case.id") xuất hiện 18 chỗ'),
    ("CaseNotes", "src/dispatch/case/models.py", 248, "case_notes",
     "suy từ resolve_table_name(); không có khoá ngoại nào trỏ tới"),
    ("CasePriority", "src/dispatch/case/priority/models.py", 13, "case_priority",
     'ForeignKey("case_priority.id")'),
    ("CaseSeverity", "src/dispatch/case/severity/models.py", 13, "case_severity",
     'ForeignKey("case_severity.id")'),
    ("CaseType", "src/dispatch/case/type/models.py", 21, "case_type",
     'ForeignKey("case_type.id")'),
    ("Incident", "src/dispatch/incident/models.py", 85, "incident",
     'ForeignKey("incident.id") xuất hiện 31 chỗ'),
    ("IncidentPriority", "src/dispatch/incident/priority/models.py", 14, "incident_priority",
     'ForeignKey("incident_priority.id")'),
    ("IncidentSeverity", "src/dispatch/incident/severity/models.py", 12, "incident_severity",
     'ForeignKey("incident_severity.id")'),
    ("IncidentType", "src/dispatch/incident/type/models.py", 24, "incident_type",
     'ForeignKey("incident_type.id")'),
]
entities = [
    {
        "class_name": c,
        "file": f,
        "line": line,
        "table_name": t,
        "table_name_source": "declared_attr trên Base (database/core.py:95) — sinh lúc chạy",
        "table_name_evidence": e,
    }
    for c, f, line, t, e in ENTITIES_RAW
]

# (file, dòng, thư viện, method, url trong code, trong try/except, ghi chú)
EXT_RAW = [
    ("src/dispatch/plugins/dispatch_atlassian_confluence/plugin.py", 135, "requests", "PUT",
     "{url}", True, 'requests.request("PUT", url, ...)'),
    ("src/dispatch/plugins/dispatch_core/plugin.py", 129, "requests", "GET",
     "{DISPATCH_AUTHENTICATION_PROVIDER_PKCE_JWKS}", False, ""),
    ("src/dispatch/plugins/dispatch_core/plugin.py", 188, "requests", "GET",
     "{url} — gán ở dòng trên: https://public-keys.auth.elb.{region}.amazonaws.com/{kid}", False, ""),
    ("src/dispatch/plugins/dispatch_github/plugin.py", 94, "requests", "GET",
     "{request_url}", False, ""),
    ("src/dispatch/plugins/dispatch_jira/plugin.py", 88, "requests", "GET",
     "{url}", False, 'requests.request("GET", ...) — method là tham số vị trí, không phải tên hàm'),
    ("src/dispatch/plugins/dispatch_jira/plugin.py", 98, "requests", "GET",
     "{url}", False, 'requests.request("GET", ...)'),
    ("src/dispatch/plugins/dispatch_microsoft_teams/conference/client.py", 66, "requests", "POST",
     "https://graph.microsoft.com/v1.0/users/{self.user_id}/onlineMeetings", False,
     "url truyền bằng keyword arg url=..., không phải tham số vị trí. "
     "ĐÍNH CHÍNH: bản đầu tôi ghi inside_try_except=True do đọc nhầm mức thụt đầu dòng; "
     "khối bao ngoài là if \"access_token\" in result, không phải try. Công cụ báo đúng."),
    ("src/dispatch/plugins/dispatch_opsgenie/service.py", 13, "requests", "GET",
     "{schedule_api}/{team_id}/on-calls", False, "schedule_api = https://api.opsgenie.com/v2/schedules"),
    ("src/dispatch/plugins/dispatch_opsgenie/service.py", 43, "requests", "POST",
     "https://api.opsgenie.com/v2/alerts", False, "chuỗi hằng đầy đủ"),
    ("src/dispatch/plugins/dispatch_zoom/client.py", 28, "requests", "GET",
     "{API_BASE_URI}/{path}", False, 'ghép bằng "{}/{}".format(), không phải f-string'),
    ("src/dispatch/plugins/dispatch_zoom/client.py", 36, "requests", "POST",
     "{API_BASE_URI}/{path}", False, ".format()"),
    ("src/dispatch/plugins/dispatch_zoom/client.py", 44, "requests", "DELETE",
     "{API_BASE_URI}/{path}", False, ".format()"),
    ("src/dispatch/plugins/generic_workflow/plugin.py", 95, "requests", "GET",
     "{api_url}", False, ""),
    ("src/dispatch/plugins/generic_workflow/plugin.py", 111, "requests", "POST",
     "{api_url}", False, ""),
]
ext = [
    {
        "file": f,
        "line": line,
        "library": lib,
        "http_method": m,
        "url_in_code": u,
        "inside_try_except": t,
        "note": n,
        "in_spec_scope": True,
    }
    for f, line, lib, m, u, t, n in EXT_RAW
]

# Có gọi ra ngoài thật nhưng không khớp dạng httpx./requests.<verb> mà SPEC liệt kê.
ext_borderline = [
    {
        "file": "src/dispatch/cli.py",
        "line": 1071,
        "library": "requests",
        "http_method": "POST",
        "url_in_code": "{api_endpoint}",
        "inside_try_except": True,
        "note": (
            "gọi qua đối tượng session tạo bởi requests.Session() ở cli.py:1055. "
            "SPEC mục 6c.3 liệt kê httpx.Client() nhưng không nói rõ requests.Session(). "
            "Ghi riêng, KHÔNG tính vào precision/recall."
        ),
        "in_spec_scope": False,
    }
]

# Chỗ dễ báo thừa: biến local trùng tên thư viện, chú thích kiểu, lớp exception.
fp_traps = [
    {
        "file": "src/dispatch/plugins/dispatch_google/docs/plugin.py",
        "line": 113,
        "why": "requests là biến local kiểu list (gán ở dòng 108). requests.append() KHÔNG phải lời gọi HTTP.",
    },
    {
        "file": "src/dispatch/plugins/dispatch_google/docs/plugin.py",
        "line": 148,
        "why": "cùng biến local đó.",
    },
    {
        "file": "src/dispatch/cli.py",
        "line": 1087,
        "why": "requests.exceptions.RequestException — lớp exception, không phải lời gọi.",
    },
    {
        "file": "src/dispatch/cli.py",
        "line": 1067,
        "why": "session: requests.Session — chú thích kiểu, không phải lời gọi.",
    },
]

gt = {
    "meta": {
        "repo": "Netflix/dispatch",
        "commit": COMMIT,
        "local_path": REPO,
        "ngay_lap": "2026-09-15",
        "nguoi_lap": (
            "Agent (Claude Opus 5) đọc tay source. KHÔNG phải hai kỹ sư đọc độc lập "
            "như SPEC mục 8.5.1 yêu cầu. Hạn chế ghi rõ ở EVALUATION.md mục 2."
        ),
        "quy_trinh": (
            "Lập ground truth TRƯỚC khi chạy công cụ và trước khi xem bất kỳ output nào "
            "của công cụ trên phạm vi này."
        ),
        "scope_dirs": ["src/dispatch/case/", "src/dispatch/incident/"],
        "so_file_trong_pham_vi": 48,
        "pham_vi_external_call": (
            "toàn bộ src/dispatch/ — case/ và incident/ không có lời gọi HTTP nào"
        ),
        "mount_prefix": MOUNT,
        "mount_note": (
            'main.py:268 có app.mount("/api/v1", app=api). URL thật có tiền tố này. '
            "So khớp sẽ báo cả hai cách: có và không có /api/v1."
        ),
    },
    "routes": routes,
    "entities": entities,
    "external_calls": ext,
    "external_calls_borderline": ext_borderline,
    "false_positive_traps": fp_traps,
    "ngoai_dinh_nghia_spec": {
        "assoc_tables": [
            {"var": "assoc_case_tags", "table": "assoc_case_tags",
             "file": "src/dispatch/case/models.py", "line": 63},
            {"var": "assoc_cases_incidents", "table": "assoc_case_incidents",
             "file": "src/dispatch/case/models.py", "line": 72,
             "note": "tên biến số nhiều nhưng tên bảng số ít"},
            {"var": "assoc_incident_terms", "table": "assoc_incident_terms",
             "file": "src/dispatch/incident/models.py", "line": 68},
            {"var": "assoc_incident_tags", "table": "assoc_incident_tags",
             "file": "src/dispatch/incident/models.py", "line": 76},
        ],
        "ly_do_khong_tinh": (
            "SPEC mục 6c.2 định nghĩa entity là 'class kế thừa Base'. Bảng liên kết tạo "
            "bằng Table(...) không phải class nên nằm ngoài phạm vi đó. Ghi lại để người "
            "đọc biết chúng tồn tại."
        ),
    },
    "thong_ke": {
        "routes": len(routes),
        "entities": len(entities),
        "external_calls": len(ext),
        "external_calls_borderline": len(ext_borderline),
    },
}

out = pathlib.Path("evaluation/ground_truth.json")
out.write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")
print("Da ghi", out, gt["thong_ke"])
