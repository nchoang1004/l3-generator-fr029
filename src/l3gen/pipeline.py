"""Điều phối các bước xử lý.

Thứ tự bắt buộc, bước sau cần kết quả bước trước:

    1.  Kiểm kê mọi source file và phân loại ngôn ngữ từng file
    2.  Đưa file qua frontend ngôn ngữ tương ứng; nhận diện framework chỉ là metadata
    3.  Dựng bảng danh bạ và bảng tên gọi theo từng file
    4.  Chạy các bộ trích xuất, nối tham chiếu
    5.  Gộp thành IAM
    6.  Chuyển IAM sang node/cạnh
    7.  Hai bước AI, đọc IAM ĐỘC LẬP với nhau
    8.  Sinh tài liệu

Bước 1-6 không dùng AI và cho kết quả giống hệt qua hai lần chạy. Bước 7 chỉ thêm
lời văn: mô tả ghi ra file riêng, cảnh báo cũng ra file riêng, không thứ nào chạm
vào IAM.
"""

from dataclasses import dataclass, field
from pathlib import Path
import time
from l3gen.core.metrics import peak_process_memory

from l3gen.ai.enrichment import Descriptions, enrich, write_descriptions
from l3gen.ai.reviewer import Review, review
from l3gen.core.builder import EmptyInputError, build
from l3gen.core.graph_builder import build_graph
from l3gen.models.graph import RepositoryGraph
from l3gen.models.iam import IntermediateArchitectureModel
from l3gen.output.json_export import write_findings, write_graph, write_iam, write_inventory
from l3gen.output.json_export import write_run_metrics
from l3gen.output.markdown import write_markdown
from l3gen.output.mermaid import write_mermaid

__all__ = ["EmptyInputError", "Result", "analyze", "write_outputs"]


@dataclass
class Result:
    iam: IntermediateArchitectureModel
    graph: RepositoryGraph
    descriptions: Descriptions = field(default_factory=Descriptions)
    review: Review = field(default_factory=Review)

    @property
    def ai_problems(self) -> list[str]:
        return [*self.descriptions.problems, *self.review.problems]


def analyze(root: Path, excludes: tuple[str, ...], ai_enabled: bool) -> Result:
    started = time.perf_counter()
    iam = build(root, excludes, ai_enabled)
    graph_started = time.perf_counter()
    graph = build_graph(iam)
    iam.metrics.stage_seconds["architecture_graph"] = round(
        time.perf_counter() - graph_started, 6
    )
    iam.metrics.peak_memory_bytes = peak_process_memory()
    iam.metrics.duration_seconds = round(time.perf_counter() - started, 3)
    result = Result(iam=iam, graph=graph)

    # Hai bước AI đọc cùng một IAM, không đọc kết quả của nhau.
    if ai_enabled:
        result.descriptions = enrich(iam)
    result.review = review(iam, use_ai=ai_enabled)
    return result


def write_outputs(result: Result, output_dir: Path) -> list[Path]:
    started = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)
    written = [
        write_markdown(result.iam, output_dir, result.descriptions, result.review),
        write_mermaid(result.iam, output_dir),
        write_graph(result.graph, output_dir),
        write_iam(result.iam, output_dir),
        write_inventory(result.iam.file_inventory, output_dir),
        write_findings(result.review.findings, output_dir),
    ]
    if result.descriptions.by_id:
        written.append(write_descriptions(result.descriptions, output_dir))
    result.iam.metrics.stage_seconds["outputs"] = round(time.perf_counter() - started, 6)
    result.iam.metrics.peak_memory_bytes = peak_process_memory()
    write_run_metrics(result.iam, output_dir)
    return written
