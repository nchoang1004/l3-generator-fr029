"""Kiểm tra ranh giới AI (SPEC mục 8.3, 8.4).

Đây là bài kiểm tra "khoá cửa": dù AI có cố sáng tạo đến đâu cũng không có đường
nào chèn được vào phần dữ liệu đọc từ code.

Kiểm bằng code, không kiểm bằng cách đọc thấy hợp lý.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

from l3gen.ai.enrichment import Descriptions, enrich
from l3gen.ai.reviewer import Review, detect, review
from l3gen.ai.schemas import Description, DescriptionBatch, FindingSummary
from l3gen.languages.python.parser import DEFAULT_EXCLUDES
from l3gen.models.findings import FindingCategory, ReviewFinding
from l3gen.pipeline import analyze, write_outputs

FIXTURES = Path(__file__).parents[1] / "fixtures"
SAMPLE_APP = FIXTURES / "python" / "fastapi" / "sample_app"

ALLOWED_CATEGORIES = {
    "unresolved_reference",
    "empty_handler_calls",
    "orphan_entity",
    "external_call_no_error_handling",
}


def build_iam():
    return analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False).iam


# --- 8.3: schema của bước viết mô tả -------------------------------------

def test_schema_mo_ta_chi_co_dung_hai_truong():
    """Không có trường nào để chèn route, bảng dữ liệu hay quan hệ."""
    assert set(Description.model_fields) == {"target_id", "text"}
    assert set(DescriptionBatch.model_fields) == {"descriptions"}


def test_ai_khong_the_chen_route_moi_qua_schema():
    """Thử nhét một route vào output của AI — Pydantic không nhận."""
    payload = {
        "descriptions": [{"target_id": "route-0", "text": "mô tả"}],
        "routes": [{"method": "GET", "path": "/bia-ra"}],
    }
    batch = DescriptionBatch.model_validate(payload)

    assert not hasattr(batch, "routes")
    assert len(batch.descriptions) == 1


def test_mo_ta_bi_gioi_han_do_dai():
    with pytest.raises(ValidationError):
        Description(target_id="route-0", text="x" * 5000)


# --- 8.3: mô tả không được lọt vào IAM ----------------------------------

def test_iam_giong_het_du_co_hay_khong_co_mo_ta(tmp_path):
    """Phép thử mạnh nhất: chạy có AI và không AI cho ra IAM.json giống hệt.

    Mô tả do AI viết được ghi ra file riêng, nên đây không phải lời hứa mà là
    điều kiểm chứng được bằng lệnh diff.
    """
    without = analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False)

    with_ai = analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False)
    with_ai.descriptions = Descriptions(
        by_id={"route-0": "AI viết thêm câu này", "entity-0": "và câu này"}
    )

    write_outputs(without, tmp_path / "khong-ai")
    write_outputs(with_ai, tmp_path / "co-ai")

    for name in ("IAM.json", "graph.json", "diagram.mmd"):
        assert (tmp_path / "khong-ai" / name).read_bytes() == (
            tmp_path / "co-ai" / name
        ).read_bytes(), f"{name} bị đổi khi có mô tả AI"


def test_mo_ta_ai_van_hien_trong_tai_lieu(tmp_path):
    """Mô tả không vào IAM, nhưng vẫn phải hiện trong tài liệu cho người đọc."""
    result = analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False)
    result.descriptions = Descriptions(by_id={"route-0": "Xác nhận một đơn hàng."})
    write_outputs(result, tmp_path)

    document = (tmp_path / "L3.md").read_text(encoding="utf-8")
    assert "Xác nhận một đơn hàng." in document
    assert "Mô tả (AI)" in document


def test_mo_ta_tro_toi_ma_khong_ton_tai_bi_loai(monkeypatch):
    """AI trả về target_id bịa ra thì bỏ, không đưa vào tài liệu."""
    from l3gen.ai import enrichment

    def fake_ask(prompt, system, model):
        from l3gen.ai.client import AIResult

        return AIResult(
            value=DescriptionBatch(
                descriptions=[
                    Description(target_id="route-0", text="thật"),
                    Description(target_id="route-999", text="bịa"),
                ]
            )
        )

    monkeypatch.setattr(enrichment, "ask", fake_ask)
    result = enrichment.enrich(build_iam())

    assert result.by_id == {"route-0": "thật"}
    assert result.rejected == 1


# --- 8.4: schema và loại của bước rà soát -------------------------------

def test_review_finding_chi_co_bon_loai():
    assert set(FindingCategory.__args__) == ALLOWED_CATEGORIES


def test_ai_khong_the_tao_loai_canh_bao_moi():
    with pytest.raises(ValidationError):
        ReviewFinding(
            category="loai_tu_bia",
            summary="x",
            evidence_location={"file": "a.py", "line_start": 1, "line_end": 1},
            related_iam_ref="routes[0]",
        )


def test_schema_tom_tat_canh_bao_khong_co_truong_nao_sua_duoc_iam():
    assert set(FindingSummary.model_fields) == {"finding_id", "summary"}


# --- 8.4: mọi cảnh báo phải trỏ đúng vị trí trong source ----------------

def test_moi_canh_bao_tro_ve_vi_tri_co_that_trong_source():
    iam = build_iam()
    result = review(iam, use_ai=False)

    assert result.findings
    for finding in result.findings:
        location = finding.evidence_location
        source = SAMPLE_APP / location.file
        assert source.exists(), f"{location.file} không tồn tại"
        line_count = len(source.read_text(encoding="utf-8").splitlines())
        assert 1 <= location.line_start <= line_count


def test_canh_bao_goi_ra_ngoai_khong_co_try_except():
    """sample_app gọi httpx.post không bọc try — phải bị gắn cờ."""
    iam = build_iam()
    findings = review(iam, use_ai=False).findings

    matching = [f for f in findings if f.category == "external_call_no_error_handling"]
    assert len(matching) == 1
    assert matching[0].evidence_location.file == "app/services/order.py"


def test_canh_bao_khong_dung_giong_khang_dinh():
    """SPEC mục 6b.1: phải dùng giọng 'có thể thiếu', không nói 'sẽ lỗi'."""
    findings = review(build_iam(), use_ai=False).findings

    for finding in findings:
        assert "sẽ lỗi" not in finding.summary
        assert "chắc chắn" not in finding.summary


def test_phat_hien_khong_can_ai():
    """Việc phát hiện là tất định. Không có AI thì vẫn ra đúng ngần ấy cảnh báo."""
    iam = build_iam()

    assert len(detect(iam)) == len(review(iam, use_ai=False).findings)


def test_canh_bao_ghi_ra_file_rieng_khong_tron_vao_iam(tmp_path):
    result = analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False)
    write_outputs(result, tmp_path)

    assert (tmp_path / "findings.json").exists()
    iam_text = (tmp_path / "IAM.json").read_text(encoding="utf-8")
    assert "external_call_no_error_handling" not in iam_text


# --- AI hỏng thì chỉ giảm chất lượng, không mất output ------------------

def test_ai_hong_van_sinh_du_tai_lieu(monkeypatch, tmp_path):
    """SPEC mục 4.3: LLM hỏng chỉ làm giảm chất lượng, không làm mất output."""
    from l3gen.ai import client, enrichment

    monkeypatch.setattr(client, "read_api_key", lambda: "khoa-gia")
    monkeypatch.setattr(
        enrichment, "ask", lambda *a: client.AIResult(problems=["mạng hỏng"])
    )

    result = analyze(SAMPLE_APP, DEFAULT_EXCLUDES, ai_enabled=False)
    result.descriptions = enrichment.enrich(result.iam)
    write_outputs(result, tmp_path)

    document = (tmp_path / "L3.md").read_text(encoding="utf-8")
    assert "/api/v1/orders/{order_id}/confirm" in document
    assert "mạng hỏng" in document
    assert "Phần AI không chạy được" in document
