"""Ca phản ví dụ từ review; không chạy source được phân tích."""

import ast
import json

from l3gen.core.resolution.dataflow import resolve_program
from l3gen.core.semantics.registry import builtin_registry
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.modules import module_map
from l3gen.languages.python.parser import ParsedFile
from l3gen.languages.python.frameworks.fastapi.adapter_v2 import analyze_fastapi, materialize_routes
from l3gen.orm.sqlalchemy_v2 import extract_entities_v2
from l3gen.output.json_export import _write


def program(files):
    parsed = [ParsedFile(path, ast.parse(source), source.count("\n") + 1) for path, source in files.items()]
    return build_semantic_program(parsed, module_map(list(files)))


def routes(source):
    ir = program({"main.py": source})
    resolution = resolve_program(ir)
    framework = analyze_fastapi(ir, resolution, builtin_registry())
    return materialize_routes(framework, [])[0], framework


def test_surrogate_unicode_roundtrips_and_does_not_destroy_previous_output(tmp_path):
    target = tmp_path / "IAM.json"
    _write(target, {"text": "tiếng Việt\ud800"})
    assert json.loads(target.read_text(encoding="utf-8"))["text"] == "tiếng Việt\ud800"
    assert not list(tmp_path.glob("*.tmp"))


def test_identical_calls_on_same_line_allocate_distinct_objects():
    result, framework = routes('from fastapi import FastAPI\na, b = FastAPI(), FastAPI()\n@a.get("/a")\ndef one(): pass\n@b.get("/b")\ndef two(): pass\n')
    assert len(framework.objects) == 2
    operations = [op for op in framework.operations if op.kind == "RegisterEndpoint"]
    assert operations[0].parent_object_ids != operations[1].parent_object_ids
    assert len(result) == 2


def test_multiline_factory_and_return_bind_to_exact_call_position():
    ir = program({"main.py": 'class A:\n def run(self): pass\ndef make():\n return (\n  A()\n )\nobj = (\n make()\n)\nobj.run()\n'})
    result = resolve_program(ir)
    assert next(call for call in result.calls if call.written_callee == "obj.run").targets == ["main.A.run"]


def test_package_init_reexport_and_nested_source_root():
    ir = program({
        "backend/src/shop/__init__.py": "from .api import router\n",
        "backend/src/shop/api.py": "from fastapi import APIRouter\nrouter=APIRouter()\n@router.get('/health')\ndef health(): pass\n",
        "backend/main.py": "from fastapi import FastAPI\nfrom shop import router\napp=FastAPI()\napp.include_router(router,prefix='/api')\n",
    })
    resolved = resolve_program(ir)
    framework = analyze_fastapi(ir, resolved, builtin_registry())
    result, _ = materialize_routes(framework, [])
    assert [route.path for route in result] == ["/api/health"]
    assert result[0].completeness == "full"


def test_orphan_router_and_cycle_are_partial():
    orphan, _ = routes('from fastapi import APIRouter\nr=APIRouter()\n@r.get("/x")\ndef x(): pass\n')
    assert orphan[0].completeness == "partial"
    cycle, _ = routes('from fastapi import APIRouter\na=APIRouter()\nb=APIRouter()\na.include_router(b)\nb.include_router(a)\n@a.get("/x")\ndef x(): pass\n')
    assert cycle[0].completeness == "partial"


def test_dynamic_http_methods_do_not_silently_become_get():
    result, framework = routes('from fastapi import FastAPI\napp=FastAPI()\ndef handler(): pass\napp.add_api_route("/x", handler, methods=config.methods)\n')
    assert result == []
    assert any(op.reason and "methods" in op.reason for op in framework.operations)


def test_runtime_plus_known_target_is_not_claimed_resolved():
    ir = program({"main.py": "def known(): pass\nhandler = known if flag else getattr(plugin, name)\nhandler()\n"})
    call = next(item for item in resolve_program(ir).calls if item.written_callee == "handler")
    assert call.targets == ["main.known"]
    assert call.status == "candidates"


def test_analysis_budget_never_reports_a_truncated_single_candidate_as_certain():
    ir = program({"main.py": "def a(): pass\ndef b(): pass\nf = a if flag else b\nf()\n"})
    result = resolve_program(ir, max_candidates=1)
    call = next(item for item in result.calls if item.written_callee == "f")
    assert call.truncated and call.status != "resolved" and result.partial


def test_table_keyword_on_unrelated_class_does_not_create_entity():
    ir = program({"models.py": "class Normal(table=True):\n id: int = 1\n"})
    assert extract_entities_v2(ir, resolve_program(ir)) == []


def test_sqlmodel_fields_without_default_are_preserved_and_schema_is_not_table():
    ir = program({"models.py": "from sqlmodel import SQLModel\nclass Schema(SQLModel):\n name: str\nclass User(SQLModel, table=True):\n name: str\n"})
    entities = extract_entities_v2(ir, resolve_program(ir))
    assert [entity.class_name for entity in entities] == ["User"]
    assert [column.name for column in entities[0].columns] == ["name"]


def test_python_diamond_mro_does_not_stop_at_first_grandparent():
    ir = program({"main.py": "class A:\n def run(self): pass\nclass B(A): pass\nclass C(A):\n def run(self): pass\nclass D(B, C): pass\nx=D()\nx.run()\n"})
    result = resolve_program(ir)
    assert next(call for call in result.calls if call.written_callee == "x.run").targets == ["main.C.run"]


def test_starlette_route_list_is_registered_with_get_and_head():
    result, _ = routes('from starlette.applications import Starlette\nfrom starlette.routing import Route\ndef health(request): pass\napp=Starlette(routes=[Route("/health", health)])\n')
    assert {(route.method, route.path) for route in result} == {("GET", "/health"), ("HEAD", "/health")}


def test_bare_annotation_is_not_a_sqlalchemy_column():
    ir = program({"models.py": 'from sqlalchemy.orm import DeclarativeBase, Mapped\nclass Base(DeclarativeBase): pass\nclass User(Base):\n __tablename__="users"\n id: Mapped[int]\n cache: str = "local"\n'})
    entities = extract_entities_v2(ir, resolve_program(ir))
    assert [col.name for col in entities[0].columns] == ["id"]


def test_framework_bound_method_alias_keeps_receiver():
    result, _ = routes('from fastapi import FastAPI\napp=FastAPI()\nregister=app.get\n@register("/health")\ndef health(): pass\n')
    assert [(route.method, route.path) for route in result] == [("GET", "/health")]


def test_method_call_evidence_contains_type_and_import_steps():
    ir = program({"main.py": 'from fastapi import FastAPI\napp=FastAPI()\napp.mount("/x", app)\n'})
    call = next(item for item in resolve_program(ir).calls if item.written_callee == "app.mount")
    assert call.evidence
    assert any("type" in step.description for step in call.evidence)
