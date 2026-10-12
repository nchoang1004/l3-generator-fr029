"""FR-029 N1 + N4: what the agent submits, how code checks it, and how checked items become API-004 facts.

The agent never mints IDs or evidence objects. It cites `path:line` or `path:start-end`; code checks that the
lines exist, were sent to the model, and hold what the claim depends on (literal, decorator, call shape, signal).
These checks catch invented or misplaced evidence. They cannot prove meaning (a wrong type next to the right line);
that is measured against the independent gold (N4, check 3).
A failed check goes back to the agent per field; an item that never passes is not kept.
"""
from __future__ import annotations

import ast
import io
import re
import tokenize
from collections import Counter

from . import astscan
from .common import compact, has_secret, is_known, known, sha, unknown
from .source_tools import MAX_LINE_CHARS, mask_text

METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"}
PARAM_PLACES = {"path", "query", "header", "cookie"}
BASE_TYPES = {"integer": {"type": "integer"}, "number": {"type": "number"}, "string": {"type": "string"},
              "binary": {"type": "string", "format": "binary"}, "uuid": {"type": "string", "format": "uuid"},
              "datetime": {"type": "string", "format": "date-time"}, "date": {"type": "string", "format": "date"},
              "email": {"type": "string", "format": "email"},
              "boolean": {"type": "boolean"}, "object": {"type": "object"}, "any": {}}
ROLES = ["Điểm vào", "Route", "Model bảng", "Hạ tầng", "Truy cập dữ liệu", "Schema API", "Cấu hình", "Service", "Khác"]
HTTP_LIBS = {"httpx", "requests", "aiohttp"}
LIMIT_KINDS = {"add_api_route": "ROUTE_NOT_DECORATOR", "add_route": "ROUTE_NOT_DECORATOR",
               "add_websocket_route": "ROUTE_NOT_DECORATOR", "unsupported_http_library": "HTTP_LIBRARY_UNSUPPORTED"}
FORM_MEDIA = ("multipart/form-data", "application/x-www-form-urlencoded")
MODEL_ID = re.compile(r"[^:\s]+\.py::[A-Za-z_]\w*")

# A03: the only names an `inferred` value may cite. Each is a documented framework default, not a guess.
RULES = {
    "fastapi.default_status_200": "Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse",
    "fastapi.response_class_default_status": "Không khai status_code nhưng có response_class (ở decorator, hoặc "
                                             "default_response_class của app/router); status là mặc định của lớp đó",
    "fastapi.header_underscore_to_hyphen": "Tham số Header: FastAPI đổi dấu _ trong tên biến thành - trong tên header",
    "fastapi.status_constant": "status_code là hằng status.HTTP_<mã>_…; mã lấy từ tên hằng (giá trị khai rõ, nhãn exact)",
    "fastapi.return_annotation_response_model": "Không khai response_model; FastAPI dùng kiểu trả về của handler",
    "fastapi.json_body_media": "Body là Pydantic model; FastAPI nhận application/json",
    "fastapi.scalar_param_query": "Tham số kiểu đơn, không có trong path, không khai Query/Header/Cookie; FastAPI coi là query",
    "fastapi.model_param_body": "Tham số kiểu Pydantic model không khai Body; FastAPI coi là body",
    "fastapi.multiple_body_embed": "Có từ hai tham số body; FastAPI bọc body theo tên tham số",
    "settings.default_prefix": "Prefix là giá trị mặc định khai trong lớp Settings; biến môi trường có thể ghi đè lúc chạy",
    "pydantic.v2_required_no_default": "Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None",
    "pydantic.v1_optional_not_required": "Pydantic v1: trường Optional không có default được mặc định None, nên không bắt buộc",
}
# Signals a role claim must show on its cited line. Roles not listed here depend on meaning and are checked by gold.
ROLE_SIGNALS = {
    "Điểm vào": re.compile(r"FastAPI\s*\(|uvicorn\.run\s*\(|__name__\s*==\s*['\"]__main__['\"]|@\s*[\w.]*(command|group)\b|Typer\s*\("),
    "Route": re.compile(r"@\s*[\w.]+\.(get|post|put|patch|delete|head|options|trace|api_route|websocket)\s*\("),
    "Model bảng": re.compile(r"__tablename__|table\s*=\s*True|\bTable\s*\("),
    "Cấu hình": re.compile(r"BaseSettings|os\.environ|os\.getenv"),
    # a class, or a model made at run time (X = pydantic_model_creator(Y), X = create_model(...))
    "Schema API": re.compile(r"^\s*class\s+\w+\s*\(|^\s*\w+\s*=\s*[\w.]*(pydantic_model_creator|pydantic_queryset_creator|create_model)\s*\("),
}
# Roles whose regex signal is reliable enough to enforce the FR-029 order: a file that shows one of these must not
# get a later role unless the agent says why the match is not that signal (`not_signal`).
ORDER_SIGNALS = ["Điểm vào", "Route", "Model bảng"]
PART_CALLS = {"include_prefix": ("include_router",), "router_prefix": ("APIRouter",), "mount_prefix": ("mount",)}
PART_SIGNALS = {"include_prefix": re.compile(r"include_router\s*\("), "router_prefix": re.compile(r"APIRouter\s*\("),
                "mount_prefix": re.compile(r"\.mount\s*\("), "settings_default": re.compile(r"^\s*\w+\s*(:[^=]*)?="),
                "decorator": re.compile(r"@")}
SUSPECTS = {  # lines every run must account for: a claim at that line, or a dismissal with a reason
    "route": re.compile(r"^\s*@\s*[\w.]+\.(get|post|put|patch|delete|head|options|trace|api_route|websocket)\s*\("),
    "registration": re.compile(r"\.(add_api_route|add_route|add_websocket_route)\s*\("),
    "http": re.compile(r"\.(get|post|put|patch|delete|head|options|request|stream|send)\s*\("),
    "other_http": re.compile(r"\burlopen\s*\(|\burllib3\b.*\.request\s*\(|\bHTTPS?Connection\s*\("),
}
LOC = re.compile(r"^(?P<path>[^:]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")
STRING = re.compile(r"(?<![\w])[rRuU]?(\"(?:[^\"\\\n]|\\.)*\"|'(?:[^'\\\n]|\\.)*')")
# a line that can prove an auth mechanism: a dependency or a fastapi.security scheme (code only, strings removed)
AUTH_SIGNAL = re.compile(r"\b(?:Depends|Security)\s*\(|\b(?:OAuth2\w*|HTTPBearer|HTTPBasic\w*|HTTPDigest|"
                         r"APIKey(?:Header|Query|Cookie)|SecurityScopes|HTTPAuthorizationCredentials)\b")
IMPORT_LINE = re.compile(r"^\s*(import|from)\s")


def _unknown(v) -> bool:
    return isinstance(v, dict) and isinstance(v.get("unknown"), str) and bool(v["unknown"])


