"""FastAPI adapter chỉ diễn giải call đã được resolver nối đúng symbol."""

import ast

from l3gen.core.resolution.dataflow import resolve_program
from l3gen.core.semantics.registry import builtin_registry
from l3gen.languages.python.frameworks.fastapi.adapter_v2 import (
    analyze_fastapi,
    materialize_routes,
)
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.parser import ParsedFile


def analyze(files: dict[str, str]):
    parsed = [
        ParsedFile(path, ast.parse(source), source.count("\n") + 1)
        for path, source in files.items()
    ]
    modules = {path: path.removesuffix(".py").replace("/", ".") for path in files}
    program = build_semantic_program(parsed, modules)
    registry = builtin_registry()
    resolution = resolve_program(program, registry)
    return program, resolution, analyze_fastapi(program, resolution, registry)


def test_include_router_ghep_du_prefix_xuyen_file_va_alias():
    _, _, framework = analyze(
        {
            "main.py": """
from fastapi import FastAPI
from routes import router as orders
app = FastAPI()
app.include_router(orders, prefix="/api")
""",
            "routes.py": """
from fastapi import APIRouter
router = APIRouter(prefix="/orders")
@router.post("/{order_id}")
def update_order(): pass
""",
        }
    )

    routes, dropped = materialize_routes(framework, [])
    assert dropped == []
    attach = next(item for item in framework.operations if item.kind == "AttachRouter")
    assert attach.child_object_ids, attach.model_dump()
    assert [(route.method, route.path, route.handler_symbol) for route in routes] == [
        ("POST", "/api/orders/{order_id}", "routes.update_order")
    ], framework.model_dump()


def test_mount_duoc_hieu_nho_type_khong_phai_nho_ten_method():
    _, resolution, framework = analyze(
        {
            "main.py": """
from fastapi import FastAPI
app = FastAPI()
child = FastAPI()
app.mount("/v1", app=child)

class Disk:
    def mount(self, path): pass
disk = Disk()
disk.mount("/dev/sdb")
"""
        }
    )

    mounts = [item for item in framework.operations if item.kind == "MountApplication"]
    assert len(mounts) == 1
    disk = next(item for item in resolution.calls if item.written_callee == "disk.mount")
    assert disk.targets == ["main.Disk.mount"]


def test_add_api_route_va_dieu_kien_duoc_bao_toan():
    _, _, framework = analyze(
        {
            "main.py": """
from fastapi import FastAPI
app = FastAPI()
def health(): pass
if settings.ENABLED:
    app.add_api_route("/health", health, methods=["GET", "HEAD"])
"""
        }
    )

    routes, _ = materialize_routes(framework, [])
    assert [item.method for item in routes] == ["GET", "HEAD"]
    assert all(item.completeness == "partial" for item in routes)
    assert all("settings.ENABLED" in (item.reason or "") for item in routes)
