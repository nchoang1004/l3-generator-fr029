"""Khóa ranh giới: frontend ghi cú pháp, không tự suy semantics framework."""

import ast

from l3gen.languages.python.frontend import FRONTEND_VERSION, build_semantic_program
from l3gen.languages.python.parser import ParsedFile
from l3gen.models.semantic import AssignmentFact, CallFact, ImportFact


def frontend(source: str):
    parsed = ParsedFile("main.py", ast.parse(source), source.count("\n") + 1)
    return build_semantic_program([parsed], {"main.py": "main"}).modules[0]


def test_assignment_call_chi_bao_toan_cau_truc_chua_suy_fastapi_application():
    module = frontend("from fastapi import FastAPI\napp = FastAPI()\n")

    imported = next(fact for fact in module.facts if isinstance(fact, ImportFact))
    assigned = next(fact for fact in module.facts if isinstance(fact, AssignmentFact))

    assert imported.local_name == "FastAPI"
    assert imported.imported_symbol == "fastapi.FastAPI"
    assert assigned.target.kind == "name"
    assert assigned.target.text == "app"
    assert assigned.value.kind == "call"
    assert assigned.value.callee.kind == "name"
    assert assigned.value.callee.text == "FastAPI"
    assert "application" not in assigned.model_dump_json().lower()


def test_alias_duoc_ghi_o_import_nhung_call_van_giu_ten_da_viet():
    module = frontend("from fastapi import FastAPI as Application\napp = Application()\n")

    imported = next(fact for fact in module.facts if isinstance(fact, ImportFact))
    call = next(fact for fact in module.facts if isinstance(fact, CallFact))

    assert imported.local_name == "Application"
    assert imported.imported_symbol == "fastapi.FastAPI"
    assert call.callee.text == "Application"


def test_fact_id_on_dinh_va_co_vi_tri_phien_ban_frontend():
    first = frontend("value = factory()\n")
    second = frontend("value = factory()\n")

    assert [fact.id for fact in first.facts] == [fact.id for fact in second.facts]
    assert all(fact.frontend_version == FRONTEND_VERSION for fact in first.facts)
    assert all(fact.location.file == "main.py" for fact in first.facts)