class Claims:
    """The agent's accepted items, keyed so that a resubmission replaces the earlier version."""

    def __init__(self, tools):
        self.tools = tools
        self.routes, self.models, self.http, self.roles, self.limits, self.dismissed = {}, {}, {}, {}, {}, {}
        self.rejected: list[dict] = []
        self._defs = None  # function name -> [(path, ast node)], built on first use
        self._trees = {}  # path -> parsed module, filled with _defs
        self._classes = {}  # class name -> [(path, ast node)], filled with _defs
        self._scans, self._clients = {}, {}  # per file: HTTP client names; module-level clients
        self._module_index = None  # module name -> readable file
        self._edges = None  # include_router/mount graph, built on first use
        self._edges_open = False  # some registration could not be resolved: never conclude "not registered"
        self._states = None  # attributes holding a client on an app state
        self._bindings = {}  # per file: name -> values assigned to it, for _is_app
        self._aliases = None  # Annotated alias name -> [(file, [(dependency, called)])]
        self._marker_aliases = {}  # Annotated alias name -> [(file, [Header(...)/Query(...) calls])], with _aliases

    # ---------------------------------------------------------------- helpers

    def loc(self, value, field: str, errors: list) -> tuple[str, int, int] | None:
        if not isinstance(value, str) or not (m := LOC.match(value)):
            errors.append(f"{field}: cần dạng 'path:dòng' hoặc 'path:đầu-cuối', nhận {value!r}")
            return None
        path, start = m["path"], int(m["start"])
        end = int(m["end"]) if m["end"] else start
        lines = self.tools.lines.get(path)
        if lines is None or path not in self.tools.state:
            errors.append(f"{field}: {path} không thuộc phạm vi đọc")
            return None
        if not 1 <= start <= end <= len(lines) or end - start > 60:
            errors.append(f"{field}: dòng {start}-{end} ngoài file ({len(lines)} dòng) hoặc dài quá 60 dòng")
            return None
        if not self.tools.was_delivered(path, start, end):
            errors.append(f"{field}: dòng {start}-{end} của {path} chưa được đọc qua read_file")
            return None
        return path, start, end

    def text(self, where) -> str:
        """The cited lines as delivered: a line cut for length keeps only the part the model was sent."""
        path, start, end = where
        cut = self.tools.cut.get(path, ())
        return "\n".join(line[:MAX_LINE_CHARS] if i in cut else line
                         for i, line in enumerate(self.tools.lines[path][start - 1:end], start))

    def _hidden(self, where, value) -> bool:
        """`value` is in the cited lines only after the cut: the model was never sent it."""
        path, start, end = where
        if not isinstance(value, str) or not value or not any(i in self.tools.cut.get(path, ()) for i in range(start, end + 1)):
            return False
        full = "\n".join(self.tools.lines[path][start - 1:end])
        return value in full and value not in self.text(where) and value not in self.shown(where)

    def shown(self, where) -> str:
        path, start, end = where
        cut = self.tools.cut.get(path, ())
        return "\n".join(line[:MAX_LINE_CHARS] if i in cut else line
                         for i, line in enumerate(self.tools.shown[path][start - 1:end], start))

    def literals(self, text: str) -> list[str]:
        out = []
        for m in STRING.finditer(text):
            try:
                v = ast.literal_eval(m.group(0))
            except (ValueError, SyntaxError):
                continue
            if isinstance(v, str):
                out.append(v)
        return out

    def has_literal(self, where, value) -> bool:
        """The model saw the masked text, so a literal may match either the source or what was sent."""
        return isinstance(value, str) and (value in self.literals(self.text(where)) or value in self.literals(self.shown(where)))

    def rule(self, value, field: str, errors: list) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or value not in RULES:
            errors.append(f"{field}: quy tắc {value!r} không có trong danh sách được phép")
            return None
        return value

    def type_(self, value, field: str, errors: list):
        """Type notation -> parsed tree: ('base', name) | ('array', inner) | ('model', 'file::Class')."""
        if not isinstance(value, str):
            errors.append(f"{field}: kiểu phải là chuỗi")
            return None
        v = value.strip()
        if v in BASE_TYPES:
            return ("base", v)
        if v.startswith("array[") and v.endswith("]"):
            inner = self.type_(v[6:-1], field, errors)
            return ("array", inner) if inner else None
        if MODEL_ID.fullmatch(v):
            return ("model", v)
        errors.append(f"{field}: kiểu {value!r} không đúng ký pháp (integer|number|string|binary|uuid|datetime|date|email|boolean|object|any|"
                      "array[...]|file.py::Class)")
        return None

    def boolean_or_unknown(self, item, key, field, errors):
        v = item.get(key)
        if isinstance(v, bool) or _unknown(v):
            return v
        errors.append(f"{field}.{key}: phải là true/false hoặc {{\"unknown\": lý do}}")
        return None

    def type_or_unknown(self, v, field, errors):
        return v if _unknown(v) else self.type_(v, field, errors)

    # ---------------------------------------------------------------- submit

    def submit(self, payload) -> dict:
        if not isinstance(payload, dict):
            return {"accepted": 0, "errors": [{"kind": "payload", "errors": ["findings phải là object"]}]}
        accepted, problems = 0, []
        for kind, fn in (("models", self.add_model), ("routes", self.add_route), ("http_calls", self.add_http),
                         ("file_roles", self.add_role), ("limitations", self.add_limit), ("dismissed", self.add_dismissed)):
            items = payload.get(kind, [])
            if not isinstance(items, list):
                problems.append({"kind": kind, "errors": ["phải là danh sách"]})
                continue
            for i, item in enumerate(items):
                errors = fn(item) if isinstance(item, dict) else ["phải là object"]
                if errors:
                    problems.append({"kind": kind, "index": i, "errors": errors})
                    self.rejected.append({"kind": kind, "fields": sorted(item) if isinstance(item, dict) else [],
                                          "errors": [mask_text(e) for e in errors]})
                else:
                    accepted += 1
        return {"accepted": accepted, "errors": problems}

    # ---- models

    def add_model(self, item) -> list:
        errors = []
        ident = item.get("id")
        if not isinstance(ident, str) or not MODEL_ID.fullmatch(ident):
            return ["id: cần dạng 'file.py::Class'"]
        path, name = ident.split("::")
        where = self.loc(item.get("at"), "at", errors)
        dynamic = item.get("dynamic")
        if dynamic is not None:  # created at runtime: X = factory(...); fields are unknown, never guessed
            if not _unknown_reason(dynamic):
                errors.append("dynamic: {\"reason\": vì sao trường chỉ biết lúc chạy}")
            if where and (where[0] != path or not re.search(rf"^\s*{re.escape(name)}\s*(?::[^=\n]*)?=\s*[\w.]+\s*\(",
                                                            self.text(where), re.M)):
                errors.append(f"at: model dynamic cần dòng '{name} = hàm(...)' tại {item.get('at')}")
            if item.get("fields"):
                errors.append("fields: model dynamic để danh sách rỗng; trường ghi unknown kèm lý do")
        elif where and (where[0] != path or not re.search(rf"^\s*class\s+{re.escape(name)}\b", self.text(where), re.M)):
            errors.append(f"at: không thấy 'class {name}' tại {item.get('at')}")
        fields = item.get("fields")
        if not isinstance(fields, list):
            errors.append("fields: phải là danh sách (danh sách rỗng nếu model không có trường)")
            fields = []
        parsed, unchecked = [], []
        for j, f in enumerate(fields):
            if not isinstance(f, dict):
                errors.append(f"fields[{j}]: phải là object")
                continue
            fname = f.get("name")
            fat = self.loc(f.get("at"), f"fields[{j}].at", errors)
            if not isinstance(fname, str) or not fname:
                errors.append(f"fields[{j}].name: thiếu")
            elif fat and not re.search(rf"\b{re.escape(fname)}\b", self.text(fat)):
                errors.append(f"fields[{j}].name: '{fname}' không có tại {f.get('at')}")
            alias = f.get("alias")
            if alias is not None and fat and not self.has_literal(fat, alias):
                errors.append(f"fields[{j}].alias: không có literal {alias!r} tại {f.get('at')}")
            parsed.append({"name": fname, "alias": alias, "at": fat, "rule": self.rule(f.get("rule"), f"fields[{j}].rule", errors),
                           "required": self.boolean_or_unknown(f, "required", f"fields[{j}]", errors),
                           "nullable": self.boolean_or_unknown(f, "nullable", f"fields[{j}]", errors),
                           "type": self.type_or_unknown(f.get("type"), f"fields[{j}].type", errors)})
            if fat and not self._field_check(f, fat, parsed[-1]["type"], j, errors):
                unchecked.append(fname)
        if errors:
            return errors
        self.models[ident] = {"id": ident, "name": name, "at": where, "fields": parsed, "unchecked": unchecked,
                              "dynamic": dynamic["reason"] if dynamic is not None else None}
        return []

    def _annotation_type(self, node):
        """Expected claim for an annotation: ('base', T) | ('array', inner) | ('class', name) | None (not decidable)."""
        if isinstance(node, (ast.Name, ast.Attribute)):
            name = (astscan.dotted(node) or "").split(".")[-1]
            if name in FIELD_BASES:
                return ("base", FIELD_BASES[name])
            if name in FIELD_ARRAYS:
                return ("array", None)
            self._function_defs()
            return ("class", name) if name in self._classes and name not in self._enum_names() else None
        if isinstance(node, ast.Subscript):
            name = astscan.name_of(node.value)
            if name in FIELD_ARRAYS:
                inner = node.slice.elts[0] if isinstance(node.slice, ast.Tuple) else node.slice
                return ("array", self._annotation_type(_strip_optional(inner)[0]))
            if name in ("dict", "Dict", "Mapping"):
                return ("base", "object")
        return None

    def _field_check(self, f, fat, got, j, errors) -> bool:
        """Compare a field claim with the annotated assignment it cites. True when type, required and nullable
        could all be decided from the declaration (otherwise the agent's answer stands, with lower confidence)."""
        tree = self._tree(fat[0])
        st = next((n for n in ast.walk(tree) if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
                   and n.target.id == f.get("name") and n.lineno <= fat[1] <= (n.end_lineno or n.lineno)),
                  None) if tree is not None else None
        if st is None:
            return False
        decl = ast.unparse(st)[:120]
        base, optional = _strip_optional(st.annotation)
        has_default, default_none = _default_of(st.value)
        want_type = self._annotation_type(base)
        # Optional without default: required differs between Pydantic v1 and v2; `x: int = None`: v1 allows None
        want = {"required": False if has_default else (None if optional else True),
                "nullable": True if optional else (None if default_none else False)}
        if _type_conflict(want_type, got):
            errors.append(f"fields[{j}].type: khai báo `{decl}` không phải kiểu {f.get('type')}")
        for key, value in want.items():
            if value is not None and isinstance(f.get(key), bool) and f[key] is not value:
                errors.append(f"fields[{j}].{key}: khai báo `{decl}` cho {key} = {str(value).lower()}")
        return want_type is not None and None not in want.values()

    # ---- routes

    def add_route(self, item) -> list:
        errors = []
        method = item.get("method")
        if not isinstance(method, str) or method not in METHODS:
            errors.append(f"method: phải là một trong {sorted(METHODS)}")
            method = None
        handler = item.get("handler")
        if not isinstance(handler, str) or not MODEL_ID.fullmatch(handler):
            errors.append("handler: cần dạng 'file.py::ten_ham'")
            handler = None
        dec = self.loc(item.get("decorator"), "decorator", errors)
        if dec and handler:
            errors += self._decorator_problems(dec, handler, method)
        app = item.get("application")
        app_where = None
        if not _unknown(app):
            app_where = self.loc(app, "application", errors)
            if app_where and not re.search(r"FastAPI\s*\(", self.text(app_where)):
                errors.append("application: dòng phải tạo FastAPI(...)")
        parts = item.get("path_parts")
        parsed_parts = []
        if not isinstance(parts, list) or not parts:
            errors.append("path_parts: danh sách các phần path theo thứ tự từ app tới decorator")
            parts = []
        for j, part in enumerate(parts):
            if not isinstance(part, dict) or not isinstance(part.get("kind"), str) or part["kind"] not in PART_SIGNALS:
                errors.append(f"path_parts[{j}].kind: một trong {sorted(PART_SIGNALS)}")
                continue
            where = self.loc(part.get("at"), f"path_parts[{j}].at", errors)
            # `used_at`: the registration line, when the literal sits elsewhere (a Settings default, or an argument
            # passed through a helper such as attach(app, router, prefix="/api/v1"))
            used_at = None
            if part["kind"] == "settings_default" or (part.get("used_at") and part["kind"] != "decorator"):
                used_at = self.loc(part.get("used_at"), f"path_parts[{j}].used_at", errors)
                if used_at and not re.search(r"include_router\s*\(|APIRouter\s*\(|\.mount\s*\(", self.text(used_at)):
                    errors.append(f"path_parts[{j}].used_at: phải là dòng include_router/APIRouter/mount dùng giá trị này")
            elif where and part["kind"] != "decorator" and not PART_SIGNALS[part["kind"]].search(self.text(where)) \
                    and not self._inside_call(where, PART_CALLS.get(part["kind"], ())):  # prefix= on a later line
                errors.append(f"path_parts[{j}]: dòng {part.get('at')} không có dạng của {part['kind']}; nếu giá trị "
                              "được truyền qua hàm/biến thì thêm used_at là dòng đăng ký")
            if "unknown" in part:
                if not _unknown(part):
                    errors.append(f"path_parts[{j}].unknown: cần lý do")
                elif where and part["kind"] in ("include_prefix", "router_prefix") and "prefix" not in self.text(where):
                    errors.append(f"path_parts[{j}]: lời gọi tại {part.get('at')} không có prefix; bỏ phần này khỏi path_parts")
                parsed_parts.append({"kind": part["kind"], "value": None, "reason": part.get("unknown"), "at": where,
                                     "used_at": used_at})
            else:
                value = part.get("value")
                if not isinstance(value, str):
                    errors.append(f"path_parts[{j}].value: phải là chuỗi, hoặc dùng {{\"unknown\": lý do}}")
                elif where and value and not self.has_literal(where, value):
                    errors.append(f"path_parts[{j}].value: không có literal {value!r} tại {part.get('at')}")
                elif where and part["kind"] == "decorator" and (paths := self._decorator_paths(where, method)) is not None \
                        and value not in paths:
                    errors.append(f"path_parts[{j}].value: path của decorator là {sorted(paths)}, không phải {value!r} "
                                  "(name=, summary= không phải path)")
                elif where and value == "" and re.search(r"prefix\s*=\s*[rRuU]?[\"'][^\"']+[\"']", self.text(where)):
                    errors.append(f"path_parts[{j}].value: dòng {part.get('at')} có prefix khác rỗng")
                parsed_parts.append({"kind": part["kind"], "value": value, "at": where, "used_at": used_at})
        if dec and parsed_parts and (parsed_parts[-1]["kind"] != "decorator" or parsed_parts[-1]["at"] is None
                                     or parsed_parts[-1]["at"][0] != dec[0]
                                     or not dec[1] <= parsed_parts[-1]["at"][1] <= dec[2]):
            errors.append("path_parts: phần cuối phải là kind 'decorator' nằm trong khoảng decorator")
        if any(p["kind"] == "decorator" for p in parsed_parts[:-1]):
            errors.append("path_parts: chỉ phần cuối là decorator")
        params = self.params(item.get("params"), errors)
        body = self.body(item.get("request_body"), errors)
        resp = self.response(item.get("response"), errors)
        status = self.status(item.get("status"), dec, errors)
        deps = item.get("dependencies")
        deps_v = None
        if _unknown(deps):
            deps_v = {"unknown": deps["unknown"]}
        elif isinstance(deps, list):
            deps_v = []
            for j, d in enumerate(deps):
                if not isinstance(d, dict) or not isinstance(d.get("name"), str) or not d["name"]:
                    errors.append(f"dependencies[{j}]: cần object có name")
                    continue
                dat = self.loc(d.get("at"), f"dependencies[{j}].at", errors)
                if dat and not self.dependency_at(d["name"], dat):
                    errors.append(f"dependencies[{j}].name: '{d['name']}' không có tại {d.get('at')}"
                                  + ("; Depends(f) và Depends(f(...)) ghi tên hàm f, không ghi lời gọi" if "(" in d["name"] else ""))
                deps_v.append({"name": d["name"], "at": dat})
        else:
            errors.append("dependencies: danh sách Depends của route (rỗng nếu không có) hoặc {\"unknown\": lý do}")
        auth = item.get("auth")
        auth_v = None
        if _unknown(auth):
            auth_v = {"unknown": auth["unknown"]}
        elif isinstance(auth, dict) and isinstance(auth.get("value"), str) and auth["value"]:
            auth_v = {"value": auth["value"], "at": self.loc(auth.get("at"), "auth.at", errors)}
            if auth_v["at"] and not AUTH_SIGNAL.search(STRING.sub('""', self.text(auth_v["at"]))):
                errors.append("auth.at: dòng không có dấu hiệu xác thực (Depends/Security, lớp của fastapi.security); "
                              "không chứng minh được thì ghi {\"unknown\": lý do}")
        else:
            errors.append("auth: {\"unknown\": lý do} hoặc {\"value\": mô tả, \"at\": vị trí}")
        extras = self._route_extras(item, dec, errors)
        if errors:
            return errors
        if app_where is not None and dec is not None:
            chain = self._registration_problems(dec, app_where, parsed_parts)
            if chain:
                return chain
        key = (handler, method, app_where, tuple((p["kind"], p["at"]) for p in parsed_parts))
        same = [k for k in self.routes if k[0] == handler and k[1] == method]
        if app_where is None and any(k[2] is not None for k in same):
            return []  # already known to be served by an application; an unattached version adds nothing
        if app_where is not None:  # a version attached to an application supersedes "not attached anywhere"
            for k in same:
                if k[2] is None:
                    del self.routes[k]
        full = _full_path(parsed_parts)
        for k in [k for k in self.routes if k[:3] == (handler, method, app_where) and k != key]:
            if full is not None and _full_path(self.routes[k]["parts"]) == full:
                del self.routes[k]  # the same route through an equivalent chain: the newer submission wins
        self.routes[key] = {"method": method, "handler": handler, "decorator": dec, "application": app_where,
                            "application_unknown": app.get("unknown") if isinstance(app, dict) else None,
                            "parts": parsed_parts, "params": params, "body": body, "response": resp,
                            "status": status, "auth": auth_v, "dependencies": deps_v, **extras}
        return []

    # ---- optional route parts: errors, tags, deprecated, summary

    def _inside_call(self, where, names) -> bool:
        """The cited line sits inside a call to one of `names` written over several lines (include_router(\n r, prefix=...))."""
        tree = self._tree(where[0]) if names else None
        return tree is not None and any(isinstance(n, ast.Call) and astscan.name_of(n.func) in names
                                        and n.lineno < where[1] <= (n.end_lineno or n.lineno) for n in ast.walk(tree))

    def _handler_fn(self, dec):
        tree = self._tree(dec[0])
        # The cited range runs from the decorator to the def line, or on through a multi-line signature.
        return next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                     and dec[1] < n.lineno <= dec[2]), None) if tree is not None else None

    def _node_text(self, path, node) -> str:
        return "\n".join(self.tools.lines[path][node.lineno - 1:node.end_lineno or node.lineno])

    def _route_extras(self, item, dec, errors) -> dict:
        """errors (what the handler can answer with besides its declared status), tags, deprecated, summary."""
        out = {"errors": [], "tags": None, "deprecated": None, "summary": None, "examples": []}
        fn = self._handler_fn(dec) if dec else None
        span = (dec[1], fn.end_lineno or fn.lineno) if fn is not None else None
        raw_ex = item.get("examples")
        if raw_ex is not None and not isinstance(raw_ex, list):
            errors.append("examples: danh sách [{\"at\": dòng có example=/examples=}]")
            raw_ex = []
        rb, resp = item.get("request_body"), item.get("response")
        named = (rb.get("models") or [] if isinstance(rb, dict) else []) + \
            ([resp.get("model")] + list(resp.get("args") or []) if isinstance(resp, dict) else [])
        used = {m.split("::")[-1] for m in named if isinstance(m, str) and "::" in m}  # this route's model classes
        for j, x in enumerate(raw_ex or []):
            where = self.loc(x.get("at") if isinstance(x, dict) else None, f"examples[{j}].at", errors)
            if where is None:
                continue
            found, value = self._example_at(where)
            owner = self._class_at(where)
            inside = span is not None and where[0] == dec[0] and span[0] <= where[1] <= span[1]
            if not found:
                errors.append(f"examples[{j}]: dòng {x.get('at')} không có example=/examples= với giá trị literal")
            elif not (inside or (owner is not None and owner.name in used)):
                errors.append(f"examples[{j}]: dòng phải nằm trong hàm xử lý hoặc trong model request/response của route")
            else:
                out["examples"].append({"value": value, "at": where})
        raw = item.get("errors")
        if raw is not None and not isinstance(raw, list):
            errors.append("errors: danh sách [{status, exception, raised_at, status_at}]")
            raw = []
        for j, e in enumerate(raw or []):
            if not isinstance(e, dict):
                errors.append(f"errors[{j}]: phải là object")
                continue
            got = self._error_problems(e, j, dec, fn)
            errors += got
            if not got:
                out["errors"].append({"status": e["status"], "exception": e["exception"],
                                      "raised_at": self.loc(e["raised_at"], "", []),
                                      "status_at": self.loc(e["status_at"], "", []) if e.get("status_at") else None})
        tags = item.get("tags")
        if tags is not None:
            where = self.loc(tags.get("at") if isinstance(tags, dict) else None, "tags.at", errors)
            values = tags.get("value") if isinstance(tags, dict) else None
            if not isinstance(values, list) or not values or not all(isinstance(t, str) for t in values):
                errors.append("tags: {\"value\": [chuỗi], \"at\": dòng có tags=[...]}")
            elif where and ("tags" not in self.text(where) or not all(self.has_literal(where, t) for t in values)):
                errors.append(f"tags: dòng {tags.get('at')} không khai tags={values}")
            else:
                out["tags"] = {"value": values, "at": where}
        dep = item.get("deprecated")
        if dep is not None:
            where = self.loc(dep.get("at") if isinstance(dep, dict) else None, "deprecated.at", errors)
            if where and not re.search(r"\bdeprecated\s*=\s*True\b", self.text(where)):
                errors.append(f"deprecated: dòng {dep.get('at')} không có deprecated=True")
            elif where:
                out["deprecated"] = {"value": True, "at": where}
        summ = item.get("summary")
        if summ is not None:
            where = self.loc(summ.get("at") if isinstance(summ, dict) else None, "summary.at", errors)
            text = summ.get("text") if isinstance(summ, dict) else None
            if not isinstance(text, str) or not text.strip() or len(text) > 300:
                errors.append("summary: {\"text\": mô tả ngắn ≤300 ký tự, \"at\": dòng trong decorator hoặc thân handler}")
            elif where and (span is None or where[0] != dec[0] or not span[0] <= where[1] <= span[1]):
                errors.append("summary.at: phải nằm trong decorator hoặc thân hàm xử lý của route")
            elif where:
                out["summary"] = {"value": mask_text(text.strip()), "at": where}
        return out

    def _example_at(self, where) -> tuple[bool, object]:
        """(found, value) of an example=/examples=/openapi_examples= keyword or "example(s)" dict key on the cited
        lines whose value is a Python literal."""
        tree = self._tree(where[0])
        for n in ast.walk(tree) if tree is not None else ():
            if not where[1] <= getattr(n, "lineno", 0) <= where[2]:
                continue
            pairs = [(k.arg, k.value) for k in n.keywords] if isinstance(n, ast.Call) else \
                [(k.value if isinstance(k, ast.Constant) else None, v) for k, v in zip(n.keys, n.values)] \
                if isinstance(n, ast.Dict) else []
            for name, value in pairs:
                if name in ("example", "examples", "openapi_examples"):
                    try:
                        return True, ast.literal_eval(value)
                    except (ValueError, SyntaxError, TypeError):
                        continue
        return False, None

    def _error_problems(self, e, j, dec, fn) -> list:
        f, out = f"errors[{j}]", []
        status, exc = e.get("status"), e.get("exception")
        if not isinstance(status, int) or isinstance(status, bool) or not 400 <= status <= 599:
            out.append(f"{f}.status: mã HTTP 400–599")
        if not isinstance(exc, str) or not re.fullmatch(r"[A-Za-z_][\w.]*", exc):
            return out + [f"{f}.exception: tên lớp lỗi như trong code"]
        short = exc.rsplit(".", 1)[-1]
        raised = self.loc(e.get("raised_at"), f"{f}.raised_at", out)
        if raised is None:
            return out
        code = STRING.sub('""', self.text(raised))
        if not (re.search(r"\braise\b", code) and re.search(rf"\b{re.escape(short)}\b", code)):
            return out + [f"{f}.raised_at: dòng {e.get('raised_at')} không ném {exc}"]
        if fn is not None and not self._reaches(STRING.sub('""', self._node_text(dec[0], fn)), self._step_names(raised)):
            out.append(f"{f}.raised_at: hàm xử lý của route không gọi tới hàm chứa {e.get('raised_at')} qua tối đa "
                       f"{CALL_DEPTH} lời gọi")
        if short.endswith("HTTPException"):
            if isinstance(status, int) and not re.search(rf"\b{status}\b|HTTP_{status}_", self.text(raised)):
                out.append(f"{f}.status: dòng ném không ghi mã {status}")
            return out
        at = self.loc(e.get("status_at"), f"{f}.status_at", out)
        if at is None:
            return out
        chain = self._exception_chain(short)
        owner = self._class_at(at)
        m = re.match(r"\s*(\w+)\s*(?::[^=]*)?=\s*(\d{3})\b", self.text(at))
        given = m and (m.group(1), int(m.group(2)))  # `code = 404` in the class body
        if not given:  # or super().__init__(..., status_code=404) inside the class
            given = next(((kw.arg, kw.value.value) for kw in self._init_keywords(at)
                          if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, int)
                          and 100 <= kw.value.value <= 599), None)
        if owner is None or owner.name not in chain:
            out.append(f"{f}.status_at: {e.get('status_at')} không nằm trong lớp {short} hay lớp cha của nó")
        elif not given or given[1] != status:
            out.append(f"{f}.status_at: dòng không gán mã {status} (dạng `code = {status}` trong lớp, hoặc "
                       f"`super().__init__(..., status_code={status})`)")
        else:
            attr = given[0]
            for name in chain[:chain.index(owner.name)]:  # a subclass between the raised class and `owner` overrides it
                body = [(p, x) for p, c in self._classes.get(name, []) for x in c.body]
                if any(isinstance(x, (ast.Assign, ast.AnnAssign))
                       and re.match(rf"\s*{attr}\s*(?::[^=]*)?=", self.tools.lines[p][x.lineno - 1]) for p, x in body) \
                        or any(kw.arg == attr for p, x in body for n in ast.walk(x)
                               for kw in (n.keywords if isinstance(n, ast.Call) and _is_init_call(n) else [])):
                    out.append(f"{f}.status_at: lớp {name} ghi đè {attr}; mã lấy từ lớp gần nhất")
                    break
            handlers = [h for name in chain for h in self._exception_handlers().get(name, [])]
            if not handlers:
                out.append(f"{f}: không có exception_handler cho {short} hay lớp cha; FastAPI trả 500, không phải {status}")
            elif not any(re.search(rf"\.{attr}\b", self._node_text(p, h)) for p, h in handlers):
                out.append(f"{f}: exception_handler của {short} không dùng thuộc tính {attr} làm status")
        return out

    def _init_keywords(self, where) -> list:
        """Keywords of super().__init__(...) / Base.__init__(...) calls on the cited lines."""
        tree = self._tree(where[0])
        return [kw for n in (ast.walk(tree) if tree is not None else ()) if isinstance(n, ast.Call) and _is_init_call(n)
                and where[1] <= n.lineno <= where[2] for kw in n.keywords if kw.arg]

    def _exception_chain(self, name: str) -> list[str]:
        """The class and its repository base classes, nearest first (by class name)."""
        self._function_defs()
        chain, todo = [], [name]
        while todo and len(chain) < 12:
            n = todo.pop(0)
            if n in chain:
                continue
            chain.append(n)
            todo += [astscan.name_of(b) for _, c in self._classes.get(n, []) for b in c.bases if astscan.name_of(b)]
        return chain

    def _class_at(self, where):
        tree = self._tree(where[0])
        found = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                 and n.lineno <= where[1] <= (n.end_lineno or n.lineno)] if tree is not None else []
        return max(found, key=lambda n: n.lineno) if found else None

    def _exception_handlers(self) -> dict:
        """exception class name -> [(path, handler function)] from @x.exception_handler(E) and add_exception_handler(E, f)."""
        if getattr(self, "_exc_handlers", None) is None:
            self._exc_handlers = {}
            for path, tree in self._trees_all().items():
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        for d in node.decorator_list:
                            if isinstance(d, ast.Call) and astscan.name_of(d.func) == "exception_handler" and d.args:
                                self._exc_handlers.setdefault(astscan.name_of(d.args[0]), []).append((path, node))
                    elif isinstance(node, ast.Call) and astscan.name_of(node.func) == "add_exception_handler" \
                            and len(node.args) >= 2:
                        for p, fn in self._function_defs().get(astscan.name_of(node.args[1]), []):
                            self._exc_handlers.setdefault(astscan.name_of(node.args[0]), []).append((p, fn))
        return self._exc_handlers

    def _trees_all(self) -> dict:
        self._function_defs()
        return self._trees

    def dependency_at(self, name: str, where) -> bool:
        """The cited lines name the Depends function (B.inject must keep its class), directly or through an
        Annotated alias that this file defines or imports."""
        text = STRING.sub('""', self.text(where))  # a name inside a string literal is not code
        targets = self._depends_targets(where)
        if targets is not None:  # read from the tree: a parameter name (db) or its type (Session) is not the target
            if any(t == name or t.endswith("." + name) if "." in name else t.split(".")[-1] == name for t in targets):
                return True
        elif "." in name:
            if re.search(rf"(?<![\w.]){re.escape(name)}\b", text):
                return True
        elif re.search(rf"\b{re.escape(name)}\b", text):
            return True
        return any(_same_dependency(dep, name) for word in set(re.findall(r"\w+", text))
                   for dep, _ in self._alias_deps(word, where[0]))

    def _depends_targets(self, where) -> list | None:
        """Dotted targets of the Depends/Security calls on the cited lines (f for Depends(f) and Depends(f(...)),
        the annotation for Depends() without argument); None when the file does not parse."""
        tree = self._tree(where[0])
        if tree is None:
            return None
        start, end = where[1], where[2]
        out = []
        for n in ast.walk(tree):
            kw_dep = next((k.value for k in getattr(n, "keywords", []) if k.arg == "dependency"), None)
            if isinstance(n, ast.Call) and astscan.name_of(n.func) in ("Depends", "Security") and (n.args or kw_dep) \
                    and n.lineno <= end and (n.end_lineno or n.lineno) >= start:
                t = n.args[0] if n.args else kw_dep
                out.append(_dep_target(t))
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):  # f: Filters = Depends()
                a = n.args
                pos = a.posonlyargs + a.args
                pairs = list(zip(pos, [None] * (len(pos) - len(a.defaults)) + list(a.defaults))) + \
                    list(zip(a.kwonlyargs, a.kw_defaults))
                for arg, default in pairs:
                    if not (arg.lineno <= end and (arg.end_lineno or arg.lineno) >= start):
                        continue
                    ann = arg.annotation
                    extra = ann.slice.elts if isinstance(ann, ast.Subscript) and isinstance(ann.slice, ast.Tuple) else []
                    if any(isinstance(e, ast.Call) and astscan.name_of(e.func) in ("Depends", "Security") and not e.args
                           for e in [default, *extra[1:]]):
                        out.append(astscan.dotted(extra[0] if extra else ann) or "")
        return out

    def _handler_depends(self, dec) -> list:
        """(target, path:line) of the Depends(...) that apply to a route: in the handler's signature (also through
        an Annotated alias), in dependencies=[...] of its decorators, and of the routers and app it hangs below
        (APIRouter(dependencies=...), include_router(dependencies=...)). Security(...) is left to the auth part."""
        tree = self._tree(dec[0])
        fn = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.lineno == dec[2]), None) if tree is not None else None
        if fn is None:
            return []
        a = fn.args
        pos = a.posonlyargs + a.args
        exprs = [d for d in list(a.defaults) + list(a.kw_defaults) if d is not None]
        for arg in pos + a.kwonlyargs:
            if isinstance(arg.annotation, ast.Subscript) and isinstance(arg.annotation.slice, ast.Tuple):
                exprs += arg.annotation.slice.elts[1:]
        for d in fn.decorator_list:
            for k in getattr(d, "keywords", []):
                if k.arg == "dependencies" and isinstance(k.value, (ast.List, ast.Tuple)):
                    exprs += k.value.elts
        out = _depends_of(exprs, dec[0])
        for arg in pos + a.kwonlyargs:  # p: PageDep, PageDep = Annotated[..., Depends(pagination)]
            if isinstance(arg.annotation, ast.Name):
                out += [(dep, f"{dec[0]}:{arg.lineno}") for dep, _ in self._alias_deps(arg.annotation.id, dec[0])]
        for d in fn.decorator_list:
            if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and isinstance(d.func.value, ast.Name):
                router = self._resolve(dec[0], d.func.value.id)
                out += self._router_depends(router, set()) if router else []
        seen = set()
        return [x for x in out if not (x[0] in seen or seen.add(x[0]))]

    def _router_depends(self, ident, seen) -> list:
        """Depends(...) given to a router or app (its constructor), to the include_router calls that hang it below
        another one, and to those above it."""
        if ident in seen:
            return []
        seen.add(ident)
        tree = self._tree(ident[0])
        out = []
        for n in ast.walk(tree) if tree is not None else []:
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == ident[1] for t in n.targets) \
                    and isinstance(n.value, ast.Call) and self._app_class(astscan.name_of(n.value.func), ident[0], set()):
                out += [x for k in n.value.keywords if k.arg == "dependencies" and isinstance(k.value, (ast.List, ast.Tuple))
                        for x in _depends_of(k.value.elts, ident[0])]
        self._include_edges()
        out += self._edge_deps.get(ident, [])
        for parent in self._parents.get(ident, ()):
            out += self._router_depends(parent, seen)
        return out

    def _called_at(self, name: str, where):
        """Whether the route writes Depends(name(...)) (a factory call) at its cited lines; None when unclear."""
        if where is None:
            return None
        text = self.text(where)
        if re.search(rf"(?<![\w.]){re.escape(name)}\s*\(", text):
            return True
        if re.search(rf"(?<![\w.]){re.escape(name)}\b", text):
            return False
        flags = {c for word in set(re.findall(r"\w+", text)) for dep, c in self._alias_deps(word, where[0])
                 if _same_dependency(dep, name)}
        return flags.pop() if len(flags) == 1 else None

    def _alias_markers(self, word: str, citing: str) -> list:
        """Header/Query/Cookie/Path calls inside an Annotated alias, as `citing` sees it (own, imported, only one)."""
        self._alias_deps("", citing)  # builds both alias tables
        tree = self._tree(citing)
        imp = astscan.imports(tree).get(word) if tree is not None else None
        defs = self._marker_aliases.get(word, []) or (self._marker_aliases.get(imp[1], []) if imp and imp[1] else [])
        own = [m for p, m in defs if p == citing]
        if own:
            return own[0]
        if imp and imp[1]:  # from params import Tenant as TenantHeader
            source = self._modules().find(imp[0], citing)
            hit = [m for p, m in defs if p == source]
            if hit:
                return hit[0]
        return defs[0][1] if len(defs) == 1 else []

    def _alias_deps(self, word: str, citing: str) -> list[tuple[str, bool]]:
        """(dependency, called) wrapped by an Annotated alias as seen from `citing`: its own definition, the one it
        imports, the only one; several unrelated definitions with nothing to choose between give nothing."""
        if self._aliases is None:
            self._aliases = {}
            self._function_defs()  # parses every readable file once
            for path, tree in self._trees.items():  # X = Annotated[T, Depends(f)], also over several lines
                for n in ast.walk(tree):
                    target = n.targets[0] if isinstance(n, ast.Assign) and len(n.targets) == 1 else \
                        n.target if isinstance(n, ast.AnnAssign) else None
                    value = getattr(n, "value", None)
                    if not isinstance(target, ast.Name) or not isinstance(value, ast.Subscript) \
                            or astscan.name_of(value.value) != "Annotated":
                        continue
                    deps = []
                    for call in ast.walk(value):
                        if isinstance(call, ast.Call) and astscan.name_of(call.func) in ("Depends", "Security") and call.args:
                            arg = call.args[0]
                            dep = astscan.dotted(arg.func if isinstance(arg, ast.Call) else arg)
                            if dep:
                                deps.append((dep, isinstance(arg, ast.Call)))
                    if deps:
                        self._aliases.setdefault(target.id, []).append((path, deps))
                    markers = [e for e in (value.slice.elts[1:] if isinstance(value.slice, ast.Tuple) else [])
                               if isinstance(e, ast.Call) and astscan.name_of(e.func) in DEPENDENCY_MARKERS]
                    if markers:
                        self._marker_aliases.setdefault(target.id, []).append((path, markers))
        defs = self._aliases.get(word, [])
        if not defs:
            return []
        own = [d for p, d in defs if p == citing]
        if own:
            return own[0]
        tree = self._tree(citing)
        imp = astscan.imports(tree).get(word) if tree is not None else None
        if imp and imp[1]:
            source = self._modules().find(imp[0], citing)
            hit = [d for p, d in defs if p == source]
            if hit:
                return hit[0]
        return defs[0][1] if len({str(d) for _, d in defs}) == 1 else []

    def _modules(self):
        if self._module_index is None:
            self._module_index = astscan.ModuleIndex(self.tools.readable)
        return self._module_index

    def _enum_names(self) -> set:
        """Classes of the snapshot that subclass an Enum (FastAPI reads them as query values)."""
        if getattr(self, "_enums", None) is None:
            self._function_defs()
            self._enums = {name for name, defs in self._classes.items()
                           if any(any("Enum" in (astscan.name_of(b) or "") for b in c.bases) for _, c in defs)}
        return self._enums

    def _module_calls(self) -> dict:
        """name -> [(file, call)] for every module-level `name = f(...)`, read once (tenant = Tenant(), partial)."""
        if getattr(self, "_mcalls", None) is None:
            self._mcalls = {}
            self._function_defs()
            for p, tree in self._trees.items():
                for n in tree.body:
                    if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                self._mcalls.setdefault(t.id, []).append((p, n.value))
        return self._mcalls

    def _tree(self, path: str):
        self._function_defs()
        return self._trees.get(path)

    def _decorator_problems(self, dec, handler, method) -> list:
        """The range must be: decorator lines of this one function, then its `def` line, nothing else. The decorator
        must call the claimed method on a FastAPI app or APIRouter (api_route: the method is in methods=[...])."""
        hpath, hname = handler.split("::")
        lines = self.tools.lines[dec[0]][dec[1] - 1:dec[2]]
        if dec[0] != hpath:
            return ["decorator: phải nằm cùng file với handler"]
        if not lines[0].lstrip().startswith("@"):
            return ["decorator: dòng đầu của khoảng phải là dòng '@...'"]
        defs = [i for i, line in enumerate(lines) if re.match(r"\s*(async\s+)?def\s", line)]
        if len(defs) != 1 or not re.match(rf"\s*(async\s+)?def\s+{re.escape(hname)}\s*\(", lines[defs[0]]):
            return [f"decorator: khoảng phải gồm decorator và đúng một dòng 'def {hname}(' của handler"]
        tree = self._tree(hpath)
        def_line = dec[1] + defs[0]
        fn = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.name == hname and n.lineno == def_line), None) if tree is not None else None
        if fn is None:
            return self._decorator_problems_text(dec, hname, method, lines, defs)
        matched = []
        for d in fn.decorator_list:
            if d.lineno < dec[1] or not isinstance(d, ast.Call) or not isinstance(d.func, ast.Attribute):
                continue
            verb = d.func.attr
            if verb == "api_route":
                kw = next((k.value for k in d.keywords if k.arg == "methods"), None)
                allowed = [e.value.upper() for e in kw.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)] \
                    if isinstance(kw, (ast.List, ast.Tuple, ast.Set)) else ["GET"] if kw is None else []
                if method and method in allowed:
                    matched.append(d)
            elif method and verb == method.lower():
                matched.append(d)
        if not matched:
            return [f"method: không thấy .{(method or '').lower()}( hoặc api_route(methods=[...'{method}'...]) "
                    f"trong decorator của {hname}"]
        receiver = astscan.name_of(matched[0].func.value)
        if receiver and self._is_app(hpath, receiver, 0) is False:
            return [f"decorator: {receiver} không phải FastAPI(...)/APIRouter(...) (xét nơi tạo hoặc nơi import)"]
        return []

    def _resolve(self, path: str, name: str, depth: int = 0):
        """(file, name) where `name` as seen in `path` is bound: assigned in that file, or imported (renames and
        module attributes followed); None when the snapshot does not show it."""
        tree = self._tree(path)
        if tree is None or depth > 4:
            return None
        if any(isinstance(n, (ast.Assign, ast.AnnAssign)) and any(
                isinstance(t, ast.Name) and t.id == name for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))
               for n in tree.body + [x for f in ast.walk(tree) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))
                                     for x in f.body]):
            return (path, name)
        imp = astscan.imports(tree).get(name)
        if imp and imp[1]:
            target = self._modules().find(imp[0], path)
            return self._resolve(target, imp[1], depth + 1) if target else None
        return None

    def _router_of(self, path: str, expr):
        """Identity of the router expression of an include_router(...) call: `r`, `users.router`."""
        if isinstance(expr, ast.Name):
            return self._resolve(path, expr.id)
        if isinstance(expr, ast.Attribute) and isinstance(expr.value, ast.Name):
            imp = astscan.imports(self._tree(path)).get(expr.value.id)
            if imp and imp[1] is None:  # import app.api.users as users
                target = self._modules().find(imp[0], path)
            elif imp:  # from app.api import users
                target = self._modules().find(f"{imp[0]}.{imp[1]}", path)
            else:
                target = None
            return self._resolve(target, expr.attr) if target else None
        return None

    def _include_edges(self):
        """parent identity -> [(child identity or None, need or None, site)] for every include_router/mount. A need
        is {"lines": [(file, line)], "literal": str | None}: the lines an agent may cite for the prefix this call
        sets, and its value when it is a literal; None when the call sets no prefix. The site (file, line, module
        level) is where the registration runs: FastAPI copies the routes a router has at that moment."""
        if self._edges is None:
            self._edges, self._parents, self._edge_deps = {}, {}, {}
            self._function_defs()
            for path, tree in self._trees.items():
                for c in ast.walk(tree):
                    if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr in ("include_router", "mount"):
                        self._add_edge(path, tree, c)
        return self._edges

    def _add_edge(self, path, tree, c):
        if _never_runs(tree, c):  # ENABLE_API = False / if ENABLE_API: app.include_router(r)
            return
        kw = {k.arg: k.value for k in c.keywords if k.arg}  # include_router(router=r, prefix=...)
        if c.func.attr == "include_router":
            arg, prefix = (c.args[0] if c.args else kw.get("router")), kw.get("prefix")
        else:  # mount("/p", app) or mount(path="/p", app=app)
            arg = c.args[1] if len(c.args) > 1 else kw.get("app")
            prefix = c.args[0] if c.args else kw.get("path")
        lines = [(path, i) for i in range(c.lineno, (c.end_lineno or c.lineno) + 1)]
        given = prefix is not None and not (isinstance(prefix, ast.Constant) and prefix.value in ("", None))
        literal = prefix.value if isinstance(prefix, ast.Constant) and isinstance(prefix.value, str) else None
        if not isinstance(c.func.value, ast.Name):  # self.app.include_router(r): not followed
            self._edges_open = True
            return
        parent = self._resolve(path, c.func.value.id)
        if parent:
            # for r in (items, users): app.include_router(r): one edge per router of the literal sequence
            loop = next((f for f in ast.walk(tree) if isinstance(f, (ast.For, ast.AsyncFor)) and isinstance(arg, ast.Name)
                         and isinstance(f.target, ast.Name) and f.target.id == arg.id
                         and isinstance(self._module_value(path, f.iter), (ast.Tuple, ast.List))
                         and f.lineno < c.lineno <= (f.end_lineno or f.lineno)), None)
            for one in (self._module_value(path, loop.iter).elts if loop is not None else [arg]):
                child = self._router_of(path, one) if one is not None else None
                if child is not None:  # who includes whom, and with which dependencies=[...]
                    self._parents.setdefault(child, set()).add(parent)
                    deps = kw.get("dependencies")
                    self._edge_deps.setdefault(child, []).extend(
                        _depends_of(deps.elts, path) if isinstance(deps, (ast.List, ast.Tuple)) else [])
                self._edges.setdefault(parent, []).append(
                    (child, {"lines": lines, "literal": literal} if given else None, (path, c.lineno, _top_level(tree, c))))
            return
        # include_router on a parameter (register(app)): follow the calls of the helper that holds it
        holders = [f for f in ast.walk(tree) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and f.lineno <= c.lineno <= (f.end_lineno or f.lineno)]
        if not holders:
            self._edges_open = True
            return
        fn = max(holders, key=lambda f: f.lineno)
        params = [x.arg for x in fn.args.posonlyargs + fn.args.args]
        names = params + [x.arg for x in fn.args.kwonlyargs]
        uses_param = prefix is not None and any(isinstance(n, ast.Name) and n.id in names for n in ast.walk(prefix))
        calls = [(cp, n) for cp, t in self._trees.items() for n in ast.walk(t)
                 if isinstance(n, ast.Call) and astscan.name_of(n.func) == fn.name]
        for cp, call in calls:  # register(app): app is the parent here
            shift = 1 if params[:1] in (["self"], ["cls"]) and isinstance(call.func, ast.Attribute) else 0
            given_args = dict(zip(params[shift:], call.args))
            given_args.update({k.arg: k.value for k in call.keywords if k.arg})
            target = given_args.get(c.func.value.id)
            parent = self._resolve(cp, target.id) if isinstance(target, ast.Name) else None
            if isinstance(arg, ast.Name) and arg.id in names:
                child_expr, child_file = given_args.get(arg.id), cp
            else:
                child_expr, child_file = arg, path
            child = self._router_of(child_file, child_expr) if child_expr is not None else None
            if parent is None or child is None or uses_param:  # a prefix passed in, or an argument not resolved
                self._edges_open = True
                continue
            site = [(cp, i) for i in range(call.lineno, (call.end_lineno or call.lineno) + 1)]
            self._edges.setdefault(parent, []).append(
                (child, {"lines": lines + site, "literal": literal} if given else None,
                 (cp, call.lineno, _top_level(self._trees[cp], call))))

    def _built_by_factory_holding(self, ident, app_where) -> bool:
        """`app = create_application()` where the claimed FastAPI(...) line sits inside create_application."""
        tree = self._tree(ident[0])
        for n in ast.walk(tree) if tree is not None else []:
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == ident[1] for t in n.targets)                     and isinstance(n.value, ast.Call):
                for fpath, fn in self._function_defs().get(astscan.name_of(n.value.func) or "", []):
                    if fpath == app_where[0] and fn.lineno <= app_where[1] <= (fn.end_lineno or fn.lineno):
                        return True
        return False

    def _router_prefix(self, ident) -> dict | None:
        """The need of `r = APIRouter(prefix=...)` when the router is built with a prefix (its lines and literal)."""
        tree = self._tree(ident[0])
        built = [n for n in (ast.walk(tree) if tree is not None else []) if isinstance(n, (ast.Assign, ast.AnnAssign))
                 and any(isinstance(t, ast.Name) and t.id == ident[1]
                         for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))
                 and isinstance(n.value, ast.Call) and self._app_class(astscan.name_of(n.value.func), ident[0], set())]
        for n in built if len(built) == 1 else [n for n in built if n in tree.body]:  # in a factory too
            prefix = next((k.value for k in n.value.keywords if k.arg == "prefix"), None)
            if prefix is not None and not (isinstance(prefix, ast.Constant) and prefix.value in ("", None)):
                return {"lines": [(ident[0], i) for i in range(n.lineno, (n.end_lineno or n.lineno) + 1)],
                        "literal": prefix.value if isinstance(prefix, ast.Constant) and isinstance(prefix.value, str)
                        else None}
        return None

    def _registration_problems(self, dec, app_where, parts) -> list:
        """The decorator's router must hang below the claimed application through include_router/mount calls of
        the snapshot, and every one of them that sets a prefix must be among the claimed path_parts. Nothing is
        concluded when a registration on the way cannot be resolved (dynamic includes)."""
        app_line = self.tools.lines[app_where[0]][app_where[1] - 1]
        m = re.match(r"\s*(\w+)\s*(?::[^=]*)?=", app_line)
        tree = self._tree(dec[0])
        fn = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.lineno == dec[2]), None) if tree is not None else None
        calls = [x for x in fn.decorator_list if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                 and isinstance(x.func.value, ast.Name)] if fn is not None else []
        if not m or not calls:
            return []
        app = (app_where[0], m.group(1))
        results = [self._registration_for(dec, tree, fn, x, app, app_where, parts) for x in calls]
        return [] if any(not r for r in results) else results[0]

    def _registration_for(self, dec, tree, fn, call, app, app_where, parts) -> list:
        """_registration_problems for one decorator of the handler."""
        router = self._resolve(dec[0], call.func.value.id)
        if router is None or router == app or self._built_by_factory_holding(router, app_where):
            return []
        edges = self._include_edges()
        cited = []  # (position, (file, line) set, part) of every prefix part with a value
        for i, p in enumerate(parts):
            if p.get("kind") == "decorator" or not p.get("value"):
                continue
            cited.append((i, {(p[k][0], p[k][1]) for k in ("at", "used_at") if p.get(k)}, p))
        def later(site, before):  # both at module level of one file, `site` running after `before`
            return before is not None and site[0] == before[0] and site[2] and before[2] and site[1] > before[1]

        paths, incomplete, late, todo = [], False, [], [(app, [], [], None)]
        while todo:
            node, needs, passed, last = todo.pop()
            if len(passed) > 6:
                continue
            for child, need, site in edges.get(node, []):
                if child is None:
                    incomplete = True
                    continue
                if later(site, last):  # outer.include_router(inner) after app.include_router(outer): not copied
                    late.append(site)
                    continue
                # each step needs its include prefix and the prefix the child router was built with: APIRouter(prefix=)
                step = needs + [x for x in (need, self._router_prefix(child)) if x]
                if child == router:
                    if later((dec[0], dec[1], _top_level(tree, fn)), site):  # the route is added after the include
                        late.append(site)
                    else:
                        paths.append(step)
                elif child not in passed:
                    todo.append((child, step, passed + [child], site))
        if not paths:
            if late and not incomplete and not self._edges_open:
                return [f"application: include_router tại {late[0][0]}:{late[0][1]} chạy trước khi {router[1]} có route "
                        "này (FastAPI chép route có sẵn lúc include)"]
            return [] if incomplete or self._edges_open else [f"application: {router[1]} ({router[0]}) không được include_router/mount vào "
                                          f"{app[1]} ({app_where[0]}:{app_where[1]}) trong snapshot"]
        if self._edges_open:
            return []
        problems = []
        for p in paths:
            matched = {}  # need index -> parts citing it
            stray = []
            for pos, lines, part in cited:
                hits = [k for k, need in enumerate(p) if lines & set(need["lines"])]
                if hits:
                    matched.setdefault(hits[0], []).append((pos, part))
                else:
                    stray.append(part)
            missing = [need for k, need in enumerate(p) if k not in matched]
            if missing:
                problems.append("path_parts: thiếu đăng ký có prefix trên đường từ "
                                f"{app[1]} tới {router[1]}: " + ", ".join("%s:%d" % n["lines"][0] for n in missing))
                continue
            if stray or any(len(v) > 1 for v in matched.values()):
                problems.append("path_parts: có prefix không nằm trên đường đăng ký hoặc bị lặp: "
                                + ", ".join(str(x.get("at")) for x in stray + [q for v in matched.values() if len(v) > 1
                                                                                 for _, q in v[1:]]))
                continue
            wrong = [(q, p[k]["literal"]) for k, v in matched.items() for _, q in v
                     if p[k]["literal"] is not None and q.get("kind") != "settings_default" and q["value"] != p[k]["literal"]]
            if wrong:
                problems.append("path_parts: giá trị prefix khác literal trong code: "
                                + ", ".join(f"{q['value']!r} thay vì {lit!r}" for q, lit in wrong))
                continue
            seq = [matched[k][0][0] for k in range(len(p))]
            if seq != sorted(seq):
                problems.append(f"path_parts: thứ tự prefix sai; prefix áp dụng từ {app[1]} vào tới {router[1]}: "
                                + " → ".join("%s:%d" % n["lines"][0] for n in p))
                continue
            return []
        return problems[:1]

    def _decorator_paths(self, where, method=None) -> set | None:
        """The path arguments (first positional or path=) of the route decorators of `method` starting on the
        cited lines (api_route: when methods=[...] holds it); None when the file does not parse or no decorator
        call starts there. @app.get('/read') over @app.post('/write'): GET has /read only."""
        tree = self._tree(where[0])
        if tree is None:
            return None
        paths, found = set(), False
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dcall in fn.decorator_list:
                if isinstance(dcall, ast.Call) and where[1] <= dcall.lineno <= where[2]:
                    found = True
                    verb = astscan.name_of(dcall.func)
                    if method and verb != method.lower():
                        kw = next((k.value for k in dcall.keywords if k.arg == "methods"), None)
                        listed = [e.value.upper() for e in getattr(kw, "elts", []) if isinstance(e, ast.Constant)]
                        if verb != "api_route" or (kw is not None and method not in listed) or (kw is None and method != "GET"):
                            continue
                    arg = dcall.args[0] if dcall.args else next((k.value for k in dcall.keywords if k.arg == "path"), None)
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        paths.add(arg.value)
        return paths if found else None

    def _decorator_problems_text(self, dec, hname, method, lines, defs) -> list:
        """Fallback for a file that does not parse: the earlier line-based check."""
        head = "\n".join(lines[:defs[0]])
        if method and not (re.search(rf"\.{method.lower()}\s*\(", head)
                           or (".api_route" in head and (method in self.literals(head)))):
            return [f"method: không thấy .{method.lower()}( hoặc api_route có '{method}' trong decorator của {hname}"]
        return []

    def _is_app(self, path: str, name: str, depth: int):
        """True/False when `name` in `path` is (not) a FastAPI app or APIRouter, as far as the snapshot shows; None
        when it cannot be told (bound by a library, unreadable file)."""
        tree = self._tree(path)
        if tree is None or depth > 3:
            return None
        if path not in self._bindings:  # name -> values bound to it (an ast.arg for a parameter), read once per file
            index = {}
            for n in ast.walk(tree):
                if isinstance(n, ast.Assign):
                    for t in n.targets:
                        index.setdefault(astscan.name_of(t), []).append(n.value)
                elif isinstance(n, ast.AnnAssign) and n.value is not None:
                    index.setdefault(astscan.name_of(n.target), []).append(n.value)
                elif isinstance(n, ast.arg):
                    index.setdefault(n.arg, []).append(n)
            self._bindings[path] = index
        values = self._bindings[path].get(name, [])
        if values:
            if any(isinstance(v, ast.arg) for v in values):
                return None
            return any(self._makes_app(v, path, depth) for v in values)
        imp = astscan.imports(tree).get(name)
        if imp and imp[1]:
            target = self._modules().find(imp[0], path)
            if target:
                return self._is_app(target, imp[1], depth + 1)
        return None

    def _app_class(self, name, path: str, seen: set) -> bool:
        """FastAPI/APIRouter, under an import alias (APIRouter as Router) or as a class of the snapshot that
        subclasses one (class Slash(APIRouter))."""
        if name in ("FastAPI", "APIRouter"):
            return True
        if not name or name in seen:
            return False
        seen.add(name)
        tree = self._tree(path)
        imp = astscan.imports(tree).get(name) if tree is not None else None
        if imp and imp[1] in ("FastAPI", "APIRouter") and imp[0].split(".")[0] == "fastapi":
            return True
        classes = self._classes.get(name, [])
        return len(classes) == 1 and any(self._app_class(astscan.name_of(b), classes[0][0], seen)
                                         for b in classes[0][1].bases)

    def _makes_app(self, expr, path: str, depth: int) -> bool:
        """The expression builds a FastAPI app/APIRouter, directly or through a function of the snapshot that
        returns one (app = create_application())."""
        if depth > 3 or expr is None:
            return False
        if isinstance(expr, ast.Call):
            fname = astscan.name_of(expr.func)
            if self._app_class(fname, path, set()):
                return True
            defs = self._function_defs().get(fname or "", [])
            if len(defs) == 1:
                fpath, fn = defs[0]
                if fn.returns is not None and astscan.name_of(fn.returns) in ("FastAPI", "APIRouter"):
                    return True
                local = {t.id for n in ast.walk(fn) if isinstance(n, ast.Assign) and self._makes_app(n.value, fpath, depth + 1)
                         for t in n.targets if isinstance(t, ast.Name)}
                return any(isinstance(n, ast.Return) and n.value is not None and (
                    self._makes_app(n.value, fpath, depth + 1) or (isinstance(n.value, ast.Name) and n.value.id in local))
                    for n in ast.walk(fn))
            return False
        if isinstance(expr, ast.Name):
            return self._is_app(path, expr.id, depth + 1) is True
        return False

    def params(self, value, errors):
        if _unknown(value):
            return {"unknown": value["unknown"]}
        if not isinstance(value, list):
            errors.append("params: danh sách (rỗng nếu không có) hoặc {\"unknown\": lý do}")
            return None
        out = []
        for j, p in enumerate(value):
            if not isinstance(p, dict) or not isinstance(p.get("name"), str) or not p["name"]:
                errors.append(f"params[{j}]: cần object có name")
                continue
            place = p.get("in")
            if not ((isinstance(place, str) and place in PARAM_PLACES) or _unknown(place)):
                errors.append(f"params[{j}].in: một trong {sorted(PARAM_PLACES)} hoặc {{\"unknown\": lý do}}")
            where = self.loc(p.get("at"), f"params[{j}].at", errors)
            spelled = p["name"].replace("-", "_") if place == "header" else p["name"]
            if where and not re.search(rf"\b{re.escape(spelled)}\b", self.text(where)) \
                    and not self.has_literal(where, p["name"]):
                errors.append(f"params[{j}].name: '{p['name']}' không có tại {p.get('at')}")
            if place == "path" and p.get("required") is not True:
                errors.append(f"params[{j}].required: tham số path luôn bắt buộc")
            if isinstance(place, str) and any(o["in"] == place and _param_key(place, o["name"]) == _param_key(place, p["name"])
                                              for o in out):  # OpenAPI: (name, in) is unique per operation
                errors.append(f"params[{j}]: trùng tham số {place} '{p['name']}' đã khai ở trên")
            out.append({"name": p["name"], "in": place, "at": where,
                        "type": self.type_or_unknown(p.get("type"), f"params[{j}].type", errors),
                        "required": self.boolean_or_unknown(p, "required", f"params[{j}]", errors),
                        "rule": self.rule(p.get("rule"), f"params[{j}].rule", errors),
                        "nullable": self.boolean_or_unknown(p, "nullable", f"params[{j}]", errors)
                        if "nullable" in p else None})
        return out

    def body(self, value, errors):
        if value is None:
            return None
        if _unknown(value):
            return {"unknown": value["unknown"]}
        if not isinstance(value, dict) or not isinstance(value.get("models"), list):
            errors.append("request_body: null, {\"unknown\": lý do} hoặc object có models")
            return None
        where = self.loc(value.get("at"), "request_body.at", errors)
        for mid in value["models"]:
            if not isinstance(mid, str) or not MODEL_ID.fullmatch(mid):
                errors.append("request_body.models: phần tử dạng 'file.py::Class'")
            elif where and mid.split("::")[1] not in self.text(where):
                errors.append(f"request_body.models: không thấy {mid.split('::')[1]} tại {value.get('at')}")
        media = value.get("media_type")
        if media not in ("application/json", *FORM_MEDIA):
            errors.append("request_body.media_type: application/json | multipart/form-data | application/x-www-form-urlencoded")
        req = value.get("required")
        if not isinstance(req, bool) and not _unknown(req):
            errors.append("request_body.required: true/false hoặc {\"unknown\": lý do}")
        embedded = value.get("embedded") is True
        # The wire shape needs the top-level keys whenever it is not one model: Form/File fields, or an embedded body
        fields = []
        needs_fields = media in FORM_MEDIA or embedded
        if media in FORM_MEDIA and embedded:
            errors.append("request_body.embedded: chỉ dùng cho body JSON; Form/File ghi các trường ở fields")
        body_type = None
        if not value["models"] and media not in FORM_MEDIA and not embedded:
            if value.get("type") is None:  # payload: dict = Body(...), items: list[int]: the declared type is the body
                errors.append("request_body: body JSON không có model cần \"type\": kiểu đã khai (dict -> object, "
                              "list[int] -> array[integer]); models rỗng chỉ dùng cho Form/File")
            else:
                body_type = self.type_or_unknown(value["type"], "request_body.type", errors)
        elif not value["models"] and media not in FORM_MEDIA:
            errors.append("request_body.models: rỗng chỉ dùng cho Form/File hoặc body JSON có \"type\"")
        if needs_fields:
            raw = value.get("fields")
            if not isinstance(raw, list) or not raw:
                errors.append("request_body.fields: cần các khóa cấp trên cùng của body (Form/File hoặc body được bọc)")
                raw = []
            for j, f in enumerate(raw):
                if not isinstance(f, dict) or not isinstance(f.get("name"), str) or not f["name"]:
                    errors.append(f"request_body.fields[{j}]: cần object có name")
                    continue
                fat = self.loc(f.get("at"), f"request_body.fields[{j}].at", errors)
                if fat and not re.search(rf"\b{re.escape(f['name'])}\b", self.text(fat)) and not self.has_literal(fat, f["name"]):
                    errors.append(f"request_body.fields[{j}].name: '{f['name']}' không có tại {f.get('at')}")
                fields.append({"name": f["name"], "at": fat,
                               "type": self.type_or_unknown(f.get("type"), f"request_body.fields[{j}].type", errors),
                               "required": self.boolean_or_unknown(f, "required", f"request_body.fields[{j}]", errors)})
        param = value.get("param")
        if param is not None and (not isinstance(param, str) or (where and not re.search(rf"\b{re.escape(param)}\b", self.text(where)))):
            errors.append("request_body.param: tên tham số body phải có tại vị trí đã dẫn")
        return {"models": value["models"], "fields": fields, "media_type": media, "required": req, "at": where,
                "type": body_type,
                "param": param if isinstance(param, str) else None,
                "embedded": embedded, "rule": self.rule(value.get("rule"), "request_body.rule", errors)}

    def response(self, value, errors):
        if value is None:
            return None
        if _unknown(value):
            return {"unknown": value["unknown"]}
        if isinstance(value, dict) and "type" in value and "model" not in value:  # bool, Any, list[int]: not a model
            where = self.loc(value.get("at"), "response.at", errors)
            t = self.type_(value.get("type"), "response.type", errors)
            if t and _model_refs(t):
                errors.append("response.type: kiểu có model thì dùng \"model\"")
            return {"type": t, "at": where, "rule": self.rule(value.get("rule"), "response.rule", errors),
                    "media_type": value.get("media_type") if isinstance(value.get("media_type"), str) else "application/json"}
        if isinstance(value, dict) and isinstance(value.get("external"), str) and value["external"].strip():
            # a generic model class of a library outside the snapshot, as in PaginatedListResponse[Item]: the name
            # and the arguments are read from the source; its fields are not
            where = self.loc(value.get("at"), "response.at", errors)
            short = value["external"].rsplit(".", 1)[-1]
            if where and not re.search(rf"\b{re.escape(short)}\b", self.text(where)):
                errors.append(f"response.external: không thấy {short} tại {value.get('at')}")
            args = self._type_args(value, where, errors)
            return {"external": value["external"], "args": args, "array": value.get("array") is True, "at": where,
                    "rule": self.rule(value.get("rule"), "response.rule", errors)}
        if not isinstance(value, dict) or not isinstance(value.get("model"), str) or not MODEL_ID.fullmatch(value["model"]):
            errors.append("response: null, {\"unknown\": lý do}, {\"model\": 'file.py::Class', ...} hoặc {\"type\": T, ...}")
            return None
        where = self.loc(value.get("at"), "response.at", errors)
        if where and value["model"].split("::")[1] not in self.text(where):
            errors.append(f"response.model: không thấy {value['model'].split('::')[1]} tại {value.get('at')}")
        args = self._type_args(value, where, errors)
        return {"model": value["model"], "args": args, "array": value.get("array") is True, "at": where,
                "rule": self.rule(value.get("rule"), "response.rule", errors)}

    def _type_args(self, value, where, errors) -> list:
        """Generic[Arg, ...]: each argument in the type notation, its model names on the cited line."""
        args = []
        if value.get("args") is None:
            return args
        if not isinstance(value["args"], list) or not value["args"]:
            errors.append("response.args: danh sách kiểu đối số của model generic, ví dụ [\"file.py::Item\"]")
            return args
        for j, raw in enumerate(value["args"]):
            t = self.type_(raw, f"response.args[{j}]", errors)
            for m in _model_refs(t) if t else []:
                if where and m.split("::")[1] not in self.text(where):
                    errors.append(f"response.args[{j}]: không thấy {m.split('::')[1]} tại {value.get('at')}")
            if t:
                args.append(t)
        return args

    def status(self, value, dec, errors):
        if _unknown(value):
            return {"unknown": value["unknown"]}
        codes = value.get("codes") if isinstance(value, dict) else None
        if not isinstance(codes, list) or not codes or not all(isinstance(c, int) and 100 <= c <= 599 for c in codes):
            errors.append("status: {\"codes\": [mã], \"at\": ..., \"rule\": tên|null} hoặc {\"unknown\": lý do}")
            return None
        rule = self.rule(value.get("rule"), "status.rule", errors)
        where = self.loc(value.get("at"), "status.at", errors) if value.get("at") else dec
        if not where or not dec:
            return None
        text = self.text(where)
        inside = where[0] == dec[0] and dec[1] <= where[1] and where[2] <= dec[2]
        app_default = rule == "fastapi.response_class_default_status" and "default_response_class" in text
        if not inside and not app_default:
            errors.append("status.at: phải nằm trong decorator của route (trừ default_response_class của app/router)")
        elif rule == "fastapi.default_status_200":
            if codes != [200] or "status_code" in text or "response_class" in text:
                errors.append("status: quy tắc mặc định 200 chỉ dùng khi decorator không khai status_code hay response_class")
        elif rule == "fastapi.response_class_default_status":
            if "status_code" in text or "response_class" not in text:
                errors.append("status: quy tắc response_class cần response_class/default_response_class và không có status_code")
        elif rule == "fastapi.status_constant":
            if not all(re.search(rf"HTTP_{c}_\w+", text) for c in codes):
                errors.append("status: không thấy hằng HTTP_<mã>_… tại vị trí đã dẫn")
        elif not all(re.search(rf"status_code\s*=\s*{c}(?!\d)", text) for c in codes):
            errors.append("status: không thấy status_code=<mã> tại vị trí đã dẫn; nếu suy từ mặc định thì ghi rule")
        return {"codes": codes, "rule": rule, "at": where}

    # ---- HTTP, roles, limitations, dismissals

    def add_http(self, item) -> list:
        errors = []
        where = self.loc(item.get("at"), "at", errors)
        lib = item.get("library")
        if not isinstance(lib, str) or lib not in HTTP_LIBS:
            errors.append(f"library: một trong {sorted(HTTP_LIBS)}; thư viện khác nộp ở limitations")
            lib = None
        tree = self._tree(where[0]) if where else None
        imported = {mod.split(".")[0] for mod, _ in astscan.imports(tree).values()} if tree is not None else set()
        made = self.loc(item.get("client_at"), "client_at", errors) if item.get("client_at") else None
        if made and lib and (lib not in self.tools.raw[made[0]]
                             or not re.search(rf"\b{lib}\b|Client|Session", self.text(made))):
            errors.append(f"client_at: dòng đã dẫn không tạo client {lib}")
            made = None
        missing_import = bool(where and lib and lib not in imported and not re.search(
            rf"^\s*(import|from)\s+{lib}\b", self.tools.raw[where[0]], re.M) and made is None and not item.get("client_at"))
        method = item.get("method")
        node = None
        scan = self._http_scan(where[0]) if where else None
        aliases = scan.function_verb if scan is not None else {}
        candidates = astscan.calls_at(tree, where[1], where[2], names=aliases) if tree is not None and where else []
        if scan is not None and tree is not None and where:  # to_thread(c.get, url), self.fetch(url)
            candidates += scan.virtual_calls(tree, where[1], where[2])
        if candidates:  # read from the syntax tree: comments, other statements and line breaks cannot mislead
            if not ((isinstance(method, str) and method in METHODS) or _unknown(method)):
                errors.append("method: method HTTP viết hoa hoặc {\"unknown\": lý do}")
            verb = method.lower() if isinstance(method, str) else None
            ordered = [c for c in candidates if astscan.call_verb(c, aliases) == verb] + \
                [c for c in candidates if astscan.call_verb(c, aliases) != verb]
            found = None
            for c in ordered:  # two calls on one line: the claim is about the one it matches
                problems = self._http_call_problems(where, c, lib, method, item.get("target"), made)
                if not problems:
                    node, found = c, []
                    break
                if found is None:
                    node, found = c, problems
            errors += found
            call = None
            scan = self._http_scan(where[0])
            if missing_import and node is not None and isinstance(node.func, ast.Attribute) and scan is not None \
                    and scan.claim_client(node.func.value, node) and scan.receiver_lib(node.func.value, node) == lib:
                missing_import = False  # a client of this very library, handed over by a helper or module
        else:
            call = re.search(r"(?:\.|\b)(get|post|put|patch|delete|head|options|request|stream|send)\s*\(",
                             self.text(where)) if where else None
            if where and not call:
                errors.append("at: dòng không có lời gọi .get/.post/…/.request/.stream(")
            if not ((isinstance(method, str) and method in METHODS) or _unknown(method)):
                errors.append("method: method HTTP viết hoa hoặc {\"unknown\": lý do}")
        if missing_import:
            errors.append(f"library: file {where[0]} không import {lib}; nếu client tạo ở file khác thì thêm "
                          "client_at là dòng tạo client đó")
        if call and isinstance(method, str):
            verb = call.group(1)
            rest = self.text(where)[call.end():]
            kw = re.search(r"\bmethod\s*=\s*", rest)
            args = self.literals(rest[kw.end():] if kw else rest)
            if verb in ("request", "stream") and (not args or args[0].upper() != method):
                errors.append(f"method: method của .{verb}( không phải '{method}'")
            elif verb not in ("request", "stream") and verb != method.lower():
                errors.append(f"method: lời gọi là .{verb}(, không phải {method}")
        target = item.get("target")
        if where and isinstance(target, dict) and self._hidden(where, target.get("value")):
            errors.append("target.value: giá trị nằm ở phần dòng bị cắt, model chưa được gửi; ghi kind unknown kèm lý do")
        config_at = None
        kind = target.get("kind") if isinstance(target, dict) else None
        if kind in ("literal", "config") and has_secret(target.get("value")):
            errors.append("target.value: giá trị chứa bí mật; dùng đúng bản đã che mà read_file trả về")
        elif kind == "literal":
            if node is None and call and not self._url_argument(where, call, target.get("value")):
                whole = self._call_span(where, call)  # a call split over lines: its arguments follow
                if not (whole and self._url_argument(whole, call, target.get("value"))):
                    errors.append("target.value: URL phải là đối số URL của lời gọi (url= hoặc đối số vị trí đúng)")
        elif kind == "config":
            value = target.get("value") if isinstance(target.get("value"), str) and target["value"] else None
            config_at = self.loc(target["config_at"], "target.config_at", errors) if target.get("config_at") else None
            other = self._config_builds_other(where[0], node.func.value, config_at) \
                if config_at and node is not None and isinstance(node.func, ast.Attribute) else None
            base_urls = self._base_urls(config_at) if config_at else None
            if config_at and not (value and (value in set().union(*[_config_names(b) for b in base_urls])
                                             if base_urls else value in self.text(config_at) and "base_url" in self.text(config_at))):
                errors.append("target.config_at: dòng phải tạo client với base_url= dùng khóa cấu hình này")
            elif other:
                errors.append(f"target.config_at: dòng {config_at[0]}:{config_at[1]} tạo client {other}, "
                              "không phải client của lời gọi")
            elif not config_at and where and not (value and value in (
                    self.text((where[0], where[1], max(where[2], node.end_lineno))) if node is not None else self.text(where))):
                errors.append("target.value: khóa cấu hình phải xuất hiện tại lời gọi; nếu URL tương đối trên client "
                              "tạo với base_url=settings.X thì thêm config_at là dòng base_url đó")
        elif kind == "unknown":
            if not isinstance(target.get("reason"), str) or not target["reason"]:
                errors.append("target.reason: cần lý do khi đích chỉ biết lúc chạy")
        else:
            errors.append("target: {kind: literal|config|unknown, value | reason}")
        if errors:
            return errors
        # one claim per call: two calls on one line are two items (the column tells them apart)
        self.http[where + (node.col_offset,) if node is not None else where] = {
            "at": where, "library": lib, "method": method, "target": target,
                            "config_at": config_at if kind == "config" else None}
        return []

    def _base_urls(self, where) -> list:
        """The base_url= values of the calls on the cited lines; [] when the file does not parse or has none."""
        tree = self._tree(where[0])
        return [k.value for n in ast.walk(tree) if isinstance(n, ast.Call) and n.lineno <= where[2]
                and (n.end_lineno or n.lineno) >= where[1] for k in n.keywords if k.arg == "base_url"] if tree is not None else []

    def _config_builds_other(self, path, recv, config_at) -> str | None:
        """The name config_at's statement binds when it is plainly another client than the call's receiver
        (a = httpx.Client(base_url=settings.A) cited for b.get); None when it is the receiver, or cannot be told
        (a provider's return, an attribute chain)."""
        names = {astscan.name_of(recv)} - {None}
        tree = self._tree(path)
        if isinstance(recv, ast.Name) and tree is not None:
            imp = astscan.imports(tree).get(recv.id)
            if imp and imp[1]:
                names.add(imp[1])  # from clients import wire as w
            for n in ast.walk(tree):  # c = a: a builds c
                if isinstance(n, ast.Assign) and isinstance(n.value, ast.Name):
                    bound = {t.id for t in n.targets if isinstance(t, ast.Name)}
                    if bound & names:
                        names.add(n.value.id)
        stmts = [n for n in ast.walk(self._tree(config_at[0]) or ast.Module(body=[], type_ignores=[]))
                 if isinstance(n, ast.stmt) and n.lineno <= config_at[1] <= (n.end_lineno or n.lineno)]
        stmt = max(stmts, key=lambda n: n.lineno, default=None)
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            bound = {astscan.name_of(t) for t in (stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target])}
        elif isinstance(stmt, (ast.With, ast.AsyncWith)):
            bound = {astscan.name_of(i.optional_vars) for i in stmt.items if i.optional_vars is not None
                     and i.context_expr.lineno <= config_at[1] <= (i.context_expr.end_lineno or i.context_expr.lineno)}
        else:
            return None
        if not names or not bound or None in bound:
            return None
        if bound & names:
            if isinstance(recv, ast.Attribute) and astscan.name_of(recv.value) == "self" and config_at[0] == path:
                classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                around = lambda line: max((c for c in classes if c.lineno <= line <= (c.end_lineno or c.lineno)),  # noqa: E731
                                          key=lambda c: c.lineno, default=None)
                mine, theirs = around(recv.lineno), around(config_at[1])
                if mine is not None and theirs is not None and mine is not theirs:
                    return f"self.{recv.attr} của class {theirs.name}"
            return None
        return sorted(bound)[0]

    def _http_call_problems(self, where, node, lib, method, target, client_at=None) -> list:
        """Method, URL argument and library of one call, read from its syntax tree."""
        errors = []
        path = where[0]
        scan = self._http_scan(path)
        verb = astscan.call_verb(node, scan.function_verb if scan is not None else None)
        base = astscan.root_name(node.func.value) if isinstance(node.func, ast.Attribute) else node.func.id
        module = scan.module_of.get(base) if isinstance(node.func, ast.Attribute) else (
            (scan.function_lib.get(base) if scan is not None else None)
            or astscan.imports(self._tree(path)).get(base, ("", ""))[0].split(".")[0] or None)
        if lib and module in astscan.HTTP_LIBS and module != lib:
            errors.append(f"library: lời gọi đi qua {module}, không phải {lib}")
        if isinstance(node.func, ast.Attribute) and scan is not None:
            recv_lib = scan.receiver_lib(node.func.value, node)
            if lib and recv_lib and recv_lib != lib:
                errors.append(f"library: client của lời gọi được tạo từ {recv_lib}, không phải {lib}")
        if isinstance(node.func, ast.Attribute) and client_at:
            recv_name = astscan.name_of(node.func.value) or astscan.root_name(node.func.value)
            if recv_name and not re.search(rf"\b{re.escape(recv_name)}\b", self.text(client_at)):
                errors.append(f"client_at: dòng {client_at[0]}:{client_at[1]} không tạo/gán {recv_name} của lời gọi")
            elif scan is not None and client_at[0] == path and isinstance(node.func.value, ast.Name):
                at_fn, call_fn = scan._enclosing(client_at[1]), scan._enclosing(node.lineno)
                if at_fn is not None and at_fn is not call_fn:  # cache in remote() is not cache in local()
                    errors.append(f"client_at: dòng {client_at[0]}:{client_at[1]} nằm trong hàm khác với lời gọi")
        if isinstance(node.func, ast.Attribute) and scan is not None and not client_at:
            recv = node.func.value
            name = astscan.name_of(recv) if isinstance(recv, (ast.Name, ast.Attribute)) else astscan.root_name(recv)
            # a claim needs a client the file shows (or client_at); a name like `session` only makes a suspect
            if not scan.claim_client(recv, node):
                errors.append(f"at: {name or 'đối tượng'}.{verb}( không gọi trên client HTTP thấy được trong file; "
                              "nếu client được tạo/truyền từ nơi khác thì thêm client_at là dòng tạo client")
        args, kws = node.args, {k.arg: k.value for k in node.keywords if k.arg}
        if verb in ("request", "stream"):
            mexpr = kws.get("method", args[0] if args else None)
            if isinstance(method, str):
                if not (isinstance(mexpr, ast.Constant) and isinstance(mexpr.value, str)):
                    errors.append(f"method: method của .{verb}( là biểu thức chỉ biết lúc chạy; ghi {{\"unknown\": lý do}}")
                elif mexpr.value.upper() != method:
                    errors.append(f"method: method của .{verb}( là '{mexpr.value.upper()}', không phải '{method}'")
            url = kws.get("url", args[1] if "method" not in kws and len(args) > 1 else args[0] if "method" in kws and args else None)
        elif verb == "send":
            inner = next((c for a in args for c in ast.walk(a) if isinstance(c, ast.Call)
                          and astscan.name_of(c.func) in ("Request", "build_request")), None)
            if isinstance(method, str) and not (inner and inner.args and isinstance(inner.args[0], ast.Constant)
                                                and str(inner.args[0].value).upper() == method):
                errors.append("method: .send( không cho thấy method; ghi {\"unknown\": lý do}")
            url = (inner.args[1] if inner and len(inner.args) > 1 else None) if inner else None
        else:
            if isinstance(method, str) and verb != method.lower():
                errors.append(f"method: lời gọi là .{verb}(, không phải {method}")
            url = kws.get("url", args[0] if args else None)
        if isinstance(target, dict) and target.get("kind") == "config" and target.get("config_at") \
                and isinstance(url, ast.Constant) and isinstance(url.value, str) and re.match(r"https?://", url.value):
            errors.append("target.config_at: lời gọi dùng URL tuyệt đối nên base_url của client không quyết định đích; "
                          "ghi literal")
        if isinstance(target, dict) and target.get("kind") == "config" and not target.get("config_at") and url is not None:
            if not (isinstance(target.get("value"), str) and target["value"] in _config_names(url)):
                errors.append("target.value: khóa cấu hình phải nằm trong đối số URL của lời gọi (không phải headers=, "
                              "params=...); URL tương đối trên client base_url=settings.X thì dùng config_at")
        if isinstance(target, dict) and target.get("kind") == "literal":
            value = target.get("value")
            ok = isinstance(url, ast.Constant) and url.value == value
            if ok and not self.tools.was_delivered(path, node.lineno, url.end_lineno):
                ok = False
            if not ok and isinstance(url, ast.Constant) and isinstance(value, str) and has_secret(url.value):
                ok = self.shown((path, url.lineno, url.end_lineno)).find(value) >= 0  # the masked text the model saw
            if not ok:
                errors.append("target.value: URL phải là đối số URL của chính lời gọi này (url= hoặc đối số vị trí), "
                              "nguyên một literal; URL ghép hoặc lấy từ biến thì dùng config/unknown")
        return errors

    def _http_scan(self, path: str):
        """Client and HTTP-function names of one file, with clients imported from other files of the snapshot."""
        if path not in self._scans:
            tree = self._tree(path)
            if tree is None:
                self._scans[path] = None
            else:
                imported, makers, providers, qualified, aliases, inherited = {}, {}, {}, {}, {}, {}
                for local, (mod, name) in astscan.imports(tree).items():
                    # import clients / from app import clients: clients.wire is a client of that module
                    module = self._modules().find(f"{mod}.{name}" if name else mod, path)
                    if module and self._tree(module) is not None:
                        prefix = local if name or local != mod.split(".")[0] else mod
                        qualified.update({f"{prefix}.{c}": lib for c, lib in self._exports(module)[0].items()})
                    target = self._modules().find(mod, path) if name else None
                    if target and self._tree(target) is not None:
                        target, name = self._origin(target, name)  # infra/__init__.py: from .transport import wire
                        clients, classes, handed, found, attrs = self._exports(target)
                        if name in attrs:  # class GitHub(BaseAPI): BaseAPI sets self._client
                            inherited[local] = attrs[name]
                        if name in clients:
                            imported[local] = clients[name]
                        if name in found:
                            aliases[local] = found[name]
                        if name in classes:  # a client class of the repository: InventoryClient(httpx.AsyncClient)
                            makers[local] = classes[name]
                        if name in handed:
                            providers[local] = handed[name]  # def get_wire(): with httpx.Client() as c: yield c
                state = self._state_clients() if ".state." in self.tools.raw[path] else set()
                state = set(state) | {a for c in ast.walk(tree) if isinstance(c, ast.ClassDef)
                                      for b in c.bases for a in inherited.get(astscan.name_of(b), ())}
                state |= {a for c in ast.walk(tree) if isinstance(c, ast.ClassDef)  # class Bot(TokenMixin) sets it
                          for a in self._subclass_attrs().get(c.name, ())}
                self._scans[path] = astscan.HttpScan(self.tools.raw[path], tree, imported, makers, providers, state,
                                                     qualified, aliases)
        return self._scans[path]

    def _state_clients(self) -> set:
        """Attributes set to an HTTP client on an app state (app.state.wire = wire in a lifespan), read elsewhere
        as request.app.state.wire."""
        if self._states is None:
            self._states = set()
            for path, tree in self._trees.items():
                if ".state." not in self.tools.raw[path] or not any(lib in self.tools.raw[path] for lib in HTTP_LIBS):
                    continue
                scan = astscan.HttpScan(self.tools.raw[path], tree)
                for n in ast.walk(tree):
                    if isinstance(n, ast.Assign):
                        for t in n.targets:
                            if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Attribute) and t.value.attr == "state" \
                                    and (scan.makes(n.value, scan.maker_functions)
                                         or (isinstance(n.value, ast.Name) and n.value.id in scan.clients)):
                                self._states.add(t.attr)
        return self._states

    def _subclass_attrs(self) -> dict:
        """class name -> client attributes its subclasses set (class Bot(TokenMixin): self.session = ClientSession()):
        the mixin's self.session is that client at run time."""
        if getattr(self, "_mixins", None) is None:
            self._mixins = {}
            self._function_defs()
            for path, tree in self._trees.items():
                attrs = self._exports(path)[4]
                for c in ast.walk(tree):
                    if isinstance(c, ast.ClassDef) and c.name in attrs:
                        for b in c.bases:
                            self._mixins.setdefault(astscan.name_of(b), set()).update(attrs[c.name])
        return self._mixins

    def _origin(self, path: str, name: str, depth: int = 0) -> tuple:
        """(file, name) where an imported name is defined, following re-exports such as a package __init__.py
        holding `from .transport import wire`."""
        if depth > 4 or any(name in d for d in self._exports(path)):
            return path, name
        imp = astscan.imports(self._tree(path)).get(name)
        source = self._modules().find(imp[0], path) if imp and imp[1] else None
        if source and source != path and self._tree(source) is not None:
            return self._origin(source, imp[1], depth + 1)
        return path, name

    def _exports(self, path: str) -> tuple:
        """What other files can import from `path`, read once: (module clients, client classes, client providers,
        Annotated client aliases) each name -> library, and classes -> the attributes they set to a client
        (self._client = httpx.AsyncClient() in a base class)."""
        if path not in self._clients:
            tree, raw = self._tree(path), self.tools.raw[path]
            if not any(lib in raw for lib in HTTP_LIBS) and ".state." not in raw:
                self._clients[path] = ({}, {}, {}, {}, {})
            else:  # get_http(request): return request.app.state.http hands out a client too
                scan = astscan.HttpScan(raw, tree, state_clients=self._state_clients() if ".state." in raw else set())
                attrs = {c.name: {t.attr for n in ast.walk(c) if isinstance(n, ast.Assign) and scan.makes(n.value, scan.maker_functions)
                                  for t in n.targets if isinstance(t, ast.Attribute) and astscan.name_of(t.value) == "self"}
                         for c in ast.walk(tree) if isinstance(c, ast.ClassDef)}
                self._clients[path] = (astscan.module_clients(tree, raw, scan), astscan.client_classes(tree),
                                       {f: scan.maker_function_lib.get(f) for f in scan.maker_functions},
                                       scan.client_aliases, {k: v for k, v in attrs.items() if v})
        return self._clients[path]

    def _url_argument(self, where, call, value) -> bool:
        if not isinstance(value, str):
            return False
        for text in (self.text(where), self.shown(where)):
            rest = text[call.end():]
            kw = re.search(r"\burl\s*=\s*", rest)
            if kw and value in self.literals(rest[kw.end():])[:1]:
                return True
            args = rest
            if call.group(1) in ("request", "stream") and not re.search(r"\bmethod\s*=", rest):
                m = STRING.match(rest.lstrip())  # skip the method literal and its comma
                args = rest.lstrip()[m.end():].lstrip().lstrip(",") if m else ""
            first = STRING.match(args.lstrip())
            if first and self.literals(first.group(0)) == [value]:
                return True
        return False

    def add_role(self, item) -> list:
        errors = []
        path, role = item.get("file"), item.get("role")
        if not isinstance(path, str) or path not in self.tools.state:
            return [f"file: {path!r} không thuộc phạm vi đọc"]
        if not isinstance(role, str) or role not in ROLES:
            return [f"role: một trong {ROLES}"]
        where = None
        if not self.tools.lines[path]:
            return ["file rỗng thuộc component Khác theo FR-028; không nộp vai trò cho file này"]
        if self.tools.lines[path]:  # every non-empty file cites a line, Khác included (AC-07)
            where = self.loc(item.get("at"), "at", errors)
            if where and where[0] != path:
                errors.append("at: phải nằm trong chính file đó")
                where = None
            if where and role in ROLE_SIGNALS and not ROLE_SIGNALS[role].search(self.text(where)):
                errors.append(f"at: dòng không có dấu hiệu của vai trò {role} theo FR-029")
            if where and role in ("Hạ tầng", "Truy cập dữ liệu") and IMPORT_LINE.match(self.text(where)):
                errors.append("at: dòng import không phải dấu hiệu; dẫn dòng tạo kết nối hoặc gọi session/truy vấn")
        rank = ROLES.index(role)
        raw = "\n".join(self.tools.lines[path])
        for earlier in ORDER_SIGNALS:
            hit = ROLE_SIGNALS[earlier].search(raw) if ROLES.index(earlier) < rank else None
            if hit and not item.get("not_signal"):
                line = raw.count("\n", 0, hit.start()) + 1
                errors.append(f"role: file có dấu hiệu {earlier} ở dòng {line}, đứng trước {role}; nếu đó không phải "
                              "dấu hiệu thật thì nộp lại kèm not_signal: lý do")
                break
        call_path = []
        if role == "Service":
            cp = item.get("call_path")
            if not isinstance(cp, list) or len(cp) < 2:
                errors.append("call_path: Service cần đường gọi ≥2 vị trí, từ route tới truy cập dữ liệu/hạ tầng")
            else:
                call_path = [self.loc(x, f"call_path[{j}]", errors) for j, x in enumerate(cp)]
                if all(call_path) and not any(w[0] == path for w in call_path):
                    errors.append("call_path: phải đi qua chính file này")
                for j in range(len(call_path) - 1) if all(call_path) else ():  # each step reaches the next one
                    names = self._step_names(call_path[j + 1])
                    if not names:
                        errors.append(f"call_path[{j + 1}]: {cp[j + 1]} không nằm trong hàm nào; dẫn dòng trong thân hàm")
                    elif not self._reaches(STRING.sub('""', self.text(call_path[j])), names):
                        errors.append(f"call_path[{j}]: từ dòng {cp[j]} không tới được {'/'.join(names)} (hàm chứa "
                                      f"{cp[j + 1]}) qua tối đa {CALL_DEPTH} lời gọi; dẫn dòng gọi ở mỗi bước")
        if errors:
            return errors
        self.roles[path] = {"file": path, "role": role, "at": where, "call_path": call_path,
                            "reason": item.get("reason") if isinstance(item.get("reason"), str) else None,
                            "not_signal": item.get("not_signal") if isinstance(item.get("not_signal"), str) else None}
        return []

    def _step_names(self, where) -> list[str]:
        """What a call path step is reached through: the functions holding the line (a closure and the factory
        around it), or the names a module-level line assigns (engine = create_engine(...))."""
        tree = self._tree(where[0])
        if tree is None:
            return []
        fns = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and n.lineno <= where[1] <= (n.end_lineno or n.lineno)]  # a method is also reached through its class:
        return fns or [t.id for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign))  # Cls(...), Depends(Cls())
                       and n.lineno <= where[1] <= (n.end_lineno or n.lineno)
                       for t in (n.targets if isinstance(n, ast.Assign) else [n.target]) if isinstance(t, ast.Name)]

    def _reaches(self, code: str, targets: list[str]) -> bool:
        """A name on the cited line is one of `targets`, or calls into one within CALL_DEPTH calls. Calls are
        matched by name only (any function of that name), so this refuses unrelated steps, it does not prove a path."""
        want = set(targets)
        seen = frontier = set(re.findall(r"\w+", code))
        for _ in range(CALL_DEPTH + 1):
            if frontier & want:
                return True
            frontier = {c for n in frontier for c in self._call_graph().get(n, ())} - seen
            seen = seen | frontier
        return False

    def _call_graph(self) -> dict:
        """function name -> names it calls or hands to Depends/Security, over every function of that name."""
        if getattr(self, "_calls", None) is None:
            self._calls = {}
            for name, defs in self._function_defs().items():
                out = self._calls.setdefault(name, set())
                for _, fn in defs:
                    for n in ast.walk(fn):
                        if isinstance(n, ast.Call):
                            out.add(astscan.name_of(n.func))
                            if astscan.name_of(n.func) in ("Depends", "Security"):
                                out.update(astscan.name_of(a) for a in n.args)
                out.discard(None)
        return self._calls

    def add_limit(self, item) -> list:
        errors = []
        kind = item.get("kind")
        if not isinstance(kind, str) or kind not in LIMIT_KINDS:
            return [f"kind: một trong {sorted(LIMIT_KINDS)}"]
        where = self.loc(item.get("at"), "at", errors)
        if where and kind != "unsupported_http_library" and not re.search(rf"\.{kind}\s*\(", self.text(where)):
            errors.append(f"at: không thấy lời gọi .{kind}( tại vị trí đã dẫn")
        if errors:
            return errors
        self.limits[(kind, where)] = {"kind": kind, "at": where,
                                      "detail": item.get("detail") if isinstance(item.get("detail"), str) else ""}
        return []

    def add_dismissed(self, item) -> list:
        """A suspect line that is not a route/registration/HTTP call, with the reason (kept in result.json)."""
        errors = []
        where = self.loc(item.get("at"), "at", errors)
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            errors.append("reason: cần lý do vì sao dòng này không phải route/đăng ký route/lời gọi HTTP")
        reg = re.search(r"([\w.]+)\.(add_api_route|add_route|add_websocket_route)\s*\(", self.text(where)) if where else None
        if reg:
            name = reg.group(1).split(".")[-1]
            built = re.findall(rf"^\s*{re.escape(name)}\s*(?::[^=\n]*)?=\s*(.+)$", "\n".join(self.tools.lines[where[0]]), re.M)
            if any(re.search(r"FastAPI\s*\(|APIRouter\s*\(", rhs) for rhs in built):
                errors.append(f"dismissed: {name} là FastAPI/APIRouter tạo ở file này; lời gọi {reg.group(2)} phải vào limitations")
        if errors:
            return errors
        self.dismissed[(where[0], where[1])] = {"at": where, "reason": item["reason"]}
        return []

    # ---------------------------------------------------------------- whole-set checks

    def suspects(self) -> list[dict]:
        """Lines that look like a route, a non-decorator registration or an HTTP call and are not accounted for."""
        covered = set()
        for r in self.routes.values():
            path, start, end = r["decorator"]
            for i in range(start, end + 1):
                line = self.tools.lines[path][i - 1]
                if line.lstrip().startswith("@") and (re.search(rf"\.{r['method'].lower()}\s*\(", line)
                                                      or (".api_route" in line and r["method"] in self.literals(line))):
                    covered.add((path, i))
        claimed_calls = Counter((w[0], w[1]) for w in self.http)
        covered |= {(w[0], w[1]) for (_, w) in self.limits}
        covered |= set(self.dismissed)
        out = []
        for path in self.tools.readable:
            if not path.endswith(".py"):
                continue
            raw = "\n".join(self.tools.lines[path])
            in_string = astscan.string_rows(raw)  # an example inside a docstring is not code
            scan = self._http_scan(path)
            if scan is not None:  # calls on HTTP modules, clients and imported HTTP functions, read from the tree
                http_lines = scan.http_lines(self._tree(path)) if scan.capable else Counter()
            else:  # a file that does not parse: every .get(-like line of a file importing an HTTP library
                http_file = any(re.search(rf"^\s*(import|from)\s+[\w., ]*\b{lib}\b", raw, re.M) for lib in HTTP_LIBS)
                http_lines = Counter(i for i, line in enumerate(self.tools.lines[path], 1)
                                     if http_file and SUSPECTS["http"].search(line))
            for i, line in enumerate(self.tools.lines[path], 1):
                if (path, i) in covered or line.lstrip().startswith("#") or i in in_string:
                    continue
                for kind, rx in SUSPECTS.items():
                    if kind == "http":  # a line with more HTTP calls than claims stays a suspect
                        if http_lines.get(i, 0) > claimed_calls.get((path, i), 0) and not SUSPECTS["route"].search(line):
                            out.append({"at": f"{path}:{i}", "looks_like": kind})
                            break
                        continue
                    if rx.search(line):
                        out.append({"at": f"{path}:{i}", "looks_like": kind})
                        break
        return out

    def open_problems(self, components: list[dict]) -> list[str]:
        """Cross-item gaps the agent must fix before finishing; empty when the set is consistent."""
        out = []
        known_models = set(self.models)
        for r in self.routes.values():
            out += [f"Route {r['method']} {r['handler']}: model {m} chưa được nộp" for m in route_model_refs(r)
                    if m not in known_models]
        for m in self.models.values():
            for f in m["fields"]:
                out += [f"Model {m['id']}.{f['name']}: model lồng {x} chưa được nộp" for x in _model_refs(f["type"])
                        if x not in known_models]
        listed = {p for c in components if c.get("kind", "normal") == "normal" for p in c["files"]}
        out += [f"Chưa có vai trò cho file {p}" for p in self.tools.readable  # an empty file takes no role (add_role)
                if p in listed and p.endswith(".py") and p not in self.roles and self.tools.lines[p]]
        route_files = {r["decorator"][0] for r in self.routes.values()}
        data_files = {p for p, x in self.roles.items() if x["role"] in ("Truy cập dữ liệu", "Hạ tầng")}
        for x in self.roles.values():
            if x["role"] == "Service" and x["call_path"]:
                if x["call_path"][0][0] not in route_files or x["call_path"][-1][0] not in data_files:
                    out.append(f"Service {x['file']}: call_path phải bắt đầu ở file route và kết thúc ở file "
                               "Truy cập dữ liệu/Hạ tầng")
        out += [f"Dòng {s['at']} trông giống {s['looks_like']} nhưng chưa có item nào; nộp item, hoặc nộp dismissed "
                "kèm lý do" for s in self.suspects()]
        for r in self.routes.values():
            if not isinstance(r["params"], list) or not isinstance(r["dependencies"], list):
                continue
            have = {(p["in"], _param_key(p["in"], p["name"])) for p in r["params"]}
            route_path = "".join(p["value"] or "" for p in r["parts"])
            for target, at in self._handler_depends(r["decorator"]):  # Depends(verify) the agent left out
                if not any(_same_dependency(target, d["name"]) or _same_dependency(d["name"], target)
                           for d in r["dependencies"]):
                    out.append(f"Route {r['method']} {r['handler']}: Depends({target}) tại {at} áp dụng cho route nhưng "
                               "chưa khai dependency này; thêm vào dependencies")
            for d in r["dependencies"]:
                for place, name, at in self.dependency_params(d["name"], set(), self._called_at(d["name"], d["at"]),
                                                              d["at"][0] if d["at"] else None):
                    if place == "query" and re.search(r"\{" + re.escape(name) + r"(:[^}]*)?\}", route_path):
                        place = "path"  # a scalar named in the route path is read from the path
                    if (place, _param_key(place, name)) in have:
                        continue
                    have.add((place, _param_key(place, name)))
                    out.append(f"Route {r['method']} {r['handler']}: dependency {d['name']} khai tham số {place} "
                               f"'{name}' tại {at}; thêm vào params (at = dòng đó) hoặc giải thích bằng params unknown")
        return out

    @property
    def unreferenced_models(self) -> list[str]:
        """Submitted models no route uses, directly or through nested fields. FR-029 documents request/response
        models only, so these stay out of the facts; result.json lists them."""
        seen, todo = set(), [m for r in self.routes.values() for m in route_model_refs(r)]
        while todo:
            m = todo.pop()
            if m in seen or m not in self.models:
                continue
            seen.add(m)
            todo += [x for f in self.models[m]["fields"] for x in _model_refs(f["type"])]
        return sorted(set(self.models) - seen)

    def dependency_params(self, name: str, seen: set, called=None, context: str | None = None,
                          bound: frozenset = frozenset()) -> list[tuple]:
        """(place, HTTP name, path:line) of the request parameters a Depends function declares: Header/Query/Cookie/
        Path markers and plain scalars (query), following nested Depends and Annotated aliases. `called`: the route
        wrote Depends(f(...)), so f is a factory and the function it returns is the dependency; Depends(f) makes f
        itself the dependency. A name the snapshot does not define once (after its class, for B.inject) is skipped:
        the check only reminds the agent, it must not guess which function is meant."""
        short = name.split(".")[-1]
        defs = self._function_defs().get(short, [])
        if not defs and self._classes.get(short):
            # Depends(Filters): FastAPI builds the class, so it reads __init__; Depends(Authentication()) hands over an
            # instance, so it reads __call__ (the constructor's arguments are configuration)
            defs = self._class_method(short, "__call__" if called else "__init__", set())
            if not defs and not called:  # f: Filters = Depends() with Filters a pydantic model: its fields
                fields = self._model_fields(short, set())
                return [("query", n, at) for ann, at, n in (fields or {}).values()
                        if n and astscan.scalar(ann, self._enum_names())]
            called = False  # the chosen method is the dependency itself, not a factory
        if not defs:  # tenant = Tenant(): FastAPI calls Tenant.__call__
            for p, value in self._module_calls().get(short, []):
                if astscan.name_of(value.func) in self._classes:
                    defs += self._class_method(astscan.name_of(value.func), "__call__", set())
        if not defs:  # tenant = partial(check, 'read'): check, without the arguments partial binds
            for p, value in self._module_calls().get(short, []):
                if astscan.name_of(value.func) == "partial" and value.args:
                    inner = astscan.dotted(value.args[0])
                    wrapped = self._function_defs().get((inner or "").split(".")[-1], [])
                    if len(wrapped) == 1:
                        a = wrapped[0][1].args
                        # partial(f, 'read', limit=20): the positional ones are bound; a keyword stays an
                        # overridable default in the signature FastAPI reads
                        fixed = {x.arg for x in (a.posonlyargs + a.args)[:len(value.args) - 1]}
                        return self.dependency_params(inner, seen, False, p, frozenset(fixed))
        if not defs and context and "." not in name:  # from deps import dep as tenant
            tree = self._tree(context)
            imp = astscan.imports(tree).get(short) if tree is not None else None
            if imp and imp[1] and imp[1] != short:
                return self.dependency_params(imp[1], seen, called, self._modules().find(imp[0], context))
        if len(defs) != 1 and "." in name:  # OrganizationCrud.inject: the method of that class
            owner = name.split(".")[-2]
            by_class = [(p, f) for p, f in defs if self._class_of(p, f) == owner]
            if not by_class and context:  # deps.common: `common` of the module the file imports as deps
                tree = self._tree(context)
                imp = astscan.imports(tree).get(owner) if tree is not None else None
                module = self._modules().find(f"{imp[0]}.{imp[1]}" if imp[1] else imp[0], context) if imp else None
                by_class = [(p, f) for p, f in defs if p == module]
            defs = by_class
        if len(defs) > 1 and context:  # the same name in several modules: the one this file defines or imports
            own = [(p, f) for p, f in defs if p == context]
            tree = self._tree(context)
            imp = astscan.imports(tree).get(short) if tree is not None else None
            source = self._modules().find(imp[0], context) if imp and imp[1] else None
            defs = own if len(own) == 1 else [(p, f) for p, f in defs if p == source] or defs
        key = (name, called)
        if len(defs) != 1 or key in seen:
            return []
        seen.add(key)
        path, fn = defs[0]
        inner = {x.name: x for x in fn.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))}
        chosen = []
        if called is not False:  # a factory returns a function: `return inner`, `return _a if flag else _b`
            returned = set()
            for n in fn.body:
                if isinstance(n, ast.Return) and n.value is not None:
                    returned |= astscan.returned_names(n.value)
            assigned = {t.id for n in ast.walk(fn) if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
            chosen = [x for x in sorted(returned - assigned) if x in inner or x in self._function_defs()]
        functions = [inner[x] for x in chosen if x in inner] or ([] if chosen else [fn])
        out = []
        for x in chosen:
            if x not in inner:
                out += self.dependency_params(x, seen, False, path)
        for f in functions:
            a = f.args
            pos = a.posonlyargs + a.args
            pairs = list(zip(pos, [None] * (len(pos) - len(a.defaults)) + list(a.defaults))) + \
                list(zip(a.kwonlyargs, a.kw_defaults))
            for arg, default in pairs:
                if arg.arg in bound and f is fn:
                    continue  # already given by partial(...)
                ann = arg.annotation
                if isinstance(default, ast.Name) and isinstance(self._module_value(path, default), ast.Call):
                    default = self._module_value(path, default)  # tenant_header = Header(alias="X-Tenant")
                exprs = [default] + (ann.slice.elts[1:] if isinstance(ann, ast.Subscript)
                                     and astscan.name_of(ann.value) == "Annotated" and isinstance(ann.slice, ast.Tuple) else [])
                if isinstance(ann, ast.Name):  # Tenant = Annotated[str, Header(alias="X-Tenant")]
                    exprs += self._alias_markers(ann.id, path)
                marked = any(isinstance(e, ast.Call) and self._marker(path, e) in (
                    *DEPENDENCY_MARKERS, "Depends", "Security", "Body", "Form", "File") for e in exprs)
                if not marked and arg.arg not in ("self", "cls") and (ann is None or self._scalar(ann, path)):
                    out.append(("query", arg.arg, f"{path}:{arg.lineno}"))  # FastAPI: a plain scalar is a query
                if isinstance(ann, ast.Name):  # user: CurrentUserDep, an Annotated alias wrapping Depends(...)
                    for dep, dep_called in self._alias_deps(ann.id, path):
                        out += self.dependency_params(dep, seen, dep_called, path)
                for e in exprs:
                    if not isinstance(e, ast.Call):
                        continue
                    marker = self._marker(path, e)
                    typ = ann.slice.elts[0] if isinstance(ann, ast.Subscript) and isinstance(ann.slice, ast.Tuple) else ann
                    model = self._model_fields(astscan.dotted(typ), set()) \
                        if marker in DEPENDENCY_MARKERS and isinstance(typ, (ast.Name, ast.Attribute)) else None
                    if model is not None:  # f: Annotated[Filters, Query()]: the model's fields are the parameters
                        place = DEPENDENCY_MARKERS[marker]
                        out += [(place, n.replace("_", "-") if place == "header" and n == field else n, at)
                                for field, (fann, at, n) in model.items() if n and (
                                    astscan.scalar(fann, self._enum_names()) or _scalar_list(fann, self._enum_names()))]
                    elif marker in DEPENDENCY_MARKERS:
                        place = DEPENDENCY_MARKERS[marker]
                        alias = next((v.value for k in e.keywords if k.arg == "alias"  # alias="X" or alias=PAGE
                                      for v in [self._module_value(path, k.value)]
                                      if isinstance(v, ast.Constant) and isinstance(v.value, str)), None)
                        convert = not any(k.arg == "convert_underscores" and isinstance(k.value, ast.Constant)
                                          and k.value.value is False for k in e.keywords)
                        out.append((place, alias or (arg.arg.replace("_", "-") if place == "header" and convert
                                                     else arg.arg), f"{path}:{arg.lineno}"))
                    elif marker in ("Depends", "Security") and (e.args or any(k.arg == "dependency" for k in e.keywords)):
                        target = e.args[0] if e.args else next(k.value for k in e.keywords if k.arg == "dependency")
                        dep = astscan.dotted(target.func if isinstance(target, ast.Call) else target)
                        if dep:
                            out += self.dependency_params(dep, seen, isinstance(target, ast.Call), path)
                    elif marker in ("Depends", "Security"):  # f: Filters = Depends(), Annotated[Filters, Depends()]
                        if isinstance(typ, (ast.Name, ast.Attribute)):
                            out += self.dependency_params(astscan.dotted(typ), seen, False, path)
        return out

    def _module_value(self, path, expr):
        """A Name resolved to the value it is given once at module level in `path`; anything else as is."""
        if not isinstance(expr, ast.Name):
            return expr
        tree = self._tree(path)
        values = [st.value for st in (tree.body if tree is not None else []) if isinstance(st, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == expr.id for t in st.targets)]
        return values[0] if len(values) == 1 else expr

    def _scalar(self, ann, path) -> bool:
        """astscan.scalar, also through a module-level type alias of the file: UserId = UUID,
        Page = Annotated[int, Field(ge=1)]. An alias holding Depends/Header/... is not a plain query parameter."""
        if astscan.scalar(ann, self._enum_names()):
            return True
        if not isinstance(ann, ast.Name):
            return False
        tree = self._tree(path)
        value = next((st.value for st in (tree.body if tree is not None else []) if isinstance(st, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == ann.id for t in st.targets)), None)
        if isinstance(value, ast.Subscript) and astscan.name_of(value.value) == "Annotated" and isinstance(value.slice, ast.Tuple) \
                and any(isinstance(e, ast.Call) and self._marker(path, e) in (*DEPENDENCY_MARKERS, "Depends", "Security",
                                                                             "Body", "Form", "File") for e in value.slice.elts[1:]):
            return False
        return value is not None and astscan.scalar(value, self._enum_names())

    def _marker(self, path, call) -> str | None:
        """The FastAPI name of a marker call, through an import alias: `from fastapi import Header as H`."""
        name = astscan.name_of(call.func)
        tree = self._tree(path)
        imp = astscan.imports(tree).get(name) if tree is not None and name else None
        return imp[1] if imp and imp[1] and imp[0].split(".")[0] == "fastapi" else name

    def _class_method(self, name, method, visited) -> list:
        """[(path, def)] of `method` in the class, or in the first base class of the snapshot that has it."""
        classes = self._classes.get(name, [])
        if name in visited:
            return []
        visited.add(name)
        if len(classes) != 1:  # the same class name in several modules: their own methods, chosen later by import
            return [(p, x) for p, c in classes for x in c.body
                    if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == method]
        path, cls = classes[0]
        own = [(path, x) for x in cls.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == method]
        for b in cls.bases if not own else []:
            own = self._class_method(astscan.name_of(b), method, visited)
            if own:
                break
        return own

    def _model_fields(self, name, visited, top=True) -> dict | None:
        """{field: (annotation, path:line, HTTP name)} of a pydantic model or dataclass, inherited fields first
        (Field(alias="sortBy") names the query parameter), so FastAPI's
        reading of its signature can be followed; None when the class is not known to be one (a plain class without
        __init__ takes no request parameter)."""
        classes = self._classes.get(name, [])
        if len(classes) != 1 or name in visited:
            return None
        visited.add(name)
        path, cls = classes[0]
        model = any(astscan.name_of(b) in ("BaseModel", "SQLModel") for b in cls.bases) or any(
            astscan.name_of(d.func if isinstance(d, ast.Call) else d) == "dataclass" for d in cls.decorator_list)
        fields = {}
        for b in cls.bases:
            inherited = self._model_fields(astscan.name_of(b), visited, False)
            if inherited is not None:
                model, fields = True, {**fields, **inherited}
        if not model:
            return None
        for x in cls.body:
            if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name) and not x.target.id.startswith("_"):
                exprs = [x.value] + (x.annotation.slice.elts[1:] if isinstance(x.annotation, ast.Subscript)
                                     and isinstance(x.annotation.slice, ast.Tuple) else [])
                alias = next((k.value.value for e in exprs if isinstance(e, ast.Call) and astscan.name_of(e.func) == "Field"
                              for k in e.keywords if k.arg in ("alias", "validation_alias")
                              and isinstance(k.value, ast.Constant) and isinstance(k.value.value, str)), None)
                fields[x.target.id] = (x.annotation, f"{path}:{x.lineno}", alias)
        if top:  # model_config = ConfigDict(alias_generator=to_camel) names the fields without an alias
            gen = self._alias_generator(name, set())
            fields = {f: (ann, at, alias or (gen(f) if gen else f)) for f, (ann, at, alias) in fields.items()}
        return fields

    def _alias_generator(self, name, seen):
        """The alias generator of a model (own config, else a base's): a function of the field name, or None.
        An unknown generator names no parameter (lambda _: None) rather than a guessed one."""
        classes = self._classes.get(name, [])
        if len(classes) != 1 or name in seen:
            return None
        seen.add(name)
        cls = classes[0][1]
        for x in cls.body:
            calls = [x.value] if isinstance(x, (ast.Assign, ast.AnnAssign)) and any(
                astscan.name_of(t) == "model_config" for t in (x.targets if isinstance(x, ast.Assign) else [x.target])) else []
            kws = [k for c in calls if isinstance(c, ast.Call) for k in c.keywords if k.arg == "alias_generator"]
            if isinstance(x, ast.ClassDef) and x.name == "Config":  # pydantic v1: class Config: alias_generator = f
                kws += [type("K", (), {"value": a.value}) for a in x.body if isinstance(a, ast.Assign)
                        and any(astscan.name_of(t) == "alias_generator" for t in a.targets)]
            for k in kws:
                return ALIAS_GENERATORS.get(astscan.name_of(k.value), lambda _: None)
        for b in cls.bases:
            gen = self._alias_generator(astscan.name_of(b), seen)
            if gen:
                return gen
        return None

    def _class_of(self, path, fn) -> str | None:
        """Name of the class whose body holds fn, if any."""
        for node in ast.walk(self._trees[path]):
            if isinstance(node, ast.ClassDef) and fn in node.body:
                return node.name
        return None

    def _function_defs(self) -> dict:
        if self._defs is None:
            self._defs = {}
            for p in self.tools.readable:
                if not p.endswith(".py"):
                    continue
                tree = astscan.parse(self.tools.raw[p])  # also Python 3.14 `except A, B:`
                if tree is None:
                    continue
                self._trees[p] = tree
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self._defs.setdefault(node.name, []).append((p, node))
                    elif isinstance(node, ast.ClassDef):
                        self._classes.setdefault(node.name, []).append((p, node))
        return self._defs


