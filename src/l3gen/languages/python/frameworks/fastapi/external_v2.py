"""HTTP client adapter V2 dựa trên target đầy đủ do resolver cung cấp."""

from __future__ import annotations

from l3gen.models.iam import ExternalCall, SourceLocation
from l3gen.models.resolution import ResolutionResult
from l3gen.models.semantic import CallFact, ExpressionIR, SemanticProgram

_LIBRARIES = ("httpx.", "requests.")
_VERBS = {"get", "post", "put", "delete", "patch", "head", "options", "request"}


def extract_external_calls_v2(
    program: SemanticProgram,
    resolution: ResolutionResult,
    service: str = "python",
) -> list[ExternalCall]:
    calls = {
        fact.id: fact for fact in program.all_facts() if isinstance(fact, CallFact)
    }
    result: list[ExternalCall] = []
    for item in resolution.calls:
        source = calls[item.call_fact_id]
        if not source.enclosing_function:
            continue
        targets = [target for target in item.targets if _is_http_target(target)]
        if not targets:
            continue
        methods = {_method_and_url(source, target)[0] for target in targets}
        url_expressions = [_method_and_url(source, target)[1] for target in targets]
        method = next(iter(methods)) if len(methods) == 1 else None
        url_expression = next((value for value in url_expressions if value is not None), None)
        url, literal = _text(url_expression)
        reasons: list[str] = []
        if not literal:
            reasons.append(f"đường dẫn có phần phụ thuộc runtime: {url}")
        if method is None:
            reasons.append("phương thức HTTP chưa xác định duy nhất")
        if item.status != "resolved":
            reasons.append(item.reason or f"call có trạng thái {item.status}")
        result.append(
            ExternalCall(
                service=service,
                caller_function=source.enclosing_function,
                url_or_host=url or "{không đọc được đối số URL}",
                http_method=method,
                inside_try_except=source.inside_try_except,
                confidence="exact",
                completeness="partial" if reasons else "full",
                reason="; ".join(dict.fromkeys(reasons)) or None,
                location=SourceLocation(
                    file=source.location.file,
                    line_start=source.location.line_start,
                    line_end=source.location.line_end,
                ),
            )
        )
    return sorted(result, key=lambda item: (item.location.file, item.location.line_start))


def _is_http_target(target: str) -> bool:
    owner, _, verb = target.rpartition(".")
    return owner in {"httpx", "requests", "httpx.Client", "httpx.AsyncClient", "requests.Session"} and verb in _VERBS


def _method_and_url(call: CallFact, target: str) -> tuple[str | None, ExpressionIR | None]:
    verb = target.rsplit(".", 1)[-1]
    if verb == "request":
        method_expr = call.arguments[0] if call.arguments else call.keywords.get("method")
        method, literal = _text(method_expr)
        url = call.arguments[1] if len(call.arguments) > 1 else call.keywords.get("url")
        return (method.upper() if method and literal else None), url
    url = call.arguments[0] if call.arguments else call.keywords.get("url")
    return verb.upper(), url


def _text(expression: ExpressionIR | None) -> tuple[str | None, bool]:
    if expression is None:
        return None, False
    if expression.kind == "literal" and isinstance(expression.literal, str):
        return expression.literal, True
    if (expression.kind == "formatted_string" or (expression.kind == "binary" and expression.operator == "Add")) and expression.elements:
        pieces = [_text(item) for item in expression.elements]
        if all(text is not None for text, _ in pieces):
            return "".join(text or "" for text, _ in pieces), all(ok for _, ok in pieces)
    return "{" + expression.text + "}", False
