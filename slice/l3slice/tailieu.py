"""TAI-LIEU.md: the one file a person reads (user's choice A, 11/10/2026).

Built from the same facts as README.md and the contract files, so nothing here can disagree with them. Plain
Vietnamese, no fact/evidence IDs, no machine block: those stay in result.json and the files of the appendix.
"""
from __future__ import annotations

import json
import re

from .common import is_known
from .docfacts import RULES
from .render import EXACT_STATUS_RULES, _model_label, _models_cell, _route_sort_key, _type_text, code, md

LIMITS_SECTION = 11
# column-level ORM defaults: shown as * on the value itself, not as a note on the table
COLUMN_DEFAULTS = {"không khai primary_key thì là False",
                   "nullable mặc định là not primary_key; với Mapped/SQLModel theo Optional",
                   "kiểu SQL ánh xạ từ kiểu SQLAlchemy theo dialect"}
LIMIT_TITLES = {
    "DIAGRAM_NOT_PROVIDED": "Chưa có sơ đồ component",
    "ARCHITECTURE_NOT_EVALUATED": "Chưa đối chiếu với dữ liệu kiến trúc",
    "ROUTE_NOT_DECORATOR": "Route đăng ký không qua decorator, không có trong tài liệu",
    "HTTP_LIBRARY_UNSUPPORTED": "Lời gọi HTTP qua thư viện chưa hỗ trợ",
    "ANALYSIS_PARTIAL": "Phân tích chưa xong",
    "SOURCE_NOT_FULLY_READ": "Có phần source chưa đọc",
    "OUT_OF_SCOPE_FILES": "File ngoài phạm vi đọc",
    "CLAIMS_REJECTED": "Có đề xuất của model bị bộ kiểm từ chối",
    "MEMBERSHIP_KIND_DERIVED": "Loại component được suy từ phạm vi đọc",
    "MEMBERSHIP_KIND_SUSPECT": "Loại component đáng ngờ",
    "QUEUE_LIBRARY_UNSUPPORTED": "Thư viện hàng đợi chưa hỗ trợ, chưa đọc bên gửi/nhận",
    "TABLES_IN_MIGRATIONS_NOT_READ": "Bảng khai trong migration chưa được đọc",
    "VALUE_REDACTED": "Giá trị có dấu hiệu bí mật đã được che",
    "MANIFEST_INVALID": "File khai thư viện không đọc được",
    "PARSE_FAILED": "File lỗi cú pháp, không đọc được",
    "STATIC_READ_FAILED": "Phần đọc tĩnh bị lỗi",
    "TABLES_NOT_READ": "Có bảng chưa đọc được",
}
LEGEND = ("Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của "
          "framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model "
          "viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.")


def _plain(reason: str) -> str:
    """A run reason without its machine code: "REPAIR_ROUNDS: còn lỗi" -> "còn lỗi"."""
    return re.sub(r"^[A-Z_]+: ", "", reason or "")


def _yes(field) -> str:
    if is_known(field):
        return "có" if field["value"] else "không"
    if isinstance(field, dict) and field.get("state") == "not_applicable":
        return "không"
    return "chưa rõ"


def _text(field, empty="—") -> str:
    if is_known(field):
        v = field["value"]
        return md(", ".join(map(str, v)) if isinstance(v, list) else v) if v not in ([], "", None) else empty
    if isinstance(field, dict) and field.get("state") == "not_applicable":
        return "—"
    if isinstance(field, dict) and field.get("state") == "redacted":
        return "đã che (dấu hiệu bí mật)"
    return "chưa rõ" + (f" ({md(field['reason'])})" if isinstance(field, dict) and field.get("reason") else "")


def _reasons(fact) -> list[str]:
    """Why a fact is inferred, without rule names. A rule text may itself contain "; ", so the known rules are cut
    out whole first; what is left is split on "; "."""
    text, out = fact.get("confidence_reason") or "", []
    for r in sorted(RULES, key=lambda k: text.find(f"{k}: {RULES[k]}")):
        if f"{r}: {RULES[r]}" in text:
            out.append(RULES[r])
            text = text.replace(f"{r}: {RULES[r]}", "")
    for part in re.split(r"; (?=[a-z][\w.-]*-v\d+: )", text):  # cut only where the next rule name starts
        head, _, tail = part.strip().partition(": ")
        if part.strip():
            out.append(tail if re.fullmatch(r"[\w.-]+", head) and tail else part.strip())
    return out