DEPENDENCY_MARKERS = {"Header": "header", "Query": "query", "Cookie": "cookie", "Path": "path"}


def _name_of(node) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _param_key(place, name: str) -> str:
    return name.lower() if place == "header" else name  # HTTP names on both sides; x_a and x-a differ


def _camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(x[:1].upper() + x[1:] for x in rest)


ALIAS_GENERATORS = {"to_camel": _camel, "to_lower_camel": _camel,
                    "to_pascal": lambda n: "".join(x[:1].upper() + x[1:] for x in n.split("_")),
                    "to_snake": lambda n: re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower()}


def _scalar_list(ann, enums) -> bool:
    """list[str], List[int], set[str], tuple[str, ...], Sequence[str]: a repeated query parameter."""
    if isinstance(ann, ast.BinOp) and isinstance(ann.op, ast.BitOr):  # list[str] | None
        sides = [x for x in (ann.left, ann.right) if not (isinstance(x, ast.Constant) and x.value is None)]
        return len(sides) == 1 and _scalar_list(sides[0], enums)
    if isinstance(ann, ast.Subscript) and astscan.name_of(ann.value) == "Optional":
        return _scalar_list(ann.slice, enums)
    if isinstance(ann, ast.Subscript) and astscan.name_of(ann.value) in ("list", "List", "set", "Set", "tuple", "Tuple",
                                                                        "Sequence", "frozenset", "FrozenSet"):
        inner = ann.slice.elts[0] if isinstance(ann.slice, ast.Tuple) else ann.slice
        return astscan.scalar(inner, enums)
    return False


