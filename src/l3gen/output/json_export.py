"""Ghi IAM.json và graph.json.

Hai lần chạy trên cùng source phải cho file giống hệt từng byte. Vì vậy khoá JSON
được sắp xếp và số liệu phụ thuộc thời gian (thời điểm chạy, thời lượng chạy)
được tách riêng ra file khác — chúng đổi mỗi lần chạy nên không nằm trong phần
so sánh.
"""

import json
import os
import tempfile
from pathlib import Path

from l3gen.models.findings import ReviewFinding, ReviewFindings
from l3gen.models.graph import RepositoryGraph
from l3gen.models.iam import IntermediateArchitectureModel
from l3gen.models.inventory import FileInventory

VOLATILE_METRIC_FIELDS = (
    "scanned_at",
    "duration_seconds",
    "stage_seconds",
    "peak_memory_bytes",
)
"""Số liệu đổi theo mỗi lần chạy. Tách ra để chạy hai lần vẫn so sánh được."""


def _write(path: Path, payload: dict) -> None:
    # Ghi tuần tự tránh tạo thêm một chuỗi JSON khổng lồ trong RAM. Surrogate
    # xuất hiện hợp lệ trong literal Python được giữ bằng escape JSON.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", errors="backslashreplace", newline="\n",
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, indent=2, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_iam(iam: IntermediateArchitectureModel, output_dir: Path) -> Path:
    payload = iam.model_dump(mode="json", exclude={"semantic_program", "resolution"})
    # Không lặp hàng loạt trường rỗng ở mọi nút biểu thức trong IR.
    payload["semantic_program"] = iam.semantic_program.model_dump(exclude_defaults=True)
    payload["resolution"] = iam.resolution.model_dump()
    volatile = {k: payload["metrics"].pop(k) for k in VOLATILE_METRIC_FIELDS}
    volatile["resolver_duration_seconds"] = payload["resolution"]["metrics"].pop(
        "duration_seconds"
    )

    path = output_dir / "IAM.json"
    _write(path, payload)
    _write(output_dir / "run.json", volatile)
    return path


def write_graph(graph: RepositoryGraph, output_dir: Path) -> Path:
    path = output_dir / "graph.json"
    _write(path, graph.model_dump(mode="json"))
    return path


def write_run_metrics(iam: IntermediateArchitectureModel, output_dir: Path) -> None:
    metrics = iam.metrics.model_dump(mode="json")
    payload = {name: metrics[name] for name in VOLATILE_METRIC_FIELDS}
    payload["resolver_duration_seconds"] = iam.resolution.metrics.duration_seconds
    payload["memory_measurement"] = "OS process peak resident/working set; includes previous runs in this process"
    payload["elapsed_analysis_and_outputs_seconds"] = round(
        iam.metrics.duration_seconds + iam.metrics.stage_seconds.get("outputs", 0), 6
    )
    _write(output_dir / "run.json", payload)


def write_inventory(inventory: FileInventory, output_dir: Path) -> Path:
    """Ghi sổ cái coverage riêng để kiểm tra file mà không cần đọc toàn bộ IAM."""
    path = output_dir / "file-inventory.json"
    _write(path, inventory.model_dump(mode="json"))
    return path


def write_findings(findings: list[ReviewFinding], output_dir: Path) -> Path:
    """Cảnh báo ghi ra file riêng, không trộn vào IAM.

    IAM là dữ liệu đọc từ code. Cảnh báo là suy luận cần người xác nhận. Hai thứ
    khác bản chất nên không để chung file.
    """
    path = output_dir / "findings.json"
    _write(path, ReviewFindings(findings=findings).model_dump(mode="json"))
    return path
