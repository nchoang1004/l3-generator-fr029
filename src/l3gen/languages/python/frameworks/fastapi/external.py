"""Tìm chỗ code gọi HTTP ra ngoài hệ thống (bước 3c).

Nhận hai thư viện theo SPEC mục 2.1: `httpx` và `requests`.

    httpx.post("https://payment.internal/charge")     -> exact + full
    requests.get(f"{settings.URL}/charge")            -> exact + partial

Đường dẫn ghép từ biến thì giữ nguyên tên biến, KHÔNG đoán giá trị thật.
"""

import ast
from dataclasses import dataclass

from l3gen.languages.python.literals import keyword_of, read_text
from l3gen.languages.python.parser import ParsedFile
from l3gen.languages.python.resolution import (
    FUNCTION_NODES,
    Resolver,
    dotted_name,
    infer_variable_types,
)
from l3gen.models.iam import ExternalCall, SourceLocation

HTTP_LIBRARIES = ("httpx", "requests")
HTTP_VERBS = ("get", "post", "put", "delete", "patch", "head", "options")
CLIENT_CLASSES = ("Client", "AsyncClient", "Session")


@dataclass
class CallSite:
    node: ast.Call
    method: str | None
    """Chữ hoa, ví dụ "POST". None nếu chưa xác định được."""


def _library_of(qname: str | None) -> str | None:
    if not qname:
        return None
    root = qname.split(".")[0]
    return root if root in HTTP_LIBRARIES else None


def _classify(
    call: ast.Call, scope, var_types: dict[str, str], resolver: Resolver
) -> CallSite | None:
    """Lời gọi này có phải gọi HTTP ra ngoài không."""
    if not isinstance(call.func, ast.Attribute):
        return None

    verb = call.func.attr
    receiver = dotted_name(call.func.value)
    if receiver is None:
        return None

    # Dạng 1: httpx.post(...) / requests.get(...)
    receiver_qname = resolver.qualify(scope, receiver)
    if _library_of(receiver_qname) and verb in (*HTTP_VERBS, "request"):
        return _with_method(call, verb)

    # Dạng 2: client.post(...) với client = httpx.Client()
    head = receiver.split(".")[0]
    holder = var_types.get(head)
    if holder and _library_of(holder) and holder.split(".")[-1] in CLIENT_CLASSES:
        if verb in (*HTTP_VERBS, "request"):
            return _with_method(call, verb)

    return None


def _with_method(call: ast.Call, verb: str) -> CallSite:
    if verb != "request":
        return CallSite(call, verb.upper())
    first = read_text(call.args[0]) if call.args else None
    return CallSite(call, first.text.upper() if first and first.is_literal else None)


def _url_argument(call: ast.Call, verb_is_request: bool) -> ast.expr | None:
    positional = call.args[1:] if verb_is_request else call.args
    if positional:
        return positional[0]
    return keyword_of(call, "url")


def calls_inside_try(func) -> set[int]:
    """Vị trí bộ nhớ của mọi node Call nằm trong một khối try/except.

    Dùng id() vì node của cây cú pháp không băm được theo giá trị.
    """
    protected: set[int] = set()
    for node in ast.walk(func):
        if not isinstance(node, ast.Try):
            continue
        for statement in node.body:
            for inner in ast.walk(statement):
                if isinstance(inner, ast.Call):
                    protected.add(id(inner))
    return protected


def _to_external_call(
    site: CallSite, caller: str, rel_path: str, service: str, in_try: bool
) -> ExternalCall:
    is_request = isinstance(site.node.func, ast.Attribute) and site.node.func.attr == "request"
    url_node = _url_argument(site.node, is_request)
    url = read_text(url_node)

    if url is None:
        text, complete = "{không đọc được đối số URL}", False
    else:
        text, complete = url.text, url.is_literal

    reasons = []
    if not complete:
        reasons.append(f"đường dẫn có phần phụ thuộc lúc chạy: {text}")
    if site.method is None:
        reasons.append("phương thức HTTP là biến, chưa giải được giá trị")

    return ExternalCall(
        service=service,
        caller_function=caller,
        url_or_host=text,
        http_method=site.method,
        inside_try_except=in_try,
        confidence="exact",
        completeness="full" if not reasons else "partial",
        reason="; ".join(reasons) or None,
        location=SourceLocation(
            file=rel_path,
            line_start=site.node.lineno,
            line_end=getattr(site.node, "end_lineno", site.node.lineno) or site.node.lineno,
        ),
    )


def extract_external_calls(
    files: list[ParsedFile], resolver: Resolver, module_of: dict[str, str], service: str
) -> list[ExternalCall]:
    calls: list[ExternalCall] = []

    for parsed in files:
        scope = resolver.tables.for_file(parsed.rel_path)
        if scope is None:
            continue
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""

        for func, caller in _walk_functions(parsed.tree, prefix, scope, resolver):
            var_types = infer_variable_types(func, scope, resolver)
            protected = calls_inside_try(func)
            for statement in func.body:
                for node in ast.walk(statement):
                    if not isinstance(node, ast.Call):
                        continue
                    site = _classify(node, scope, var_types, resolver)
                    if site is not None:
                        calls.append(
                            _to_external_call(
                                site, caller, parsed.rel_path, service,
                                id(node) in protected,
                            )
                        )

    calls.sort(key=lambda c: (c.url_or_host, c.location.file, c.location.line_start))
    return calls


def _walk_functions(tree: ast.Module, prefix: str, scope, resolver: Resolver):
    """Mọi hàm và method trong file, kèm tên đầy đủ để khớp với FunctionNode."""
    for node in tree.body:
        if isinstance(node, FUNCTION_NODES):
            yield node, f"{prefix}{node.name}"
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, FUNCTION_NODES):
                    yield child, f"{prefix}{node.name}.{child.name}"