FIELD_BASES = {"str": "string", "int": "integer", "float": "number", "Decimal": "number", "bool": "boolean",
               "bytes": "binary", "UUID": "uuid", "datetime": "datetime", "date": "date", "EmailStr": "email",
               "dict": "object", "Dict": "object", "Mapping": "object", "Any": "any"}
CALL_DEPTH = 3  # calls a Service call path step may skip
FIELD_ARRAYS = {"list", "List", "Sequence", "set", "Set", "frozenset", "FrozenSet", "Iterable"}


def _strip_optional(node) -> tuple:
    """(annotation without None, whether None is allowed); a union of two real types gives (None, ...)."""
    if isinstance(node, ast.Subscript) and astscan.name_of(node.value) == "Annotated" and isinstance(node.slice, ast.Tuple):
        return _strip_optional(node.slice.elts[0])
    if isinstance(node, ast.Subscript) and astscan.name_of(node.value) == "Optional":
        inner, _ = _strip_optional(node.slice)
        return inner, True
    parts = None
    if isinstance(node, ast.Subscript) and astscan.name_of(node.value) == "Union":
        parts = list(node.slice.elts) if isinstance(node.slice, ast.Tuple) else [node.slice]
    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        parts, todo = [], [node]
        while todo:
            x = todo.pop()
            if isinstance(x, ast.BinOp) and isinstance(x.op, ast.BitOr):
                todo += [x.right, x.left]
            else:
                parts.append(x)
    if parts is None:
        return node, False
    real = [p for p in parts if not (isinstance(p, ast.Constant) and p.value is None)]
    return (_strip_optional(real[0])[0] if len(real) == 1 else None), len(real) < len(parts)


