"""Ghi IAM.json và graph.json.

Hai lần chạy trên cùng source phải cho file giống hệt từng byte. Vì vậy khoá JSON
được sắp xếp và số liệu phụ thuộc thời gian (thời điểm chạy, thời lượng chạy)
được tách riêng ra file khác — chúng đổi mỗi lần chạy nên không nằm trong phần
so sánh.
"""

import json
from pathlib import Path

from l3gen.models.findings import ReviewFinding, ReviewFindings
from l3gen.models.graph import RepositoryGraph
from l3gen.models.iam import IntermediateArchitectureModel

VOLATILE_METRIC_FIELDS = ("scanned_at", "duration_seconds")
"""Số liệu đổi theo mỗi lần chạy. Tách ra để chạy hai lần vẫn so sánh được."""


def _write(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_iam(iam: IntermediateArchitectureModel, output_dir: Path) -> Path:
    payload = iam.model_dump(mode="json")
    volatile = {k: payload["metrics"].pop(k) for k in VOLATILE_METRIC_FIELDS}

    path = output_dir / "IAM.json"
    _write(path, payload)
    _write(output_dir / "run.json", volatile)
    return path


def write_graph(graph: RepositoryGraph, output_dir: Path) -> Path:
    path = output_dir / "graph.json"
    _write(path, graph.model_dump(mode="json"))
    return path


def write_findings(findings: list[ReviewFinding], output_dir: Path) -> Path:
    """Cảnh báo ghi ra file riêng, không trộn vào IAM.

    IAM là dữ liệu đọc từ code. Cảnh báo là suy luận cần người xác nhận. Hai thứ
    khác bản chất nên không để chung file.
    """
    path = output_dir / "findings.json"
    _write(path, ReviewFindings(findings=findings).model_dump(mode="json"))
    return path
