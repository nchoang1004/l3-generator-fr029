from pathlib import Path

from l3gen.languages.python.parser import DEFAULT_EXCLUDES
from l3gen.pipeline import analyze


SAMPLE = Path(__file__).parents[1] / "fixtures" / "python" / "fastapi" / "sample_app"


def result():
    return analyze(SAMPLE, DEFAULT_EXCLUDES, ai_enabled=False)


def test_iam_chua_day_du_cac_tang_v2_va_so_lieu_resolver():
    iam = result().iam
    assert iam.semantic_program.frontend_version == "python-ast-v2"
    assert iam.resolution.calls
    assert iam.resolution.metrics.resolved_calls > 0
    assert iam.framework_analysis.registry_version == "builtin-semantics-v1"
    assert {item.kind for item in iam.framework_analysis.operations} >= {
        "AttachRouter",
        "RegisterEndpoint",
    }
    assert iam.metrics.stage_seconds.keys() >= {
        "file_inventory",
        "language_frontend",
        "resolver_dataflow",
        "framework_adapters",
        "architecture_graph",
    }
    assert iam.metrics.peak_memory_bytes > 0


def test_graph_v2_co_quan_he_phan_biet_va_boundary_khong_dua_vao_folder():
    graph = result().graph
    kinds = {edge.type for edge in graph.edges}
    assert {"imports", "constructs", "registers", "mounts", "exposes"} <= kinds
    assert "reads" in kinds or "writes" in kinds
    assert "calls_external" in kinds
    assert graph.application_boundaries
    assert all(item.status in ("candidate", "unknown") for item in graph.application_boundaries)