def _default_of(value) -> tuple:
    """(has a default, the default is None) of a field assignment; `= Field(...)` and `= ...` mean no default."""
    if value is None or (isinstance(value, ast.Constant) and value.value is Ellipsis):
        return False, False
    if isinstance(value, ast.Call) and astscan.name_of(value.func) == "Field":
        if any(k.arg == "default_factory" for k in value.keywords):
            return True, False
        d = value.args[0] if value.args else next((k.value for k in value.keywords if k.arg == "default"), None)
        if d is None or (isinstance(d, ast.Constant) and d.value is Ellipsis):
            return False, False
        return True, isinstance(d, ast.Constant) and d.value is None
    return True, isinstance(value, ast.Constant) and value.value is None


def _type_conflict(want, got) -> bool:
    """`want` read from the annotation (None: not decidable), `got` the parsed claim; True when they disagree."""
    if want is None or not isinstance(got, tuple):  # {"unknown": ...} is the agent's own answer
        return False
    if want[0] == "class":  # a model class of the snapshot: a model of another name, a scalar or a list is wrong
        return (got[0] == "model" and got[1].split("::")[1] != want[1]) or got[0] == "array" or \
            (got[0] == "base" and got[1] not in ("object", "any"))
    if want[0] == "array":
        return got[0] != "array" or _type_conflict(want[1], got[1])
    return got != want