def _where(ev) -> str:
    return code(f"{ev['path']}:{ev['start_line']}") if ev else "—"


def _declared(f):
    decl = f["attributes"].get("declaration_evidence_id")
    return next((e for e in f["evidence"] if is_known(decl) and e["id"] == decl["value"]),
                f["evidence"][0] if f["evidence"] else None)


def _request(a, facts) -> str:
    if is_known(a.get("request_inline")):
        inline = a["request_inline"]["value"]
        return md(f"{inline['media_type']}: " + ", ".join(f["name"] for f in inline["fields"]))
    if is_known(a.get("request_type")):
        return md(_type_text(a["request_type"]["value"]["schema"], facts))
    text = _models_cell(a.get("request_model_ids"), facts)
    return "—" if text == "(không có)" else text


def _response(a, facts) -> str:
    if is_known(a.get("response_type")):
        return md(_type_text(a["response_type"]["value"]["schema"], facts))
    text = _models_cell(a.get("response_model_ids"), facts, a.get("bodies"))
    return "—" if text == "(không có)" else text


def _status_note(a) -> str:
    rule = a.get("status_rule")
    if not is_known(rule) or rule["value"] in EXACT_STATUS_RULES:
        return "khai trong code"
    return "mặc định của framework, xem chú thích"


def _errors(a) -> list[dict]:
    return a["errors"]["value"] if is_known(a.get("errors")) else []


def _status_codes(a) -> str:
    """Declared codes, then each error code once, marked * (inferred from a raise)."""
    codes = [str(c) for c in (a["status_codes"]["value"] if is_known(a.get("status_codes")) else [])]
    for e in _errors(a):
        if str(e["status"]) not in codes and f"{e['status']}*" not in codes:
            codes.append(f"{e['status']}*")
    return ", ".join(codes) or "chưa rõ"


def _fk_text(field) -> str:
    """A foreign key as table.column."""
    if is_known(field) and isinstance(field["value"], dict):
        v = field["value"]
        return md(f"{v.get('table', '?')}.{v.get('column', '?')}")
    return _text(field)


def _declared_by(a, long=False) -> str:
    """How a table is declared: by a model class, or by `var = Table(...)`."""
    if is_known(a.get("class_name")):
        return f"Lớp {code(a['class_name']['value'])}, khai ở" if long else md(a["class_name"]["value"])
    if is_known(a.get("variable_name")):
        text = code(a["variable_name"]["value"] + " = Table(...)")
        return f"Khai bằng {text} ở" if long else text
    return "Khai ở" if long else "chưa rõ"


def _constraints(col) -> str:
    """unique / index written in code, and what a foreign key does on delete."""
    out = list(col["constraints"]["value"]) if is_known(col.get("constraints")) else []
    fk = col.get("foreign_key")
    if is_known(fk) and isinstance(fk["value"], dict) and fk["value"].get("ondelete"):
        out.append(f"xóa theo: {fk['value']['ondelete']}")
    return md(", ".join(out)) or "—"


def _column_type(field) -> str:
    """A column type; when the SQL dialect is unknown, the type as written in code."""
    if not is_known(field) and isinstance(field, dict):
        m = re.search(r"khai trong code: (.+)$", field.get("reason", ""))
        if m:
            return f"{md(m.group(1))} (chưa quy ra kiểu SQL)"
    return _text(field)


class _Notes:
    """Numbered reasons, each written once at the end of a section."""

    def __init__(self):
        self.items = []

    def ref(self, fact) -> str:
        if fact["confidence"] == "exact":
            return "chắc chắn"
        marks = []
        for r in _reasons(fact):
            if r not in self.items:
                self.items.append(r)
            marks.append(f"[{self.items.index(r) + 1}]")
        return "suy luận " + "".join(marks)

    def lines(self) -> list[str]:
        return (["Chú thích:", ""] + [f"[{i}] {md(r)}" + "  " for i, r in enumerate(self.items, 1)] + [""]) if self.items else []


