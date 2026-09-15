"""Gộp kết quả các bộ trích xuất thành một IAM hoàn chỉnh (bước 4).

Mỗi đơn vị phân tích chạy độc lập: quét file, dựng hai bảng tra cứu, chạy các bộ
trích xuất. Kết quả gộp lại thành một IAM chung, nhưng mọi thực thể đều mang
trường `service` chỉ rõ nó thuộc đơn vị nào.
"""

import time
from datetime import datetime, timezone
from pathlib import Path

from l3gen import __version__
from l3gen.detection.discovery import Unit, discover
from l3gen.languages.python.common.callgraph import extract_functions
from l3gen.languages.python.frameworks.fastapi.external import extract_external_calls
from l3gen.languages.python.frameworks.fastapi.routes import extract_routes
from l3gen.languages.python.parser import FailedFile, parse_all
from l3gen.languages.python.resolution import build_resolver, is_external
from l3gen.models.iam import (
    IntermediateArchitectureModel,
    ParseError,
    RunMetrics,
    SourceLocation,
    UnresolvedReference,
)
from l3gen.orm.sqlalchemy import extract_entities


class EmptyInputError(Exception):
    """Thư mục đầu vào không có đơn vị nào phân tích được."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def build(root: Path, excludes: tuple[str, ...], ai_enabled: bool) -> IntermediateArchitectureModel:
    started = time.perf_counter()
    stack, units = discover(root, excludes)

    if not stack.services:
        raise EmptyInputError(f"không tìm thấy file source nào trong '{root}'")
    if not units:
        lines = [
            f"  - {s.name or '(thư mục gốc)'}: {s.language or 'chưa rõ'}"
            f"{', ' + ', '.join(s.frameworks) if s.frameworks else ''} — {s.skip_reason}"
            for s in stack.services
        ]
        raise EmptyInputError(
            "không đơn vị nào dùng stack đang hỗ trợ (Python + FastAPI):\n" + "\n".join(lines)
        )

    routes, entities, external_calls, functions = [], [], [], []
    parse_errors: list[ParseError] = []
    unresolved: list[UnresolvedReference] = []
    files_found = files_analyzed = 0
    lines_of_code = 0

    for unit in units:
        service = unit.rel_root or unit.root.name
        parsed, failed = parse_all(unit.files, unit.root)

        files_found += len(unit.files)
        files_analyzed += len(parsed)
        lines_of_code += sum(f.line_count for f in parsed)
        parse_errors.extend(_prefix_errors(failed, unit, root))

        resolver, module_of = build_resolver(parsed)

        unit_entities = extract_entities(parsed, resolver, module_of, service)
        entity_classes = frozenset(_entity_qualified_names(unit_entities, resolver))

        unit_routes, dropped = extract_routes(parsed, resolver, module_of, service)
        routes.extend(_reroot_routes(unit_routes, unit, root))
        entities.extend(_reroot(unit_entities, unit, root))
        external_calls.extend(
            _reroot(extract_external_calls(parsed, resolver, module_of, service), unit, root)
        )

        unit_functions = extract_functions(
            parsed, resolver, module_of, service, entity_classes
        )
        functions.extend(_reroot_functions(unit_functions, unit, root))
        unresolved.extend(_collect_unresolved(unit_functions, unit, root))
        unresolved.extend(
            UnresolvedReference(
                description=f"route không lần được về ứng dụng gốc: {item}",
                location=SourceLocation(file=unit.rel_root or ".", line_start=0, line_end=0),
            )
            for item in dropped
        )

    files_skipped = len(parse_errors)
    metrics = RunMetrics(
        scanned_at=datetime.now(timezone.utc),
        files_found=files_found,
        files_analyzed=files_analyzed,
        files_skipped=files_skipped,
        is_partial=files_skipped > 0 or stack.skipped_count > 0,
        lines_of_code=lines_of_code,
        duration_seconds=round(time.perf_counter() - started, 3),
        ai_enabled=ai_enabled,
        tool_version=__version__,
    )

    return IntermediateArchitectureModel(
        detected_stack=stack,
        routes=sorted(routes, key=lambda r: (r.service, r.path, r.method)),
        entities=sorted(entities, key=lambda e: (e.service, e.table_name or "", e.class_name)),
        external_calls=sorted(external_calls, key=lambda c: (c.service, c.url_or_host)),
        functions=sorted(functions, key=lambda f: (f.service, f.module, f.qualified_name)),
        unresolved_references=unresolved,
        parse_errors=parse_errors,
        metrics=metrics,
    )


def _entity_qualified_names(entities, resolver) -> list[str]:
    """Tên đầy đủ của các class bảng, tra ngược từ danh bạ."""
    names = []
    for entity in entities:
        for qname, definition in resolver.index.definitions.items():
            if (
                definition.rel_path == entity.location.file
                and definition.line == entity.location.line_start
                and qname.split(".")[-1] == entity.class_name
            ):
                names.append(qname)
                break
    return names


def _full_path(rel_path: str, unit: Unit, root: Path) -> str:
    """Đường dẫn trong đơn vị -> đường dẫn tính từ thư mục đầu vào."""
    return f"{unit.rel_root}/{rel_path}" if unit.rel_root else rel_path


def _reroot(items, unit: Unit, root: Path):
    for item in items:
        item.location.file = _full_path(item.location.file, unit, root)
    return items


def _reroot_routes(routes, unit: Unit, root: Path):
    for route in routes:
        route.location.file = _full_path(route.location.file, unit, root)
        _reroot_refs(route.calls, unit, root)
    return routes


def _reroot_functions(functions, unit: Unit, root: Path):
    for function in functions:
        function.module = _full_path(function.module, unit, root)
        function.location.file = _full_path(function.location.file, unit, root)
        _reroot_refs(function.calls, unit, root)
        _reroot_refs(function.entity_refs, unit, root)
    return functions


def _reroot_refs(refs, unit: Unit, root: Path) -> None:
    for ref in refs:
        if ref.resolved_module:
            ref.resolved_module = _full_path(ref.resolved_module, unit, root)


def _prefix_errors(failed: list[FailedFile], unit: Unit, root: Path) -> list[ParseError]:
    return [
        ParseError(file=_full_path(f.rel_path, unit, root), error_message=f.error_message)
        for f in failed
    ]


def _collect_unresolved(functions, unit: Unit, root: Path) -> list[UnresolvedReference]:
    """Ghi lại lời gọi không nối được, bỏ qua lời gọi ra thư viện ngoài.

    Gọi thư viện ngoài là phân loại đúng, không phải chỗ thiếu sót.
    """
    found: list[UnresolvedReference] = []
    for function in functions:
        for ref in function.calls:
            if ref.resolved or is_external(ref):
                continue
            found.append(
                UnresolvedReference(
                    description=f"{function.qualified_name} gọi '{ref.name}': {ref.reason}",
                    location=function.location,
                )
            )
    return found