def _is_init_call(node) -> bool:
    """super().__init__(...) or Base.__init__(self, ...)."""
    return isinstance(node.func, ast.Attribute) and node.func.attr == "__init__"


def _dep_target(node) -> str:
    """Name of a Depends target: f for f and f(...); a subscript as written (Provide[Container.svc], dependency-injector)."""
    if isinstance(node, ast.Subscript):
        return ast.unparse(node)
    return astscan.dotted(node.func if isinstance(node, ast.Call) else node) or ""


def _depends_of(exprs, path) -> list:
    """(target, path:line) of the Depends(f) / Depends(f(...)) calls among expressions."""
    out = []
    for e in exprs:
        if isinstance(e, ast.Call) and astscan.name_of(e.func) == "Depends" and e.args:
            t = _dep_target(e.args[0])
            if t:
                out.append((t, f"{path}:{e.lineno}"))
    return out


def _never_runs(tree, node) -> bool:
    """`node` sits in the body of an `if` whose test is a falsy literal, or a module name set once to one."""
    consts = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            name = st.targets[0].id
            consts[name] = st.value if name not in consts and isinstance(st.value, ast.Constant) else None
    for n in ast.walk(tree):
        if isinstance(n, ast.If) and any(b.lineno <= node.lineno <= (b.end_lineno or b.lineno) for b in n.body):
            test = consts.get(n.test.id) if isinstance(n.test, ast.Name) else n.test
            if isinstance(test, ast.Constant) and not test.value:
                return True
    return False