def tai_lieu(repository_name, agent, coverage, components, facts, limitations, contract_files, unconfirmed=(),
             other_files=(), app_globals=(), provenance=None, route_chains=None, relations=()) -> str:
    """`unconfirmed`: Claims.suspects(); `other_files`: [(TBL|EVT, path, component, error)]; `app_globals`:
    docstatic.app_globals(); `route_chains`: route fact id -> [{"steps": [...], "tables": [...]}]."""
    by_id = {f["id"]: f for f in facts}
    of = {k: [f for f in facts if f["kind"] == k] for k in ("route", "model", "http_call", "file_role", "table", "event",
                                                              "library", "config")}
    routes = sorted(of["route"], key=_route_sort_key)
    models = sorted(of["model"], key=lambda f: _model_label(f, by_id))
    roles = {f["attributes"]["file"]["value"]: f for f in of["file_role"]}
    file_owner = {p: c for c in components for p in c["files"]}
    files = coverage["files"]
    done = sum(1 for f in files if f["status"] in ("processed", "empty") and not f["cut_lines"])
    ok = agent.status == "completed" and coverage["complete"]
    prov = provenance or {}
    unread_bus = any(x["code"] == "QUEUE_LIBRARY_UNSUPPORTED" for x in limitations)
    unread_tables = any(x["code"] == "TABLES_NOT_READ" for x in limitations)
    lines = [f"# {md(repository_name)} — tài liệu API", "",
             "Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ "
             "cho máy nằm ở `result.json` và các file ở phụ lục.", "",
             "| Mục | Giá trị |", "|---|---|",
             "| Tình trạng | " + ("Đủ" if ok else f"Chưa đủ — {md(_plain(agent.reason) or agent.status)}, xem mục "
                                 f"{LIMITS_SECTION}") + " |",
             f"| Đọc source | {done}/{len(files)} file trong phạm vi |",
             f"| Endpoint | {len(routes)} |", f"| Model | {len(models)} |", f"| Bảng CSDL | {len(of['table'])}"
             + (f"; có bảng chưa đọc được, xem mục {LIMITS_SECTION}" if unread_tables else "") + " |",
             f"| Sự kiện, tác vụ nền | {len(of['event'])} điểm gửi/nhận"
             + (f"; có kênh chưa đọc được, xem mục {LIMITS_SECTION}" if unread_bus else "") + " |", f"| Gọi HTTP ra ngoài | {len(of['http_call'])} |",
             f"| Sinh bởi | model {md(prov.get('model', '?'))}, prompt {md(prov.get('prompt_version', '?'))}; bảng, sự kiện, "
             "thư viện, cấu hình, middleware đọc tĩnh từ code |", "", LEGEND, ""]

    # 1-3: API
    lines += ["## 1. Danh sách endpoint", ""]
    if routes:
        lines += ["| # | Method | Path | Vào | Ra | Status | Auth |", "|---|---|---|---|---|---|---|"]
        for i, f in enumerate(routes, 1):
            a = f["attributes"]
            lines.append(f"| {i} | {_text(a.get('method'))} | {_text(a.get('path'))} | {_request(a, by_id)} | "
                         f"{_response(a, by_id)} | {_status_codes(a)} | "
                         f"{_text(a['auth']) if is_known(a.get('auth')) else 'chưa rõ'} |")
        if any(_errors(f["attributes"]) for f in routes):
            lines += ["", "\\* mã lỗi suy từ chỗ ném lỗi trong code, xem mục 2."]
    else:
        lines.append("Không có endpoint nào được xác nhận.")

    lines += ["", "## 2. Chi tiết từng endpoint", ""]
    notes = _Notes()
    for i, f in enumerate(routes, 1):
        a = f["attributes"]
        decl = _declared(f)
        handler = a["handler"]["value"].rsplit("::", 1)[-1] if is_known(a.get("handler")) else "?"
        lines += [f"### {i}. {_text(a.get('method'))} {_text(a.get('path'))}", ""]
        if is_known(a.get("summary")):
            lines += [f"- Mô tả (AI viết): {md(a['summary']['value'])}"]
        lines += [f"- Hàm xử lý: {code(handler)} tại {_where(decl)}"]
        params = a.get("parameters")
        if is_known(params) and params["value"]:
            lines += ["- Tham số:", "", "  | Tên | Ở đâu | Kiểu | Bắt buộc |", "  |---|---|---|---|"]
            lines += [f"  | {md(p['name']['value'])} | {_text(p.get('in'))} | "
                      f"{md(_type_text(p['schema']['value'], by_id)) if is_known(p.get('schema')) else 'chưa rõ'} | "
                      f"{_yes(p.get('required'))} |" for p in params["value"]]
            lines.append("")
        else:
            lines.append("- Tham số: " + ("không có" if is_known(params) else _text(params)))
        req = _request(a, by_id)
        if req != "—":
            lines.append(f"- Body: {req}")
        lines += [f"- Trả về: {_response(a, by_id)}",
                  f"- Status: {_text(a.get('status_codes'))} ({_status_note(a)})"]
        for e in _errors(a):
            lines.append(f"- Lỗi có thể trả về: {e['status']} — {md(e['exception'])}, ném ở {code(e['raised_at'])}"
                         + (f", mã khai ở {code(e['status_at'])}" if e.get("status_at") else ""))
        lines += [f"- Dependency: {_text(a.get('dependencies'), 'không có')}",
                  "- Auth: " + (_text(a["auth"]) if is_known(a.get("auth")) else
                                "chưa rõ" + (f" — {md(a['auth']['reason'])}" if a.get("auth") else ""))]
        if is_known(a.get("tags")):
            lines.append(f"- Nhóm (tags): {_text(a['tags'])}")
        if is_known(a.get("deprecated")) and a["deprecated"]["value"]:
            lines.append("- Đã đánh dấu ngừng dùng (deprecated)")
        for x in (a["examples"]["value"] if is_known(a.get("examples")) else []):
            text = json.dumps(x, ensure_ascii=False, default=str)
            lines.append(f"- Ví dụ (từ code): {code(text if len(text) <= 200 else text[:200] + ' …')}")
        for chain in (route_chains or {}).get(f["id"], []):
            lines.append("- Đường gọi tới dữ liệu (suy luận từ vai trò Service): "
                         + " → ".join(code(s) for s in chain["steps"])
                         + (f"; bảng nhắc tới: {', '.join(code(t) for t in chain['tables'])}" if chain["tables"] else ""))
        lines.append(f"- Mức chắc chắn: {notes.ref(f)}")
        if f["completeness"] != "full":
            lines.append(f"- Còn thiếu: {md(f.get('completeness_reason', ''))}")
        lines.append("")
    lines += notes.lines()

    lines += ["## 3. Model dữ liệu", ""]
    notes = _Notes()
    for f in models:
        a = f["attributes"]
        ev = f["evidence"][0] if f["evidence"] else None
        lines += [f"### {md(_model_label(f, by_id))}", "", f"Khai ở {_where(ev)}. Mức chắc chắn: {notes.ref(f)}.", ""]
        if not is_known(a.get("fields")):
            lines += [f"Trường chỉ biết lúc chạy: {md(a['fields']['reason'])}", ""]
            continue
        lines += ["| Trường | Kiểu | Bắt buộc | Được null |", "|---|---|---|---|"]
        for x in a["fields"]["value"]:
            name = md(x["name"]["value"]) + (f" (tên JSON: {md(x['alias']['value'])})" if is_known(x.get("alias")) else "")
            kind = md(_type_text(x["type"]["value"], by_id)) if is_known(x.get("type")) else "chưa rõ"
            lines.append(f"| {name} | {kind} | {_yes(x.get('required'))} | {_yes(x.get('nullable'))} |")
        lines.append("")
    if not models:
        lines += ["Không có model nào.", ""]
    lines += notes.lines()

    # 4-5: data and events (read statically)
    lines += ["## 4. Bảng CSDL", ""]
    notes = _Notes()
    tables = sorted(of["table"], key=lambda f: _text(f["attributes"].get("name")))
    dialects = {_text(f["attributes"].get("dialect")) for f in tables}
    none_known = bool(tables) and not any(is_known(f["attributes"].get("dialect")) for f in tables)
    one_dialect = len(dialects) == 1 or none_known
    if tables and one_dialect:  # said once, not on every table
        reasons = sorted({f["attributes"]["dialect"].get("reason", "") for f in tables} - {""}) if none_known else []
        lines += [(f"SQL dialect: chưa rõ ({md('; '.join(reasons))})." if none_known else f"SQL dialect: {next(iter(dialects))}.")
                  + (" Kiểu cột ghi như khai trong code, chưa quy ra kiểu SQL." if none_known else ""), ""]
    owners = {(file_owner.get((_declared(f) or {}).get("path", "")) or {}).get("name") for f in tables}
    one_owner = len(owners) == 1 and None not in owners
    if tables:  # overview first: what tables exist, where, and how they point at each other
        lines += (["Mọi bảng thuộc component " + md(next(iter(owners))) + ".", ""] if one_owner else []) + [
            "Dấu \\* sau một giá trị: code không khai, giá trị lấy theo mặc định có tài liệu của ORM.", "",
            "| Bảng | Lớp model |" + ("" if one_owner else " Component |") + " Số cột | Khóa ngoại tới |",
            "|---|---|" + ("" if one_owner else "---|") + "---|---|"]
        for f in tables:
            a = f["attributes"]
            cols = a["columns"]["value"] if is_known(a.get("columns")) else []
            owner = file_owner.get((_declared(f) or {}).get("path", ""))
            targets = sorted({c["foreign_key"]["value"]["table"] for c in cols if is_known(c.get("foreign_key"))
                              and isinstance(c["foreign_key"]["value"], dict)})
            lines.append(f"| {_text(a.get('name'))} | {_declared_by(a)} | "
                         + ("" if one_owner else f"{md(owner['name']) if owner else '—'} | ")
                         + f"{len(cols)} | {md(', '.join(targets)) or '—'} |")
        lines.append("")
    for f in tables:
        a = f["attributes"]
        owner = file_owner.get((_declared(f) or {}).get("path", ""))
        table_rules = [r for r in _reasons(f) if r not in COLUMN_DEFAULTS]  # column defaults are the * in the cells
        lines += [f"### {_text(a.get('name'))}", "",
                  f"{_declared_by(a, long=True)} "
                  f"{_where(_declared(f))}" + ("" if one_owner or not owner else f", component {md(owner['name'])}")
                  + ("" if one_dialect else f". SQL dialect: {_text(a.get('dialect'))}")
                  + (f". Suy luận: {md('; '.join(table_rules))}" if table_rules else "") + ".", ""]
        pks = [c["name"]["value"] for c in (a["columns"]["value"] if is_known(a.get("columns")) else [])
               if is_known(c.get("primary_key")) and c["primary_key"]["value"]]
        if len(pks) > 1:  # several columns marked primary key make one key (association tables)
            lines += [f"Khóa chính ghép: {md(', '.join(pks))}.", ""]
        if is_known(a.get("table_constraints")):
            lines += [f"Ràng buộc bảng: {md('; '.join(a['table_constraints']['value']))}.", ""]
        lines += ["| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |", "|---|---|---|---|---|---|"]
        for col in (a["columns"]["value"] if is_known(a.get("columns")) else []):
            guessed = set(col["inferred_fields"]["value"]) if is_known(col.get("inferred_fields")) else set()
            kind = _column_type(col.get("type"))
            if one_dialect and kind.endswith(" (chưa quy ra kiểu SQL)"):
                kind = kind[:-len(" (chưa quy ra kiểu SQL)")]
            star = {k: ("\\*" if k in guessed else "") for k in ("type", "primary_key", "nullable")}
            lines.append(f"| {_text(col.get('name'))} | {kind}{star['type']} | {_yes(col.get('primary_key'))}{star['primary_key']} | "
                         f"{_fk_text(col.get('foreign_key'))} | {_yes(col.get('nullable'))}{star['nullable']} | "
                         f"{_constraints(col)} |")
        lines.append("")
    if not of["table"]:
        lines += ["Không thấy bảng nào khai bằng SQLAlchemy/SQLModel trong phạm vi đọc."
                  + (f" Có bảng khai theo cách chưa đọc được, xem mục {LIMITS_SECTION}." if unread_tables else ""), ""]
    lines += notes.lines()

    lines += ["## 5. Sự kiện và tác vụ nền", ""]
    if of["event"]:
        lines += ["| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |", "|---|---|---|---|---|"]
        for f in sorted(of["event"], key=lambda f: (_text(f["attributes"].get("topic")), _where(_declared(f)))):
            a = f["attributes"]
            role = {"publish": "gửi", "consume": "nhận"}.get(a["action"]["value"], "?") if is_known(a.get("action")) else "?"
            owner = file_owner.get((_declared(f) or {}).get("path", ""))
            lines.append(f"| {role} | {_text(a.get('topic'))} | {_text(a.get('broker'))} | "
                         f"{md(owner['name']) if owner else '—'} | {_where(_declared(f))} |")
        lines += ["", "Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng "
                  "component ghi bên liên quan.", ""]
    else:
        lines += ["Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks."
                  + (f" Có kênh sự kiện chưa đọc được, xem mục {LIMITS_SECTION}." if unread_bus else ""), ""]

    # 6: structure
    lines += ["## 6. Cấu trúc code", "",
              "Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.", ""]
    empty = {f["path"] for f in files if f["status"] == "empty"}
    readable = {f["path"] for f in files}
    for c in components:
        if c["kind"] != "normal":
            continue
        lines += [f"### {md(c['name'])}", ""]
        own = [p for p in c["files"] if p in roles]
        if own:
            lines += ["| File | Vai trò | Dấu hiệu |", "|---|---|---|"]
            for p in own:
                a = roles[p]["attributes"]
                if a["role"]["value"] == "Service":
                    sign = "đường gọi " + " → ".join(code(x) for x in a["call_path"]["value"])
                else:
                    sign = _where(roles[p]["evidence"][0] if roles[p]["evidence"] else None)
                lines.append(f"| {code(p)} | {md(a['role']['value'])} | {sign} |")
            lines.append("")
        unknown = [p for p in c["files"] if p not in roles and p in readable and p not in empty and p.endswith(".py")]
        rest = [f"{sum(1 for p in c['files'] if p in empty)} file rỗng"] if any(p in empty for p in c["files"]) else []
        if unknown:
            rest.append("chưa xác định vai trò: " + ", ".join(code(p) for p in unknown))
        if rest:
            lines += ["Không có vai trò: " + "; ".join(rest) + ".", ""]

    if relations:
        lines += ["### Quan hệ giữa component", "",
                  "Đọc tĩnh từ lời gọi, Depends và chỗ dùng bảng đã nối được tới nơi định nghĩa.", "",
                  "| Từ | Tới | Cách dùng | Số chỗ | Ví dụ |", "|---|---|---|---|---|"]
        kinds = {"calls": "gọi hàm", "depends": "Depends", "reads": "dùng bảng"}
        lines += [f"| {md(r['from'])} | {md(r['to'])} | {', '.join(kinds.get(k, k) for k in r['kinds'])} | {r['count']} | "
                  f"{code(r['example'])} |" for r in relations]
        lines.append("")

    # 7-10: outside world and globals
    lines += ["## 7. Gọi HTTP ra ngoài", ""]
    if of["http_call"]:
        lines += ["| Thư viện | Method | Đích | Ở đâu |", "|---|---|---|---|"]
        for f in of["http_call"]:
            a, ev = f["attributes"], f["evidence"][0]
            if is_known(a.get("url")):
                target = md(a["url"]["value"])
            elif is_known(a.get("url_config_key")):
                target = "khóa cấu hình " + code(a["url_config_key"]["value"])
            else:
                target = _text(a.get("url"))
            lines.append(f"| {_text(a.get('library'))} | {_text(a.get('method'))} | {target} | {_where(ev)} |")
    else:
        lines.append("Không có lời gọi nào qua httpx, requests, aiohttp.")

    lines += ["", "## 8. Thư viện", ""]
    if of["library"]:
        lines += ["| Thư viện | Phiên bản | Có import trong code | Khai ở |", "|---|---|---|---|"]
        libs = {}  # one row per package and version, every manifest that declares it
        for f in sorted(of["library"], key=lambda f: _text(f["attributes"].get("name"))):
            a = f["attributes"]
            version = _text(a["version"]) if is_known(a.get("version")) else "—"
            row = libs.setdefault((_text(a.get("name")), version), {"used": False, "at": []})
            row["used"] = row["used"] or (is_known(a.get("used")) and a["used"]["value"])
            row["at"].append(_where(_declared(f)))
        lines += [f"| {name} | {version} | {'có' if r['used'] else 'chưa thấy import'} | {', '.join(r['at'])} |"
                  for (name, version), r in libs.items()]
        lines += ["", "\"Chưa thấy import\": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).", ""]
    else:
        lines += ["Không có `pyproject.toml` hay `requirements*.txt` trong phạm vi đọc.", ""]

    lines += ["## 9. Cấu hình", ""]
    if of["config"]:
        lines += ["| Khóa | Nguồn | Giá trị mặc định | Khai ở |", "|---|---|---|---|"]
        rows = {}  # one row per key, source and value; every place it is read is listed
        for f in sorted(of["config"], key=lambda f: (_text(f["attributes"].get("key")), _declared(f)["path"],
                                                     _declared(f)["start_line"])):
            a = f["attributes"]
            source = {"settings": "lớp Settings", "env": "biến môi trường"}.get(
                a["source_kind"]["value"], md(a["source_kind"]["value"])) if is_known(a.get("source_kind")) else "?"
            rows.setdefault((_text(a.get("key")), source, _text(a.get("value"))), []).append(_where(_declared(f)))
        lines += [f"| {key} | {source} | {value} | {', '.join(places)} |" for (key, source, value), places in rows.items()]
        lines.append("")
    else:
        lines += ["Không thấy lớp Settings hay biến môi trường.", ""]

    lines += ["## 10. Middleware và xử lý lỗi toàn cục", ""]
    if app_globals:
        lines += ["| Loại | Tên | Ở đâu |", "|---|---|---|"]
        lines += [f"| {'middleware' if g['kind'] == 'middleware' else 'xử lý lỗi'} | {code(g['name'])} | {code(g['at'])} |"
                  for g in app_globals]
        lines += ["", "Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin "
                  "đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.", ""]
    else:
        lines += ["Không thấy middleware hay hàm xử lý lỗi đăng ký trên app.", ""]

    lines += [f"## {LIMITS_SECTION}. Chưa biết và giới hạn", ""]
    lines += [f"- **{LIMIT_TITLES.get(x['code'], x['code'])}.** {md(_plain(x['message']))}" for x in limitations] \
        or ["Không có."]
    if unconfirmed:  # a route or call no item accounts for: the reader must know it may be missing
        lines.append("- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** "
                     + ", ".join(code(x["at"]) for x in unconfirmed))

    lines += ["", "## Phụ lục: file cho máy", ""]
    entries = [("API (OpenAPI)", p, c, err) for p, c, err in contract_files] + \
        [("TBL (DDL)" if k == "TBL" else "EVT", p, c, err) for k, p, c, err in other_files]
    lines += [f"- {k}: [{p}]({p}) — component {md(c['name'])}" if not err else
              f"- {k}: {p} — component {md(c['name'])} — chưa xuất được: {md(err)}" for k, p, c, err in entries] \
        or ["Không có file contract."]
    return "\n".join(lines) + "\n"
