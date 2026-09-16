"""Sinh sơ đồ phụ thuộc dạng Mermaid.

Sơ đồ phải mở được trên GitLab và GitHub. Graph thật có thể hàng nghìn node nên
sơ đồ này cố tình rút gọn: chỉ vẽ route, bảng dữ liệu và đích gọi ra ngoài. Dữ
liệu đầy đủ nằm trong graph.json (SPEC mục 7).
"""

import re
import hashlib
from pathlib import Path

from l3gen.models.iam import IntermediateArchitectureModel

MAX_NODES = 40
MAX_LABEL = 38


def write_mermaid(iam: IntermediateArchitectureModel, output_dir: Path) -> Path:
    path = output_dir / "diagram.mmd"
    path.write_text("\n".join(_render(iam)) + "\n", encoding="utf-8", errors="backslashreplace")
    return path


def _safe_id(prefix: str, text: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", text).strip("_")
    digest = hashlib.sha256(text.encode("utf-8", errors="surrogatepass")).hexdigest()[:12]
    return f"{prefix}_{cleaned[:55]}_{digest}"


def _route_key(route) -> str:
    return f"{route.service}:{route.location.file}:{route.method}:{route.path}:{route.handler_symbol or route.handler_function}"


def _label(text: str) -> str:
    trimmed = text if len(text) <= MAX_LABEL else text[: MAX_LABEL - 1] + "…"
    return trimmed.replace('"', "'")


def _render(iam: IntermediateArchitectureModel) -> list[str]:
    lines = [
        "%% Sơ đồ rút gọn. Dữ liệu đầy đủ nằm trong graph.json.",
        "flowchart LR",
    ]

    budget = MAX_NODES
    routes = iam.routes[:budget]
    budget -= len(routes)
    entities = iam.entities[: max(budget, 0)]
    budget -= len(entities)
    hosts = sorted({c.url_or_host for c in iam.external_calls})[: max(budget, 0)]

    if routes:
        lines.append("  subgraph API")
        for route in routes:
            lines.append(
                f'    {_safe_id("r", _route_key(route))}["{_label(route.method + " " + route.path)}"]'
            )
        lines.append("  end")

    if entities:
        lines.append("  subgraph Bảng dữ liệu")
        for entity in entities:
            name = entity.table_name or entity.class_name
            lines.append(f'    {_safe_id("e", name)}[("{_label(name)}")]')
        lines.append("  end")

    if hosts:
        lines.append("  subgraph Bên ngoài")
        for host in hosts:
            lines.append(f'    {_safe_id("x", host)}>"{_label(host)}"]')
        lines.append("  end")

    lines += _edges(iam, routes, entities, hosts)

    if len(iam.routes) > len(routes) or len(iam.entities) > len(entities):
        hidden = (len(iam.routes) - len(routes)) + (len(iam.entities) - len(entities))
        lines.append(f'  more["… {hidden} thành phần nữa, xem graph.json"]')

    return lines


MAX_HOPS = 3


def _edges(iam, routes, entities, hosts) -> list[str]:
    """Nối route xuống bảng dữ liệu và đích bên ngoài, đi theo chuỗi lời gọi.

    Đi tối đa MAX_HOPS chặng: route -> handler -> service -> repository là chuỗi
    điển hình của một dự án FastAPI phân tầng.
    """
    tables = {e.class_name: (e.table_name or e.class_name) for e in entities}
    by_symbol = {f.qualified_name: f for f in iam.functions}

    host_by_caller: dict[str, set[str]] = {}
    for call in iam.external_calls:
        if call.url_or_host in hosts:
            host_by_caller.setdefault(call.caller_function, set()).add(call.url_or_host)

    edges: set[tuple[str, str]] = set()
    for route in routes:
        route_id = _safe_id("r", _route_key(route))
        for symbol in _reachable(route, by_symbol):
            function = by_symbol.get(symbol)
            if function is None:
                continue
            for ref in function.entity_refs:
                if ref.name in tables:
                    edges.add((route_id, _safe_id("e", tables[ref.name])))
            for host in host_by_caller.get(symbol, set()):
                edges.add((route_id, _safe_id("x", host)))

    return [f"  {source} --> {target}" for source, target in sorted(edges)]


def _reachable(route, by_symbol) -> set[str]:
    """Mọi hàm mà route này chạm tới, trong giới hạn MAX_HOPS chặng."""
    frontier = {r.resolved_symbol for r in route.calls if r.resolved and r.resolved_symbol}
    if route.handler_symbol:
        frontier.add(route.handler_symbol)
    seen = set(frontier)
    for _ in range(MAX_HOPS):
        nxt: set[str] = set()
        for symbol in frontier:
            function = by_symbol.get(symbol)
            if function is None:
                continue
            for ref in function.calls:
                if ref.resolved and ref.resolved_symbol and ref.resolved_symbol not in seen:
                    seen.add(ref.resolved_symbol)
                    nxt.add(ref.resolved_symbol)
        frontier = nxt
    return seen