def _top_level(tree, node) -> bool:
    """`node` runs at import time of its module: inside a top-level statement that is not a def or class."""
    return any(not isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and st.lineno <= node.lineno <= (st.end_lineno or st.lineno) for st in tree.body)


def _config_names(expr) -> set:
    """Names a config key may be given as inside an expression: settings.X and X for an attribute chain, a bare
    constant name, the key string of os.getenv("X") / os.environ["X"]. Not the root `settings` alone."""
    if expr is None:
        return set()
    inner = {id(n.value) for n in ast.walk(expr) if isinstance(n, ast.Attribute)}  # roots and middles of chains
    out = set()
    for n in ast.walk(expr):
        if id(n) in inner:
            continue
        if isinstance(n, ast.Attribute):
            out |= {astscan.dotted(n) or n.attr, n.attr}
        elif isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Call) and astscan.name_of(n.func) in ("getenv", "get") and n.args \
                and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
            out.add(n.args[0].value)
        elif isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
            out.add(n.slice.value)
    return out


def _same_dependency(dep: str, name: str) -> bool:
    """B.inject matches only B.inject; a bare name matches by its last part (the agent may omit the class)."""
    return dep == name if "." in name else dep.split(".")[-1] == name.split(".")[-1]


def _full_path(parts: list[dict]) -> str | None:
    values = [p["value"] for p in parts]
    return join_path(values) if values and all(isinstance(v, str) for v in values) else None


