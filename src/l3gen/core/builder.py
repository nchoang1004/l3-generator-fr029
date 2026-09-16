"""Gộp inventory và kết quả các frontend/adapter thành IAM hoàn chỉnh.

Source được kiểm kê trước rồi nhóm theo ngôn ngữ để chọn parser. Framework không
quyết định file nào được parse. Trường ``service`` của mô hình V1 hiện mang tên
nhóm ngôn ngữ; application boundary thật sẽ được dựng sau graph ở mốc V2.5.
"""

import time
from datetime import datetime, timezone
from pathlib import Path

from l3gen import __version__
from l3gen.detection.discovery import Unit, discover
from l3gen.core.resolution.dataflow import resolve_program
from l3gen.core.semantic_extractors import attach_entity_references, extract_functions_v2
from l3gen.core.semantics.registry import builtin_registry
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.frameworks.fastapi.adapter_v2 import (
    analyze_fastapi,
    materialize_routes,
)
from l3gen.languages.python.frameworks.fastapi.external_v2 import extract_external_calls_v2
from l3gen.languages.python.parser import FailedFile, parse_all
from l3gen.languages.python.modules import module_map
from l3gen.models.iam import (
    IntermediateArchitectureModel,
    ParseError,
    RunMetrics,
    SourceLocation,
    UnresolvedReference,
)
from l3gen.orm.sqlalchemy_v2 import extract_entities_v2


class EmptyInputError(Exception):
    """Thư mục đầu vào không có đơn vị nào phân tích được."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def build(root: Path, excludes: tuple[str, ...], ai_enabled: bool) -> IntermediateArchitectureModel:
    started = time.perf_counter()
    discovery_started = time.perf_counter()
    stack, units, inventory = discover(root, excludes)
    discovery_seconds = time.perf_counter() - discovery_started

    if not stack.services:
        raise EmptyInputError(f"không tìm thấy file source nào trong '{root}'")

    parse_errors = [
        ParseError(file=item.path, error_message=item.reason or "không đọc được file")
        for item in inventory.files
        if item.status == "parse_error"
    ]
    parsed_files = []
    files_analyzed = 0
    lines_of_code = 0
    inventory_by_path = {item.path: item for item in inventory.files}

    frontend_started = time.perf_counter()
    for unit in units:
        parsed, failed = parse_all(unit.files, unit.root)

        files_analyzed += len(parsed)
        lines_of_code += sum(f.line_count for f in parsed)
        parse_errors.extend(_prefix_errors(failed, unit, root))
        for parsed_file in parsed:
            record = inventory_by_path[parsed_file.rel_path]
            record.status = "parsed"
            record.reason = None
        for failed_file in failed:
            record = inventory_by_path[failed_file.rel_path]
            record.status = "parse_error"
            record.reason = failed_file.error_message

        parsed_files.extend(parsed)

    module_of = module_map([item.rel_path for item in parsed_files])
    semantic_program = build_semantic_program(parsed_files, module_of)
    for module in semantic_program.modules:
        if module.module.startswith("@file:"):
            module.analysis_notes.append("module trùng tên ở nhiều source root; import cần cấu hình root để phân giải duy nhất")
    semantic_program.modules.sort(key=lambda module: module.file)
    frontend_seconds = time.perf_counter() - frontend_started

    registry = builtin_registry()
    resolution_started = time.perf_counter()
    resolution = resolve_program(semantic_program, registry)
    resolution_seconds = time.perf_counter() - resolution_started

    adapters_started = time.perf_counter()
    functions, unresolved = extract_functions_v2(
        semantic_program, resolution, registry, service="python"
    )
    entities = extract_entities_v2(semantic_program, resolution, service="python")
    attach_entity_references(functions, entities, semantic_program, resolution)
    framework_analysis = analyze_fastapi(semantic_program, resolution, registry)
    routes, dropped = materialize_routes(framework_analysis, functions, service="python")
    external_calls = extract_external_calls_v2(
        semantic_program, resolution, service="python"
    )
    unresolved.extend(
        UnresolvedReference(
            description=f"framework operation chưa hoàn chỉnh: {item}",
            location=SourceLocation(file=".", line_start=0, line_end=0),
        )
        for item in dropped
    )
    adapter_seconds = time.perf_counter() - adapters_started

    files_found = len(inventory.files)
    files_skipped = files_found - files_analyzed
    metrics = RunMetrics(
        scanned_at=datetime.now(timezone.utc),
        files_found=files_found,
        files_analyzed=files_analyzed,
        files_skipped=files_skipped,
        is_partial=files_skipped > 0 or stack.skipped_count > 0 or resolution.partial or bool(unresolved)
                   or any(module.analysis_notes for module in semantic_program.modules)
                   or any(item.completeness == "partial" for item in [*routes, *entities, *external_calls]),
        lines_of_code=lines_of_code,
        duration_seconds=round(time.perf_counter() - started, 3),
        ai_enabled=ai_enabled,
        tool_version=__version__,
        stage_seconds={
            "file_inventory": round(discovery_seconds, 6),
            "language_frontend": round(frontend_seconds, 6),
            "resolver_dataflow": round(resolution_seconds, 6),
            "framework_adapters": round(adapter_seconds, 6),
        },
    )

    return IntermediateArchitectureModel(
        file_inventory=inventory,
        semantic_program=semantic_program,
        resolution=resolution,
        framework_analysis=framework_analysis,
        detected_stack=stack,
        routes=sorted(routes, key=lambda r: (r.service, r.path, r.method)),
        entities=sorted(entities, key=lambda e: (e.service, e.table_name or "", e.class_name)),
        external_calls=sorted(external_calls, key=lambda c: (c.service, c.url_or_host)),
        functions=sorted(functions, key=lambda f: (f.service, f.module, f.qualified_name)),
        unresolved_references=unresolved,
        parse_errors=parse_errors,
        metrics=metrics,
    )


def _full_path(rel_path: str, unit: Unit, root: Path) -> str:
    """Đường dẫn trong đơn vị -> đường dẫn tính từ thư mục đầu vào."""
    return f"{unit.rel_root}/{rel_path}" if unit.rel_root else rel_path


def _prefix_errors(failed: list[FailedFile], unit: Unit, root: Path) -> list[ParseError]:
    return [
        ParseError(file=_full_path(f.rel_path, unit, root), error_message=f.error_message)
        for f in failed
    ]