def _unknown_reason(v) -> bool:
    return isinstance(v, dict) and isinstance(v.get("reason"), str) and bool(v["reason"].strip())


def _model_refs(t) -> list[str]:
    if not isinstance(t, tuple):
        return []
    if t[0] == "model":
        return [t[1]]
    if t[0] == "array":
        return _model_refs(t[1])
    return []


def route_model_refs(r: dict) -> list[str]:
    refs = []
    if isinstance(r["body"], dict) and "models" in r["body"]:
        refs += r["body"]["models"]
        for f in r["body"]["fields"]:
            refs += _model_refs(f["type"])
    if isinstance(r["response"], dict) and "model" in r["response"]:
        refs.append(r["response"]["model"])
    if isinstance(r["response"], dict):
        for t in r["response"].get("args", []):
            refs += _model_refs(t)
    for p in r["params"] if isinstance(r["params"], list) else []:
        refs += _model_refs(p["type"])
    return refs


# ---------------------------------------------------------------- facts (API-004 shape)

def join_path(parts: list[str]) -> str:
    segs = [p.strip("/") for p in parts if p.strip("/")]
    joined = "/" + "/".join(segs) if segs else "/"
    if parts and parts[-1].endswith("/") and joined != "/":
        joined += "/"
    return joined


def _has_unknown(value) -> bool:
    if isinstance(value, dict):
        return value.get("state") == "unknown" or any(_has_unknown(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_unknown(v) for v in value)
    return False


class FactBuilder:
    def __init__(self, snapshot: dict, unit_id: str):
        self.snap = snapshot["snapshot_id"]
        self.unit_id = unit_id
        self.files = {f["path"]: f for f in snapshot["files"]}

    def ev(self, where) -> dict:
        path, start, end = where
        f = self.files[path]
        return {"id": "ev:" + sha(compact([self.snap, path, start, None, end, None]).encode()), "snapshot_id": self.snap,
                "file_id": f["file_id"], "path": path, "sha256": f["sha256"], "start_line": start, "end_line": end,
                "start_column": None, "end_column": None}

    def fact(self, kind: str, main: dict | None, key, attributes: dict, extra=(), inferred=()) -> dict:
        ident = "fact:" + sha(compact([self.snap, kind, key]).encode())
        evidence = {main["id"]: main} if main else {}
        for e in extra:
            evidence.setdefault(e["id"], e)
        gaps = sorted(k for k, v in attributes.items() if _has_unknown(v))
        fact = {"id": ident, "unit_id": self.unit_id, "kind": kind, "attributes": attributes,
                "evidence": list(evidence.values()), "resolution": "not_applicable", "target_fact_ids": [],
                "confidence": "inferred" if inferred else "exact", "completeness": "partial" if gaps else "full"}
        if gaps:
            fact["completeness_reason"] = "Trường chưa xác định: " + ", ".join(gaps)
        if inferred:
            fact["confidence_reason"] = "; ".join(f"{r}: {RULES[r]}" for r in sorted(set(inferred)))
        return fact


def _schema(t, model_ids: dict, ev_id: str) -> dict:
    """Known JSON schema for a parsed type, or unknown when it names a model the agent never submitted."""
    missing = [m for m in _model_refs(t) if m not in model_ids]
    if missing:
        return unknown("Model chưa được agent nộp: " + ", ".join(missing))
    return known(schema_of(t, model_ids), ev_id)


def schema_of(t, model_ids: dict):
    if t[0] == "base":
        return dict(BASE_TYPES[t[1]])
    if t[0] == "array":
        return {"type": "array", "items": schema_of(t[1], model_ids)}
    return {"x-model-fact": model_ids[t[1]]}


def _flag(v, ev_id):
    return known(v, ev_id) if isinstance(v, bool) else unknown(v["unknown"])


def _typed(v, model_ids, ev_id):
    return unknown(v["unknown"]) if isinstance(v, dict) else _schema(v, model_ids, ev_id)


def build_facts(claims: Claims, snapshot: dict, unit_id: str) -> list[dict]:
    """Checked claims -> facts the existing API renderer reads. Order is deterministic.
    Works on whatever the agent left, also after a partial run: missing references become unknown."""
    b = FactBuilder(snapshot, unit_id)
    model_ids = {mid: "fact:" + sha(compact([b.snap, "model", mid]).encode()) for mid in claims.models}
    facts = []
    unused = set(claims.unreferenced_models)
    for mid in sorted(claims.models):
        if mid in unused:
            continue
        m = claims.models[mid]
        main = b.ev(m["at"])
        extra, inferred, fields = [], [], []
        for f in m["fields"]:
            fe = b.ev(f["at"])
            extra.append(fe)
            if f["rule"]:
                inferred.append(f["rule"])
            fv = {"name": known(f["name"], fe["id"])}
            if f["alias"]:
                fv["alias"] = known(f["alias"], fe["id"])
            fv["type"] = _typed(f["type"], model_ids, fe["id"])
            for key in ("required", "nullable"):
                fv[key] = unknown(f[key]["unknown"]) if isinstance(f[key], dict) else known(f[key], fe["id"])
            fields.append(fv)
        attrs = {"name": known(m["name"], main["id"]), "declared_in": known(m["at"][0], main["id"]),
                 "fields": unknown("Model sinh lúc chạy: " + m["dynamic"]) if m.get("dynamic") else known(fields, main["id"])}
        fact = b.fact("model", main, mid, attrs, extra, inferred)
        if m.get("unchecked"):  # the agent's answer stands where the declaration could not be read
            note = "Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: " + ", ".join(m["unchecked"])
            fact["confidence"] = "inferred"
            fact["confidence_reason"] = "; ".join(x for x in (fact.get("confidence_reason"), note) if x)
        fact["id"] = model_ids[mid]
        facts.append(fact)
    for key in sorted(claims.routes, key=str):
        facts.append(_route_fact(b, claims.routes[key], model_ids))
    for key in sorted(claims.http):
        h = claims.http[key]
        where = h["at"]
        main = b.ev(where)
        t = h["target"]
        attrs = {"library": known(h["library"], main["id"]),
                 "method": known(h["method"], main["id"]) if isinstance(h["method"], str) else unknown(h["method"]["unknown"]),
                 "call_text": known(claims.tools.shown[where[0]][where[1] - 1].strip(), main["id"])}
        extra = []
        if t["kind"] == "literal":
            attrs["url"] = known(t["value"], main["id"])
        elif t["kind"] == "config":  # key = the setting name; the expression at the call is kept beside it
            src = b.ev(h["config_at"]) if h.get("config_at") else main  # base_url= line of the client, when given
            extra = [src] if h.get("config_at") else []
            attrs["url"] = unknown("URL lấy từ khóa cấu hình" + (" (base_url của client, đường dẫn tương đối)"
                                                                if h.get("config_at") else ""))
            attrs["url_config_key"] = known(t["value"].rsplit(".", 1)[-1], src["id"])
            if "." in t["value"]:
                attrs["url_config_expr"] = known(t["value"], src["id"])
        else:
            attrs["url"] = unknown(t["reason"])
        facts.append(b.fact("http_call", main, list(key), attrs, extra))
    for path in sorted(claims.roles):
        x = claims.roles[path]
        main = b.ev(x["at"]) if x["at"] else None  # only an empty file has no line to cite
        cp = [b.ev(w) for w in x["call_path"]]
        ids = ([main["id"]] if main else []) + [e["id"] for e in cp]
        attrs = {"file": known(path, *ids), "role": known(x["role"], *ids)}
        if main:  # the code line itself, as sent to the model (secrets masked)
            attrs["code"] = known(claims.tools.shown[path][x["at"][1] - 1].strip(), main["id"])
        if x["role"] == "Service":
            attrs["call_path"] = known([f"{e['path']}:{e['start_line']}" for e in cp], *(e["id"] for e in cp))
            attrs["reason"] = known("Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng", *(e["id"] for e in cp))
        elif x["role"] == "Khác":
            attrs["reason"] = known("Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file", *ids)
        if x["not_signal"]:
            attrs["not_signal"] = known(x["not_signal"], *ids)
        fact = b.fact("file_role", main, path, attrs, cp)
        if x["role"] == "Service":
            fact["confidence"], fact["confidence_reason"] = "inferred", attrs["reason"]["value"]
        facts.append(fact)
    return facts


def _route_fact(b: FactBuilder, r: dict, model_ids: dict) -> dict:
    dec = b.ev(r["decorator"])
    extra, inferred = [], []
    attrs = {"method": known(r["method"], dec["id"]), "handler": known(r["handler"], dec["id"]),
             "declaration_evidence_id": known(dec["id"], dec["id"])}
    part_evs = [b.ev(p["at"]) for p in r["parts"]]
    extra += part_evs + [b.ev(p["used_at"]) for p in r["parts"] if p.get("used_at")]
    attrs["registration_context"] = known(" -> ".join(f"{p['kind']}@{p['at'][0]}:{p['at'][1]}" for p in r["parts"]),
                                          *(e["id"] for e in part_evs))
    if r["application"]:
        app_ev = b.ev(r["application"])
        extra.append(app_ev)
        attrs["application_id"] = known(f"app:{r['application'][0]}:{r['application'][1]}", app_ev["id"])
    else:
        attrs["application_id"] = unknown(r["application_unknown"] or "Router chưa được gắn vào application nào")
    unknown_parts = [p for p in r["parts"] if p["value"] is None]
    if r["application"] and not unknown_parts:
        attrs["path"] = known(join_path([p["value"] for p in r["parts"]]), *(e["id"] for e in part_evs))
        if any(p["kind"] == "settings_default" for p in r["parts"]):
            attrs["prefix_rule"] = known("settings.default_prefix", *(e["id"] for e in part_evs))
            inferred.append("settings.default_prefix")
    else:
        attrs["path"] = unknown("; ".join(p["reason"] for p in unknown_parts) if unknown_parts
                                else attrs["application_id"]["reason"])
        last = max((i for i, p in enumerate(r["parts"]) if p["value"] is None), default=-1)
        tail = [p["value"] for p in r["parts"][last + 1:]]
        if tail:
            attrs["path_suffix"] = known(join_path(tail), *(e["id"] for e in part_evs[last + 1:]))
    st = r["status"]
    if "unknown" in st:
        attrs["status_codes"] = unknown(st["unknown"])
    else:
        sev = b.ev(st["at"])
        extra.append(sev)
        attrs["status_codes"] = known(st["codes"], sev["id"])
        if st["rule"]:
            attrs["status_rule"] = known(st["rule"], sev["id"])
            if st["rule"] != "fastapi.status_constant":  # a named constant is declared in code, not a default
                inferred.append(st["rule"])
    if isinstance(r["params"], dict):
        attrs["parameters"] = unknown(r["params"]["unknown"])
    else:
        plist = []
        for p in r["params"]:
            pe = b.ev(p["at"])
            extra.append(pe)
            if p["rule"]:
                inferred.append(p["rule"])
            plist.append({"name": known(p["name"], pe["id"]),
                          "in": known(p["in"], pe["id"]) if isinstance(p["in"], str) else unknown(p["in"]["unknown"]),
                          "required": known(p["required"], pe["id"]) if isinstance(p["required"], bool)
                          else unknown(p["required"]["unknown"]),
                          "schema": _typed(p["type"], model_ids, pe["id"]),
                          **({"nullable": known(p["nullable"], pe["id"]) if isinstance(p["nullable"], bool)
                              else unknown(p["nullable"]["unknown"])} if p["nullable"] is not None else {})})
        attrs["parameters"] = known(plist, dec["id"])
    bodies = []
    body = r["body"]
    if isinstance(body, dict) and "unknown" in body:
        attrs["request_model_ids"] = unknown(body["unknown"])
    elif body and [m for m in body["models"] if m not in model_ids]:
        attrs["request_model_ids"] = unknown("Model chưa được agent nộp: " +
                                             ", ".join(m for m in body["models"] if m not in model_ids))
    else:
        ids = []
        if body:
            be = b.ev(body["at"])
            extra.append(be)
            if body["rule"]:
                inferred.append(body["rule"])
            if isinstance(body["required"], dict):
                attrs["request_body_required"] = unknown(body["required"]["unknown"])
            for mid in body["models"]:
                ids.append(model_ids[mid])
                bodies.append({"direction": "request", "model_id": model_ids[mid], "status": None,
                               "media_type": body["media_type"],
                               "required": body["required"] if isinstance(body["required"], bool) else None})
            if body.get("type") is not None:  # JSON body without a model: its declared type is the schema
                t = body["type"]
                if isinstance(t, dict):
                    attrs["request_type"] = unknown(t["unknown"])
                else:
                    ts = _schema(t, model_ids, be["id"])
                    attrs["request_type"] = known({"schema": ts["value"], "media_type": body["media_type"],
                                                   "required": body["required"] if isinstance(body["required"], bool)
                                                   else None}, be["id"]) if is_known(ts) else ts
            if body["embedded"]:
                attrs["request_body_embedded"] = known(True, be["id"])
            if body["param"]:
                attrs["request_body_param"] = known(body["param"], be["id"])
            if body["fields"]:
                fevs = [b.ev(f["at"]) for f in body["fields"]]
                extra += fevs
                attrs["request_inline"] = known({
                    "media_type": body["media_type"],
                    "required": _flag(body["required"], be["id"]),
                    "fields": [{"name": f["name"], "schema": _typed(f["type"], model_ids, e["id"]),
                                "required": _flag(f["required"], e["id"])}
                               for f, e in zip(body["fields"], fevs)]}, be["id"], *(e["id"] for e in fevs))
        attrs["request_model_ids"] = known(ids, dec["id"])
    resp = r["response"]
    if isinstance(resp, dict) and "unknown" in resp:
        attrs["response_model_ids"] = unknown(resp["unknown"])
    elif resp and "type" in resp:  # a declared type that is not a model: no model ids, the schema itself
        rt = b.ev(resp["at"])
        extra.append(rt)
        if resp["rule"]:
            inferred.append(resp["rule"])
        attrs["response_model_ids"] = known([], dec["id"])
        attrs["response_type"] = known({"schema": schema_of(resp["type"], model_ids), "media_type": resp["media_type"]},
                                       rt["id"])
    elif resp and "external" in resp:  # library generic: a typed response, its model arguments resolved
        rt = b.ev(resp["at"])
        extra.append(rt)
        if resp["rule"]:
            inferred.append(resp["rule"])
        missing = [x for t in resp["args"] for x in _model_refs(t) if x not in model_ids]
        if missing:
            attrs["response_model_ids"] = unknown("Model chưa được agent nộp: " + ", ".join(missing))
        else:
            schema = {"type": "object", "x-external-model": resp["external"],
                      "x-type-args": [schema_of(t, model_ids) for t in resp["args"]]}
            attrs["response_model_ids"] = known([], rt["id"])
            attrs["response_type"] = known({"schema": {"type": "array", "items": schema} if resp["array"] else schema,
                                            "media_type": "application/json"}, rt["id"])
    elif resp and (missing := [m for m in [resp["model"], *(x for t in resp.get("args", []) for x in _model_refs(t))]
                               if m not in model_ids]):
        attrs["response_model_ids"] = unknown("Model chưa được agent nộp: " + ", ".join(missing))
    elif resp:
        re_ = b.ev(resp["at"])
        extra.append(re_)
        if resp["rule"]:
            inferred.append(resp["rule"])
        attrs["response_model_ids"] = known([model_ids[resp["model"]]], re_["id"])
        code = st["codes"][0] if "codes" in st else None
        bodies.append({"direction": "response", "model_id": model_ids[resp["model"]], "status": code,
                       "media_type": "application/json", "required": None, **({"array": True} if resp["array"] else {}),
                       **({"type_args": [schema_of(t, model_ids) for t in resp["args"]]} if resp.get("args") else {})})
    else:
        attrs["response_model_ids"] = known([], dec["id"])
    if bodies:
        attrs["bodies"] = known(bodies, dec["id"])
    d = r["dependencies"]
    if isinstance(d, dict):
        attrs["dependencies"] = unknown(d["unknown"])
    else:
        devs = [b.ev(x["at"]) for x in d]
        extra += devs
        attrs["dependencies"] = known([x["name"] for x in d], *(e["id"] for e in devs)) if d else known([], dec["id"])
    a = r["auth"]
    if "unknown" in a:
        attrs["auth"] = unknown(a["unknown"])
    else:
        ae = b.ev(a["at"])
        extra.append(ae)
        attrs["auth"] = known(a["value"], ae["id"])
    if r.get("errors"):  # statuses the handler can answer with besides the declared ones (raise + handler)
        vals, ids = [], []
        for e in r["errors"]:
            evs = [b.ev(e["raised_at"])] + ([b.ev(e["status_at"])] if e["status_at"] else [])
            extra += evs
            ids += [x["id"] for x in evs]
            vals.append({"status": e["status"], "exception": e["exception"],
                         "raised_at": f"{e['raised_at'][0]}:{e['raised_at'][1]}",
                         "status_at": f"{e['status_at'][0]}:{e['status_at'][1]}" if e["status_at"] else None})
        attrs["errors"] = known(sorted(vals, key=lambda v: (v["status"], v["exception"])), *ids)
    if r.get("examples"):  # literal example=/examples= values read from the cited lines
        evs = [b.ev(x["at"]) for x in r["examples"]]
        extra += evs
        attrs["examples"] = known([x["value"] for x in r["examples"]], *(e["id"] for e in evs))
    for name in ("tags", "deprecated", "summary"):  # summary: written by the model, shown as "AI viết"
        if r.get(name):
            ev = b.ev(r[name]["at"])
            extra.append(ev)
            attrs[name] = known(r[name]["value"], ev["id"])
    key = [r["handler"], r["method"], list(r["application"]) if r["application"] else None,
           [[p["kind"], list(p["at"]), p["value"]] for p in r["parts"]]]
    return b.fact("route", dec, key, attrs, extra, inferred)
